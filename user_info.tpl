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
<h1>Benutzer Informationen</h1>

<table>
    <tr>
        <th>Key</th>
        <th>Value</th>
    </tr>
    <tr>
        <td>Vorname</td>
        <td>{{user['attributes']['givenName'][0]}}</td>
    </tr>
    <tr>
        <td>Nachname</td>
        <td>{{user['attributes']['sn'][0]}}</td>
    </tr>
    <tr>
        <td>E-Mail</td>
        <td>{{user['attributes']['mail'][0]}}</td>
    </tr>
    <tr>
        <td>DN</td>
        <td>{{user['dn']}}</td>
    </tr>
</table>

<form action="/">
    <button type="submit">Zurück</button>
</form>

</body>

</html>