from getpass import getpass
import sys

from webapp import create_app
from webapp.models import db, User

app = create_app()

with app.app_context():
    username = input("Введите имя пользователя: ")

    if User.query.filter(User.username == username).count():
        print("Такой пользователь уже зарегистрирован")
        sys.exit(0)

    user_email = input("Введите email: ")
    if User.query.filter(User.email == user_email).count():
        print("Пользователь с таким email уже зарегистрирован")
        sys.exit(0)

    password1 = getpass("Введите пароль: ")
    password2 = getpass("Повторите пароль: ")
    if not password1 == password2:
        print("Пароли не совпадают")
        sys.exit(0)

    new_user = User(username=username, email=user_email, role="admin")
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print("Создан пользователь с id={}".format(new_user.id))
