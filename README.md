# Sistema back-end para um blog

## Instalação

- Clone o repositório;
- Vá para a pasta local do projeto;
- Inicie um ambiente virtual: `virtualenv -p python3.10 venv`;
- Ative o ambiente virtual venv `source venv/bin/activate`;
- Instale o Poetry: `pip install poetry`;
- Instale as dependências: `poetry install`
- Configure o postgresql em config -> base.py -> DATABASES(variável)
- Ative o servidor RabbitMQ para rodar o Celery
- Ative o Celery através do comando: 

`celery -A config worker -l info --pool=solo` (Windows)

`celery -A config worker -l info` (Linux/Mac)

- Run the migrations: `python manage.py migrate`;
- Crie um superuser: `python manage.py createsuperuser`;
- Run the server: `python manage.py runserver`.

## Endpoints

**/docs/** -> Documentação com todos os endpoints

### Artigos:

**/api/register/** -> registre um usuário 

**/api/login/** -> retorna o token do usuário logado

**/articles/** -> feed de artigos ordenados pelos mais recentes

**/articles/create/** -> cria um artigo e associa o campo "author" com o usuário logado

**/articles/id/** -> retorna um artigo pelo id do mesmo

**/articles/search/?q=query&classify=most_views** -> endpoint para pesquisa, o parâmentro 'q' é query da pesquisa, e o parâmetro 'classify' é usado para classificar os artigos.
O parâmetro 'classify' pode ser entre as seguintes opções:
- classify=most_recent -> retorna a pesquisa ordenado pelos artigos mais recentes 
- classify=top_rated -> retorna a pesquisa ordenado pelos artigos com mais avaliações
- classify=best_rated -> retorna a pesquisa ordenado pelos artigos com melhores avaliações
- classify=older -> retorna a pesquisa ordenado pelos artigos mais antigos
- classify=most_views -> retorna a pesquisa ordenado pelos artigos mais visualizados

**/articles/id/delete/** -> usado para deletar um artigo pelo id

**/articles/id/rating/** -> usado para avaliar um artigo pelo id (um usuário pode avaliar apenas uma vez cada artigo)

**/articles/id/update/** -> usado para editar um artigo pelo id

## Categorias (Os endpoints de categorias só podem ser acessados por um usuário admin)

**/articles/category/** -> (GET)Lista as categorias, (POST)Cria categorias

**/articles/category/id/** -> (GET)Vizualiza a categoria, (PUT,PATCH)Edita categoria, (DELETE)Destroi a categoria

## Usuários

**/user/** -> (GET)Listar informações do usuário logado, (POST)Criar usuário

**/user/id/** -> (GET)Ver informações do usuário (caso o id não seja do usuário logado,não irá mostrar as informações), (PUT,PATCH)Editar o usuário, (DELETE)Destruir o usuário
