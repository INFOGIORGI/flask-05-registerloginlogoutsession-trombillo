from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configurazione del database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modello utente per il database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Creazione del database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Pagina principale dove l'utente può scegliere tra login e registrazione
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Troviamo l'utente nel database
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Verifica la password
            session['username'] = user.username
            return redirect(url_for('home'))

        return 'Username o password errati!'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))  # Torna alla pagina iniziale

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se il nome utente è già presente nel database
        if User.query.filter_by(username=username).first():
            return 'Nome utente già esistente. Scegli un altro nome.'

        # Crea un nuovo utente e salva nel database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Dopo la registrazione, logga automaticamente l'utente
        session['username'] = username

        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('index'))  # Torna alla pagina principale se non loggato

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('index'))  # Torna alla pagina principale se non loggato

if __name__ == '__main__':
    app.run(debug=True)
