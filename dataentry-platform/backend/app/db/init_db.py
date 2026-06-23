from app.db.database import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_no TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'medium',
        status TEXT NOT NULL DEFAULT 'draft',
        owner TEXT NOT NULL,
        due_date TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS workflows(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        stage TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS imports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        rows_count INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'queued',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS exports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        format TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'ready',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        actor TEXT NOT NULL,
        action TEXT NOT NULL,
        target TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.executemany("INSERT OR IGNORE INTO users(id,full_name,email,role,status) VALUES(?,?,?,?,?)", [
        (1,"Admin User","admin@demo.com","admin","active"),
        (2,"Entry Manager","manager@demo.com","manager","active")
    ])
    cur.executemany("INSERT OR IGNORE INTO records(id,ref_no,title,category,priority,status,owner,due_date) VALUES(?,?,?,?,?,?,?,?)", [
        (1,"REC-1001","Vendor onboarding","Operations","high","review","Admin User","2026-06-30"),
        (2,"REC-1002","Client KYC packet","Compliance","medium","draft","Entry Manager","2026-07-05"),
        (3,"REC-1003","Invoice batch upload","Finance","high","approved","Admin User","2026-06-28")
    ])
    cur.executemany("INSERT OR IGNORE INTO workflows(id,name,stage,status) VALUES(?,?,?,?)", [
        (1,"KYC Review","Validation","active"),
        (2,"Finance Intake","Approval","active"),
        (3,"Operations Queue","Processing","active")
    ])
    cur.executemany("INSERT OR IGNORE INTO imports(id,filename,rows_count,status) VALUES(?,?,?,?)", [
        (1,"vendors.csv",120,"completed"),
        (2,"clients.xlsx",54,"processing")
    ])
    cur.executemany("INSERT OR IGNORE INTO exports(id,name,format,status) VALUES(?,?,?,?)", [
        (1,"Daily Records","CSV","ready"),
        (2,"Monthly Report","XLSX","ready")
    ])
    cur.executemany("INSERT OR IGNORE INTO audit_logs(id,actor,action,target) VALUES(?,?,?,?)", [
        (1,"Admin User","created","REC-1001"),
        (2,"Entry Manager","updated","REC-1002")
    ])
    conn.commit()
    conn.close()
