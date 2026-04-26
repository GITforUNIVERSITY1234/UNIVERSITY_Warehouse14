""" 
from flask import Flask, request, render_template, session, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# @app.route('/')
# def index():
#     return 'Index Page'

# @app.route('/hello')
# def hello_world():
#     return '<h1>Hello World!</h1>'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    if not name:
        name = "World"
    # return f'<h1>Hello {escape(name)}!</h1>'
    return render_template("hello.html", person = name)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

# Запуск - python -m flask --app main run 
"""