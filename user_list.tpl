<html>
<head>
    <title>LDAP Benutzer Panel</title>
    <style>
    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }

    td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even) {
        background-color: #dddddd;
    }
    </style>
</head>
<body>
<h1>Benutzer Liste</h1>

<table>
    <tr>
        <th>Name</th>
        <th>E-Mail</th>
        <th>Benutzername</th>
        <th>Gruppen</th>
    </tr>
  % for user in users:
    <tr onclick="window.location='/user_info/{{user['dn']}}';">
        <td>{{user['attributes']['givenName'][0]}} {{user['attributes']['sn'][0]}}</td>
        <td>{{user['attributes']['mail'][0]}}</td>
        <td>{{user['attributes']['uid'][0]}}</td>
        <!--<td>{{groups[user['attributes']['gidNumber']]}}</td>-->
    </tr>
  % end
</table>

<form action="/">
    <button type="submit">Zurück</button>
</form>

</body>

</html>