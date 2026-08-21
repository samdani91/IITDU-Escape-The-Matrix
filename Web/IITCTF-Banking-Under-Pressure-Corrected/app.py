from flask import Flask, request, redirect, session, render_template_string, jsonify, flash
import threading
import time
import re

app = Flask(__name__)
app.secret_key = "iitctf-local-training-secret"

FLAG = "IITCTF{banking_under_pressure_race_bola}"

# Server-side challenge state.
# This survives page refreshes but resets when the container restarts.
challenge_completed = False

# Intentionally vulnerable CTF state.
users = {
    1: {
        "id": 1,
        "name": "Training User",
        "username": "student",
        "mobile": "01700000000",
        "nid": "TRAINING-001",
        "password": "student123",
        "balance": 10000.00,
        "role": "user",
    },
    2: {
        "id": 2,
        "name": "Campus Store",
        "username": "campus_store",
        "mobile": "01800000000",
        "nid": "MERCHANT-001",
        "password": "store123",
        "balance": 0.00,
        "role": "merchant",
    },
    3: {
        "id": 3,
        "name": "Bank Administrator",
        "username": "admin",
        "mobile": "01900000000",
        "nid": "ADMIN-001",
        "password": "admin123",
        "balance": 25000.00,
        "role": "admin",
    },
}

transactions = [
    {
        "id": 1,
        "sender_id": 2,
        "recipient_id": 1,
        "amount": 10000.00,
        "type": "DEPOSIT",
    }
]

next_tx_id = 2

# Used only to serialize the final write.
# The balance check deliberately happens before this lock.
balance_write_lock = threading.Lock()


# ---------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------

