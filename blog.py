from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    post = db.Column(db.String(), nullable=False)

    def __repr__(self):
        f'<Post {self.id} {self.post}>'


migrate = Migrate(app, db)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error), status_code


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were looged out')
    return redirect(url_for('login'))


@app.route('/main')
@login_required
def main():
    posts = Posts.query.order_by('id').all()
    return render_template('main.html', data=posts)


if __name__ == '__main__':
    app.run(host='192.168.1.173')
