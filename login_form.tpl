<html>
<head>
    <title>LDAP Benutzer Panel</title>
</head>
<body>
<h1>Login</h1>

<form action="/login" method="post">
    <h4>Benutzername oder Email:</h4>
    <input type="text" name="username" required/>
    <h4>Passwort:</h4>
    <input type="password" name="password" required>
    <br><br>
    <input type="submit" value="Login">
</form>
<form action="/">
    <button type="submit">Zurück</button>
</form>
</body>

</html>
