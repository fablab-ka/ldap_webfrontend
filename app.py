from ldap_class import LdapClass
import bottle
from bottle import template, route, request, post
from gevent import monkey; monkey.patch_all()
from beaker.middleware import SessionMiddleware
import configparser
import io
import os

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


@route('/')
@route('/register')
def show_reg_form():
    return template('reg_form.tpl')


@post('/send_reg')
def register():
    name = request.forms.name
    surname = request.forms.surname
    email = request.forms.email
    password = request.forms.password
    print(name)
    try:
        ldap = LdapClass(connection=config['ldap']['server'],
                         bind_dn=config['ldap']['bind'],
                         password=config['ldap']['password'],
                         base_dn=config['ldap']['ldap_base'],
                         ou_users=config['ldap']['ou_users'],
                         ou_groups=config['ldap']['ou_groups'],
                         gidNumber=config['ldap']['gid_number'])
    except:
        return "Could not connect to LDAP webserver at " + config['ldap']['server']
    success = ldap.add_user(name=name, surname=surname, email=email, password=password)
    if not success:
        return "Could not register User to LDAP Server!"
    return "Registration complete!"


bottle.run(app=app, host='0.0.0.0', port=8095, server='gevent')