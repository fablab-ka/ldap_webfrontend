# coding: utf8
from ldap_class import LdapClass
import ldap3
import bottle
from bottle import template, route, request, redirect, get, post, hook
from gevent import monkey; monkey.patch_all()
from beaker.middleware import SessionMiddleware
import configparser
import os
import smtplib
from email.mime.text import MIMEText
import uuid
import datetime

# Check if there is already a configurtion file
if not os.path.isfile("config/config.ini"):
    Config = configparser.RawConfigParser()
    with open("config.ini.example", 'r') as cfgfile:
        Config.read(cfgfile)
    with open("config/config.ini", 'w') as cfgfile:
        Config.write(cfgfile)

# Load the configuration file
config = configparser.RawConfigParser()
config.read("config.ini.example")
config.read("config/config.ini")

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


def LdapAdmin():
    return LdapClass(connection=config['ldap']['server'],
                 bind_dn=config['ldap']['bind'],
                 password=config['ldap']['password'],
                 base_dn=config['ldap']['ldap_base'],
                 ou_users=config['ldap']['ou_users'],
                 ou_groups=config['ldap']['ou_groups'],)


def LdapUser(dn, password):
    return LdapClass(connection=config['ldap']['server'],
                 bind_dn=dn,
                 password=password,
                 base_dn=config['ldap']['ldap_base'],
                 ou_users=config['ldap']['ou_users'],
                 ou_groups=config['ldap']['ou_groups'],)


def getUsers(identifier):
    return LdapAdmin().search("(&(objectClass=inetOrgPerson)(|(mail={0})(uid={0})))".format(identifier))


def getGroups(dn):
    groups = LdapAdmin().search("(&(objectClass=groupOfNames)(member={}))".format(dn))
    user_groups = []
    for group in groups:
        user_groups.append(group['attributes']['cn'][0])
    return user_groups


def warning(text):
    if not text:
        text = ""
    return template("warning.tpl", text=text)


@get('/login')
def login():
    return template("login_form.tpl")


@post('/login')
def do_login():
    form = request.forms.getunicode
    username = form('username')
    password = form('password')
    ldap_admin = LdapAdmin()
    users = getUsers(username)
    if len(users) != 1:
        return warning("Benutzer nicht gefunden!")

    user_dn = users[0]['dn']
    try:
        LdapUser(user_dn, password)
    except ldap3.core.exceptions.LDAPBindError:
        return warning("Kein gültiges Passwort!")

    request.session['dn'] = user_dn
    request.session['id'] = username
    return redirect('/')


@route('/logout')
def logout():
    if 'dn' in request.session:
        del request.session['dn']
    if 'id' in request.session:
        del request.session['id']

    return redirect('/')


@route('/user_list')
def show_users():
    if "Vorstand" not in getGroups(request.session['dn']):
        return warning("Zugriff nicht erlaubt!")
    users = LdapAdmin().search()
    return template('user_list.tpl', users=users)



@route('/user_info/<id>')
def user_info(id):
    if "Vorstand" in getGroups(request.session['dn']) or id == request.session['id']:
        users = getUsers(id)
        if len(users) != 1:
            return warning("Kein Benutzer mit id {} gefunden!".format(id))
        return template('user_info.tpl', user=users[0])
    return warning("Zugriff nicht erlaubt!")


@route('/')
def main_menu():
    user = ""
    if 'id' in request.session:
        user = request.session['id']
    return template('main_menu.tpl', user=user)


@route('/register')
def register():
    return template('reg_form.tpl')

pw_tokens = []

@get('/pw_reset')
def show_pw_reset():
    return template("pw_request_form.tpl")

