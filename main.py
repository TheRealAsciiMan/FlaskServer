from flask import Flask, render_template, request, redirect
import sqlite3
def main():
    app = Flask(__name__)
    @app.route('/')
    def index():
        conn = sqlite3.connect('dataBase.db')
        cur = conn.cursor()
        cur.execute('SELECT Posts.*, Users.pseudo FROM Posts INNER JOIN Users ON Posts.auteur = Users.Mail;')
        conn.commit()
        liste = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", liste = liste)

    @app.route('/ajout')
    def ajout():
        return render_template("ajout.html")

    @app.route('/ajouter_livre', methods=['POST', 'GET'])
    def ajouter_livre():
        if request.method == 'GET':
            return redirect('/')
        elif request.method == 'POST':
            titre = request.form.get('titre')
            auteur = request.form.get('auteur')
            annee = int(request.form.get('annee'))
            note = int(request.form.get('note'))
            data = (titre, auteur, annee, note)
            conn = sqlite3.connect('baseDonnees.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO LIVRES(titre,auteur,ann_publi,note) VALUES(?, ?, ?, ?)", data)
            conn.commit()
            cur.close()
            conn.close()
            return redirect('/')
    app.run(debug=True, host='0.0.0.0', port=80)


if __name__ == "__main__":
    main()