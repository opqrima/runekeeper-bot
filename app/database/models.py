import sqlite3
from pathlib import Path
from app.config import DATABASE_PATH

def init_db():
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS airdrops
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         project_name TEXT NOT NULL,
         category TEXT,
         date_posted TEXT,
         link TEXT,
         description TEXT,
         reward TEXT,
         tasks TEXT,
         status TEXT DEFAULT 'Pending',
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()