import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ServerDatabase:
    Base = declarative_base()

    class Users(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        login = Column(String(255), unique=True)
        password = Column(String(255))
        login_at = Column(DateTime)

        def __init__(self, login, password):
            self.id = None
            self.login = login
            self.password = password
            self.login_at = datetime.datetime.now()

    class ActiveUsers(Base):
        __tablename__ = 'users_active'
        id = Column(Integer, primary_key=True)
        login = Column(String(255), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
        ip = Column(String(255))
        port = Column(Integer)
        login_at = Column(DateTime)

        def __init__(self, login, ip, port, login_at):
            self.id = None
            self.login = login
            self.ip = ip
            self.port = port
            self.login_at = login_at

    class HistoryUsers(Base):
        __tablename__ = 'users_history'
        id = Column(Integer, primary_key=True)
        login = Column(String(255), ForeignKey('users.id', ondelete='CASCADE'))
        ip = Column(String(255))
        port = Column(Integer)
        login_at = Column(DateTime)

        def __init__(self, login, ip, port, login_at):
            self.id = None
            self.login = login
            self.ip = ip
            self.port = port
            self.login_at = login_at

    def __init__(self):
        """
        Задаём СУБД для базы, инициализируем создание таблиц в базе и открываем сессию взаимодействия с ней
        """
        self.engine_database = create_engine('sqlite:///:memory:', echo=False, pool_recycle=7200)

        self.Base.metadata.create_all(self.engine_database)

        Session = sessionmaker(bind=self.engine_database)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, login, password, ip, port):
        """
        Регистрация входа пользователя

        :param login:
        :param password:
        :param ip:
        :param port:
        """
        user_query = self.session.query(self.Users).filter_by(login=login).first()

        if user_query is not None:
            user = user_query
            user.login_at = datetime.datetime.now()
        else:
            user = self.Users(login, password)

            self.session.add(user)
            self.session.commit()

        active_user = self.ActiveUsers(user.id, ip, port, user.login_at)
        history_mark = self.HistoryUsers(user.id, ip, port, user.login_at)

        self.session.add_all([active_user, history_mark])
        self.session.commit()

    def user_logout(self, login):
        """
        Регистрация выхода пользователя

        :param login:
        """
        user = self.session.query(self.Users).filter_by(login=login).first()

        self.session.query(self.ActiveUsers).filter_by(id=user.id).delete()
        self.session.commit()

    def users_list(self):
        """
        Получение списка всех пользователей

        :return:
        """
        query = self.session.query(
            self.Users.login,
            self.Users.login_at,
        )

        return query.all()

    def active_users_list(self):
        """
        Получение списка активных пользователей

        :return:
        """
        query = self.session.query(
            self.Users.login,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.login_at
            ).join(self.Users)

        return query.all()

    def users_history(self, login=None):
        """
        Получение всей истории регистрации или только конкретного юзера

        :param login:
        :return:
        """
        query = self.session.query(
            self.Users.login,
            self.HistoryUsers.ip,
            self.HistoryUsers.port,
            self.HistoryUsers.login_at
           ).join(self.Users)

        if login:
            query = query.filter(self.Users.login == login)

        return query.all()


if __name__ == '__main__':
    database = ServerDatabase()

    print('Проверяем функцию логина и активных пользователей...')
    database.user_login('client_1', 'asd', '192.168.1.4', 8888)
    database.user_login('client_2', 'zxc', '192.168.1.5', 7777)
    print('Должно быть 2 клиента: ', database.active_users_list())

    print('Проверяем функцию разлогина...')
    database.user_logout('client_1')
    print('Должен быть удалён первый клиент и остаться второй: ', database.active_users_list())

    print('Проверяем функцию истории посещений...')
    database.user_login('client_1', 'asd', '192.168.1.4', 8888)
    database.user_logout('client_1')
    print('Должны быть 2 посещения первым клиентом: ', database.users_history('client_1'))

    print('Проверяем функцию получения всех юзеров...')
    print('Должно быть всего 2 юзера: ', database.users_list())