BASE_STYLE = """
<style>
:root{
    --bg:#061522;
    --panel:#0c2234;
    --panel2:#102b40;
    --line:#244760;
    --text:#f4f8fc;
    --muted:#8fa9bc;
    --accent:#62a5ff;
    --accent2:#7d7cff;
    --good:#62e1c1;
    --danger:#ff8795;
}

*{
    box-sizing:border-box;
}

html,body{
    margin:0;
    min-height:100%;
    font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    color:var(--text);
    background:
        radial-gradient(circle at 10% 10%,#123a5b 0,transparent 32%),
        radial-gradient(circle at 90% 20%,#073b35 0,transparent 26%),
        linear-gradient(135deg,#061522,#020b13);
}

body{
    min-height:100vh;
}

a{
    color:inherit;
    text-decoration:none;
}

.nav{
    height:74px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 6%;
    border-bottom:1px solid rgba(80,130,160,.25);
    background:rgba(3,15,25,.86);
    backdrop-filter:blur(16px);
    position:sticky;
    top:0;
    z-index:20;
}

.brand{
    display:flex;
    align-items:center;
    gap:12px;
    font-weight:850;
    font-size:19px;
}

.logo{
    width:38px;
    height:38px;
    border-radius:11px;
    display:grid;
    place-items:center;
    background:linear-gradient(135deg,#62e1c1,#62a5ff);
    color:#061522;
    font-weight:950;
}

.navlinks{
    display:flex;
    align-items:center;
    gap:28px;
    color:#9fb8ca;
    font-size:14px;
    font-weight:650;
}

.navlinks a:hover{
    color:white;
}

.pill{
    border:1px solid #315873;
    color:#a8c4d8;
    border-radius:999px;
    padding:7px 12px;
    font-size:10px;
    letter-spacing:.06em;
    text-transform:uppercase;
}

.wrap{
    width:min(980px,92%);
    margin:42px auto 80px;
}

.eyebrow{
    color:#62e1c1;
    font-size:11px;
    font-weight:800;
    letter-spacing:.16em;
    text-transform:uppercase;
}

.hero{
    display:flex;
    justify-content:space-between;
    gap:20px;
    align-items:end;
    margin-bottom:24px;
}

.hero h1{
    font-size:34px;
    margin:7px 0;
}

.muted{
    color:var(--muted);
}

.grid{
    display:grid;
    grid-template-columns:2fr 1fr;
    gap:14px;
}

.card{
    background:linear-gradient(180deg,rgba(16,40,59,.96),rgba(9,27,42,.96));
    border:1px solid var(--line);
    border-radius:18px;
    box-shadow:0 20px 60px #0005;
    overflow:hidden;
    margin-bottom:14px;
}

.cardhead{
    padding:18px 20px;
    border-bottom:1px solid var(--line);
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.cardbody{
    padding:20px;
}

.balance{
    font-size:36px;
    font-weight:850;
    margin:3px 0 18px;
}

.stats{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:8px;
}

.stat{
    border:1px solid var(--line);
    background:#071725;
    border-radius:12px;
    padding:12px;
}

.stat b{
    display:block;
    font-size:16px;
}

.stat span{
    font-size:10px;
    color:var(--muted);
    text-transform:uppercase;
    letter-spacing:.08em;
}

.forms{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:14px;
}

.field{
    margin-bottom:13px;
}

.field label{
    display:block;
    font-size:10px;
    font-weight:800;
    color:#a9bfd0;
    letter-spacing:.07em;
    text-transform:uppercase;
    margin-bottom:7px;
}

.field input{
    width:100%;
    background:#061522;
    border:1px solid #294d68;
    border-radius:10px;
    padding:12px;
    color:white;
    outline:none;
}

.field input:focus{
    border-color:var(--accent);
    box-shadow:0 0 0 3px #63a4ff18;
}

.btn{
    border:0;
    border-radius:10px;
    padding:12px 16px;
    font-weight:800;
    color:white;
    background:linear-gradient(135deg,#62a5ff,#7d7cff);
    cursor:pointer;
    width:100%;
}

.btn:hover{
    filter:brightness(1.08);
}

.table{
    width:100%;
    border-collapse:collapse;
    font-size:12px;
}

.table th,
.table td{
    text-align:left;
    padding:11px 8px;
    border-bottom:1px solid #19364d;
}

.table th{
    font-size:10px;
    color:#7895aa;
    text-transform:uppercase;
}

.good{
    color:var(--good);
}

.danger{
    color:var(--danger);
}

.alert{
    padding:12px 14px;
    border-radius:11px;
    background:#09251f;
    border:1px solid #1e6d58;
    color:#82eac8;
    margin-bottom:14px;
}

.error{
    background:#2b1118;
    border-color:#713040;
    color:#ff9ba7;
}

.auth{
    min-height:100vh;
    display:grid;
    place-items:center;
    padding:24px;
}

.authbox{
    width:min(460px,100%);
    background:#091a29;
    border:1px solid var(--line);
    border-radius:22px;
    padding:30px;
    box-shadow:0 30px 100px #0008;
}

.authbox h1{
    margin:4px 0 8px;
    font-size:30px;
}

.authbox .logo{
    margin-bottom:20px;
}

.footer{
    color:#638096;
    font-size:11px;
    margin-top:24px;
}

.code{
    font-family:ui-monospace,monospace;
    background:#06131f;
    padding:2px 6px;
    border-radius:5px;
}

@media(max-width:760px){
    .grid,
    .forms{
        grid-template-columns:1fr;
    }

    .hero{
        display:block;
    }

    .nav{
        padding:0 4%;
    }

    .navlinks{
        gap:10px;
    }

    .navlinks a:nth-child(2),
    .navlinks a:nth-child(3){
        display:none;
    }
}
</style>
"""


def page(title, body):
    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
{BASE_STYLE}
</head>
<body>
{body}
</body>
</html>
"""


def navigation():
    return """
<nav class="nav">
    <a href="/" class="brand">
        <span class="logo">N</span>
        <span>NovaBank</span>
    </a>

    <div class="navlinks">
        <a href="/">Dashboard</a>
        <a href="/transfer">Transfer</a>
        <a href="/transactions">Transactions</a>
    </div>

    <div>
        <span class="pill">IITCTF • LAB</span>
        &nbsp;
        <a class="muted" href="/logout">Sign out</a>
    </div>
