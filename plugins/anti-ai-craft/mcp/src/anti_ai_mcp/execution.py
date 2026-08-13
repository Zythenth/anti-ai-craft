from __future__ import annotations

import os
import math
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import resolve_within_repository


DEFAULT_TIMEOUT_SECONDS = 120.0
DEFAULT_OUTPUT_BYTES = 128 * 1024


@dataclass(frozen=True)
class CommandSpec:
    argv: tuple[str, ...]
    cwd: Path
    category: str
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": list(self.argv),
            "cwd": self.cwd.as_posix(),
            "category": self.category,
            "source": self.source,
        }


@dataclass(frozen=True)
class CommandExecution:
    command: tuple[str, ...]
    category: str
    exit_code: int | None
    duration_seconds: float
    stdout: str
    stderr: str
    stdout_truncated: bool
    stderr_truncated: bool
    timed_out: bool = False
    unavailable: bool = False
    error: str | None = None

    @property
    def truncated(self) -> bool:
        return self.stdout_truncated or self.stderr_truncated

    @property
    def status(self) -> str:
        if self.unavailable or self.error is not None:
            return "ERROR"
        if self.timed_out or self.exit_code != 0:
            return "FAIL"
        return "PASS"

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": list(self.command),
            "category": self.category,
            "exit_code": self.exit_code,
            "duration_seconds": round(self.duration_seconds, 3),
            "stdout_summary": self.stdout,
            "stderr_summary": self.stderr,
            "truncated": self.truncated,
            "stdout_truncated": self.stdout_truncated,
            "stderr_truncated": self.stderr_truncated,
            "timed_out": self.timed_out,
            "unavailable": self.unavailable,
            "status": self.status,
            "error": self.error,
        }


def controlled_environment() -> dict[str, str]:
    allowed = {
        "APPDATA",
        "COMSPEC",
        "HOME",
        "LANG",
        "LC_ALL",
        "LOCALAPPDATA",
        "PATH",
        "PATHEXT",
        "SYSTEMDRIVE",
        "SYSTEMROOT",
        "TEMP",
        "TMP",
        "USERPROFILE",
        "WINDIR",
    }
    environment = {key.upper(): value for key, value in os.environ.items() if key.upper() in allowed}
    environment.update(
        {
            "NO_COLOR": "1",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PYTHONUNBUFFERED": "1",
        }
    )
    return environment


