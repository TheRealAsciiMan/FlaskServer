from flask import Flask, render_template, request, redirect, session, url_for
from markupsafe import escape
import datetime
import sqlite3


def main():
    app = Flask(__name__)
    app.secret_key = "SD>HD"
    @app.route('/')
    def index():
        conn = sqlite3.connect('DataBase.db')
        cur = conn.cursor()
        cur.execute('SELECT Posts.*, Users.pseudo FROM Posts INNER JOIN Users ON Posts.auteur = Users.Mail ORDER BY Date DESC;')
        conn.commit()
        liste = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", liste = liste)


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
            conn = sqlite3.connect('DataBase.db')
            cur = conn.cursor()
            cur.execute('SELECT *  FROM Users WHERE Mail = ? AND "Date d\'inscription" = ?', data)
            conn.commit()
            info = cur.fetchone()
            cur.close()
            conn.close()
            if info:
                session.clear()
                session["pseudo"] = info[0]
                session["mail"] = info[1]
                session["mod"] = info[3]
                session["admin"] = info[4]
                return redirect("/ajout")
            else:
                return redirect(url_for("login", error = 1))
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect("/login")


    @app.route('/inscription')
    def inscription():
        return render_template("register.html")

    @app.route('/action_inscription', methods=['POST', 'GET'])
    def action_inscription():
        if request.method == 'GET':
            return redirect('/')
        elif request.method == 'POST':
            pseudo = request.form.get('pseudo')
            mail = request.form.get('mail')
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            admin, mod = 0, 0
            data = (pseudo, mail, date, admin, mod)
            conn = sqlite3.connect('DataBase.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM Users WHERE Mail = ?', [mail])
            conn.commit()
            info = cur.fetchone()
            if info:
                cur.close()
                conn.close()
                return redirect(url_for("inscription", error=1))
            else:
                cur.execute('INSERT INTO Users(Pseudo,Mail,"Date d\'inscription",Administrateur,Modérateur) VALUES(?, ?, ?, ?, ?)', data)
                conn.commit()
                cur.close()
                conn.close()
                return redirect('/')

    @app.route('/ajout')
    def ajout():
        if 'pseudo' in session and type(session["pseudo"]) == str:
            return render_template("ajout.html")
        else:
            return redirect("/")

    @app.route('/action_post', methods=['POST', 'GET'])
    def action_post():
        if request.method == 'GET':
            return redirect('/')
        elif request.method == 'POST':
            if 'pseudo' in session and type(session["pseudo"]) == str:
                titre = request.form.get('titre')
                contenu = escape(request.form.get('contenu')).replace("\r\n", "<br>").replace("\n", "<br>").replace("\r", "<br>")
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                auteur = session["mail"]
                data = (titre, contenu, date, auteur)
                conn = sqlite3.connect('DataBase.db')
                cur = conn.cursor()
                cur.execute("SELECT * FROM Posts WHERE Contenu = ?", [contenu])
                conn.commit()
                info = cur.fetchone()
                if info:
                    cur.close()
                    conn.close()
                    return redirect(url_for("ajout", error=1))
                else:
                    cur.execute("INSERT INTO Posts(Titre,Contenu,Date,Auteur) VALUES(?, ?, ?, ?)", data)
                    conn.commit()
                    cur.close()
                    conn.close()
                    return redirect('/')

            else:
                return redirect(url_for("login", error=1))


    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
