# Bluestorm teste coding
Teste para admissao na empresa

## Instalacao de dependencias 

pip install -r requirements.txt


## Executar 

Para criacao do banco de dados 

	python create_db.py
	
Para executar o sistema

	python app.py

## Usando API 

A API conta com un sistema de autenticacao, entao nenhum comando funcionara sem a creacao de um usuario ativo, para ser criado um usuario ativo por meio da API sem usar diretamente o DB foi criado um sistema superuser 

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

Inserir o super user apena creato como username/password com o tipo de Basic Auth na aba Auth, assim sera gerado um token com validade por 20 minutos.
Copiar este token, e inserir no headers como:

key  	= x-access-token
value 	= {token copiado}

Ps. Apenas usuarios ATIVOS tem permisao de usar o sistema 

### Cadastrar Usuarios / Clientes / Medicamentos / Venda

http://127.0.0.1:5000/usuarios

http://127.0.0.1:5000/clientes

http://127.0.0.1:5000/medicamentos

http://127.0.0.1:5000/venda

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
	"telefone": "005511967594312",
}

{
	"cli_id": 2,
	"med_id": 61,
}



### Consultar todos Usuarios / Clientes / Medicamentos

http://127.0.0.1:5000/usuarios

http://127.0.0.1:5000/clientes

http://127.0.0.1:5000/medicamentos

Metodo - GET



### Consultar Usuario unico

http://127.0.0.1:5000/usuarios/{username}

Metodo - GET



### Consultar os Medicamentos mais vendidos 

http://127.0.0.1:5000/topmedicamentos

Retorna uma lista com todos os medicamentos ordenados por quantidade vendidas no periodo determinado 

Metodo - POST

Body -

{
	"start": "2019-12-14",
	"end": "2019-12-14"
}

Resultado no formato - Id do medicamento, quantidade vendida
