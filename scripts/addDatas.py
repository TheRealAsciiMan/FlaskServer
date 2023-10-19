import sqlite3
conn = sqlite3.connect('baseDonnees.db')
cur = conn.cursor()
nvx_data = ('Hypérion','Simmons',1989,8)
cur.execute("INSERT INTO LIVRES(titre,auteur,ann_publi,note) VALUES(?, ?, ?, ?)", nvx_data)
conn.commit()
cur.close()
conn.close()