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

@app.route("/")
def root():
    loggedIn, email = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, available FROM products')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)   
    return render_template('home.html', itemData=itemData, loggedIn=loggedIn, email = email, categoryData=categoryData)

#Fetch user details if logged in
def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            email = ''
            # noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, email FROM users WHERE email = '" + session['email'] + "'")
            userId, email = cur.fetchone()
            # cur.execute("SELECT count(productId) FROM kart WHERE userId = " + str(userId))
            # noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, email)

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
@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))
def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)