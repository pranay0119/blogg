from flask import Flask,render_template,request,redirect, url_for,session
import mysql.connector
mydb = mysql.connector.connect(host='localhost', user='root', password='system', db='flaskblog')
app = Flask(__name__)
app.secret_key=" my secret is too secret"
@app.route('/home')
def home():
    return render_template('homepage.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        mobilenumber = request.form.get('mobilenumber')
        email = request.form.get('email')
        address = request.form.get('address')
        password = request.form.get('password')
        cursor = mydb.cursor(buffered=True)
        cursor.execute("INSERT INTO registration (username, mobilenumber, email, address, password) VALUES (%s, %s, %s, %s, %s)", (username, mobilenumber, email, address, password))
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('registrationform.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  
        password = request.form.get('password')  
        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT COUNT(*) FROM registration WHERE username = %s AND password = %s", (username, password))
        data = cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['username']=username
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('loginform.html')
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        slug = request.form.get('slug')
        print(title)
        print(content)
        print(slug)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('INSERT INTO posts (title, content, slug) VALUES(%s,%s,%s)', (title, content, slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')  
@app.route('/blog')
def blog():
    return render_template('blog.html')
@app.route('/viewpost',methods=['GET','POST'])
def view():
    cursor = mydb.cursor(buffered=True)
    cursor.execute('Select * from posts')
    posts=cursor.fetchall()
    cursor.close()
    return render_template('viewpost.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor = mydb.cursor(buffered=True)
    cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('view'))
@app.route('/updatepost', methods=['GET', 'POST'])
def update_post():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        slug = request.form.get('slug')
        print(title)
        print(content)
        print(slug)
        return redirect(url_for('home'))
    
        cursor=mydb.cursor(buffered=True)
        cursor.execute('UPDATE POSTS SET title=%s,content=%s,slug=%s WHERE id=%s',(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('home'))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s,(id)')

        post=cursor.fetchone()
        cursor.close()
        return render_template('updatepost.html',post=post)
app.run()
