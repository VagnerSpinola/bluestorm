'''
#========================================
# Criado por: Vagner Spinola
# Python 3.6
# Data: 15/12/2019
#========================================

    Sistema para gerenciamento de uma farmacia:
    
    Caracteristicas:

        Criacao de superuser
            A API conta com un sistema de autenticacao, entao 
            nenhum comando funcionara sem a creacao de um usuario ativo, 
            para ser criado um usuario ativo por meio da API sem usar diretamente 
            o DB foi criado um sistema superuser 

            http://127.0.0.1:5000/superuser

            metodo - POST

            Modelo de json a ser enviado no corpo do request

                {
                    "name": "username",
                    "password": "senha",
                    "ativo": true
                }

        ===================================================================================
        Controle de usuarios

            Validacao de usuario atraves de username / password
                http://127.0.0.1:5000/login

                metodo - GET
                resposta sera um token a ser inserido no headers das requests

            Acesso atraves de tokem de autenticacao 
                Modelo 
                    key  	= x-access-token
                    value 	= {token}

            Token de autenticacao expira a cada 30 minutos 


        ===================================================================================
        Cadastro de usuarios

            http://127.0.0.1:5000/usuarios

            Metodo - POST   

            Modelo de json a ser enviado no corpo do request
            {
                "name": "username",
                "password": "senha",
                "ativo": True / False
            }

        ===================================================================================
        Cadastro de medicamentos

            http://127.0.0.1:5000/medicamentos

            Metodo - POST

            Modelo de json a ser enviado no corpo do request
            {
                "nome": "titulo_medicamento",
                "tipo": "tipo_de_medicamento",
                "dosagem_vol": 5,
                "dosagem_type": "ml",
                "valor": 245,
                "fabricante": "nome_fabricante"
            }

        ===================================================================================
        Cadastro de clientes

            http://127.0.0.1:5000/clientes

            Metodo - POST

            Modelo de json a ser enviado no corpo do request
            {
                "nome": "nome_cliente",
                "telefone": "005511967594312",
            }


        ===================================================================================
        Cadastro de Vendas

            http://127.0.0.1:5000/vendas

            Metodo - POST

            Modelo de json a ser enviado no corpo do request
            {
                "cli_id": id_do_cliente,
                "med_id": id_do_medicamento,
            }

        ===================================================================================
        Controle de medicamentos mais vendidos

            http://127.0.0.1:5000/topmedicamentos

            Metodo - POST

            Modelo de json a ser enviado no corpo do request

            {
                "start": "2019-12-14",
                "end": "2019-12-14"
            }

        ===================================================================================
        Sistema de importacao de Medicamentos para o Banco de dados

            Para enviar medicamentos a API por meio de un file.csv

            http://127.0.0.1:5000/import

            Metodo - POST

            Script client.py para enviar o csv e um file CSV

        ===================================================================================
        Sistema de exportacao de Medicamentos mais vendidos em um periodo

            Para fazer download te uma lista de  medicamentos mais vendidos em um determinado periodo 
            em umformato CSV

            http://127.0.0.1:5000/export

            Metodo - POST

            Modelo de json a ser enviado no corpo do request

            {
                "start": "2019-12-14",
                "end": "2019-12-14"
            }

        ===================================================================================
        O sistema consta com Metodos [POST, GET, PUT, DELETE] para todas as atividades do banco de dados como:

        Metodo [GET] - Recebe uma lista com todos os registros 
        Metodo [POST] - Cadastra um registro no DB

        http://127.0.0.1:5000/usuarios
        http://127.0.0.1:5000/clientes
        http://127.0.0.1:5000/medicamentos
        http://127.0.0.1:5000/vendas

        Metodo [PUT] - Faz update do registro escolhido 
        Metodo [DELETE] - Faz cancelamento do registro escolhido 

        http://127.0.0.1:5000/usuarios/{public_id}
        http://127.0.0.1:5000/clientes/{id}
        http://127.0.0.1:5000/medicamentos/{id}
        http://127.0.0.1:5000/vendas{id}
'''

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os, sys
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, and_, desc
import jwt
from functools import  wraps
from flask_restful import Resource
import pandas as pd
import operator
from sqlalchemy_utils import force_auto_coercion
from settings import app, db
from model import *

