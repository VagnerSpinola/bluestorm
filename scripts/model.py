from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PasswordType, force_auto_coercion, types
import passlib
from passlib.context import LazyCryptContext
import enum
import os
import sys
import psycopg2
import psycopg2.extras
import datetime
from sqlalchemy import DateTime
from settings import app, db


class Usuarios(db.Model):
    '''
        Define as tablelas do banco de dados:

        Usuarios
            Tabela para o controle de acesso dos usuarios conta com uma chave public_id para que o ID do usuario nao seja divulgado para outros usuarios, 
            e um campo ativo caso este campo seja falso o usuario nao tem acesso ao sistema API sendo assim necessario que um usuario ATIVO (True) faca update 
            do outro usuario para que o mesmo posso acessar o sistema.

            :type db.Model: object
            :param db.Model: importa todos os tipos de dados para criar a tabela
    '''
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(80))
    ativo =  db.Column(db.Boolean, default=True)


class Medicamentos(db.Model):
    '''
        Define as tablelas do banco de dados:

        Medicamentos
            Tabela com caracteristicas dos mediacamentos cadastrados no sistema.

            :type db.Model: object
            :param db.Model: importa todos os tipos de dados para criar a tabela           
    '''
    __tablename__ = 'Medicamentos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30))
    tipo = db.Column(db.String(20))
    dosagem_type = db.Column(db.String(2))
    dosagem_vol = db.Column(db.Integer)
    valor = db.Column(db.Numeric(10,2))
    fabricante = db.Column(db.String(80))


class Clientes(db.Model):
    '''
        Define as tablelas do banco de dados:

        Clientes
            Tabela com caracteristicas dos Cliente da empresa. TODO o sistema nao faz validacao do campo telefone 

            :type db.Model: object
            :param db.Model: importa todos os tipos de dados para criar a tabela           
    '''
    __tablename__ = 'Clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(60))
    telefone = db.Column(db.String(15))


class Cli_Med(db.Model):
    '''
        Define as tablelas do banco de dados:

        Cli_Med
            Tabela faz o relacionamento entre as tabelas Clientes e Medicamentos podendo assim um cliente ter varios medicamentos e um medicamento ter varios clientes 
            Relacao Many-to-Many

            :type db.Model: object
            :param db.Model: importa todos os tipos de dados para criar a tabela
            
    '''
    __tablename__ = 'Cli_Med'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cli_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'))
    med_id = db.Column(db.Integer, db.ForeignKey('Medicamentos.id'))
    vendido = db.Column(DateTime, default=datetime.datetime.utcnow)