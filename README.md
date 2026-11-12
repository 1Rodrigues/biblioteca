# biblioteca
 set null porque um livro pode existir mesmo que seu autor faleça ou suma do banco por restrições judiciais

## Teste do csrf_token

Tirei o `{% csrf_token %}` do template `cadastrar_autor.html` e tentei cadastrar um autor. O formulário aparece normal, mas quando clica em Cadastrar o Django não salva nada e retorna erro **403 Proibido** com a mensagem "Verificação CSRF falhou. Pedido cancelado." (com DEBUG=True ele mostra o motivo: o token CSRF está faltando).

Isso acontece porque o middleware `CsrfViewMiddleware` confere em todo POST se veio o token junto. Sem ele, o Django entende que a requisição pode ter vindo de outro site tentando se passar pelo usuário e bloqueia. Depois do teste coloquei o token de volta.
