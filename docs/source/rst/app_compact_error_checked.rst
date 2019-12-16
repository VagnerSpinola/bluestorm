===========
Bibliotecas
===========

flask
=====

.. code-block:: python

   from flask import Flask, request, jsonify, make_response
   from flask_sqlalchemy import SQLAlchemy



=========
Aplicacao
=========

check_access
============

.. code-block:: python

   def check_access(current_user):	
       '''

        Controla se usuario que esta usando o sistema e um usuario ativo 


        param current_user : string
        param current_user : Usuario logado no sistema
        returns : Message  

		'''
	    return jsonify({message': 'Acesso nao autorizado'})



get_lista_medicamentos
======================

.. code-block:: python

   def get_lista_medicamentos(data):
	   '''

	   Retorna uma lista de medicamentos mais vendidos em um determinado periodo para ser usado 
	   na funcao de consulta e tambem para elaborar o CSV

	   param data: dict
	   param data: json enviado pelo usuario para ser usado na consulta por intervalo de tempo
	   returns: lista de todos os medicamentos
	   '''      
	   return list_medicamentos



==============
Banco de Dados
==============

Usuarios
========

.. code-block:: python

   class Usuarios(db.Model):
       '''
	Usuarios
	Tabela para o controle de acesso dos usuarios conta com uma chave public_id para que o ID do usuario nao seja divulgado para outros usuarios, um campo ativo caso este campo seja falso o usuario nao tem acesso ao sistema API sendo assim necessario que um usuario ATIVO (True) faca update do outro usuario para que o mesmo posso acessar o sistema.

	:param db.Model: object
	:param db.Model: importa todos os tipos de dados para criar a tabela
       '''



Medicamentos
============

.. code-block:: python

   class Medicamentos(db.Model):
	'''
		Tabela com caracteristicas dos mediacamentos cadastrados no sistema.

		:type db.Model: object
		:param db.Model: importa todos os tipos de dados para criar a tabela           
	'''











