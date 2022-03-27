import unittest

from flask import  Flask, request, make_response, redirect, render_template, session, url_for, flash

'''
objetos
request -> informacion sobre la peticion que realiza al browser
session -> storage que permanece entre cada request
current_app -> la aplicacion actual,  nos va a dar informacion de la aplicacion que esta corriendo
g -> Storage temporal, se reinicia en cada request, por cada request 
'''

from flask_bootstrap import  Bootstrap
from flask_wtf import  FlaskForm
from wtforms.fields import  StringField, PasswordField, SubmitField
#existen un monton de validadores
from wtforms.validators import DataRequired

import unittest

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')


'''
en template_folder van los archivos html
en static van los recursos como las imagenes y los archivos .css -> manejo de archivos estaticos
'''

app = Flask(__name__, template_folder='templates', static_folder='static')

'''
Aqui van las variables de configuración, peroe en la documentación de flask nos dicen lo siquiente, que a pesar de que 
es posible establecer las configuraciones ENV y DEBUG dentro de nuestro código o en las configuraciones, eso es muy mala
practica ya que esas configuraciones no pueden ser leidas por el comando flask run y algunas extensiones o sistemas se configuran
desde el mismo momento en que corremos ese comando, entonces si configuramos las variables ENV y DEBUG dentro del codigo puede ser
que algunas extenciones de flask no funcionen bien porque necesitan tener la información que esas variables guardan desde  el mismo
momneto en que arrancamos el servidor
'''
app.config.update(
    DEBUG= True,
    ENV= 'development'
)


'''aqui agregamos las extensiones de Flask, practicamente la mayoria de estas extensiones se hacen de esa manera
en este caso con Bootstrap toca hacerlo, pero con flask-wtform no hay necesidad de hacer esto'''
bootstrap = Bootstrap(app)

'''para guardar informacion que se mantenga hacemos uso de session, para hacer uso de session necesitamos generar una clave '''
app.config['SECRET_KEY'] = 'SUPER SECRETO'

todos = ['TODO 1', 'TODO 2', 'TODO 3']


'''
vamos aprender como manejar errores, para rutas que no estan declaradas en nuestro proyecto
-flask dispone de un decorador llamado app.errorhandler(404)
-Un decorador no es más que un envoltorio de una función
'''


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error = error)


@app.cli.command()
def test():
    #nos va a permitir explorar toda la carpeta donde tenemos nuestros tests o todo el directorio donde estan los tests
    # y unittest se encargara de correr todos los tests
    #la forma de leer la linea 75 es la siguiente , los test van hacer todo lo que encuentre en la carpeta que se encuentra
    #en el directorio raiz test
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(tests)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    '''
    guardar la ip dentro de una cookie dentro del navegador, no es la forma segura de hacerlo o cualquier informacion compleja
    '''
    #response.set_cookie('user_ip', user_ip)
    '''Guardar en session'''
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods = ['GET', 'POST'])
def home():
    #obtenemos la ip del usuario a traves de cookie
    #user_ip = request.cookies.get('user_ip')

    #obetnemos la ip del usuario con session
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }

    '''cuanod llamamos el metodo validate_on_submit, esta ruta va a detectar cuando estas mandando un post y va a validar la forma
    de esta forma estamos dividiendo esta funcion en dos partes'''
    if login_form.validate_on_submit():
        print('entro por aca')
        username = login_form.username.data
        session['username'] = username

        '''vamos a crear ahora un flash(mensajes emergentes), es un banner que va aparecer abajo de nuestra barra de navegacion donde
        indica mensaje de exitos, error, o warning, entre otros
        1.importar flash'''

        '''de esta manera  flash va a guardar un mensaje dentro de memoria los flashes, los flashes debemos renderiarlos dentro de los html'''
        flash('Nombre de usuario registrado con exito')

        '''como se hace redirecciones desde flask, nos importamos url_for'''
        return redirect(url_for('index'))


    return render_template('hello.html', **context, cosita = 1)


'''
vamos aprender como hacer pruebas con flask, probar nuestro software antes de hacer deploy, para que el usuario no se encuentre con errores
las pruebas nos va ayudar hacer todo esto.
1.primero instalamos una extension flask-testing
2.crear un comando en la consola, para cuando corramos flask test corrar todas las pruebas necesarias
3.crear un decorador @app.cli.command() -> creamos un nuevo comando, se llama test def test() del nombre de la clase
4.despues se escribir los tests, se crea un archivo que debe empezar  con la palabra test porque lo que va hacer
unitest es buscar todos los archivos que empiecen con test y correrlos 
'''

if __name__ == '__main__':
    app.run()