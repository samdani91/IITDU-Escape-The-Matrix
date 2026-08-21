from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>IITCTF • StockCheck</title>
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;color:#e7eef7;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;background:radial-gradient(circle at 15% 10%,#4878ff2e,transparent 30%),radial-gradient(circle at 85% 80%,#00d6aa1f,transparent 30%),#07111f}
.nav{height:70px;display:flex;align-items:center;justify-content:space-between;padding:0 6vw;border-bottom:1px solid #ffffff14;background:#07111fc7;backdrop-filter:blur(14px)}
.brand{font-weight:800;letter-spacing:.4px}.brand span{color:#6ea8ff}.badge{font-size:12px;padding:7px 11px;border:1px solid #6ea8ff4d;border-radius:999px;color:#a9c8ff;background:#6ea8ff14}
main{width:min(1050px,92vw);margin:70px auto}.hero{display:grid;grid-template-columns:1.2fr .8fr;gap:28px}
.card{border:1px solid #ffffff17;border-radius:22px;background:#0d1b2dd1;box-shadow:0 20px 70px #00000047}.content{padding:38px}.eyebrow{color:#69a1ff;font-size:12px;font-weight:800;letter-spacing:1.7px;text-transform:uppercase}
h1{font-size:clamp(38px,5vw,64px);line-height:1.02;margin:14px 0 18px}.sub{color:#9db0c5;line-height:1.7;max-width:650px}
.panel{padding:28px}label{display:block;font-size:13px;color:#aabbd0;margin-bottom:9px}.inputrow{display:flex;gap:10px}
input{flex:1;min-width:0;padding:14px 15px;border-radius:12px;border:1px solid #263c56;background:#081522;color:#f4f8fc;outline:none}
input:focus{border-color:#5f9bff;box-shadow:0 0 0 3px #5f9bff1f}
button{border:0;border-radius:12px;padding:0 20px;font-weight:800;cursor:pointer;color:#06101b;background:linear-gradient(135deg,#78adff,#6be7c5)}
button:hover{filter:brightness(1.08);transform:translateY(-1px)}
.hint{margin-top:14px;font-size:12px;color:#71859b}.result{margin-top:20px;padding:18px;border-radius:14px;background:#06101b;border:1px solid #ffffff12;overflow:auto}
pre{margin:0;white-space:pre-wrap;word-break:break-word;color:#b9f7d8;font-family:"SFMono-Regular",Consolas,monospace}.status{display:flex;gap:10px;align-items:center;margin-bottom:20px;color:#aabbd0;font-size:13px}
.dot{width:9px;height:9px;border-radius:50%;background:#42e6a4;box-shadow:0 0 14px #42e6a4}.info{padding:28px}.info h3{margin-top:0}
.feature{display:flex;gap:12px;margin:19px 0;color:#9db0c5;line-height:1.55}.icon{width:34px;height:34px;display:grid;place-items:center;flex:none;border-radius:10px;background:#6ea8ff1a;color:#78adff}
footer{text-align:center;color:#647991;font-size:12px;margin-top:55px}@media(max-width:800px){.hero{grid-template-columns:1fr}.content{padding:28px}}
</style></head>
<body>
<nav class="nav"><div class="brand">IIT<span>CTF</span> • StockCheck</div><div class="badge">SECURITY TRAINING</div></nav>
<main><section class="hero">
<div class="card content"><div class="eyebrow">Product Operations</div><h1>Check product stock.</h1>
<p class="sub">Enter a product identifier to retrieve its current stock status. This environment is part of an IITCTF security exercise.</p>
<div class="panel" style="padding:0;margin-top:30px"><form action="/stock" method="get">
<label for="productId">Product ID</label><div class="inputrow"><input id="productId" name="productId" value="{{ value }}" placeholder="e.g. 1001" autocomplete="off"><button>Check stock</button></div>
<div class="hint">Challenge endpoint: <code>/stock</code></div></form>
{% if output is not none %}<div class="result"><div class="status"><span class="dot"></span>Command response received</div><pre>{{ output }}</pre></div>{% endif %}
</div></div>
<aside class="card info"><h3>Challenge Console</h3><p class="sub">A controlled environment for practicing OS command injection.</p>
<div class="feature"><div class="icon">01</div><div><strong>Inspect</strong><br>Understand the product lookup behavior.</div></div>
<div class="feature"><div class="icon">02</div><div><strong>Test</strong><br>Investigate whether input reaches a system command.</div></div>
<div class="feature"><div class="icon">03</div><div><strong>Explore</strong><br>Use the discovered execution primitive to complete the challenge.</div></div>
</aside></section><footer>IITCTF • Authorized CTF environment only</footer></main>
</body></html>"""

@app.get("/")
def index():
    return render_template_string(PAGE, value="", output=None)

@app.get("/stock")
def stock():
    value = request.args.get("productId", "")
    # INTENTIONALLY VULNERABLE — CTF challenge only.
    command = f"echo Stock available for product {value}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Command timed out."
    return render_template_string(PAGE, value=value, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
