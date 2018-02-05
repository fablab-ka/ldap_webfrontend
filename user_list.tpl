<html>
<head>
    <title>LDAP User List</title>
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
<h1>User List</h1>

<table>
    <tr>
        <th>Name</th>
        <th>E-Mail</th>
        <th>User Name</th>
        <th>Group</th>
    </tr>
  % for user in users:
    <tr onclick="window.location='/user_info/{{user['dn']}}';">
        <td>{{user['attributes']['cn'][0]}}</td>
        <td>{{user['attributes']['mail'][0]}}</td>
        <td>{{user['attributes']['uid'][0]}}</td>
        <td>{{groups[user['attributes']['gidNumber']]}}</td>
    </tr>
  % end
</table>

</body>

</html>