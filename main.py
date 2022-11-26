from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
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

@app.route("/profile")
def profile():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT userId FROM users WHERE email = "' + session['email'] +'"')
        user = cur.fetchone()
        cur.execute('SELECT * FROM products WHERE userId = ?', user)
        
        products = cur.fetchall()
    productData = parse(products)
    return render_template('profile.html' , products = products , email = session['email'])
@app.route('/uploadForm')
def uploadForm():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT name FROM categories')
        categories = cur.fetchall()
    return render_template('upload.html' , categories = categories)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload' , methods= ['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category = request.form['category']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute('SELECT userId FROM users where email = "' +session['email'] + '"')
                user = cur.fetchone()[0]
                cur.execute('SELECT categoryId from categories where name = "'  +category+ '"')
                cate = cur.fetchone()[0]
                print(user, name , price, description, cate , filename)
                
                cur.execute("INSERT INTO products(name , price, description , image , categoryId, userId ,available) VALUES (?,?,?,?,?,?,?)",(str(name), float(price), str(description) , str('uploads/'+filename) , int(cate) , int(user) , 1))
                conn.commit()
            return redirect(url_for('uploaded_file',
                                    filename=filename))
@app.route('/uploaded_file')
def uploaded_file():
    return render_template('uploaded_file.html')
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