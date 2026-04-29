from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

app = Flask(__name__)

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tournoi.db')
    c = conn.cursor()
    
    # Table EQUIPES
    c.execute('''CREATE TABLE IF NOT EXISTS equipes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nom_equipe TEXT NOT NULL,
                  capitaine TEXT NOT NULL,
                  telephone TEXT NOT NULL,
                  email TEXT NOT NULL,
                  quartier TEXT,
                  nb_joueurs INTEGER)''')
    
    # Table JOUEURS
    c.execute('''CREATE TABLE IF NOT EXISTS joueurs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nom TEXT NOT NULL,
                  equipe_id INTEGER)''')
    
    # Table MATCHS
    c.execute('''CREATE TABLE IF NOT EXISTS matchs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  equipe1 TEXT,
                  equipe2 TEXT,
                  score_equipe1 INTEGER,
                  score_equipe2 INTEGER)''')
    
    conn.commit()
    conn.close()

init_db()  # On lance la fonction ici

@app.route('/')
def formulaire():
    return render_template('formulaire.html')

@app.route('/inscrire', methods=['POST'])
def inscrire():
    nom_equipe = request.form.get('nom_equipe')
    capitaine = request.form.get('capitaine')
    telephone = request.form.get('telephone')
    email = request.form.get('email')

    if not all([nom_equipe, capitaine, telephone, email]):
        return "Erreur : remplis tous les champs obligatoires.", 400

    quartier = request.form.get('quartier')
    nb_joueurs = request.form.get('nb_joueurs')

    conn = sqlite3.connect('tournoi.db')
    c = conn.cursor()
    c.execute("INSERT INTO equipes (nom_equipe, capitaine, telephone, email, quartier, nb_joueurs) VALUES (?,?,?,?,?,?)",
              (nom_equipe, capitaine, telephone, email, quartier, nb_joueurs))
    conn.commit()
    conn.close()

    return redirect(url_for('merci'))

@app.route('/merci')
def merci():
    return "<h1>Merci! Inscription réussie.</h1><p>Ton équipe est bien enregistrée pour le tournoi.</p><a href='/'>Retour</a>"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('tournoi.db')
    c = conn.cursor()
    c.execute("SELECT * FROM equipes")
    equipes = c.fetchall()
    conn.close()
    return render_template('admin.html', equipes=equipes)
@app.route('/statistiques')
def statistiques():
    conn = sqlite3.connect('tournoi.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM equipes")
    total_equipes = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM joueurs") 
    total_joueurs = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM matchs")
    matchs_joues = c.fetchone()[0]
    
    conn.close()
    return render_template('statistiques.html', 
                           equipes=total_equipes,
                           joueurs=total_joueurs, 
                           matchs=matchs_joues)
@app.route('/equipes')
def liste_equipes():
    conn = sqlite3.connect('tournoi.db')
    c = conn.cursor()
    c.execute("SELECT id, nom_quartier, nom_coach, telephone FROM equipes ORDER BY id DESC")
    equipes = c.fetchall()
    conn.close()
    return render_template('equipes.html', equipes=equipes)
    
if __name__ == '__main__':
    init_db()
    port = int(os.environ.-get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


