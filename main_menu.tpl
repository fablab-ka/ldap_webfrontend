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

<h1>Aktionen</h1>

% if user == "":
<form action="/login">
    <button type="submit">Einlogen</button>
</form>

<form action="/register">
    <button type="submit">Registrieren</button>
</form>

<form action="/pw_reset">
    <button type="submit">Passwort vergessen</button>
</form>

% else:
<form action="/logout">
    <button type="submit">Auslogen</button>
</form>

<form action="/user_info/{{user}}">
    <button type="submit">Meine Daten</button>
</form>

<form action="/delete">
    <button type="submit">Account löschen</button>
</form>
% end

</body>

</html>