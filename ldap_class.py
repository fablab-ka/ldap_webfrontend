from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES


class LdapClass:
    con = None
    ldap_base = ""
    ou_users = "ou=users"
    ou_groups = "ou=groups"

    def __init__(self, connection, bind_dn, password, base_dn, ou_users, ou_groups):
        self.ldap_base = str(base_dn)
        self.ou_groups = str(ou_groups)
        self.ou_users = str(ou_users)
        self.con = Connection(server=str(connection),user=str(bind_dn)
                              ,password=str(password),auto_bind=True)

    def search(self, search_filter='(objectClass=inetOrgPerson)', base=None):
        if not base:
            base = self.ldap_base
        self.con.search(base, search_filter, attributes=ALL_ATTRIBUTES)
        return self.con.response
