from flask import Flask, render_template, request, redirect
import sqlite3
def main():
    app = Flask(__name__)
    @app.route('/')
    def index():
        conn = sqlite3.connect('baseDonnees.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM LIVRES')
        conn.commit()
        liste = cur.fetchall()
        cur.close()
        conn.close()
        table_html =  "<table class=\"table table-dark table-hover table-bordered table-striped \"><thead class=\"table-danger\"><tr><th>ID</th><th>Titre</th><th>Auteur</th><th>Année de publication</th><th>Note</th></tr></thead><tbody class=\"table-group-divider\">"
        for livre in liste:
                table_html += "<tr>"
                for i in range(len(livre)):
                    table_html += "<td>" + str(livre[i]) + "</td>"
                table_html += "</tr>"
        table_html += "</tbody></table>"
        return render_template("index.html", liste = table_html)

    @app.route('/ajout')
    def ajout():
        return render_template("ajout.html")

    @app.route('/ajouter_livre', methods=['POST'])
    def ajouter_livre():
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
    app.run(debug=True)

if __name__ == "__main__":
    main()