</nav>
"""


# ---------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = next(
            (
                u for u in users.values()
                if u["username"] == username and u["password"] == password
            ),
            None,
        )

        if user:
            session["user_id"] = user["id"]
            return redirect("/")

        flash("Invalid username or password.", "error")

    body = """
<div class="auth">
    <div class="authbox">
        <div class="logo">N</div>

        <div class="eyebrow">Secure Digital Banking</div>
        <h1>Welcome back</h1>
        <p class="muted">
            Sign in to continue to your NovaBank training account.
        </p>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% for category, message in messages %}
                <div class="alert error">{{ message }}</div>
            {% endfor %}
        {% endwith %}

        <form method="post">
            <div class="field">
                <label>Username</label>
                <input
                    name="username"
                    placeholder="your username"
                    required
                >
            </div>

            <div class="field">
                <label>Password</label>
                <input
                    type="password"
                    name="password"
                    placeholder="your password"
                    required
                >
            </div>

            <button class="btn">Sign in securely</button>
        </form>

        <p class="footer">
            New to NovaBank?
            <a href="/register">Create an account</a>
        </p>
    </div>
</div>
"""

    return render_template_string(
        page("NovaBank — Login", body),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        mobile = request.form.get("mobile", "").strip()
        nid = request.form.get("nid", "").strip()
        password = request.form.get("password", "")

        if not all([name, username, mobile, nid, password]):
            flash("All fields are required.", "error")
            return redirect("/register")

        if any(u["username"] == username for u in users.values()):
            flash("Username already exists.", "error")
            return redirect("/register")

        new_id = max(users.keys()) + 1

        users[new_id] = {
            "id": new_id,
            "name": name,
            "username": username,
            "mobile": mobile,
            "nid": nid,
            "password": password,
            "balance": 0.00,
            "role": "user",
        }

        session["user_id"] = new_id
        return redirect("/")

    body = """
<div class="auth">
    <div class="authbox">
        <div class="logo">N</div>

        <div class="eyebrow">Open a training account</div>
        <h1>Start your banking journey</h1>

        <p class="muted">
            Create a fictional NovaBank account for this CTF.
        </p>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% for category, message in messages %}
                <div class="alert error">{{ message }}</div>
            {% endfor %}
        {% endwith %}

        <form method="post">

            <div class="field">
                <label>Full name</label>
                <input name="name" placeholder="Test User" required>
            </div>

            <div class="field">
                <label>Username</label>
                <input name="username" placeholder="your_username" required>
            </div>

            <div class="field">
                <label>Mobile number</label>
                <input name="mobile" placeholder="01700000000" required>
            </div>

            <div class="field">
                <label>NID</label>
                <input name="nid" placeholder="TRAINING-001" required>
            </div>

            <div class="field">
                <label>Password</label>
                <input
                    type="password"
                    name="password"
                    placeholder="Create a password"
                    required
                >
            </div>

            <button class="btn">Create account</button>
        </form>

        <p class="footer">
            Already registered?
            <a href="/login">Sign in</a>
        </p>
    </div>
</div>
"""

    return render_template_string(
        page("NovaBank — Create Account", body)
    )


@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------

@app.get("/")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    u = users[session["user_id"]]

    recent = [
        t for t in reversed(transactions)
        if t["sender_id"] == u["id"] or t["recipient_id"] == u["id"]
    ][:10]

    flag_msg = FLAG if challenge_completed else None

    body = """
{{ navigation|safe }}

