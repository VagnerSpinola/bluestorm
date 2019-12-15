from settings import app
import unittest
from json import dumps

class FlaskTestCase(unittest.TestCase):
    '''
        Para fazer os teste precisa desativar o sistema de autenticacao pois o token e' necessario para todas as funcoes
    '''
    def test_superuser(self):
        tester = app.test_client(self)
        r = tester.post('/superuser', 
                    data=dumps({ "name": "username", "password": "senha", "ativo": True }),
                    content_type='application/json'
                    )
        self.assertEqual(r.status_code, 200)

    def del_user(self):
        tester = app.test_client(self)
        r = tester.delete('/usuarios/42a92f85-d1ac-4a43-9789-4e4260fb77ed')
        self.assertEqual(r.status_code, 200)

    def add_clientes(self):
        tester = app.test_client(self)

        r = tester.post('/clientes', 
                    data=dumps({ "nome": "nome_cliente", "telefone": "005511967594312" }),
                    content_type='application/json'
                    )
        self.assertEqual(r.status_code, 200)

    def update_medicamentos(self):
        tester = app.test_client(self)
        r = tester.put('/medicamentos/1', 
                    data=dumps({ "nome": "titulo_medicamento1", "tipo": "comprimido", "dosagem_vol": 5, "dosagem_type": "ml", "valor": 245, "fabricante": "nome_fabricante" }),
                    content_type='application/json'
                    )
        self.assertEqual(r.status_code, 200)

    def export(self):
        tester = app.test_client(self)
        r = tester.post('/export', 
                        data=dumps({ "start": "2019-12-14", "end": "2019-12-14" }), 
                        content_type='application/json'
                        )
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()