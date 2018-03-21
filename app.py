from bottle import run, route, template, request, response, redirect
import os

#Einfalt cookie sýnidæmi
'''''
@route('/')
def index():
    if request.get_cookie('hello'):
        return 'Hello again'
    else:
        response.set_cookie('hello', 'world')
        return "cookies test"
'''''

adminuser = 'admin'
adminpwd = '12345'

@route('/')
def index():
    return template('index')

@route('/login')
def login():
    return template('login')

@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username == adminuser and password == adminpwd:
        response.set_cookie('account', username, secret='my_secret_code')
        return redirect('/restricted')
    else:
        return "Login failed. <br> <a href='login'>Login</a>"

@route('/restricted')
def restricted():
    user = request.get_cookie('account', secret='my_secret_code')
    if(user):
        return "Restriced area <br> " \
               "<a href='/signout'> Log off</a>"
    else:
        return "You are no logged in. Access denied."

@route('/signout')
def signput():
    response.set_cookie('account', "", expires=0)
    return "You have signed out" \
           "<br> <a href='/login'>Log in</a>"



run()