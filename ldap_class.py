# coding: utf8
# import ldap
# from ldap import modlist
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES
from ldap3 import set_config_parameter
# import sha
import unicodedata
from base64 import b64encode
from ldap3.utils.conv import to_unicode

class LdapClass:
    con = None
    ldap_base = ""
    ou_users = "ou=users"
    ou_groups = "ou=groups"
    gid_number= "500" # ToDo de-hardcode

    def __init__(self, connection, bind_dn, password, base_dn, ou_users, ou_groups, gidNumber):
        #set_config_parameter('DEFAULT_CLIENT_ENCODING', 'utf-8')
        self.ldap_base = str(base_dn)
        self.ou_groups = str(ou_groups)
        self.ou_users = str(ou_users)
        self.gid_number = str(gidNumber)
        self.con = Connection(server=str(connection),user=str(bind_dn)
                              ,password=str(password),auto_bind=True)


    def search_users(self, search_filter):
        self.con.search(self.ldap_base, search_filter, attributes=ALL_ATTRIBUTES)
        return self.con.entries

    def add_user(self, name, surname, email, password, uid):
        name = str(name).strip(' ')
        surname = str(surname).strip(' ')

        dn = ("cn=" + email + "," + self.ou_users + "," + self.ldap_base)
        user = {
            "objectClass": ["inetOrgPerson", "posixAccount"],
            "uid": [(uid)],
            "sn": [(name)],
            "givenName": [(surname)],
            "displayName": [((surname + " " + name))],
            "uidNumber": [(self.get_next_uid())],
            "gidNumber": [(self.gid_number)],
            "loginShell": ["/bin/bash"], #IA5
            "homeDirectory": [(("/home/" + uid))], #IA5
            "mail": [(email)], #IA5
        }
        if self.con.add(dn,attributes=user):
            if self.con.extend.standard.modify_password(user=dn,new_password=password):
                return True
        return False


    def get_next_uid(self):
        uid = 1000
        for user in self.search_users("(objectClass=posixAccount)"):
            user_uid = int(str(user['uidNumber'])) #fuck you, ldap3
            if user_uid > uid:
                uid = user_uid
        return uid + 1
