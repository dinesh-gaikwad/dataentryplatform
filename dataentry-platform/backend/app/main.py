from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.db.init_db import init_db
from app.db.database import get_connection
from app.services.nav_service import nav_items

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup():
    init_db()

def render(request: Request, template: str, title: str, active: str, **ctx):
    data = {"page_title": title, "nav": nav_items(active)}
    data.update(ctx)
    return templates.TemplateResponse(request, template, data)

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    conn = get_connection()
    cur = conn.cursor()
    counts = {
        "records": cur.execute("SELECT COUNT(*) FROM records").fetchone()[0],
        "users": cur.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "workflows": cur.execute("SELECT COUNT(*) FROM workflows").fetchone()[0],
        "imports": cur.execute("SELECT COUNT(*) FROM imports").fetchone()[0],
    }
    recent_records = cur.execute("SELECT * FROM records ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    return render(request, "dashboard/index.html", "Dashboard", "dashboard", counts=counts, recent_records=[dict(x) for x in recent_records])

@app.get("/records", response_class=HTMLResponse)
def records(request: Request):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM records ORDER BY id DESC").fetchall()
    conn.close()
    return render(request, "records/index.html", "Records", "records", records=[dict(x) for x in rows])

@app.get("/users", response_class=HTMLResponse)
def users(request: Request):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return render(request, "users/index.html", "Users", "users", users=[dict(x) for x in rows])

@app.get("/workflows", response_class=HTMLResponse)
def workflows(request: Request):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM workflows ORDER BY id DESC").fetchall()
    conn.close()
    return render(request, "workflows/index.html", "Workflows", "workflows", workflows=[dict(x) for x in rows])

@app.get("/forms", response_class=HTMLResponse)
def forms(request: Request):
    return render(request, "forms/index.html", "Forms", "forms")

@app.get("/imports", response_class=HTMLResponse)
def imports(request: Request):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM imports ORDER BY id DESC").fetchall()
    conn.close()
    return render(request, "imports/index.html", "Imports", "imports", imports=[dict(x) for x in rows])

@app.get("/exports", response_class=HTMLResponse)
def exports(request: Request):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM exports ORDER BY id DESC").fetchall()
    conn.close()
    return render(request, "exports/index.html", "Exports", "exports", exports=[dict(x) for x in rows])

@app.get("/analytics", response_class=HTMLResponse)
def analytics(request: Request):
    return render(request, "analytics/index.html", "Analytics", "analytics")

@app.get("/reports", response_class=HTMLResponse)
def reports(request: Request):
    return render(request, "reports/index.html", "Reports", "reports")

@app.get("/notifications", response_class=HTMLResponse)
def notifications(request: Request):
    return render(request, "notifications/index.html", "Notifications", "notifications")

@app.get("/logs", response_class=HTMLResponse)
def logs(request: Request):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM audit_logs ORDER BY id DESC").fetchall()
    conn.close()
    return render(request, "logs/index.html", "Logs", "logs", logs=[dict(x) for x in rows])

@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    return render(request, "settings/index.html", "Settings", "settings")

@app.get("/help", response_class=HTMLResponse)
def help_page(request: Request):
    return render(request, "help/index.html", "Help", "help")

@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return render(request, "auth/login.html", "Login", "login")

@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return render(request, "auth/register.html", "Register", "register")

@app.post("/api/auth/login")
def api_login(email: str = Form(...), password: str = Form(...)):
    return {"message": "login stub", "email": email}

@app.post("/api/auth/register")
def api_register(full_name: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form("user")):
    conn = get_connection()
    cur = conn.cursor()
    exists = cur.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
    if exists:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    cur.execute("INSERT INTO users(full_name,email,role,status) VALUES(?,?,?,?)", (full_name, email, role, "active"))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/users", status_code=303)
