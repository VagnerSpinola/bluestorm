# Bluestorm teste coding

Teste para admissao na empresa

## Instalacao de dependencias 

	pip install -r requirements.txt
	cd scripts

## Executar 

Para criacao do banco de dados 

	python create_db.py
	
Para executar o sistema

Executa um file com a aplicacao inicial sem tratamento de erros e nao compacto melhor script para ser analisado por iniciantes pois contem cada chamada em funcoes separadas.

	python app.py 

Executa um file compacto onde as funcoes fazem um controle de methodo enviado

	python app_compact.py
	
Executa um file compacto e com tratamentos de erros ex. se os dados enviados estao de acordo com os dados esperados pelo sistema 

	python app_compact_error_check.py

## Usando API 

A API conta com un sistema de autenticacao, entao nenhum comando funcionara sem a criacao de um usuario ativo, para ser criado um usuario ativo por meio da API sem usar diretamente o DB foi criado um sistema superuser este processo nao deveria existir por deixar uma brexa na seguranca ja que nao requer nenhuma autenticacao mas para proposta de um teste e facilitar foi inserido.

	http://127.0.0.1:5000/superuser

metodo - POST

{
	"name": "username",
	"password": "senha",
	"ativo": true
}

Apos a criacao do usuario usar o sistema de login 

	http://127.0.0.1:5000/login

metodo - GET

Inserir o usuario apena criado como username/password com o tipo de Basic Auth, assim sera gerado um token com validade por 20 minutos.
Copiar este token, e inserir no headers como:

key  	= x-access-token
value 	= {token copiado}

Ps. Apenas usuarios ATIVOS tem permisao de usar o sistema

### Cadastrar -  Usuarios / Clientes / Medicamentos / Vendas

	http://127.0.0.1:5000/usuarios

	http://127.0.0.1:5000/clientes

	http://127.0.0.1:5000/medicamentos

	http://127.0.0.1:5000/vendas

Metodo - POST

Body -

{
	"name": "username",
	"password": "senha",
	"ativo": True / False
}

{
	"nome": "titulo_medicamento",
	"tipo": "tipo_de_medicamento",
	"dosagem_vol": 5,
	"dosagem_type": "ml",
	"valor": 245,
	"fabricante": "nome_fabricante"
}

{
	"nome": "nome_cliente",
	"telefone": "005511967594312"
}

{
	"cli_id": 2,
	"med_id": 61
}



### Consultar geral -  Usuarios / Clientes / Medicamentos / Vendas

	http://127.0.0.1:5000/usuarios

	http://127.0.0.1:5000/clientes

	http://127.0.0.1:5000/medicamentos

	http://127.0.0.1:5000/vendas

Metodo - GET



### Atualizacao e Delete 

	http://127.0.0.1:5000/usuarios/{public_id}

	http://127.0.0.1:5000/clientes/{id}

	http://127.0.0.1:5000/medicamentos/{id}

	http://127.0.0.1:5000/vendas/{id}

Metodo - PUT / DELETE

Para o metodo PUT sao necessarios os dados a serem atualizados 

Usuarios sera atualizado apenas o inativo para ativo caso nao deseje maiso usuario fazer um DELETE

Medicamentos

{
	"nome": "titulo_medicamento",
	"tipo": "tipo_de_medicamento",
	"dosagem_vol": 5,
	"dosagem_type": "ml",
	"valor": 245,
	"fabricante": "nome_fabricante"
}

Clientes

{
	"nome": "nome_cliente",
	"telefone": "005511967594312"
}

Vendas

cli_id = ID do cliente, caso nao seja claro 
med_id = ID do medicamento

{
	"cli_id": 2,
	"med_id": 61
}

### Consultar os Medicamentos mais vendidos 

	http://127.0.0.1:5000/topmedicamentos

Retorna uma lista com todos os medicamentos ordenados por quantidade vendidas no periodo determinado 

Metodo - POST

Body -

{
	"start": "2019-12-14",
	"end": "2019-12-14"
}


### Importing CSV

Para enviar medicamentos a API por meio de un file.csv

	http://127.0.0.1:5000/import

Metodo - POST

Script client.py para enviar o csv e um file CSV com a ordem das colunas ( nao criei um sistema de analise do titulo das colunas para inserir no DB corretamente assim nao precisando ter order de coluna o file CSV )


### Export CSV

Exporta um file CSV com todos os medicamentos ordenados por quantidade vendidas no periodo determinado 

	http://127.0.0.1:5000/export

Metodo - POST

Body -

{
	"start": "2019-12-14",
	"end": "2019-12-14"
}


# Documentacao

Para criar a documentacao automatizada va em ../bluestorm/docs 

	make html
	
Ira criar a documentacao do projeto onde o index.html sera incluido em ../bluestorm/docs/_build/html
Foi criado apenas uma amostra de como criar documentacao usando Sphinx que e' a biblioteca de python onde ate a documentacao de python foi criada com ela.


# Tests Unitarios 

Para executar os testes unitarios o sistema de autenticacao deve ser removido 
