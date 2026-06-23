
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
    active_user = cur.execute("SELECT * FROM users ORDER BY id ASC LIMIT 1").fetchone()
    conn.close()
    return render(
        request,
        "dashboard/index.html",
        "Dashboard",
        "dashboard",
        counts=counts,
        recent_records=[dict(x) for x in recent_records],
        active_user=dict(active_user) if active_user else None,
    )

@app.get("/records", response_class=HTMLResponse)
def records(request: Request, q: str = ""):
    conn = get_connection()
    cur = conn.cursor()
    if q:
        rows = cur.execute(
            "SELECT * FROM records WHERE ref_no LIKE ? OR title LIKE ? OR category LIKE ? OR owner LIKE ? ORDER BY id DESC",
            (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%")
        ).fetchall()
    else:
        rows = cur.execute("SELECT * FROM records ORDER BY id DESC").fetchall()
    conn.close()
    return render(request, "records/index.html", "Records", "records", records=[dict(x) for x in rows], q=q)

@app.post("/records/create")
def record_create(
    ref_no: str = Form(...),
    title: str = Form(...),
    category: str = Form(...),
    priority: str = Form("medium"),
    status: str = Form("draft"),
    owner: str = Form(...),
    due_date: str = Form("")
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO records(ref_no,title,category,priority,status,owner,due_date) VALUES(?,?,?,?,?,?,?)",
        (ref_no, title, category, priority, status, owner, due_date or None)
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/records", status_code=303)

@app.post("/records/{record_id}/update")
def record_update(
    record_id: int,
    ref_no: str = Form(...),
    title: str = Form(...),
    category: str = Form(...),
    priority: str = Form("medium"),
    status: str = Form("draft"),
    owner: str = Form(...),
    due_date: str = Form("")
):
    conn = get_connection()
    conn.execute(
        "UPDATE records SET ref_no=?, title=?, category=?, priority=?, status=?, owner=?, due_date=? WHERE id=?",
        (ref_no, title, category, priority, status, owner, due_date or None, record_id)
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/records", status_code=303)

@app.post("/records/{record_id}/delete")
def record_delete(record_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM records WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/records", status_code=303)

@app.get("/users", response_class=HTMLResponse)
def users(request: Request, q: str = ""):
    conn = get_connection()
    cur = conn.cursor()
    if q:
        rows = cur.execute(
            "SELECT * FROM users WHERE full_name LIKE ? OR email LIKE ? OR role LIKE ? ORDER BY id DESC",
            (f"%{q}%", f"%{q}%", f"%{q}%")
        ).fetchall()
    else:
        rows = cur.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return render(request, "users/index.html", "Users", "users", users=[dict(x) for x in rows], q=q)

@app.post("/users/create")
def user_create(
    full_name: str = Form(...),
    email: str = Form(...),
    role: str = Form("user"),
    status: str = Form("active")
):
    conn = get_connection()
    cur = conn.cursor()
    exists = cur.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
    if exists:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    cur.execute(
        "INSERT INTO users(full_name,email,role,status) VALUES(?,?,?,?)",
        (full_name, email, role, status)
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/users", status_code=303)

@app.post("/users/{user_id}/update")
def user_update(
    user_id: int,
    full_name: str = Form(...),
    email: str = Form(...),
    role: str = Form("user"),
    status: str = Form("active")
):
    conn = get_connection()
    cur = conn.cursor()
    other = cur.execute("SELECT id FROM users WHERE email=? AND id<>?", (email, user_id)).fetchone()
    if other:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    cur.execute(
        "UPDATE users SET full_name=?, email=?, role=?, status=? WHERE id=?",
        (full_name, email, role, status, user_id)
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/users", status_code=303)

@app.post("/users/{user_id}/delete")
def user_delete(user_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/users", status_code=303)

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
