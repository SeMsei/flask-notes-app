from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

app = Flask(__name__, template_folder=os.path.abspath('../front/templates'), static_folder = os.path.abspath('../front/static'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    Header = db.Column(db.String(80), nullable=False)
    Text = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return f'Header: {self.Header}; Text: {self.Text};'

    def set_header(self, header):
        self.Header = header

    def set_text(self, text):
        self.Text = text


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'GET':
        note = Note.query.filter_by(id=id).first()

        if not note:
            return redirect(url_for('main'))
        
        return render_template('edit.html', note=note)

    elif request.method == 'POST':
        with app.app_context():
            note = db.session.query(Note).filter_by(id=id).update(dict(Header=request.form.get('header'), Text=request.form.get('text')))
            db.session.commit()

        return redirect(url_for('main'))

@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        note = Note(Header=request.form.get('header'), Text=request.form.get('text'), user_id=current_user.get_id())
        
        with app.app_context():
            db.session.add(note)
            db.session.commit()

        return redirect(url_for('main'))

@app.route('/delete/<int:id>')
def delete_note(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    with app.app_context():

        Note.query.filter_by(id=id).delete()
        db.session.commit()

    return redirect(url_for('main'))

@app.route('/')
def main():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        notes = Note.query.filter_by(user_id=user_id)

        return render_template('main.html', notes=notes)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']

        print(username, password, password1)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already exists'
            return render_template('register.html', error=error)
        
        if password1 != password:
            error = 'Passwords must match '
            return render_template('register.html', error=error)
        
        create_user(username, password)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(username, password)

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
        else:
            login_user(user)
            return redirect(url_for('main'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    with app.app_context():
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    print(123)
    with app.app_context():
        db.create_all()
    app.run(debug=True)