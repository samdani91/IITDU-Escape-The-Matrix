from flask import Flask, request, redirect, url_for, render_template_string, make_response
import secrets

app = Flask(__name__)
USERNAME = "student"
PASSWORD = "student123"
FLAG = f"IITCTF{{{secrets.token_hex(16)}}}"

HOME = r"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>University Portal | IITCTF</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;color:#18212b;background:#f5f7fa}
.top{background:#082b1f;color:white;font-size:13px}.topin,.headin,.navin,.heroin,.main,.footin{max-width:1180px;margin:auto}
.topin{padding:8px 20px;display:flex;justify-content:space-between}.header{background:#fff;border-bottom:1px solid #dfe5e9}
.headin{padding:18px 20px;display:flex;align-items:center;gap:18px}.crest{width:62px;height:62px;border-radius:50%;background:#0b5d3b;color:#f5d77a;display:grid;place-items:center;font-size:25px;font-weight:800;border:4px solid #e9d28a}
.uni{font-family:Georgia,serif}.uni h1{font-size:25px;margin:0;color:#073d29}.uni p{margin:5px 0;color:#66717c;font-size:13px}
.nav{background:#073d29}.navin{display:flex;padding:0 20px}.nav a{color:white;text-decoration:none;padding:14px 18px;font-size:14px}.nav a:hover{background:#0b5d3b}
.hero{background:linear-gradient(120deg,#073d29,#0b6844);color:white}.heroin{padding:58px 20px}.eyebrow{text-transform:uppercase;letter-spacing:2px;font-size:12px;color:#f1d475;font-weight:700}.hero h2{font:42px Georgia,serif;max-width:720px;margin:12px 0}.hero p{max-width:650px;line-height:1.7;color:#d9ebe2}
.main{padding:30px 20px;display:grid;grid-template-columns:2fr 1fr;gap:22px}.card{background:white;border:1px solid #e0e5e9;box-shadow:0 8px 25px #1020300d}.card h3{margin:0;padding:18px 20px;border-bottom:1px solid #e8ecef;color:#073d29;font-family:Georgia,serif}.body{padding:22px}.notice{border-left:4px solid #d3ad3f;background:#fffaf0;padding:14px 16px;color:#59636d;line-height:1.6}
.footer{margin-top:50px;background:#082b1f;color:#cbd9d2}.footin{padding:28px 20px;font-size:13px;line-height:1.7}
@media(max-width:800px){.main{grid-template-columns:1fr}.hero h2{font-size:32px}.navin{overflow:auto}}
</style></head>
<body>
<div class="top"><div class="topin"><span>University Information Portal</span><span>Student Services | Library | Contact</span></div></div>
<header class="header"><div class="headin"><div class="crest">U</div>
<div class="uni"><h1>University of Dhaka</h1><p>Excellence in Education, Research and Innovation</p></div></div></header>
<nav class="nav"><div class="navin"><a href="/">Home</a><a href="/login">Student Login</a><a href="#">Academic</a><a href="#">Research</a><a href="#">Library</a></div></nav>
<section class="hero"><div class="heroin"><div class="eyebrow">Student Information System</div>
<h2>Welcome to the University Portal</h2><p>Access academic services, student resources and university information through this secure training portal.</p></div></section>
<section class="main"><div class="card"><h3>Student Services</h3><div class="body"><div class="notice"><strong>Important:</strong> Students can use the portal to access academic and administrative services. Please keep your credentials secure.</div><p>Use the Student Login service to access your account.</p></div></div>
<div class="card"><h3>Announcements</h3><div class="body"><p>Semester registration information is available through the academic office.</p><p>Library services remain available throughout the academic session.</p></div></div></section>
<footer class="footer"><div class="footin"><strong>University Information Portal</strong><br>CTF training environment • IITCTF<br>This is a fictional training interface and is not an official university website.</div></footer>
</body></html>"""

LOGIN = r"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Student Login | IITCTF</title><style>
body{margin:0;background:#f5f7fa;font-family:Arial;color:#18212b}.box{max-width:460px;margin:90px auto;padding:32px;background:white;border:1px solid #dfe5e9;box-shadow:0 12px 35px #0001}.brand{color:#073d29;font:700 24px Georgia;margin-bottom:25px}label{display:block;margin:15px 0 6px;font-weight:700;font-size:13px}input{width:100%;box-sizing:border-box;padding:12px;border:1px solid #ccd5dc;border-radius:4px}button{width:100%;padding:12px;margin-top:20px;background:#0b5d3b;color:white;border:0;border-radius:4px;font-weight:bold}.err{padding:10px;background:#fff0f0;border:1px solid #ecc;color:#922;margin-bottom:15px}</style></head>
<body><div class="box"><div class="brand">University Student Portal</div>{% if error %}<div class="err">{{ error }}</div>{% endif %}
<form method="post"><label>Student ID</label><input name="username" autocomplete="off"><label>Password</label><input type="password" name="password"><button>Sign in</button></form></div></body></html>"""

ADMIN = r"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Administration | IITCTF</title><style>
body{margin:0;background:#f5f7fa;font-family:Arial;color:#18212b}.bar{background:#073d29;color:white;padding:18px 5%;font-weight:700}.wrap{max-width:1050px;margin:35px auto;padding:0 20px}.card{background:white;border:1px solid #dde4e8;padding:28px;box-shadow:0 8px 25px #0000000d}.ok{color:#0b5d3b}.flag{margin-top:20px;padding:18px;background:#071d15;color:#b9f7d8;font-family:monospace;word-break:break-all}</style></head>
<body><div class="bar">University Administration Portal</div><div class="wrap"><div class="card"><h1>Administration</h1><p class="ok">Administrative area.</p><p>Challenge objective completed.</p><div class="flag">{{ flag }}</div></div></div></body></html>"""

@app.get("/")
def index():
    return render_template_string(HOME)

@app.get("/robots.txt")
def robots():
    r = make_response("User-agent: *\nDisallow: /admin\n")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == USERNAME and request.form.get("password") == PASSWORD:
            return redirect(url_for("admin"))
        return render_template_string(LOGIN, error="Invalid student ID or password.")
    return render_template_string(LOGIN, error=None)

@app.get("/admin")
def admin():
    # INTENTIONALLY VULNERABLE: no authentication check.
    return render_template_string(ADMIN, flag=FLAG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