<div class="wrap">

    {% if flag_msg %}
    <div class="alert">
        🎉 Challenge condition reached:
        <strong>{{ flag_msg }}</strong>
    </div>
    {% endif %}

    <div class="hero">
        <div>
            <div class="eyebrow">Personal Banking</div>
            <h1>Good day, {{ u.name }}</h1>
            <div class="muted">
                Manage your account and review recent activity.
            </div>
        </div>

        <span class="pill">{{ u.role }}</span>
    </div>

    <div class="grid">

        <main>

            <div class="card">
                <div class="cardhead">
                    <b>Available balance</b>
                    <span class="pill">Active</span>
                </div>

                <div class="cardbody">
                    <div class="balance">
                        ৳ {{ "%.2f"|format(u.balance) }}
                    </div>

                    <div class="stats">
                        <div class="stat">
                            <b>{{ recent|length }}</b>
                            <span>Recent transactions</span>
                        </div>

                        <div class="stat">
                            <b>Standard</b>
                            <span>Account tier</span>
                        </div>

                        <div class="stat">
                            <b>Verified</b>
                            <span>Account status</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="forms">

                <div class="card">
                    <div class="cardhead">
                        <b>Add money</b>
                        <span class="pill">Training Card</span>
                    </div>

                    <div class="cardbody">
                        <form method="post" action="/deposit">

                            <div class="field">
                                <label>Card number</label>
                                <input
                                    name="card_number"
                                    placeholder="Any 16 digits"
                                    maxlength="16"
                                    required
                                >
                            </div>

                            <div class="field">
                                <label>Expiry date</label>
                                <input
                                    name="expiry"
                                    placeholder="12/30"
                                    required
                                >
                            </div>

                            <div class="field">
                                <label>Cardholder name</label>
                                <input
                                    name="cardholder"
                                    placeholder="Test User"
                                    required
                                >
                            </div>

                            <div class="field">
                                <label>Amount (BDT)</label>
                                <input
                                    name="amount"
                                    type="number"
                                    min="1"
                                    step="0.01"
                                    value="1000"
                                    required
                                >
                            </div>

                            <button class="btn">Add funds</button>
                        </form>
                    </div>
                </div>

                <div class="card">
                    <div class="cardhead">
                        <b>Send money</b>
                        <span class="pill">Transfer</span>
                    </div>

                    <div class="cardbody">
                        <form method="post" action="/transfer">

                            <div class="field">
                                <label>Recipient username</label>
                                <input
                                    name="recipient"
                                    value="campus_store"
                                    required
                                >
                            </div>

                            <div class="field">
                                <label>Amount (BDT)</label>
                                <input
                                    name="amount"
                                    type="number"
                                    min="1"
                                    step="0.01"
                                    value="100.00"
                                    required
                                >
                            </div>

                            <button class="btn">Send transfer</button>
                        </form>
                    </div>
                </div>

            </div>

            <div class="card">
                <div class="cardhead">
                    <b>Recent transactions</b>
                    <span class="pill">Last 10</span>
                </div>

                <div class="cardbody">

                    <table class="table">
                        <tr>
                            <th>ID</th>
                            <th>Type</th>
                            <th>Amount</th>
                            <th>From / To</th>
                        </tr>

                        {% for t in recent %}
                        <tr>
                            <td>{{ t.id }}</td>
                            <td>{{ t.type }}</td>
                            <td>৳ {{ "%.2f"|format(t.amount) }}</td>
                            <td>
                                {{ users[t.sender_id].username }}
                                →
                                {{ users[t.recipient_id].username }}
                            </td>
                        </tr>
                        {% endfor %}
                    </table>

                </div>
            </div>

        </main>

        <aside>

            <div class="card">
                <div class="cardhead">
                    <b>Account</b>
                    <span class="pill">Verified</span>
                </div>

                <div class="cardbody">

                    <div class="field">
                        <label>Username</label>
                        <strong>{{ u.username }}</strong>
                    </div>

                    <div class="field">
                        <label>Mobile</label>
                        <strong>{{ u.mobile }}</strong>
                    </div>

                    <div class="field">
                        <label>NID</label>
                        <strong>{{ u.nid }}</strong>
                    </div>

                    <div class="field">
                        <label>Account ID</label>
                        <strong>{{ u.id }}</strong>
                    </div>

                </div>
            </div>

            <div class="card">
                <div class="cardhead">
                    <b>Security</b>
                    <span class="pill">Monitored</span>
                </div>

                <div class="cardbody">
                    <p class="muted">
                        Login protected<br>
                        Transaction service online<br>
                        Fraud monitoring enabled
                    </p>
                </div>
            </div>

        </aside>

    </div>

    <div class="footer">
        IITCTF LAB • All balances and payment instruments are fictional.
    </div>

