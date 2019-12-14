# Bluestorm teste coding
Teste para admissao na empresa

## Instalacao de dependencias 

pip install -r requirements.txt

python app.py

## Usando API 

### Cadastrar Usuarios / Clientes / Medicamentos / Venda

http://127.0.0.1:5000/usuarios

http://127.0.0.1:5000/clientes

http://127.0.0.1:5000/medicamentos

http://127.0.0.1:5000/venda

Metodo - POST

Body -

{
	"name": "vagner2w",
	"password": "12345",
	"ativo": 1 ou True / 0 ou False
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



