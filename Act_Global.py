import datetime
import logging
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db/basedata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
logging.basicConfig(filename="log/basedate.log", level=logging.INFO)


class Info_User(db.Model):
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


db.create_all()


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
            print(i.user_name)
            if i.user_name == ID:
                return False
        return True



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
                      f'Параметры {act, param, list}')
        db.session.rollback()
        print("Ошибка добавления в БД")


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