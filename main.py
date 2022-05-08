from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import random

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users2.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.permanent_session_lifetime = timedelta(days=5)

class users2(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    u_name = db.Column("u_name", db.String(20), nullable=False)
    name = db.Column("name", db.String(20), nullable=False)
    surname = db.Column("surname", db.String(20), nullable=False)
    email = db.Column("email", db.String(30), nullable=False)
    password = db.Column("password", db.String(30), nullable=False)
    points = db.Column("points", db.Integer, default=0)

    def __init__(self, u_name, name, surname, password, email):
        self.u_name = u_name
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.points = 0

@app.route('/account', methods=["POST", "GET"])
def account():
    if "u_name" in session:
        u_name = session["u_name"]
        found_user = users2.query.filter_by(u_name=u_name).first()
        return render_template("account.html", user=found_user, u_name=u_name)
    else:
        flash("Зарегистрируйтесь, пожалуйста", "info")
        return redirect(url_for("add_user"))    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        u_name = request.form['u_name']
        password = request.form['password']
        session["u_name"] = u_name

        found_user = users2.query.filter_by(u_name=u_name).first()
        if found_user:
            if found_user.password == password and found_user.password != '':
                session["u_name"] = found_user.u_name
                return redirect(url_for('account', user=found_user))
            else:
                flash("Неверный пароль, попробуйте снова:", "info")
                return render_template("login.html")
        else:
            flash("Пользователь не найден, попробуйте снова:", "info")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    if request.method == "POST":
        session.permanent = True
        u_name = request.form['u_name']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        session["u_name"] = u_name
        found_user = users2.query.filter_by(u_name=u_name).first()
        if found_user:
            session["email"] = found_user.email
            return redirect(url_for('account', user=found_user))
        else:
            user = users2(u_name=u_name, name=name, surname=surname, password=password, email=email)
            try:
                db.session.add(user)
                db.session.commit()
                flash(f"Вы успешно зарегистрировались, {u_name}", "info")
                return redirect(url_for("account", u_name=u_name))
            except:
                return "Error"
    else:
        if "u_name" in session:
            return redirect(url_for("account"))
        return render_template("add-user.html")

@app.route('/add-user/<int:_id>/update', methods=['POST', 'GET'])
def user_update(_id):
    user = users2.query.get(_id)
    if request.method == "POST":
        user.u_name = request.form['u_name']
        user.password = request.form['password']
        user.name = request.form['name']
        user.surname = request.form['surname']
        user.email = request.form['email']
        try:
            db.session.commit()
            return redirect(url_for('account', user=user))
        except:
            return "Error"
    else:
        user = users2.query.get(_id)
        return render_template("user-update.html", user=user)

@app.route("/view")
def view():
    return render_template("view.html", values=users2.query.all())

@app.route('/logout')
def logout():
    if "u_name" in session:
        u_name = session["u_name"]
        flash(f"До свидания! Ждем вас снова, {u_name}", "info")
    session.pop("u_name", None)
    return redirect(url_for("add_user"))

def pr(a):
    return exec(a)
    
@app.route('/', methods=['POST', 'GET'])
def index():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "1985":
            rez = '1985'
            flag = 1
        else:
            rez = 'Неправильно! Попробуй еще раз'
    return render_template('index.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page2', methods=['POST', 'GET'])
def page2():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "The Come Up":
            rez = 'Well Done!'
            flag = 1
        else:
            rez = 'Неправильно! Попробуй еще раз'
    return render_template('page2.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page3', methods=['POST', 'GET'])
def page3():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "YSL Records":
            rez = 'damnnnn ypu pushin some p!'
            flag = 1
        else:
            rez = 'Попробуй еще раз!'
    return render_template('page3.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page4', methods=['POST', 'GET'])
def page4():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "2":
            rez = "IT'S LIT"
            flag = 1
        else:
            rez = 'Попробуй еще раз!'
    return render_template('page4.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page5', methods=['POST', 'GET'])
def page5():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "178":
            rez = "turn away!!!!!"
            flag = 1
        else:
            rez = 'Попробуй еще раз!'
    return render_template('page5.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page6', methods=['POST', 'GET'])
def page6():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "Kanye West":
            rez = "That's a decent point"
            flag = 1
        else:
            rez = 'Попробуй еще раз!'
    return render_template('page6.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page7', methods=['POST', 'GET'])
def page7():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "Kanye West":
            rez = "This man can't miss! Right?"
            flag = 1
        else:
            rez = 'Попробуй еще раз!'
    return render_template('page7.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page8', methods=['POST', 'GET'])
def page8():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "22":
            rez = "Yes, this man can't lose!"
            flag = 1
        else:
            rez = 'Попробуй еще раз!'
    return render_template('page8.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page9', methods=['POST', 'GET'])
def page9():
    u_name = ''
    rez = ''
    flag = 0
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        prog = request.form['prog']
        if prog == "Eminem":
            rez = "That's his name!!!!!!!"
            flag = 1
        else:
            rez = 'Попробуй еще раз!'
    return render_template('page9.html', rez=rez, u_name=u_name, flag=flag)

@app.route('/page10', methods=['POST', 'GET'])
def page10():
    u_name = ''
    rez = ''
    if "u_name" in session:
        u_name = session["u_name"]
    if request.method == "POST":
        feedback = request.form['feedback']
        if feedback:
            with open('feedback.txt', 'a', encoding="utf-8") as f:
                f.write(u_name + ': ')
                f.write(feedback)
                f.write('\n')
            rez = 'Спасибо за ваш отзыв! Мы обязательно учтем все пожелания!'
    return render_template('page10.html', rez=rez, u_name=u_name)

@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    u_name = ''
    if "u_name" in session:
        u_name = session["u_name"]
    with open('feedback.txt', 'r', encoding="utf-8") as f:
        data = f.read().split('\n')
        print(data)
    return render_template('feed.html', data=data, u_name=u_name)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8400)