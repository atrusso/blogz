from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogoriffic7@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3Bn44TBer81DC1a'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/', methods=['GET'])
def index():
    return redirect('index')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        error = request.args.get('error')
        return render_template('signup.html', error=error)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verifypass = request.form['verifypass']
        existing_user = User.query.filter_by(username=username).first()

    #valid username, pass, verify redirect to /newpost with username stored in session
    if not existing_user and password == verifypass:
        new_user = User(username, password)
        db.session.add(new_user)
        db.commit()
        session['user'] = username
        return redirect('/newpost')

    #username, pass, verify left blank redirect to /signup with message
    if username == "" or password == "" or verifypass == "":
        error = "username, password, or verify password field(s) were empty"
        return redirect('/signup?error=' + error)

    #existing username redirect to /signup with message
    if existing_user:
        error = "username is already on file"
        return redirect('/signup?error=' + error)

    #different pass vs verify, redirect to /signup with message
    if password == verifypass:
        error = "password and verify password fields did not match"
        return redirect('/signup?error=' + error)

    #username or pass  < 3 characters, redirect to /signup with message
    if len(username) < 3 or len(password) < 3:
        error = "fields must be more than 3 characters"
        return redirect('/signup?error=' + error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        error = request.args.get('error')
        return render_template('login.html', error=error)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

    #correct creds redirect to to /newpost with username stored in session
    if user and password == User.query.filter_by(user).first():
        session['user'] = user
        return redirect('/newpost')

    #incorrect password redirect to /login with message
    if user and password != User.query.filter_by(user).first():
        error = 'password does not match the username'
        return redirect('/login?error=' + error)

    #username doesn't exist redirect to /login with message
    if not user:
        error = 'username does not exist'
        return redirect('/login?error=' + error)

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/blog')    

@app.route('/blog', methods=['GET'])
def blog():
    if 'id' in request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('blog.html', blog=blog)
    else:
        blogs = Blog.query.order_by("id desc").all()
        return render_template('blog.html',blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def add_post():
    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body']

        #empty title
        if title == "":
            title_error = "Looks like you forgot to add a title"
            if body == "":
                body_error = "Looks like you forgot to add content to your blog entry"
                return render_template('newpost.html', body_error=body_error, title_error=title_error)
            
            return render_template('newpost.html', blog_body=body, title_error=title_error)
        #empty blog body
        if body == "":
            body_error = "Looks like you forgot to add content to your blog entry"
            return render_template('newpost.html', blog_title=title, body_error=body_error)

        owner = User.query.filter_by(username=session['user']).first()
        blog = Blog(title, body, owner)
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog?id=' + str(blog.id))
        
        
if __name__ == '__main__':
    app.run()