from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3


def main():
    app = Flask(__name__)
    app.secret_key = "(L)SD>HD"
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
        if 'pseudo' in session and type(session["pseudo"]) == str:
            return render_template("ajout.html")
        else:
            return redirect("/")

    @app.route('/login')
    def login():
        return render_template("login.html")

    @app.route('/action_login', methods=['POST', 'GET'])
    def action_login():
        if request.method == 'GET':
            return redirect("/")
        elif request.method == 'POST':
            mail = request.form.get('mail')
            password = request.form.get('password')
            password = password[:4] + '-' + password[4:6] + '-' + password[6:8]
            data = (mail, password)
            conn = sqlite3.connect('dataBase.db')
            cur = conn.cursor()
            cur.execute('SELECT Pseudo, "Date d\'inscription"  FROM Users WHERE Mail = ? AND "Date d\'inscription" = ?', data)
            conn.commit()
            info = cur.fetchone()
            cur.close()
            conn.close()
            if info:
                session['pseudo'] = info[0]
                return redirect("/")
            else:
                return redirect(url_for("login", error = True))
    @app.route('/logout')
    def logout():
        session['pseudo'] = None
        return redirect("/login")




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