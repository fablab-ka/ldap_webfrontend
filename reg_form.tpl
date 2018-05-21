<html>
<head>
    <title>LDAP Benutzer Panel</title>
</head>
<body>
<h1>Registration</h1>

<form action="/send_reg" method="post">
    <h4>Vorname:</h4>
    <input type="text" name="surname" required>
    <h4>Nachname:</h4>
    <input type="text" name="name" required>
    <h4>Email:</h4>
    <input type="email" name="email" required>
    <h4>Password:</h4>
    <input type="password" name="password" pattern=".{6,20}" title="Please use between 6 and 20 characters." required>
    <h4>Benutzername:</h4>
    <input type="text" name="uid" pattern="[A-Za-z][a-zA-Z_0-9]{3,19}"
           title="Please enter a Username with at elast 6 characters and no
           special symbols, pattern: [A-Za-z][a-zA-Z_0-9]{3,19}" required>
    <h4>Datenschutzbestimmung:</h4>
    <input type="checkbox" name="dsgvo" title="Sie müssen zur Nutzung dieses Dienstes der Datenschutzbestimmung zustimmen" required>
    Ich akzeptiere die <a href="https://fablab-karlsruhe.de/datenschutzerklaerung/">Datenschutzbestimmung</a>.
    <br><br>
    <input type="submit" value="Registrieren">
</form>
<form action="/">
    <button type="submit">Zurück</button>
</form>
</body>

</html>
