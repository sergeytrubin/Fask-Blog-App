from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    post = db.Column(db.String(), nullable=False)


migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. PLease try again.'
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
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='192.168.1.173')
