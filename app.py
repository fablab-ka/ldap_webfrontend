from ldap_class import LdapClass
import bottle
from bottle import template, route, request, post
from beaker.middleware import SessionMiddleware
import ConfigParser
import io
import os

# Check if there is already a configurtion file
if not os.path.isfile("config.ini"):
    cfgfile = open("config.ini", 'w')
    Config = ConfigParser.ConfigParser()
    Config.add_section('ldap')
    Config.set('ldap', 'server', 'ldap://127.0.0.1')
    Config.set('ldap', 'bind', 'cn=admin,dc=lab,dc=flka,dc=de')
    Config.set('ldap', 'password', 'secret')
    Config.set('ldap', 'ldap_base', 'dc=lab,dc=flka,dc=de')
    Config.set('ldap', 'ou_users', 'ou=users')
    Config.set('ldap', 'ou_groups', 'ou=groups')
    Config.set('ldap', 'gid_number', '500')
    Config.write(cfgfile)
    cfgfile.close()

# Load the configuration file
with open("config.ini") as f:
    sample_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

ldap = LdapClass(connection=config.get('ldap', 'server'),
                 bind_dn=config.get('ldap', 'bind'),
                 password=config.get('ldap', 'password'),
                 base_dn=config.get('ldap', 'ldap_base'),
                 ou_users=config.get('ldap', 'ou_users'),
                 ou_groups=config.get('ldap', 'ou_groups'),
                 gidNumber=config.get('ldap', 'gid_number'))

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


@route('/test')
def test():
    s = bottle.request.environ.get('beaker.session')
    s['test'] = s.get('test',0) + 1
    s.save()
    return 'Test counter: %d' % s['test']


@post('/send_reg')
def register():
    payload = request.body.read()
    print(payload)
    name = request.forms['name']
    surname = request.forms['surname']
    email = request.forms['email']
    password = request.forms['password']
    ldap.add_user(name=name, surname=surname, email=email, password=password)
    return "Registration complete!"


bottle.run(app=app, host='0.0.0.0', port=8095)