force_auto_coercion()

# Tempo para expiracao do token gerado pelo login (em minutos)
# ===================================================================================
TEMPO_EXP_TOKEN = 90

#if os.path.isfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), DB_NAME)):

# configuracao da aplicacao 
# ===================================================================================
db.init_app(app)


def check_access(current_user):
    '''
        .. function:: def check_access(current_user)

        Controla se usuario que esta usando o sistema e um usuario ativo 


        :param type current_user: string
        :param current_user: Usuario logado no sistema
        :returns: Message 

    '''
    if not current_user.ativo:
        return jsonify({
            'message': 'Acesso nao autorizado'
        })


def get_lista_medicamentos(data):
    '''
    .. function:: def get_lista_medicamentos(data)

        Retorna uma lista de medicamentos mais vendidos em um determinado periodo para ser usado 
        na funcao de consulta e tambem para elaborar o CSV

        :param type data: dict
        :param data: json enviado pelo usuario para ser usado na consulta por intervalo de tempo
        :returns: lista de todos os medicamentos
    '''
    meds = Cli_Med.query.filter(and_(func.date(Cli_Med.vendido) >= data['start']), (func.date(Cli_Med.vendido) <= data['end'])).with_entities(Cli_Med.med_id, func.count(Cli_Med.med_id)).group_by(Cli_Med.med_id).all()
                                              
    meds.sort(reverse=True, key=operator.itemgetter(1))

    list_medicamentos = []

    for med in meds:
        dict_medicamentos = {}
        med_desc = Medicamentos.query.filter_by(id=med[0]).first()
        dict_medicamentos['ID medicamento'] = med[0]
        dict_medicamentos['Nome medicamento'] = med_desc.nome
        dict_medicamentos['Quantidade vendida'] = med[1]
        list_medicamentos.append(dict_medicamentos)
    return list_medicamentos


def toker_required(f):
    '''
    .. function:: def toker_required(f)

        Decorador de funcoes para ser inplementado em todas as funcoes do sistema 
        Verifica se o usuario esta usando um token e se este token e' ainda valido

        :type f: string
        :param f: E'  a funcao a ser decorada pelo decorator 
        :rtype: decorador para as funcoes 
    '''

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token  = request.headers['x-access-token']

        if not token:
            return jsonify({
                'message': 'Token nao encontrado'
            })

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Usuarios.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'message': 'Token nao encontrado'
            })
        
        return f(current_user, *args, **kwargs)

    return decorator