</div>
"""

    return render_template_string(
        page("NovaBank — Dashboard", body),
        navigation=navigation(),
        u=u,
        users=users,
        recent=recent,
        flag_msg=flag_msg,
    )


# ---------------------------------------------------------------------
# Deposit
# ---------------------------------------------------------------------

@app.post("/deposit")
def deposit():
    if "user_id" not in session:
        return redirect("/login")

    u = users[session["user_id"]]

    card = request.form.get("card_number", "")
    expiry = request.form.get("expiry", "")
    cardholder = request.form.get("cardholder", "")
    amount_raw = request.form.get("amount", "0")

    if not re.fullmatch(r"\d{16}", card):
        flash("Training card must contain exactly 16 digits.", "error")
        return redirect("/")

    try:
        amount = float(amount_raw)
    except ValueError:
        flash("Invalid amount.", "error")
        return redirect("/")

    if amount <= 0 or amount > 1000000:
        flash("Invalid amount.", "error")
        return redirect("/")

    if not expiry or not cardholder:
        flash("Card details are required.", "error")
        return redirect("/")

    u["balance"] += amount

    global next_tx_id

    transactions.append({
        "id": next_tx_id,
        "sender_id": 2,
        "recipient_id": u["id"],
        "amount": amount,
        "type": "DEPOSIT",
    })

    next_tx_id += 1

    return redirect("/")


# ---------------------------------------------------------------------
# Intentionally vulnerable transfer
# ---------------------------------------------------------------------

@app.post("/transfer")
def transfer():
    if "user_id" not in session:
        return redirect("/login")

    u = users[session["user_id"]]

    recipient_username = request.form.get("recipient", "").strip()
    amount_raw = request.form.get("amount", "0")

    try:
        amount = float(amount_raw)
    except ValueError:
        flash("Invalid amount.", "error")
        return redirect("/")

    if amount <= 0 or amount > 1000000:
        flash("Invalid amount.", "error")
        return redirect("/")

    recipient = next(
        (
            user
            for user in users.values()
            if user["username"] == recipient_username
        ),
        None,
    )

    if not recipient:
        flash("Recipient not found.", "error")
        return redirect("/")

    if recipient["id"] == u["id"]:
        flash("You cannot transfer money to yourself.", "error")
        return redirect("/")

    # ---------------------------------------------------------------
    # INTENTIONALLY VULNERABLE RACE CONDITION
    #
    # The balance is read and checked before the write lock.
    # Concurrent requests can therefore observe the same old balance.
    # ---------------------------------------------------------------

    observed_balance = u["balance"]

    if observed_balance < amount:
        flash("Insufficient balance.", "error")
        return redirect("/")

    # Artificial delay makes the race easier to reproduce in the CTF.
    time.sleep(0.05)

    global next_tx_id
    global challenge_completed

    with balance_write_lock:

        # IMPORTANT:
        # We intentionally use the stale observed_balance here.
        # Do NOT change this to:
        #
        #     u["balance"] -= amount
        #
        # because that would remove the intended race condition.
        u["balance"] = observed_balance - amount

        recipient["balance"] += amount

        transactions.append({
            "id": next_tx_id,
            "sender_id": u["id"],
            "recipient_id": recipient["id"],
            "amount": amount,
            "type": "TRANSFER",
        })

        next_tx_id += 1

        # Challenge completion is now server-side instead of
        # being stored in the session.
        store = users[2]

        if store["balance"] >= 50000 and u["id"] != 2:
            challenge_completed = True

    return redirect("/")


# ---------------------------------------------------------------------
# Transfer page
# ---------------------------------------------------------------------

@app.get("/transfer")
def transfer_page():
    if "user_id" not in session:
        return redirect("/login")

    u = users[session["user_id"]]

    body = """
{{ navigation|safe }}

