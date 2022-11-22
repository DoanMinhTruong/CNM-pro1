from flask import *
import sqlite3, hashlib, os
# from werkzeug.utils import secure_filename
# from instamojo_wrapper import Instamojo
import requests

app = Flask(__name__)
app.secret_key = 'abcdxyztruongdeptrai'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return render_template('home.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, name, phone) VALUES (?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, name, phone))
                con.commit()
                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("home.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('home.html', error=error)

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('home.html', error='')

if __name__ == '__main__':
    app.run(debug=True)