@app.route('/superuser', methods=['POST'])
def create_superuser():
    '''
        .. function:: def create_superuser()

        Adiciona um usuario ao sistema sem necessidade de authenticacao.
        metodo criado pelo fato de que quando o sistema e' iniciado pela primeira vez o banco de dados 
        esta vazio sendo assim ninguem teria acesso ao sistema, Metodo utilidado apenas na criacao do DB

        :returns: Mensagem do sucesso do cadastro ou erro
    '''
    data = request.get_json()
    
    if set(('name', 'password', 'ativo')).issubset(data):
        hash_pass = generate_password_hash(data['password'], method='sha256')
        new_user = Usuarios(public_id=str(uuid.uuid4()), username=data['name'], password=hash_pass, ativo=data['ativo'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Novo Usuario Cadastrado com Sucesso'})
    else:
        return jsonify({'message': 'Dados enviados em formato errado'})


@app.route('/login')
def login():
    '''
        .. function:: def login()

        Faz o login do usuario retornando um token para ser adicionado ao Headers do request 
        Verica se o usuario e password estao ok

        :returns: Retorna um tokem para ser usado nas autenticacoes
    '''

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Nao foi possivel completar a operacao', 401, {'WWW-Authenticate' : 'Basic realm="Login solicitado"'})
    
    usuario = Usuarios.query.filter_by(username=auth.username).first()

    if not usuario:
        return make_response('Nao foi possivel completar a operacao', 401, {'WWW-Authenticate' : 'Basic realm="Login solicitado"'})
    
    if check_password_hash(usuario.password, auth.password):
        token = jwt.encode({'public_id': usuario.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=TEMPO_EXP_TOKEN)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('utf-8')})
    
    return make_response('Nao foi possivel completar a operacao', 401, {'WWW-Authenticate' : 'Basic realm="Login solicitado"'})


@app.route('/usuarios', methods=['GET', 'POST'])
@toker_required
def get_all_user(current_user):

    if request.method == 'GET':
        '''
        .. function:: def get_all_user(current_user)

            Consulta os usuarios cadastrados no sistema retornado uma lista com todos os usuarios do sistema

            :param type current_user: string
            :param current_user: Usuario logado no sistema
            :returns: Retornauma lista de usuarios
        '''
        check_access(current_user)

        users = Usuarios.query.all()
        user_list = []

        for user in users:
            user_dict = {}
            user_dict['public_id'] = user.public_id
            user_dict['username'] = user.username
            user_dict['password'] = user.password
            user_dict['ativo'] = user.ativo
            user_list.append(user_dict)

        return jsonify({
            'Usuarios': user_list
        })
    elif request.method == 'POST':
        '''
            Cadastra um usuario no sitema

            :param type current_user: string
            :param current_user: Usuario logado no sistema
        '''
        check_access(current_user)

        data = request.get_json()
        if set(('name', 'password', 'ativo')).issubset(data):
            hash_pass = generate_password_hash(data['password'], method='sha256')
            new_user = Usuarios(public_id=str(uuid.uuid4()), username=data['name'], password=hash_pass, ativo=data['ativo'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Novo Usuario Cadastrado com Sucesso'})
        else:
            return jsonify({'message': 'Dados enviados em formato errado'})

    else:
        return jsonify({'message': 'Metodo nao autorizado'})
    

@app.route('/clientes', methods=['GET', 'POST'])
@toker_required
def get_all_clients(current_user):
    if request.method == 'GET':
        '''
        .. function:: def get_all_clients(current_user)

            Consulta os clientes cadastrados no sistema retornado uma lista com todos os clientes do sistema

            :param type current_user: string
            :param current_user: Usuario logado no sistema
            :returns: Retorna uma lista de clientes
        '''
        check_access(current_user)

        clientes = Clientes.query.all()
        cli_list = []

        for cliente in clientes:
            cli_dict = {}
            cli_dict['id'] = cliente.id
            cli_dict['nome'] = cliente.nome
            cli_dict['telefone'] = cliente.telefone

            cli_list.append(cli_dict)

        return jsonify({
            'Clientes': cli_list
        })

    elif request.method == 'POST':
        '''
            Cadastra um Cliente no sitema

            :param type current_user: string
            :param current_user: Usuario logado no sistema
        '''
        check_access(current_user)

        data = request.get_json()

        if set(('nome', 'telefone')).issubset(data):
            new_cli = Clientes(telefone=data['telefone'], nome=data['nome'])

            db.session.add(new_cli)
            db.session.commit()

            return jsonify({'message': 'Novo Cliente Cadastrado com Sucesso'})

        else:
            return jsonify({'message': 'Dados enviados em formato errado'})

    else:
        return jsonify({'message': 'Metodo nao autorizado'})


@app.route('/medicamentos', methods=['GET', 'POST'])
@toker_required
def get_all_med(current_user):
    if request.method == 'GET':
        '''
        .. function:: def get_all_med(current_user)

            Consulta os Medicamentos cadastrados no sistema retornado uma lista com todos os Medicamentos do sistema

            :param type current_user: string
            :param current_user: Usuario logado no sistema
            :returns: Retorna uma lista de medicamentos 
        '''
        check_access(current_user)

        meds = Medicamentos.query.all()
        med_list = []

        for med in meds:
            med_dict = {}
            med_dict['id'] = med.id
            med_dict['nome'] = med.nome
            med_dict['tipo'] = med.tipo
            med_dict['dosagem_type'] = med.dosagem_type
            med_dict['dosagem_vol'] = str(med.dosagem_vol)
            med_dict['valor'] = str(med.valor)
            med_dict['fabricante'] = med.fabricante
            med_list.append(med_dict)

        return jsonify({
            'Medicamentos': med_list
        })
    elif request.method == 'POST':
        '''
            Cadastra um Medicamento no sitema

            :type current_user: string
            :param current_user: Usuario logado no sistema
        '''

        check_access(current_user)

        data = request.get_json()
        if set(('nome', 'tipo', 'dosagem_type', 'dosagem_vol', 'valor', 'fabricante')).issubset(data):
            new_med = Medicamentos( nome=data['nome'], 
                                tipo=data['tipo'],
                                dosagem_type=data['dosagem_type'], 
                                dosagem_vol=data['dosagem_vol'], 
                                valor=data['valor'], 
                                fabricante=data['fabricante'])

            db.session.add(new_med)
            db.session.commit()

            return jsonify({'message': 'Novo Medicamento Cadastrado com Sucesso'})
        else:
            return jsonify({'message': 'Dados enviados em formato errado'})

    else:
        return jsonify({'message': 'Metodo nao encontrado'})


@app.route('/vendas', methods=['POST', 'GET'])
@toker_required
def create_venda(current_user):
    if request.method == 'POST':
        '''
        .. function:: def create_venda(current_user)

            Cadastra uma venda no sitema

            :param type current_user: string
            :param current_user: Usuario logado no sistema
            :returns: Retorna uma lista de vendas 
        '''

        check_access(current_user)

        data = request.get_json()
        if set(('cli_id', 'med_id')).issubset(data):
            new_venda = Cli_Med( cli_id=data['cli_id'], 
                                med_id=data['med_id'])

            db.session.add(new_venda)
            db.session.commit()

            return jsonify({'message': 'Nova Venda Cadastrada com Sucesso'})
        else:
            return jsonify({'message': 'Dados enviados em formato errado'})


    elif request.method == 'GET':
        '''
            Consulta as Vendas cadastrados no sistema retornado uma lista com todos os Vendas do sistema

            :param type current_user: string
            :param current_user: Usuario logado no sistema
        '''
        check_access(current_user)

        vendas = Cli_Med.query.all()
        vendas_list = []

        for venda in vendas:
            vendas_dict = {}
            vendas_dict['id'] = venda.id
            vendas_dict['cli_id'] = venda.cli_id
            vendas_dict['med_id'] = venda.med_id
            vendas_dict['vendido'] = venda.vendido

            vendas_list.append(vendas_dict)

        return jsonify({
            'Vendas': vendas_list
        })
    else:
        return jsonify({'message': 'Metodo nao autorizado'})

    
@app.route('/topmedicamentos', methods=['POST'])
@toker_required
def get_top_med(current_user):
    '''
        .. function:: def get_top_med(current_user)

        Consulta os Medicamentos Vendidos cadastrados no sistema retornado uma lista com todos os Medicamentos 
        vendidos em um periodo determinado pelo usuario

        :param type current_user: string
        :param current_user: Usuario logado no sistema
        :returns: Retorna todos os medicamentos em ordem decrecente 
    '''
    check_access(current_user)

    data = request.get_json()
    list_medicamentos = get_lista_medicamentos(data)

    return jsonify({
        'Medicamentos' : list_medicamentos
    })


@app.route('/usuarios/<username>', methods=['GET'])
@toker_required
def get_user(current_user, username):
    '''
    .. function:: def get_user(current_user, username)

        Consulta os usuarios cadastrados no sistema retornado as informacoes de apenas os usuarios
        com username passado pelo usuario 

        :param type current_user: string
        :param current_user: Usuario logado no sistema

        :param type username: string
        :param username: username do usuario a ser consultado 
        :returns: Retorna o usuario desejado
    '''
    check_access(current_user)

    users = Usuarios.query.filter_by(username=username)
    user_list = []

    if not users:
        return jsonify({'message': 'Nenhum usuario encontrado'})
    else:
        for user in users:
            user_dict = {}
            user_dict['public_id'] = user.public_id
            user_dict['username'] = user.username
            user_dict['password'] = user.password
            user_dict['ativo'] = user.ativo
            user_list.append(user_dict)

        return jsonify({ 'Usuario': user_list })


@app.route('/usuarios/<public_id>', methods=['PUT', 'DELETE'])
@toker_required
def update_user(current_user, public_id):
    if request.method == 'PUT':
        '''
        .. function:: def update_user(current_user, public_id)

            Deleta o usuario cadastrado no sistema com public_id fornecido pelo usuario 

            :param type current_user: string
            :param current_user: Usuario logado no sistema

            :param type public_id: integer
            :param public_id: ID publico do Usuario a ser Apagado do banco de dados
            :returns: Atualiza ou deleta o usuario desejado 
        '''

        check_access(current_user)

        user = Usuarios.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message': 'Nenhum usuario encontrado'})
    
        user.ativo = True
        db.session.commit()
        return jsonify({'message': 'Usuario ativado'})

    elif request.method == 'DELETE':
        '''
        .. function:: def update_user(current_user, public_id)

            Deleta o usuario cadastrado no sistema com public_id fornecido pelo usuario 

            :param type current_user: string
            :param current_user: Usuario logado no sistema

            :param type public_id: integer
            :param public_id: ID publico do Usuario a ser Apagado do banco de dados
            :returns: Atualiza ou deleta o usuario desejado 
        '''
        
        check_access(current_user)
        user = Usuarios.query.filter_by(public_id=public_id).one()
        if not user:
            return jsonify({'message': 'Nenhum usuario encontrado'})

        try:
            db.session.delete(user)
        except Exception as e:
            return jsonify({
                'message': 'Error ao deletar usuario',
                'Error': str(e)
            })
        finally:
            db.session.commit()

        return jsonify({'message': 'Usuario Foi Deletado com Sucesso'})
    else:
        return jsonify({'message': 'Metodo nao autorizado'})


@app.route('/clientes/<id>', methods=['PUT', 'DELETE'])
@toker_required
def delete_cliente(current_user, id):
    
    if request.method == 'DELETE':
        '''
        .. function:: def delete_cliente(current_user, id)

            Deleta o cliente cadastrado no sistema com id fornecido pelo usuario 

            :param type current_user: string
            :param current_user: Usuario logado no sistema

            :param type id: integer
            :param id: ID do Clientes a ser Apagado do banco de dados
            :returns: Atualiza ou deleta o cliente desejado 
        '''
        check_access(current_user)

        cliente = Clientes.query.filter_by(id=id).first()
        if not cliente:
            return jsonify({'message': 'Nenhum Cliente encontrado'})

        db.session.delete(cliente)
        db.session.commit()

        return jsonify({'message': 'Cliente Foi Deletado com Sucesso'})
    elif request.method == 'PUT':
        '''
            Atualiza o cliente cadastrado no sistema com id fornecido pelo usuario 

            :param type current_user: string
            :param current_user: Usuario logado no sistema

            :param type id: integer
            :param id: ID de Clientes a ser Atualizado no banco de dados
        '''

        check_access(current_user)
        data = request.get_json()

        cliente = Clientes.query.filter_by(id=id).first()
        if not cliente:
            return jsonify({'message': 'Nenhum Cliente encontrado'})
    
        cliente.nome = data['nome']
        cliente.telefone = data['telefone']
        db.session.commit()

        return jsonify({'message': 'Cliente Atualizado'})
    else:
        return jsonify({'message': 'Metodo nao autorizado'})
    

@app.route('/medicamentos/<id>', methods=['PUT', 'DELETE'])
@toker_required
def update_medicamentos(current_user, id):
    if request.method == 'PUT':
        '''
        .. function:: def update_medicamentos(current_user, id)

            Atualiza o Medicamento cadastrado no sistema com id fornecido pelo usuario 

            :param type current_user: string
            :param current_user: Usuario logado no sistema

            :param type id: integer
            :param id: ID de Medicamentos a ser Atualizado no banco de dados
            :returns: Atualiza ou deleta o medicamento desejado 
        '''

        check_access(current_user)
        data = request.get_json()

        med = Medicamentos.query.filter_by(id=id).first()
        if not med:
            return jsonify({'message': 'Nenhum Medicamento encontrado'})
    
        med.nome = data['nome']
        med.tipo = data['tipo']
        med.dosagem_type = data['dosagem_type']
        med.dosagem_vol = data['dosagem_vol']
        med.valor = data['valor']
        med.fabricante = data['fabricante']

        db.session.commit()

        return jsonify({'message': 'Medicamento Atualizado'})
    elif request.method == 'DELETE':
        '''
            Deleta o medicamento cadastrado no sistema com id fornecido pelo usuario

            :param type current_user: string
            :param current_user: Usuario logado no sistema

            :param type id: integer
            :param id: ID do Medicamento a ser Apagado do banco de dados
        '''
        check_access(current_user)

        med = Medicamentos.query.filter_by(id=id).first()
        if not med:
            return jsonify({'message': 'Nenhum Medicamento encontrado'})

        db.session.delete(med)
        db.session.commit()

        return jsonify({'message': 'Medicamento Foi Deletado com Sucesso'})

    else:
        return jsonify({'message': 'Metodo nao autorizado'})
        

@app.route('/vendas/<id>', methods=['PUT', 'DELETE'])
@toker_required
def delete_vendas(current_user, id):

    if request.method == 'DELETE':
        '''
        .. function:: def delete_vendas(current_user, id)

            Deleta a venda cadastrado no sistema com id fornecido pelo usuario 

            :param type current_user: string
            :param current_user: Usuario logado no sistema

            :param type id: integer
            :param id: ID de Vendas da tabela Cli_Med referente ao relacionamento Cliente x Medicamentos
            :returns: Deleta o registro desejado
        '''

        check_access(current_user)

        venda = Cli_Med.query.filter_by(id=id).first()
        if not venda:
            return jsonify({'message': 'Nenhuma Venda encontrado'})

        db.session.delete(venda)
        db.session.commit()

        return jsonify({'message': 'Venda Foi Deletado com Sucesso'})
    elif request.method == 'PUT':
        '''
            Atualiza a venda cadastrado no sistema com id fornecido pelo usuario 

            :param type current_user: string
            :param current_user: Usuario logado no sistema

            :param type id: integer
            :param id: ID de Vendas a ser Atualizado no banco de dados
        '''

        check_access(current_user)
        data = request.get_json()
        if set(('cli_id', )).issubset(data):
            venda = Cli_Med.query.filter_by(id=id).first()
            if not venda:
                return jsonify({'message': 'Nenhuma Venda encontrado'})
        
            venda.cli_id = data['cli_id']
            venda.med_id = data['med_id']
            db.session.commit()

            return jsonify({'message': 'Venda Atualizada'})
        else:
            return jsonify({'message': 'Dados enviados em formato errado'})

    else:
        return jsonify({'message': 'Metodo nao autorizado'})


@app.route('/import', methods=['POST'])
@toker_required
def import_csv(current_user):
    '''
    .. function:: def import_csv(current_user)

        Importa um file CSV com imformacoes dos medicamentos que devem serem cadastrados 
        no sistema em modo automatico 

        :param type current_user: string
        :param current_user: Usuario logado no sistema
        :returns: Retorna uma mensagem de file recebido
    '''

    check_access(current_user)
    if set(('file')).issubset(request.files):
        file = request.files['file']
        data = pd.read_csv(file)
        
        for _, row in data.iterrows():
            new_med = Medicamentos( nome=row[0], 
                                tipo=row[1],
                                dosagem_type=row[2], 
                                dosagem_vol=row[3], 
                                valor=row[4], 
                                fabricante=row[5])

            db.session.add(new_med)
            db.session.commit()

        return jsonify({'message': 'csv receved'})
    else:
        return jsonify({'message': 'Dados enviados em formato errado'})





@app.route('/export', methods=['POST'])
@toker_required
def export_csv(current_user):
    '''
    .. function:: def export_csv(current_user)

        Exporta um file CSV com informacoes dos medicamentos mais vendidos em um periodo de 
        tempo fornecido pelo usuario 

        :param type current_user: string
        :param current_user: Usuario logado no sistema
        :returns: Faz o download do file CSV  e retorna a lista dentro do file
    '''
    check_access(current_user)

    data = request.get_json()
    if set(('start', 'end')).issubset(data):
        list_medicamentos = get_lista_medicamentos(data)

        df = pd.DataFrame(list_medicamentos)
        df.to_csv("TOPMedicamentos_{}_{}.csv".format(data['start'], data['end']) )

        return jsonify({
            'message': 'Download CSV completado',
            'data' : list_medicamentos
        })
    else:
        return jsonify({'message': 'Dados enviados em formato errado'})



# Inicia o sistema 
# ===================================================================================
if __name__=='__main__':
    app.run(debug=True)
