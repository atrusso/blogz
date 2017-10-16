from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:builderbob@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3Bn44TBer81DC1a'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['GET'])
def index():
    return redirect('blog')


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

        blog = Blog(title, body)
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog?id=' + str(blog.id))
        
        
if __name__ == '__main__':
    app.run()