from flask_testing import TestCase
from flask import  current_app, url_for

from main import  app

class MainTest(TestCase):
    #debemos implementar este metodo obligatorio, debe regresar una aplicacion de flask
    def create_app(self):
        #flask va a saber que estamos haciendo prueba, en el mabiente de testing
        app.config['TESTING'] = True
        #vamos a indicarle que no vamos a usar WTF_CSRF_ENABLED token de las formas
        #en este caso no tenemos una session activa del usuario, entonces si queremos probar formas nos va a pedir
        #que tengamos un token que nos previene de los ataques en los que nos pueden inyectar scripts
        #ese token lo podemos ver en nuestra forma en la que flask-botstrap la renderio, minuto 6:40 clase Flask-testing
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    #probar si nuestra app de flask existe
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    #probar si la app se encuentra en el ambiente de testing
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    #probar que nuestro index nos redirije a hello
    def test_index_redirect(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('hello'))

    #probar que hello nos regresa 200 cuando hacemos un get
    def test_hello_get(self):
        response = self.client.get(url_for(('hello')))
        self.assert200(response)

    #estamos validando que cuando hacemos un post a hello nos esta rederigiendo a index
    def test_hello_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake'
        }
        response = self.client.post(url_for('hello'), data=fake_form)
        self.assertRedirects(response, url_for('index'))

    #para probar si un mensaje fue flasheado
    def test_user_registered_flashed_message(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake'
        }
        self.client.post(url_for('index'), data=fake_form)
        message = 'User registered successfully'
        self.assert_message_flashed(message)



