from flask import Flask, request, render_template_string
import sqlite3
import secrets

app = Flask(__name__)
DB = "/tmp/iitctf.db"
FLAG = f"IITCTF{{{secrets.token_hex(16)}}}"

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UniStore • IITCTF</title>
<style>
:root{--bg:#07111f;--panel:#0d1b2e;--panel2:#111f34;--text:#eef5ff;--muted:#91a4bc;--accent:#6ee7b7;--accent2:#60a5fa;--border:#20334d}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 15% 10%,#123052 0,transparent 32%),radial-gradient(circle at 90% 15%,#143d39 0,transparent 30%),var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;min-height:100vh}
header{height:72px;border-bottom:1px solid #ffffff12;background:#07111fcc;backdrop-filter:blur(16px);display:flex;align-items:center;justify-content:space-between;padding:0 6%;position:sticky;top:0;z-index:5}
.brand{display:flex;align-items:center;gap:12px;font-weight:800}.mark{width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,var(--accent2),var(--accent));display:grid;place-items:center;color:#06101d;font-weight:900}
nav{display:flex;gap:24px}nav a{color:var(--muted);text-decoration:none;font-size:14px}nav a:hover{color:white}
.hero{max-width:1180px;margin:auto;padding:78px 24px 45px}.pill{display:inline-flex;align-items:center;gap:8px;border:1px solid #6ee7b733;background:#6ee7b710;color:var(--accent);padding:7px 11px;border-radius:999px;font-size:12px;font-weight:700}
.dot{width:7px;height:7px;border-radius:50%;background:var(--accent);box-shadow:0 0 14px var(--accent)}
h1{font-size:clamp(38px,6vw,68px);line-height:1.02;letter-spacing:-3px;margin:20px 0 16px;max-width:800px}
.hero p{max-width:700px;color:var(--muted);font-size:17px;line-height:1.75}
.layout{max-width:1180px;margin:auto;padding:0 24px 70px;display:grid;grid-template-columns:1.45fr .75fr;gap:20px}.card{background:linear-gradient(180deg,#102139,#0b1728);border:1px solid var(--border);border-radius:20px;box-shadow:0 25px 70px #0006;overflow:hidden}.cardhead{padding:22px 24px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}.cardhead h2{font-size:17px;margin:0}.badge{font-size:11px;color:#b8c8db;border:1px solid var(--border);padding:5px 8px;border-radius:7px}.body{padding:25px}
label{display:block;color:#cbd7e6;font-size:13px;font-weight:700;margin-bottom:9px}.inputrow{display:flex;gap:10px}input{flex:1;min-width:0;background:#07111f;color:white;border:1px solid #29405d;border-radius:11px;padding:15px 16px;font-size:15px;outline:none}input:focus{border-color:var(--accent2);box-shadow:0 0 0 4px #60a5fa14}
button{border:0;border-radius:11px;padding:0 22px;background:linear-gradient(135deg,var(--accent2),#818cf8);color:white;font-weight:800;cursor:pointer}button:hover{filter:brightness(1.08)}
.result{margin-top:18px;background:#07111f;border:1px solid var(--border);border-radius:12px;padding:16px;color:#bfe8d8;font-family:"SFMono-Regular",Consolas,monospace;font-size:13px;line-height:1.65;white-space:pre-wrap;overflow:auto}
.sideitem{padding:16px 0;border-bottom:1px solid var(--border)}.sideitem:last-child{border-bottom:0}.sideitem strong{display:block;font-size:13px;margin-bottom:6px}.sideitem span{color:var(--muted);font-size:13px;line-height:1.5}
footer{max-width:1180px;margin:auto;padding:25px 24px 45px;color:#60738b;font-size:12px}
@media(max-width:850px){nav{display:none}.layout{grid-template-columns:1fr}.inputrow{flex-direction:column}button{height:48px}.hero{padding-top:55px}}
</style></head>
<body>
<header><div class="brand"><div class="mark">U</div><span>UniStore</span></div>
<nav><a href="/">Overview</a><a href="#">Inventory</a><a href="#">Resources</a><a href="#">Support</a></nav><span class="badge">IITCTF LAB</span></header>
<section class="hero"><div class="pill"><span class="dot"></span> INVENTORY API ONLINE</div>
<h1>University Store<br><span style="color:#8ba5c4">Availability Console</span></h1>
<p>Check product availability through the university's internal inventory service. Enter a product identifier to query the catalog.</p></section>
<section class="layout">
<div class="card"><div class="cardhead"><h2>Product lookup</h2><span class="badge">GET /products</span></div><div class="body">
<form method="get" action="/products"><label for="productId">PRODUCT ID</label><div class="inputrow">
<input id="productId" name="productId" value="{{ value }}" placeholder="Enter product ID">
<button type="submit">Query catalog →</button></div></form>
{% if result is not none %}<div class="result">{{ result }}</div>{% endif %}
</div></div>
<aside class="card"><div class="cardhead"><h2>System status</h2><span class="badge">LIVE</span></div><div class="body">
<div class="sideitem"><strong>Catalog service</strong><span>Operational • SQLite inventory backend</span></div>
<div class="sideitem"><strong>Access level</strong><span>Student inventory view</span></div>
<div class="sideitem"><strong>Visible records</strong><span>Standard university products</span></div>
<div class="sideitem"><strong>Environment</strong><span>Authorized IITCTF training lab</span></div>
</div></aside>
</section>
<footer>© IITCTF • Fictional university inventory interface • Authorized security training environment</footer>
</body></html>"""

def init_db():
    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("CREATE TABLE products (id INTEGER, name TEXT, description TEXT, category TEXT, visible INTEGER)")
    cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)",[
        (1,"University Hoodie","Official student hoodie","Merchandise",1),
        (2,"Campus Notebook","Academic notebook","Stationery",1),
        (3,"Library Card Holder","Student card holder","Accessories",1),
        (4,"IITCTF Admin Mug","Restricted inventory item","Internal",0),
        (5,"Research Archive Key","Restricted internal resource","Internal",0)])
    con.commit(); con.close()

@app.get("/")
def home():
    return render_template_string(PAGE,value="",result=None)

@app.get("/products")
def products():
    value=request.args.get("productId","")
    con=sqlite3.connect(DB); cur=con.cursor()
    # INTENTIONALLY VULNERABLE — isolated CTF challenge.
    query=f"SELECT id,name,description,category FROM products WHERE id={value} AND visible=1"
    try:
        rows=cur.execute(query).fetchall()
        if any(row[0]==4 for row in rows):
            result=f"Product found: {rows}\n\nFlag: {FLAG}"
        elif rows:
            result=f"Product found: {rows}"
        else:
            result="No visible product found."
    except sqlite3.Error as e:
        result=f"Database error: {e}"
    finally:
        con.close()
    return render_template_string(PAGE,value=value,result=result)

if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0",port=8080)
