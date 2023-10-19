import sqlite3
conn = sqlite3.connect('baseDonnees.db')
cur = conn.cursor()
datas = [
 ('1984','Orwell',1949,10),
 ('Dune','Herbert',1965,8),
 ('Fondation','Asimov',1951,9),
 ('Le meilleur des mondes','Huxley',1931,7),
 ('Fahrenheit 451','Bradbury',1953,7),
 ('Ubik','K.Dick',1969,9),
 ('Chroniques martiennes','Bradbury',1950,8),
 ('La nuit des temps','Barjavel',1968,7),
 ('Blade Runner','K.Dick',1968,8),
 ('Les Robots','Asimov',1950,9),
 ('La Planète des singes','Boulle',1963,8),
 ('Ravage','Barjavel',1943,8),
 ('Le Maître du Haut Château','K.Dick',1962,8),
 ('Le monde des Ā','Van Vogt',1945,7),
 ('La Fin de l’éternité','Asimov',1955,8),
 ('De la Terre à la Lune','Verne',1865,10)
 ]
cur.execute("CREATE TABLE IF NOT EXISTS LIVRES(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, titre TEXT, auteur TXT, ann_publi INT, note INT)")
cur.executemany("INSERT INTO LIVRES(titre,auteur,ann_publi,note) VALUES(?, ?, ?, ?)", datas)
conn.commit()
cur.close()
conn.close()
