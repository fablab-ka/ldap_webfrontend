# coding: utf8
from ldap_class import LdapClass
import ldap3
import bottle
from bottle import template, route, request, redirect, get, post, hook
from gevent import monkey; monkey.patch_all()
from beaker.middleware import SessionMiddleware
import configparser
import io
import os
import sys

# Check if there is already a configurtion file
if not os.path.isfile("config.ini"):
    Config = configparser.ConfigParser()
    Config.add_section('ldap')
    Config.set('ldap', 'server', 'ldap://127.0.0.1')
    Config.set('ldap', 'bind', 'cn=admin,dc=lab,dc=flka,dc=de')
    Config.set('ldap', 'password', 'secret')
    Config.set('ldap', 'ldap_base', 'dc=lab,dc=flka,dc=de')
    Config.set('ldap', 'ou_users', 'ou=users')
    Config.set('ldap', 'ou_groups', 'ou=groups')
    Config.set('ldap', 'gid_number', '500')
    with open("config.ini", 'w') as cfgfile:
        Config.write(cfgfile)

# Load the configuration file
with open("config.ini") as f:
    sample_config = f.read()
config = configparser.RawConfigParser()
config.read("config.ini")

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)


@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']


@get('/login')
def login():
    return '''
            <form action="/login" method="post">
                Username: <input name="username" type="text" />
                Password: <input name="password" type="password" />
                <input value="Login" type="submit" />
            </form>
        '''


@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    bind_dn = 'cn='+username+','+config['ldap']['ou_users']+','+config['ldap']['ldap_base']
    try:
        ldap = LdapClass(connection=config['ldap']['server'],
                     bind_dn=bind_dn,
                     password=password,
                     base_dn=config['ldap']['ldap_base'],
                     ou_users=config['ldap']['ou_users'],
                     ou_groups=config['ldap']['ou_groups'],
                     gidNumber=config['ldap']['gid_number'])
        user = ldap.search(dn=bind_dn)[0]
        request.session['dn'] = bind_dn
        request.session['group'] = grouplist(ldap)[user['attributes']['gidNumber']]
        request.session['gidNumber'] = user['attributes']['gidNumber']
    except ldap3.core.exceptions.LDAPBindError:
        return "Invalid Credentials!"
    return redirect('/')


@route('/logout')
def logout():
    if 'dn' in request.session:
        del request.session['dn']
    if 'group' in request.session:
        del request.session['group']
    if 'gidNumber' in request.session:
        del request.session['gidNumber']
    return redirect('/login')

@route('/user_list')
def show_users():
    if 'gidNumber' in request.session and request.session['gidNumber'] > 201:
        ldap = LdapClass(connection=config['ldap']['server'],
                     bind_dn=config['ldap']['bind'],
                     password=config['ldap']['password'],
                     base_dn=config['ldap']['ldap_base'],
                     ou_users=config['ldap']['ou_users'],
                     ou_groups=config['ldap']['ou_groups'],
                     gidNumber=config['ldap']['gid_number'])
        users = ldap.search('(objectClass=posixAccount)')
        return template('user_list.tpl', users=users, groups=grouplist(ldap))
    else:
        redirect('/login')


@route('/user_info/<dn>')
def user_info(dn):
    if 'gidNumber' in request.session and (request.session['gidNumber'] > 201 or request.session['dn'] == dn):
        ldap = LdapClass(connection=config['ldap']['server'],
                     bind_dn=config['ldap']['bind'],
                     password=config['ldap']['password'],
                     base_dn=config['ldap']['ldap_base'],
                     ou_users=config['ldap']['ou_users'],
                     ou_groups=config['ldap']['ou_groups'],
                     gidNumber=config['ldap']['gid_number'])
        users = ldap.search('(objectClass=posixAccount)', dn=dn)
        return template('user_info.tpl', user=users[0], groups=grouplist(ldap))
    else:
        redirect('/login')


@route('/')
def main_menu():
    user = ""
    gid = 0
    if 'dn' in request.session:
        user = request.session['dn']
        gid = request.session['gidNumber']
    return template('main_menu.tpl', user=user, gid=gid)

def grouplist(ldap):
    groups = ldap.search('(objectClass=posixGroup)')
    group_list = {}
    for group in groups:
        group_list.update({group['attributes']['gidNumber']: group['attributes']['cn'][0]})
    return group_list


@route('/register')
def show_reg_form():
    return template('reg_form.tpl')


@post('/send_reg')
def register():
    name = request.forms.name
    surname = request.forms.surname
    email = request.forms.email
    password = request.forms.password
    uid = request.forms.uid
    try:
        ldap = LdapClass(connection=config['ldap']['server'],
                         bind_dn=config['ldap']['bind'],
                         password=config['ldap']['password'],
                         base_dn=config['ldap']['ldap_base'],
                         ou_users=config['ldap']['ou_users'],
                         ou_groups=config['ldap']['ou_groups'],
                         gidNumber=config['ldap']['gid_number'])
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        return "Could not connect to LDAP webserver at " + config['ldap']['server']
    ldap.add_user(name=name, surname=surname, email=email, password=password, uid=uid)
    bind_dn = 'cn=' + email + ',' + config['ldap']['ou_users'] + ',' + config['ldap']['ldap_base']
    try:
        ldap = LdapClass(connection=config['ldap']['server'],
                         bind_dn=bind_dn,
                         password=password,
                         base_dn=config['ldap']['ldap_base'],
                         ou_users=config['ldap']['ou_users'],
                         ou_groups=config['ldap']['ou_groups'],
                         gidNumber=config['ldap']['gid_number'])
        user = ldap.search(dn=bind_dn)[0]
        request.session['dn'] = bind_dn
        request.session['group'] = grouplist(ldap)[user['attributes']['gidNumber']]
        request.session['gidNumber'] = user['attributes']['gidNumber']
    except ldap3.core.exceptions.LDAPBindError:
        return "Could not login, invalid Credentials!"
    return redirect('/')


bottle.run(app=app, host='0.0.0.0', port=8095, server='gevent')