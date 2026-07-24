# Gates de aprovação

## Permitido pela invocação

Somente:

- achados explicitamente listados/aprovados;
- arquivos e comportamento necessários;
- testes e validações diretamente relacionados;
- artefatos temporários seguros e removíveis, quando necessários.

## Pedir nova aprovação

- identidade ou navegação visual ampla;
- mudança de API pública;
- migração de dados;
- dependência/framework novo;
- atualização ampla de dependências;
- remoção de feature/compatibilidade;
- acesso externo, credencial ou serviço;
- ação destrutiva ou difícil de recuperar;
- correção que afeta área não incluída;
- alternativa com tradeoff material de produto.
- mudança material do plano, risco, comportamento, IDs ou escopo já aprovados.

## Interromper

- achado não reproduz;
- relatório contradiz o código atual;
- causa está fora do escopo;
- mudanças preexistentes colidem;
- teste exige ambiente/segredo indisponível;
- correção segura depende de decisão do usuário;
- validação crítica não pode ser executada.
- verificação congelada falha e a próxima tentativa exigiria outra hipótese ou mudança material.

Interromper não significa inventar fallback. Relatar evidência e pedir direção.

## Proibido sem autorização específica

- stage, commit, push, PR, release ou deploy;
- reset, checkout destrutivo, clean ou descarte de mudanças;
- apagar dados, migrações ou snapshots;
- modificar licenças;
- reduzir testes/cobertura;
- desativar controle de segurança;
- aprovar automaticamente resultado visual;
- marcar achado como corrigido sem reprodução e validação.

## Critério de conclusão

Concluir somente quando cada ID aprovado tiver status e evidência:

- corrigido e validado;
- corrigido com validação parcial explicitada;
- não reproduzido;
- bloqueado por decisão/ambiente;
- rejeitado após nova evidência.
- já corrigido/sem mudança;
- bloqueado por prova, produto ou escopo;
- falhou na validação.
