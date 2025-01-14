from flask import Flask , render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']=
app.config['MYSQL_HOST']=
app.config['MYSQL_HOST']=
app.config['MYSQL_HOST']=
app.config['MYSQL_HOST']=

@app.route("/")
def home():
    return render_template("index.html", titolo="Home")

@app.route("/login")
def login():
    return render_template("login.html", titolo="Login")

@app.route("/register", methods=['POST','GET'])
def register():
    if request.method=='GET':
        return render_template("register.html", titolo="register")
    fname = request.form ['fname']
    lname = request.form['lname']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password == confirm_password:
        cursor=mysql.connection.cursor()
        query="INSERT INTO users VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, password, fname, lname))
        mysql.connection.commit()
        cursor.execute("SELECT * FROM users")
        print(cursor.fetchall())
        return redirect(url_for('home'))
    return "passord diverse"

app.run(debug=True)
