from flask import Flask, request, redirect, render_template_string, abort

app = Flask(__name__)

USERS = ["carlos", "wiener", "peter"]
FLAG = "IITCTF{unprotected_admin_functionality}"

HOME = """
<!doctype html>
<title>IITCTF Access Control Lab</title>
<h1>IITCTF Access Control Lab</h1>
<p>Welcome to the training application.</p>
<ul>
  <li><a href="/robots.txt">robots.txt</a></li>
  <li><a href="/login">Login</a></li>
</ul>
"""

LOGIN = """
<!doctype html>
<title>Login</title>
<h2>Login</h2>
<p>This challenge does not require authentication to demonstrate the bug.</p>
<form method="post">
  <input name="username" placeholder="username">
  <button>Login</button>
</form>
"""

ADMIN = """
<!doctype html>
<title>Administrator panel</title>
<h1>Administrator panel</h1>
<p>Training target: administrative functionality is accidentally exposed.</p>
<p><strong>Users:</strong></p>
<ul>
{% for u in users %}
  <li>{{u}} -
    <a href="/administrator-panel/delete?username={{u}}">Delete</a>
  </li>
{% endfor %}
</ul>
"""

@app.get("/")
def home():
    return render_template_string(HOME)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    return render_template_string(LOGIN)

@app.get("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /administrator-panel\n"

# INTENTIONAL VULNERABILITY:
# No authentication/authorization check protects the administrator panel.
@app.get("/administrator-panel")
def administrator_panel():
    return render_template_string(ADMIN, users=USERS)

# INTENTIONAL VULNERABILITY:
# Administrative action is also directly reachable without authorization.
@app.get("/administrator-panel/delete")
def delete_user():
    username = request.args.get("username", "")
    if username in USERS:
        USERS.remove(username)
        return f"Deleted {username}. Flag: {FLAG}\n"
    abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
