<html>
<head>
    <title>LDAP Registration</title>
</head>
<body>
<h1>Registration</h1>

<form action="/send_reg" method="post">
    <h4>First Name:</h4>
    <input type="text" name="surname" required>
    <h4>Last Name:</h4>
    <input type="text" name="name" required>
    <h4>Email:</h4>
    <input type="email" name="email" required>
    <h4>Password:</h4>
    <input type="password" name="password" required>
    <h4>User name:</h4>
    <input type="text" name="uid" pattern="[A-Za-z][a-zA-Z_0-9]{3,19}"
           title="Please enter a Username with at elast 6 characters and no
           special symbols, pattern: [A-Za-z][a-zA-Z_0-9]{3,19}" required>
    <!--<h4>Alias:</h4>-->
    <!--<input type="text" name="alias">-->
    <br>
    <br>
    <input type="submit" value="Submit">
</form>
</body>

</html>