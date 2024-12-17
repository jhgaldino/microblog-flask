import unittest
from app import create_app
from app.extensions import db, bcrypt
from app.models import User, Post

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Desabilita CSRF para testes
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Cria um usuário de teste
            hashed_password = bcrypt.generate_password_hash('testpass').decode('utf-8')
            user = User(username='testuser', password=hashed_password)
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_home_route_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redireciona para login

    def test_register_route_get(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_register_route_post(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Feed', response.data)

    def test_login_route_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_route_post(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Feed', response.data)

    def test_feed_route_access_denied(self):
        response = self.client.get('/feed', follow_redirects=True)
        self.assertIn(b'Login', response.data)  # Deve redirecionar para login

    def test_feed_route_access_granted(self):
        # Primeiro, faz login
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        # Acessa a rota feed
        response = self.client.get('/feed')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Feed', response.data)

    def test_new_post(self):
        # Faz login
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        # Obtém o token CSRF
        response = self.client.get('/feed')
        csrf_token = self.get_csrf_token(response.data)
        # Envia um novo post
        response = self.client.post('/feed', data={
            'body': 'Este é um novo post de teste.',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Este é um novo post de teste.'.encode('utf-8'), response.data)

    def get_csrf_token(self, response_data):
        # Extrai o token CSRF da resposta
        import re
        match = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', response_data.decode('utf-8'))
        return match.group(1) if match else None

    def test_logout(self):
        # Faz login
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        # Faz logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Deve redirecionar para login

def test_home_route_redirect(client):
    response = client.get('/')
    assert response.status_code == 302  # Redireciona para login

def test_register_route_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_register_route_post(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Feed' in response.data

if __name__ == '__main__':
    unittest.main()