<div class="wrap">

    <div class="hero">
        <div>
            <div class="eyebrow">Payments</div>
            <h1>Transfer money</h1>
            <div class="muted">
                Send funds to another NovaBank username.
            </div>
        </div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="alert {% if category == 'error' %}error{% endif %}">
                {{ message }}
            </div>
        {% endfor %}
    {% endwith %}

    <div class="card">
        <div class="cardhead">
            <b>New transfer</b>
            <span class="pill">TRANSFER</span>
        </div>

        <div class="cardbody">

            <form method="post" action="/transfer">

                <div class="field">
                    <label>Recipient username</label>
                    <input
                        name="recipient"
                        placeholder="campus_store"
                        required
                    >
                </div>

                <div class="field">
                    <label>Amount (BDT)</label>
                    <input
                        name="amount"
                        type="number"
                        min="1"
                        step="0.01"
                        placeholder="1000"
                        required
                    >
                </div>

                <button class="btn">Send transfer</button>

            </form>

        </div>
    </div>

</div>
"""

    return render_template_string(
        page("NovaBank — Transfer", body),
        navigation=navigation(),
        u=u,
    )


# ---------------------------------------------------------------------
# Transactions
# ---------------------------------------------------------------------

@app.get("/transactions")
def transactions_page():
    if "user_id" not in session:
        return redirect("/login")

    u = users[session["user_id"]]

    rows = [
        t for t in reversed(transactions)
        if t["sender_id"] == u["id"]
        or t["recipient_id"] == u["id"]
    ]

    body = """
{{ navigation|safe }}

<div class="wrap">

    <div class="hero">
        <div>
            <div class="eyebrow">Activity</div>
            <h1>Transactions</h1>
            <div class="muted">
                Your recent account activity.
            </div>
        </div>
    </div>

    <div class="card">
        <div class="cardhead">
            <b>Transaction history</b>
            <span class="pill">{{ rows|length }} RECORDS</span>
        </div>

        <div class="cardbody">

            <table class="table">
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Amount</th>
                    <th>From</th>
                    <th>To</th>
                </tr>

                {% for t in rows %}
                <tr>
                    <td>{{ t.id }}</td>
                    <td>{{ t.type }}</td>
                    <td>৳ {{ "%.2f"|format(t.amount) }}</td>
                    <td>{{ users[t.sender_id].username }}</td>
                    <td>{{ users[t.recipient_id].username }}</td>
                </tr>
                {% endfor %}

            </table>

        </div>
    </div>

</div>
"""

    return render_template_string(
        page("NovaBank — Transactions", body),
        navigation=navigation(),
        rows=rows,
        users=users,
    )


# ---------------------------------------------------------------------
# Intentionally exposed API endpoints for the BOLA portion of the CTF
# ---------------------------------------------------------------------

@app.get("/api/profile/<int:account_id>")
def api_profile(account_id):
    user = users.get(account_id)

    if not user:
        return jsonify({"error": "account not found"}), 404

    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "name": user["name"],
        "role": user["role"],
        "balance": user["balance"],
    })


@app.get("/api/transactions/<int:account_id>")
def api_transactions(account_id):
    if account_id not in users:
        return jsonify({"error": "account not found"}), 404

    rows = [
        t for t in transactions
        if t["sender_id"] == account_id
        or t["recipient_id"] == account_id
    ]

    return jsonify({
        "account_id": account_id,
        "transactions": rows,
    })


# ---------------------------------------------------------------------
# robots.txt
# ---------------------------------------------------------------------

@app.get("/robots.txt")
def robots():
    return (
        "User-agent: *\n"
        "Disallow: /api/profile/3\n"
        "Disallow: /api/transactions/3\n",
        200,
        {"Content-Type": "text/plain"},
    )


# ---------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "challenge_completed": challenge_completed,
    })


# ---------------------------------------------------------------------
# Start application
# ---------------------------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8084,
        threaded=True,
        debug=False,
    )
