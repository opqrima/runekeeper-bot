import sqlite3
from app.config import DATABASE_PATH

class AirdropDB:
    @staticmethod
    def save_airdrop(data: dict) -> bool:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO airdrops 
                (project_name, category, date_posted, link, description, reward, tasks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['project_name'],
                data['category'],
                data['date_posted'],
                data['link'],
                data['description'],
                data.get('reward', ''),
                data.get('tasks', '')
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving airdrop: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all_airdrops():
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM airdrops ORDER BY date_posted DESC')
        airdrops = c.fetchall()
        conn.close()
        return airdrops