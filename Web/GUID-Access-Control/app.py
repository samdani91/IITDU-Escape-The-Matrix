from flask import Flask, request, redirect, render_template_string, abort
import secrets
import uuid

app = Flask(__name__)

# Demo credentials
USERS = {
    "wiener": {
        "password": "peter",
        "id": str(uuid.uuid4()),
        "api_key": secrets.token_hex(16),
    },
    "carlos": {
        "password": "montoya",
        "id": str(uuid.uuid4()),
        "api_key": secrets.token_hex(16),
    },
}

# The challenge flag is Carlos's API key.
FLAG = lambda: f"IITCTF{{{USERS['carlos']['api_key']}}}"

BLOG = """
<!doctype html>
<title>IITCTF Blog</title>
<h1>IITCTF Blog</h1>
<p>Training application.</p>
<ul>
  <li><a href="/post/1">Welcome post</a> — by <a href="/user/{{ carlos_id }}">carlos</a></li>
  <li><a href="/login">Login</a></li>
</ul>
"""

POST = """
<!doctype html>
<title>Blog post</title>
<h1>Welcome to the blog</h1>
<p>This is a public training post.</p>
<p>Author: <a href="/user/{{ carlos_id }}">carlos</a></p>
"""

LOGIN = """
<!doctype html>
<title>Login</title>
<h1>Login</h1>
<form method="post">
  <input name="username" placeholder="username">
  <input name="password" type="password" placeholder="password">
  <button>Login</button>
</form>
<p>Demo account: <code>wiener:peter</code></p>
"""

ACCOUNT = """
<!doctype html>
<title>My Account</title>
<h1>My Account</h1>
<p>Account ID: <code>{{ user_id }}</code></p>
<p>Username: <strong>{{ username }}</strong></p>
<p>API key: <code>{{ api_key }}</code></p>
"""

@app.get("/")
def index():
    return render_template_string(BLOG, carlos_id=USERS["carlos"]["id"])

@app.get("/post/1")
def post():
    return render_template_string(POST, carlos_id=USERS["carlos"]["id"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = USERS.get(username)
        if user and user["password"] == password:
            response = redirect(f"/my-account?id={user['id']}")
            response.set_cookie("session_user", username)
            return response
        return "Invalid credentials", 401
    return render_template_string(LOGIN)

# INTENTIONAL VULNERABILITY:
# The application trusts the user-controlled id parameter and does not
# verify that it belongs to the authenticated session.
@app.get("/my-account")
def my_account():
    requested_id = request.args.get("id", "")

    for username, user in USERS.items():
        if user["id"] == requested_id:
            return render_template_string(
                ACCOUNT,
                username=username,
                user_id=user["id"],
                api_key=user["api_key"],
            )

    abort(404)

@app.get("/user/<user_id>")
def user_profile(user_id):
    for username, user in USERS.items():
        if user["id"] == user_id:
            return f"""
            <h1>{username}</h1>
            <p>Author profile</p>
            <a href="/my-account?id={user_id}">View account</a>
            """
    abort(404)

@app.get("/flag")
def flag():
    # Convenience endpoint for the local challenge organizer.
    # Players should obtain the value by exploiting /my-account.
    return FLAG()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
