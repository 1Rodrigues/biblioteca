# biblioteca
 set null porque um livro pode existir mesmo que seu autor faleça ou suma do banco por restrições judiciais

## Teste do csrf_token

Tirei o `{% csrf_token %}` do template `cadastrar_autor.html` e tentei cadastrar um autor. O formulário aparece normal, mas quando clica em Cadastrar o Django não salva nada e retorna erro **403 Proibido** com a mensagem "Verificação CSRF falhou. Pedido cancelado." (com DEBUG=True ele mostra o motivo: o token CSRF está faltando).

Isso acontece porque o middleware `CsrfViewMiddleware` confere em todo POST se veio o token junto. Sem ele, o Django entende que a requisição pode ter vindo de outro site tentando se passar pelo usuário e bloqueia. Depois do teste coloquei o token de volta.

## Validadores - Perguntas

### a) O LivroModelForm mudou? Por que as regras do Model funcionam nele e no Admin sem nenhuma alteração?

Não, o `ModelBookForm` não precisou mudar. Os validadores foram colocados direto nos campos do model `Book`, e tanto o ModelForm quanto o Admin (que por baixo também usa um ModelForm) chamam o `full_clean()` do model quando o formulário é validado (`is_valid()`). Esse método roda os `validators` de cada campo, então a regra fica num lugar só e vale para qualquer formulário baseado no model. Se no futuro for criado outro formulário ou tela, a regra já vem junto.


### b) Qual é a diferença entre um validator e o método clean_<campo>()? Dê um exemplo de regra que só pode ser feita com clean_<campo>().

- **Validator**: é uma função (ou classe) que recebe só o valor do campo e levanta `ValidationError` se ele for inválido. Não retorna nada e não altera o valor. Pode ser reaproveitado em vários campos e models, e quando fica no model vale para todo lugar (form, admin, `full_clean()`).
- **clean_<campo>()**: é um método do formulário. Ele roda depois dos validators, tem acesso ao `self` (ao formulário, ao `self.instance`, ao `self.request` se for passado, etc.) e **precisa retornar o valor**, podendo devolver ele modificado. Só vale para aquele formulário.

Exemplo de regra que só dá pra fazer com `clean_<campo>()`: transformar o valor antes de salvar, como tirar os espaços extras do título (`' '.join(titulo.split())`) ou deixar o ISBN só com números removendo hífens. Um validator não consegue fazer isso porque ele não devolve valor, só aprova ou rejeita.

### c) Para cada regra, qual estratégia usar?

| Regra | Estratégia | Justificativa |
|---|---|---|
| O título não pode ser igual ao nome do autor. | `clean()` | Depende de dois campos ao mesmo tempo (`titulo` e `autor`). O `clean_<campo>()` só garante o valor do próprio campo, e o validator só enxerga um valor. O `clean()` roda depois de todos os campos e tem o `cleaned_data` completo. |
| O título deve ser salvo sem espaços no início e no fim. | Argumento do campo | O `forms.CharField` já tem `strip=True` por padrão, então o ModelForm já remove os espaços do início e do fim sem precisar de código. Se quisesse algo além disso (como tirar espaços duplicados no meio), aí seria `clean_titulo()`, porque precisa alterar e devolver o valor. |
| O número de páginas deve ser no máximo 5000. | `validators=[...]` | É uma regra que olha só o valor do próprio campo, então `MaxValueValidator(5000)` resolve e, por estar no model, vale no form e no admin. |
| Um livro "indisponível" precisa ter o ISBN preenchido. | `clean()` | Também envolve dois campos (`disponivel` e `isbn`). Pode ser feito no `clean()` do form ou, melhor ainda, no `clean()` do model, para valer também no admin. |

## Upload de arquivos - Perguntas

### a) O que acontece se esquecermos `request.FILES` na view? E se esquecermos o `enctype` no template?

- **Sem `request.FILES` na view**: o formulário recebe só o `request.POST`, que tem apenas os campos de texto. O arquivo chega no servidor, mas ninguém passa ele para o form, então o campo `capa` fica vazio. Como no model a `capa` é `blank=True`, o `is_valid()` dá `True` e o livro é salvo **sem capa**, sem nenhum aviso. Se o campo fosse obrigatório, apareceria só o "Este campo é obrigatório.", como se o usuário não tivesse escolhido arquivo nenhum. Obs.: nas nossas views baseadas em classe (`BookCreateView` / `BookUpdateView`) isso não acontece, porque o `get_form_kwargs()` do Django já passa `data=request.POST` e `files=request.FILES` sozinho. O erro aparece na versão com função (`ModelBookForm(request.POST, instance=livro)`), que precisaria ser `ModelBookForm(request.POST, request.FILES, instance=livro)`.
- **Sem `enctype="multipart/form-data"` no template**: o navegador envia o formulário como `application/x-www-form-urlencoded`, que não consegue carregar o conteúdo do arquivo, só o **nome** dele como texto. Então o `request.FILES` chega vazio no servidor, mesmo com a view certa. O resultado é o mesmo: o livro é salvo sem capa e o formulário **não mostra nenhum erro**.