def run_command(
    repository_root: Path,
    spec: CommandSpec,
    *,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    stdout_limit: int = DEFAULT_OUTPUT_BYTES,
    stderr_limit: int = DEFAULT_OUTPUT_BYTES,
) -> CommandExecution:
    input_error = _validate_limits(timeout_seconds, stdout_limit, stderr_limit)
    if input_error is not None:
        return _error_execution(spec, input_error)
    root = repository_root.resolve(strict=True)
    cwd = resolve_within_repository(root, spec.cwd)
    if not cwd.is_dir():
        return CommandExecution(
            command=spec.argv,
            category=spec.category,
            exit_code=None,
            duration_seconds=0.0,
            stdout="",
            stderr="",
            stdout_truncated=False,
            stderr_truncated=False,
            error=f"working directory does not exist: {cwd}",
        )
    if not spec.argv:
        return CommandExecution(
            command=(),
            category=spec.category,
            exit_code=None,
            duration_seconds=0.0,
            stdout="",
            stderr="",
            stdout_truncated=False,
            stderr_truncated=False,
            error="empty command",
        )
    environment = controlled_environment()
    executable = spec.argv[0]
    resolved_executable = _resolve_executable(executable, environment, root)
    if resolved_executable is None:
        return CommandExecution(
            command=spec.argv,
            category=spec.category,
            exit_code=None,
            duration_seconds=0.0,
            stdout="",
            stderr="",
            stdout_truncated=False,
            stderr_truncated=False,
            unavailable=True,
            error=f"executable is not available: {executable}",
        )

    argv = (str(resolved_executable), *spec.argv[1:])
    started = time.monotonic()
    timed_out = False
    error: str | None = None
    exit_code: int | None = None
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        try:
            process = subprocess.Popen(
                argv,
                cwd=cwd,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=stdout_file,
                stderr=stderr_file,
                shell=False,
                creationflags=(
                    subprocess.CREATE_NEW_PROCESS_GROUP
                    if sys.platform == "win32"
                    else 0
                ),
                start_new_session=sys.platform != "win32",
            )
            try:
                exit_code = process.wait(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    _terminate_process_tree(process, environment)
                    exit_code = process.wait(timeout=5)
                except (OSError, subprocess.TimeoutExpired) as exc:
                    error = f"timed out and termination could not be confirmed: {exc}"
        except OSError as exc:
            error = str(exc)

        stdout_file.seek(0)
        stdout_bytes = stdout_file.read(stdout_limit + 1)
        stderr_file.seek(0)
        stderr_bytes = stderr_file.read(stderr_limit + 1)

    stdout_truncated = len(stdout_bytes) > stdout_limit
    stderr_truncated = len(stderr_bytes) > stderr_limit
    stdout = stdout_bytes[:stdout_limit].decode("utf-8", errors="replace")
    stderr = stderr_bytes[:stderr_limit].decode("utf-8", errors="replace")
    return CommandExecution(
        command=spec.argv,
        category=spec.category,
        exit_code=exit_code,
        duration_seconds=time.monotonic() - started,
        stdout=stdout,
        stderr=stderr,
        stdout_truncated=stdout_truncated,
        stderr_truncated=stderr_truncated,
        timed_out=timed_out,
        error=error,
    )


def _validate_limits(
    timeout_seconds: float,
    stdout_limit: int,
    stderr_limit: int,
) -> str | None:
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        return "timeout_seconds must be a finite number greater than 0"
    for name, value in (("stdout_limit", stdout_limit), ("stderr_limit", stderr_limit)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            return f"{name} must be a non-negative integer"
    return None


def _error_execution(spec: CommandSpec, message: str) -> CommandExecution:
    return CommandExecution(
        command=spec.argv,
        category=spec.category,
        exit_code=None,
        duration_seconds=0.0,
        stdout="",
        stderr="",
        stdout_truncated=False,
        stderr_truncated=False,
        error=message,
    )


def _terminate_process_tree(
    process: subprocess.Popen[bytes],
    environment: dict[str, str],
) -> None:
    if sys.platform != "win32":
        os.killpg(process.pid, signal.SIGKILL)
        return

    system_root = Path(environment.get("SYSTEMROOT", environment.get("WINDIR", r"C:\Windows")))
    taskkill = system_root / "System32" / "taskkill.exe"
    if not taskkill.is_file():
        process.kill()
        raise OSError("Windows process-tree termination utility is unavailable")
    termination = subprocess.run(
        (str(taskkill), "/PID", str(process.pid), "/T", "/F"),
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=False,
        timeout=5,
        check=False,
    )
    if termination.returncode not in (0, 128) and process.poll() is None:
        process.kill()
        raise OSError(f"Windows process-tree termination failed with exit code {termination.returncode}")


def _resolve_executable(
    executable: str,
    environment: dict[str, str],
    repository_root: Path,
) -> Path | None:
    requested = Path(executable)
    if requested.is_absolute():
        return requested if requested.is_file() else None
    if requested.parent != Path("."):
        return None
    path_value = environment.get("PATH", "")
    extensions = [""]
    if sys.platform == "win32" and not requested.suffix:
        extensions = [
            extension.lower()
            for extension in environment.get("PATHEXT", ".COM;.EXE;.BAT;.CMD").split(";")
            if extension
        ]
    for raw_directory in path_value.split(os.pathsep):
        if not raw_directory:
            continue
        try:
            directory = Path(raw_directory).resolve(strict=True)
        except (OSError, RuntimeError):
            continue
        if directory == repository_root or directory.is_relative_to(repository_root):
            continue
        for extension in extensions:
            candidate = directory / f"{executable}{extension}"
            if candidate.is_file() and (sys.platform == "win32" or os.access(candidate, os.X_OK)):
                return candidate
    return None
