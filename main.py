import datetime
import logging
import os
import sys

from flask import Flask, request, render_template, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'icons'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db/basedata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
secret_key = ['h\x93\x14\x9fu\xdb\x08\xddk\xdaS\x8b']
login_manager = LoginManager(app)
logging.basicConfig(filename="log/basedate.log", level=logging.INFO)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager.login_view = 'login'


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS, \
           filename.rsplit('.', 1)[1].lower()


class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = index_global(8, user_id)
        return self

    def create(self, user):
        self.__user = index_global(8, index_global(6, user))
        return self

    def get_id(self):
        return str(self.__user.id)


class Info_User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    count = db.Column(db.Integer)
    icon = db.Column(db.String(100))

    # pr = db.relationship('Profiles', backref='users', uselist=False)
    def qw(self):
        print(self.id)

    def __repr__(self):
        return f"<users {self.id}>"


class Story_win_global(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_user = db.Column(db.Integer, unique=True)
    count = db.Column(db.Integer)
    icon = db.Column(db.String(100))
    date_time_win = db.Column(db.DateTime, default=datetime.datetime.now())


class User_loser(db.Model):
    place = db.Column(db.Integer, primary_key=True, unique=True)
    id_user = db.Column(db.Integer, unique=True)
    count = db.Column(db.Integer)
    icon = db.Column(db.String(100))


def index_global(param, ID, list=[]):
    if len(list) != 0:
        logging.warning(f'Внимание! Неправильно передана команда запуска кода\n'
                        'При чтений базы данных кросе номера таблицы и ID писать ничего не надо')
    if param == '1':
        info = Info_User.query.get(ID)
        return info.id, info.user_name, info.password, info.email, info.count, info.icon
        # info = Info_User.query.all()
    elif param == '2':
        info = Story_win_global.query.get(ID)
        return info.id, info.id_user, info.count, info.icon, info.date_time_win
    elif param == '3':
        info = User_loser.query.get(ID)
        return info.place, info.id_user, info.count, info.icon
    elif param == '4':
        for i in Info_User.query.all():
            if i.user_name == ID:
                return True
        return False
    elif param == 5:
        for i in Info_User.query.all():
            if i.email == ID:
                return True
        return False
    elif param == 7:
        return (Info_User.query.filter_by(user_name=ID).first()).password
    elif param == 6:
        try:
            return (Info_User.query.filter_by(user_name=ID).first()).id
        except:
            return None
    elif param == 8:
        return Info_User.query.get(ID)


def new_write(param, list):
    # здесь должна быть проверка корректности введенных данных
    try:
        if param == '1':
            u = Info_User(id=list[0], user_name=list[1],
                          password=list[2], email=list[3],
                          count=list[4], icon=list[5])
        elif param == '2':
            u = Story_win_global(id=list[0], id_user=list[1],
                                 count=list[2], icon=list[3],
                                 date_time_win=datetime.datetime.now())

        elif param == '3':
            u = User_loser(place=list[0], id_user=list[1],
                           count=list[2], icon=list[3])
        elif param == 4:
            b = index_global(8, list[0])
            try:
                db.session.delete(b)
                db.session.flush()
                db.session.commit()
            except:
                logging.error('Удаление пошло не поплану'
                              f'параметры:{param}{list}')
            u = Info_User(id=list[1], user_name=list[2],
                          password=list[3], email=list[4],
                          count=list[5], icon=list[6])
        else:
            raise FloatingPointError
        db.session.add(u)
        db.session.flush()
        db.session.commit()
    except FloatingPointError:
        logging.error(f'Error 12 not True argument param = {param}!!!')
        print('Типо ошибка, хихи')
    except:
        logging.error(f'Error 11 Ошибка При добавлений данных в базу данных\n'
                      f'Параметры {param, list}')
        db.session.rollback()
        print("Ошибка добавления в БД")


@login_manager.user_loader
def load_user(user_id):
    return Info_User.query.get(user_id)


if __name__ == "__main__":
    try:
        act = sys.argv[1]
        if act == '1':
            index_global(sys.argv[2], sys.argv[3], sys.argv[4:])
        elif act == '2':
            new_write(sys.argv[2], sys.argv[3:])
        else:
            logging.error(f'Error 12 not True argument act = {act}!!!')
    except:
        pass


# end
@app.route('/')
def a():
    return 'b'


@app.route('/login', methods=["POST", "GET"])
def login():
    dictt = {"name": "", "email": "", "password": "", "password2": "", 'error_main': '0'}

    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        dictt = {"name": name, "password": password, 'error_main': '0'}
        if len(name) == 0:
            dictt['error_class1'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Кто ты?'
        elif len(password) == 0:
            dictt['error_class2'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Введите пароль'
        elif index_global('4', name):
            if index_global(7, name) == password:
                user_login = UserLogin().create(name)
                login_user(user_login)
                return redirect(url_for('rename'))
            else:
                dictt['error_class2'] = "is-invalid"
                dictt['error_main'] = '1'
                dictt['error_info'] = 'Дед, пароль не тот, ты что забыл?'
        elif not index_global('4', name):
            dictt['error_class1'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Его тут не было, от слово совсем'
        elif len(password) == 0:
            dictt['error_class2'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Введите пароль'
    return render_template("login.html", **dictt)


@app.route('/rename')
@login_required
def rename():
    a = current_user
    dictt = {"name": a.user_name, "email": "", "password": a.password, "password2": "", 'error_main': '0'}
    icon_true = True
    print(request.method == "POST")
    print(16)

    if request.method == "POST":
        print(1212121)
        name = request.form['name']
        password = request.form['password']
        password1 = request.form['passwordone']
        email1 = request.form['email']
        '''print('icon' in request.files, request.files)
        if 'icon' not in request.files:
            print(1212121212)
            file = request.files['icon']
            if file.filename != '':
                print(1)
                a = allowed_file(secure_filename(file.filename))
                if file and a[0]:
                    filename = a[1]
                    print(filename)
                    with open('db/ID.txt', mode='r', encoding='utf-8') as ID:
                        id1 = int(ID.read())
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(id1) + f'.jpg'))
                else:
                    dictt['error_main'] = '1'
                    dictt['error_info'] = 'Ты че, вирус кинул? строго только png jpg jpeg gif'
                    icon_true = False'''
        dictt = {"name": name, "email": email1, "password": password, "password2": password1, 'error_main': '0'}
        if len(name) == 0:
            dictt['error_class1'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Неа'
        elif index_global('4', name):
            dictt['error_class1'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Тебе лутше выбрать СВОЕ имя'
        elif len(password) == 0:
            dictt['error_class2'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'ТЫ что, хочешь чтоб тебя взломали?'
        elif len(password1) == 0:
            dictt['error_class3'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Введите пароль еще раз, вдруг вы альцгеймер?))'
        elif password1 != password:
            dictt['error_class3'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Дед, пароль не совпадает'
        elif len(email1) == 0:
            dictt['error_class4'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Почту нужно ввести чтобы мы удостоверили что это Вы'
        elif index_global(5, email1):
            dictt['error_class4'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Про эту почту мы впервые видим'
        elif a.email != email1:
            dictt['error_class4'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Это не твоя почта'
        elif icon_true:
            new_write(4, [a.id, name, password, a.email, a.count, a.icon])
            dictt['error_class4'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'все ок'
    print(12121212)
    return render_template("rename.html", **dictt)


'''
@app.route('/login/', methods=['post', 'get'])
def login():
    form = LoginForm()

    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        True_password = False
        if index_global('4', name):
            try:
                temp = index_global(7, name)
            except:
                temp = None
            if temp == password:
                True_password = True




        form = LoginForm()
        if True_password:
            # Login and validate the user.
            # user should be an instance of your `User` class
            login_user(user)

            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))
        return flask.render_template('login.html', form=form)
#...
'''


@app.route('/registred', methods=["POST", "GET"])
def registred():
    dictt = {"name": "", "email": "", "password": "", "password2": "", 'error_main': '0'}
    icon_true = True
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        password1 = request.form['passwordone']
        email1 = request.form['email']
        '''print('icon' in request.files, request.files)
        if 'icon' not in request.files:
            print(1212121212)
            file = request.files['icon']
            if file.filename != '':
                print(1)
                a = allowed_file(secure_filename(file.filename))
                if file and a[0]:
                    filename = a[1]
                    print(filename)
                    with open('db/ID.txt', mode='r', encoding='utf-8') as ID:
                        id1 = int(ID.read())
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(id1) + f'.jpg'))
                else:
                    dictt['error_main'] = '1'
                    dictt['error_info'] = 'Ты че, вирус кинул? строго только png jpg jpeg gif'
                    icon_true = False'''

        dictt = {"name": name, "email": email1, "password": password, "password2": password1, 'error_main': '0'}
        if len(name) == 0:
            dictt['error_class1'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Кто ты?'
        elif index_global('4', name):
            dictt['error_class1'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Такой пользователь уже существует, сори)'
        elif len(password) == 0:
            dictt['error_class2'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Введите пароль'
        elif len(password1) == 0:
            dictt['error_class3'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Введите пароль еще раз, вдруг вы альцгеймер?))'
        elif password1 != password:
            dictt['error_class3'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Пароли не совпадают'
        elif len(email1) == 0:
            dictt['error_class4'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Введите почту, чтлб мы вам высылали спам)))))'
        elif index_global(5, email1):
            dictt['error_class4'] = "is-invalid"
            dictt['error_main'] = '1'
            dictt['error_info'] = 'Эта почта уже заражена, выберите другую)'
        elif icon_true:
            with open('db/ID.txt', mode='r', encoding='utf-8') as ID:
                id1 = int(ID.read())
            with open('db/ID.txt', 'w', encoding='utf-8') as ID:
                ID.write(str(id1 + 1))
            new_write('1', [id1, name, password, email1, 500, 'no'])
    return render_template("registred.html", **dictt)
    # with open(, 'r', encoding="utf-8") as html_stream:
    # html = html_stream.read()

    # for replace in dictt:
    # html = html.replace(f'{{{{ {replace} }}}}', dictt[replace])


if __name__ == '__main__':
    app.run(host='127.0.0.1')