Ou seja, nos dois casos o formulário não avisa nada; o único jeito de perceber é ver que a capa não aparece na lista e que nenhum arquivo foi criado em `midia/capas/`. Por isso é um erro fácil de passar despercebido.

### b) Qual é a diferença entre `STATICFILES_DIRS` / `{% static %}` e `MEDIA_ROOT` / `.url`? Quando usar cada um?

- **Arquivos estáticos** (`STATIC_URL`, `STATICFILES_DIRS`, `{% static %}`): são arquivos que fazem parte do código do projeto e são criados pelo desenvolvedor — CSS, JavaScript, logo do site, ícones. Eles vão para o git e são iguais para todo mundo. O `STATICFILES_DIRS` diz em quais pastas extras o Django procura esses arquivos, e o `{% static 'css/estilo.css' %}` monta a URL no template. Em produção são juntados com `collectstatic`.
- **Arquivos de mídia** (`MEDIA_ROOT`, `MEDIA_URL`, `.url`): são arquivos enviados pelos **usuários** enquanto o sistema roda, por um `FileField`/`ImageField`. O `MEDIA_ROOT` é a pasta onde eles são gravados (aqui `app_biblioteca/midia/`), o `MEDIA_URL` é o prefixo da URL (`/midia/`) e o `livro.capa.url` devolve o endereço daquele arquivo para usar no `<img src>`. Não deveriam ir para o git, porque mudam conforme o uso.

Na Mini biblioteca: o CSS das páginas, um logo ou uma imagem padrão de "sem capa" seriam **static**. As capas dos livros cadastrados são **media**, por isso no `lista_livros.html` usamos `{{ livro.capa.url }}`.

### c) Ao excluir um livro (ou trocar a capa), o arquivo antigo continua em `media/capas/`. Por que isso acontece e que problema pode causar?

Porque o banco guarda só o **caminho** do arquivo (uma string tipo `capas/tai_lung.jpg`), e não o arquivo em si. Quando o livro é apagado, o Django remove a linha da tabela, mas não mexe no disco. Ao trocar a capa, o campo passa a apontar para o arquivo novo e o antigo simplesmente fica sem referência. O Django faz isso de propósito desde a versão 1.3, por segurança: ele não tem como saber se outro registro usa o mesmo arquivo, e se a transação do banco desse rollback depois de apagar o arquivo, o dado ficaria quebrado.

A longo prazo isso gera **arquivos órfãos**: a pasta vai crescendo e ocupando espaço em disco (ou custando dinheiro num storage na nuvem), os backups ficam maiores, fica difícil saber o que ainda é usado, e imagens que deveriam ter sido apagadas continuam acessíveis pela URL. Dá para resolver com um signal `post_delete`/`pre_save` que apaga o arquivo antigo, com a biblioteca `django-cleanup`, ou com um comando de limpeza periódico.

### d) Por que a extensão do arquivo não basta como proteção? Que outros cuidados o servidor deve ter com uploads?

A extensão é só o final do nome, e quem escolhe o nome é o usuário. O `FileExtensionValidator(['jpeg','png','jpg'])` que usamos olha só isso, então dá para renomear um `script.php`, um `.html` com JavaScript ou um executável para `capa.jpg` e o validator aceita. O conteúdo real do arquivo não é conferido.

Outros cuidados:

- **Verificar o conteúdo**: usar `ImageField` (que abre o arquivo com o Pillow e recusa o que não for imagem de verdade) ou checar o tipo real pelos "magic bytes" (ex.: `python-magic`), e não confiar no `content_type` que o navegador manda.
- **Limitar o tamanho**: como o nosso `ValidarTamanhoCapa` (2 MB), e também `DATA_UPLOAD_MAX_MEMORY_SIZE` / limite no servidor web, para evitar encher o disco ou a memória.
- **Não confiar no nome**: deixar o Django gerar/renomear o arquivo (ex.: com `uuid`) para evitar `../` (path traversal), sobrescrever arquivos ou nomes estranhos.
- **Nunca executar a pasta de mídia**: o servidor deve servir `MEDIA_ROOT` só como arquivo estático, sem rodar PHP/CGI, e com o header `X-Content-Type-Options: nosniff`; o ideal é servir de outro domínio ou de um storage separado (S3 etc.).
- **Guardar fora do código**: a pasta de uploads não deveria ficar dentro do app nem ir para o git.
- **Em produção**, não usar o `static()` do `urls.py` (só funciona com `DEBUG=True`); quem serve os arquivos é o Nginx/storage.
- Se possível, **reprocessar a imagem** (abrir e salvar de novo com o Pillow), o que remove metadados e conteúdo escondido, e passar um antivírus em sistemas mais sensíveis.

## Class-Based Views - Perguntas

### a) Na CreateView, quem faz o `if request.method == "POST"` que escrevíamos à mão? O que acontece quando o formulário é inválido?

Quem faz é a própria classe. O `as_view()` cria a view e o método `dispatch()` olha o `request.method` e chama o método com o mesmo nome: `get()` ou `post()`. Na `CreateView` (pela `ProcessFormView`), o `get()` só monta o formulário vazio e renderiza o template, e o `post()` cria o form com os dados (`get_form()`) e chama `is_valid()`:

- se for válido, chama `form_valid()`, que salva o objeto (`self.object = form.save()`) e redireciona para o `success_url`;
- se for inválido, chama `form_invalid()`, que **não salva nada** e renderiza o mesmo template de novo com o form preenchido e os erros de cada campo (`{{ form }}` já mostra as mensagens dos validators). A resposta é um 200, não um redirect, então o usuário não perde o que digitou.

### b) Por que o upload da capa continuou funcionando na CreateView sem passarmos `request.FILES` manualmente?

Porque o `get_form_kwargs()` da `FormMixin` já monta os argumentos do formulário sozinho: em POST/PUT ele passa `data=self.request.POST` **e** `files=self.request.FILES` (e na `ModelFormMixin` também o `instance=self.object`). Ou seja, aquele `ModelBookForm(request.POST, request.FILES, instance=livro)` que a gente escrevia na função agora é feito pela classe. O que continua sendo nossa responsabilidade é o `enctype="multipart/form-data"` no template, sem ele o `request.FILES` chega vazio do mesmo jeito.

### c) Por que o DeleteView mostra uma página de confirmação e só exclui no POST? Que problema aconteceria se a exclusão ocorresse em um GET?

Porque GET deve ser uma operação "segura": só ler, sem mudar nada no servidor. No `DeleteView`, o GET só mostra o `livro_confirm_delete.html`, e a exclusão acontece no POST (`form_valid()` chama `self.object.delete()` e redireciona). Como é um POST, ele também passa pela proteção do `{% csrf_token %}`.

Se apagasse no GET, qualquer coisa que abrisse o link `deletar_livro/5/` apagaria o livro: um clique sem querer, o navegador pré-carregando links, um robô de busca ou antivírus visitando as URLs, o botão de voltar/atualizar, ou outro site com um `<img src="http://.../deletar_livro/5/">` fazendo o navegador do usuário logado apagar livros sem ele saber (CSRF, já que GET não verifica o token).

### d) Cite uma vantagem e uma desvantagem das CBVs em relação às FBVs. Em que situação você ainda escolheria uma função?

- **Vantagem**: muito menos código repetido. Listar, detalhar, criar, editar e excluir viram poucas linhas (`model`, `template_name`, `form_class`, `success_url`), e o comportamento padrão (404 automático, `request.FILES`, form inválido, redirect) já vem pronto e testado. Dá para reaproveitar com herança e mixins (ex.: `LoginRequiredMixin`).
- **Desvantagem**: o fluxo fica "escondido". Para mudar um detalhe é preciso saber qual método sobrescrever (`get_queryset`, `get_context_data`, `form_valid`, `get_success_url`...) e em que ordem eles são chamados, o que exige ler a documentação ou o código do Django. Para quem está começando é mais difícil de entender e de depurar do que uma função lida de cima para baixo.

Eu ainda usaria uma função quando a view não segue o padrão CRUD: uma página que mexe com vários models ou vários formulários ao mesmo tempo, um endpoint simples que devolve JSON, uma ação como "marcar livro como emprestado" que só altera um campo e redireciona, ou uma página com regra muito específica, em que encaixar tudo nos métodos da classe daria mais trabalho do que escrever o `if request.method == "POST"` direto.

## Observações sobre os commits

A atividade pedia um commit por parte (ex.: "Parte 1: validadores"). Isso não foi seguido direito:

- **`1b24514` "atualiza rotas e templates para usar modelform"**: além do ModelForm, esse commit já trocou as views de função por Class-Based Views (`ListView`, `DetailView`, `CreateView`, `UpdateView`), que é a **Parte 3**, porque eu comecei isso durante a aula, antes da atividade ser postada. Isso entrou antes das partes 1 e 2 e a mensagem não fala nada sobre CBV. O mesmo commit também incluiu o `base.html` e uma migration do `Author`, então não dá para separar ou desfazer só uma coisa.
- **`066565d` "aplica validators no model livro"** (Parte 1): a mensagem não segue o padrão pedido ("Parte 1: validadores"), e o validador do ISBN entrou errado (`MinLengthValidator`/`MaxLengthValidator` aceitavam 13 letras). O ISBN só foi corrigido depois, com o `RegexValidator(r'^\d{13}$')`, que ficou junto do trabalho da Parte 2 sem commit próprio.
- **Partes 2 e 3 ficaram sem commit** e misturadas na área de staging (upload da capa junto com a `DeleteView` e o total de livros). Também faltava a migration `0012` dos validators da `capa`. Depois elas foram separadas em commits próprios: correção do ISBN (Parte 1), upload da capa (Parte 2) e CBVs (Parte 3).
- As imagens enviadas (`midia/capas/*.jpg`) estavam marcadas para commit. Arquivos de mídia são enviados pelos usuários e não deveriam ir para o git (ver 2.2 b), por isso ficaram de fora.
- Na atividade anterior, mensagens como "all", "nothing" e "sccp" não descrevem a mudança, e a pasta `.idea/` (configuração do PyCharm) foi commitada em `202b7da`.
