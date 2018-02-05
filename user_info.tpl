<html>
<head>
    <title>LDAP User Info</title>
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
<h1>User Info</h1>

<table>
    <tr>
        <th>Key</th>
        <th>Value</th>
    </tr>
    <tr>
        <td>Surname</td>
        <td>{{user['attributes']['givenName'][0]}}</td>
    </tr>
    <tr>
        <td>Last Name</td>
        <td>{{user['attributes']['sn'][0]}}</td>
    </tr>
    <tr>
        <td>E-Mail</td>
        <td>{{user['attributes']['mail'][0]}}</td>
    </tr>
    <tr>
        <td>Home Directory</td>
        <td>{{user['attributes']['homedirectory']}}</td>
    </tr>
    <tr>
        <td>DN</td>
        <td>{{user['dn']}}</td>
    </tr>
    <tr>
        <td>UID Number</td>
        <td>{{user['attributes']['uidNumber']}}</td>
    </tr>
    <tr>
        <td>UID</td>
        <td>{{user['attributes']['uid'][0]}}</td>
    </tr>    <tr>
        <td>Group</td>
        <td>{{groups[user['attributes']['gidNumber']]}}</td>
    </tr>
</table>

<form action="/">
    <button type="submit">Back</button>
</form>

</body>

</html>