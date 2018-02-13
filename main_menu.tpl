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

<h1>Please select your option</h1>

% if user == "":
<form action="/login">
    <button type="submit">Login</button>
</form>

<form action="/register">
    <button type="submit">Register</button>
</form>
% else:
<form action="/logout">
    <button type="submit">Logout</button>
</form>

<form action="/user_info/{{user}}">
    <button type="submit">Show my Details</button>
</form>
% end

% if gid >= 502:
<form action="/user_list">
    <button type="submit">User List</button>
</form>
% end

</body>

</html>