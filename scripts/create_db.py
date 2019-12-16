from settings import app, db
import os


class Create_db(object):

    def __init__(self, db_name):
        '''
            Inicia as variaveis

            :type db_name: string
            :param db_name: Path + nome do banco de dados
        '''
        self.db_name = db_name

    def create(self):
        '''
            Cria o banco de dados se ainda nao foi criado 
        '''
        
        # Verifica se o Banco de dados existe ou nao para evitar sobrescrever 
        if os.path.isfile(self.db_name):
            print('Database  ja Criado')
        else:
            with app.app_context():
                db.create_all()
                print('Banco de dados criado con sucesso \n \n proceda com o commando: \n ---> python app.py')


if __name__=='__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_name = os.path.join(basedir, 'bluestorm.db')

    database = Create_db(db_name)
    database.create()
