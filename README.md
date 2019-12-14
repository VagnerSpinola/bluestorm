# Bluestorm teste coding
Teste para admissao na empresa

## Instalacao de dependencias 

pip install -r requirements.txt

python app.py

## Usando API 

### Cadastrar Usuarios / Clientes / Medicamentos

http://127.0.0.1:5000/usuarios

http://127.0.0.1:5000/clientes

http://127.0.0.1:5000/medicamentos

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

### Consultar todos Usuarios / Clientes / Medicamentos

http://127.0.0.1:5000/usuarios

http://127.0.0.1:5000/clientes

http://127.0.0.1:5000/medicamentos

Metodo - GET

### Consultar Usuario unico

http://127.0.0.1:5000/usuarios/{username}

Metodo - GET



