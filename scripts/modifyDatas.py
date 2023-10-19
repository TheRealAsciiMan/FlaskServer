import sqlite3
conn = sqlite3.connect('baseDonnees.db')
cur = conn.cursor()
modif = (7, 'Hypérion')
cur.execute('UPDATE LIVRES SET note = ? WHERE titre = ?', modif)
conn.commit()
cur.close()
conn.close()
