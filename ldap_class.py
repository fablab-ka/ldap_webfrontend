import ldap
from ldap import modlist
import sha
from base64 import b64encode

class LdapClass:
    con = None
    ldap_base = ""
    ou_users = "ou=users"
    ou_groups = "ou=groups"
    gid_number= "500" # ToDo de-hardcode

    def __init__(self, connection, bind_dn, password, base_dn, ou_users, ou_groups, gidNumber):
        self.ldap_base = base_dn
        self.ou_groups = ou_groups
        self.ou_users = ou_users
        self.gid_number = gidNumber
        self.con = ldap.initialize(connection)
        self.con.simple_bind(bind_dn, password)
        print(self.con.whoami_s())

    def search_users(self, search_filter):
        return self.con.search_s(self.ldap_base, ldap.SCOPE_SUBTREE, search_filter)

    def add_user(self, name, surname, email, password):
        name = str(name).strip(' ')
        surname = str(surname).strip(' ')
        ctx = sha.new(password)
        uid = str(surname[0] + name).lower()
        password_sha = "{SHA}" + b64encode(ctx.digest())

        dn = "cn=" + surname + " " + name + "," + self.ou_users + "," + self.ldap_base
        user = {
            "objectClass": ["inetOrgPerson", "posixAccount"],
            "uid": [uid],
            "sn": [name],
            "givenName": [surname],
            "cn": [surname + name],
            "displayName": [surname + " " + name],
            "uidNumber": [str(self.get_next_uid())],
            "gidNumber": [str(self.gid_number)],
            "loginShell": ["/bin/bash"],
            "homeDirectory": ["/home/" + uid],
            "mail": [email],
            "userPassword": [password_sha]
        }
        return self.con.add_s(dn, modlist.addModlist(user))
        # return self.con.add_s(dn, modlist)

    def get_next_uid(self):
        uid = 1000
        for user in self.search_users("(objectClass=posixAccount)"):
            user_uid = user[1]['uidNumber']
            if user_uid > uid:
                uid = user_uid
        return int(uid[0]) + 1
