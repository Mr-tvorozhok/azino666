import sys
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

if __name__ == "__main__":
    id = sys.argv[1]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db/Story_win_locale{id}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Story_win_locale(db.Model):
    id_win = db.Column(db.Integer, primary_key=True)
    count_win = db.Column(db.Integer)
    date_time_win = db.Column(db.DateTime, default=datetime.utcnow)

    # pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"


def new_table():
    db.create_all()


def index():
    info = []
    try:
        info = Story_win_locale.query.all()
    except:
        print("Ошибка чтения из БД")
    print(info)


def new_write(list):
    # здесь должна быть проверка корректности введенных данных

    try:
        u = Story_win_locale(id_win=list[0], count_win=(int(list[1])),
                             date_time_win=datetime.now())
        db.session.add(u)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")


if __name__ == "__main__":
    act = sys.argv[2]
    print(act, id)
    if act == '1':
        print(11)
        new_table()
    elif act == '2':
        new_write(sys.argv[3:])
# запуск: python Act_Story_win_locale.py (id_user) 1 or 2 (arrg)
# 1- Создание новой базы данных(python .\Act_Table_User.py 2 1)
# 2 Добавление новой записи (python .\Act_Table_User.py 2 2 2121 21212)
