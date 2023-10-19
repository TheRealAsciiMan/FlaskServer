import sqlite3
conn = sqlite3.connect('baseDonnees.db')
cur = conn.cursor()
suppr = ('Hypérion',)
cur.execute('DELETE FROM LIVRES WHERE titre = ?', suppr)
conn.commit()
cur.close()
conn.close()