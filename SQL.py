import sqlite3

class database:
    def __init__(self):
        self.con = sqlite3.connect("storage.db")

    def insert_user(self,data):
        cur = self.con.cursor()
        #cur.execute("CREATE TABLE users(id, login, pass)")
        cur.execute("SELECT MAX(ID) FROM users")
        idx = cur.fetchone()[0] + 1
        cur.execute(f"INSERT INTO users VALUES({idx},?,?)", data)
        self.con.commit()

    def select_users(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

    def insert_save(self, dt):
        cur = self.con.cursor()
        cur.execute("DELETE FROM save")
        cur.executemany("INSERT INTO save(a,b,res) VALUES(?,?,?)", dt)
        self.con.commit()

    def select_save(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM save")
        return cur.fetchall()

if __name__ == '__main__':
    d = database()
    print(d.select_users())