@post('/pw_reset')
def pw_reset():
    form = request.forms.getunicode
    username = form('username')
    users = getUsers(username)
    if len(users) != 1:
        return warning("Konnte Benutzer nicht in der Datenbank finden!")
    email = users[0]['attributes']['mail'][0]

    #ToDo: Anti-Spam-proof the Email sending

    #set token
    token = uuid.uuid4().hex
    pw_tokens.append({
        'email': email,
        'token': token,
        'time': datetime.datetime.now(),
    })

    reset_link = config['mail']['pw_link'].format(token)
    msg = MIMEText("Jemand hat die Rücksetzung Ihres Fablab-Karsruhe-Passworts angefordert. "
                   "Um Ihr Passwort zurückzusetzen, klicken Sie bitte auf folgenden Link: {}"
                   " Dieser Link ist zwei Stunden lang gültig.".format(reset_link))
    msg['subject'] = "Zurücksetzen Ihres Passworts"
    msg['from'] = config['mail']['smtp_mail']
    msg['to'] = email
    server = smtplib.SMTP(config['mail']['smtp_server'])
    server.starttls()
    server.login(config['mail']['smtp_mail'], config['mail']['smtp_pw'])
    server.send_message(msg)
    server.quit()
    return warning("Email gesendet! Bitte klicken Sie den Link in der Email an!")

@get('/pw_reset/<token>')
def reset_pw(token):
    deadline = datetime.datetime.now() - datetime.timedelta(hours=2)
    for entry in pw_tokens:
        if entry['time'] < deadline:
            pw_tokens.remove(entry)
        else:
            if entry['token'] == token:
                return'''
                    <form action="/new_pw/''' + entry['token'] + '''" method="post">
                        Neues Passwort: <input name="password" type="password" 
                        pattern=".{6,20}" title="Please use between 6 and 20 characters." required/>
                        <input value="Neues Passwort setzen" type="submit" />
                    </form>
                    '''
    return warning("Dieses Token wurde nicht gefunden!")


@post('/new_pw/<token>')
def new_pw(token):
    form = request.forms.getunicode
    password = form('password')
    deadline = datetime.datetime.now() - datetime.timedelta(hours=2)
    for entry in pw_tokens:
        if entry['time'] < deadline:
            pw_tokens.remove(entry)
        else:
            if entry['token'] == token:
                users = getUsers(entry['email'])
                if len(users) != 1:
                    return warning("Benutzer wurde nicht gefunden!")
                LdapAdmin().con.extend.standard.modify_password(user=users[0]['dn'], new_password=password)
                pw_tokens.remove(entry)
                return warning("Passwort wurde erfolgreich geändert!")
    return warning("Token wurde nicht gefunden!")

@post('/send_reg')
def do_register():
    form = request.forms.getunicode
    name = form('name')
    surname = form('surname')
    email = form('email')
    password = form('password')
    uid = form('uid')
    name = str(name).strip(' ')
    surname = str(surname).strip(' ')

    #check if user already exists
    if len(getUsers(email)) > 0:
        return warning("Diese Email-Adresse wird schon benutzt!")
    if len(getUsers(uid)) > 0:
        return warning("Dieser Benutzername wird schon benutzt!")

    ldap = LdapAdmin()
    user_dn = ("cn=" + uid + "," + ldap.ou_users + "," + ldap.ldap_base)
    user = {
        "objectClass": ["inetOrgPerson"],
        "sn": [name],
        "givenName": [surname],
        "displayName": [(surname + " " + name)],
        "mail": [email],  # IA5
        "uid": [uid],
    }

    if not ldap.con.add(user_dn, attributes=user):
        return warning("Der Benutzer konnte nicht angelegt werden!")
    ldap.con.extend.standard.modify_password(user=user_dn, new_password=password)

    #Try to login to check if everything worked
    try:
        LdapUser(user_dn, password)
    except ldap3.core.exceptions.LDAPBindError:
        return warning("Es gab ein Encoding-Problem mit dem Passwort!")

    request.session['dn'] = user_dn
    request.session['id'] = uid
    return redirect('/')


bottle.run(app=app, host='0.0.0.0', port=9002)
