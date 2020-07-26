import datetime


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addUser(self, username, login, password_hash, registration_date):
        self.__cur.execute("INSERT INTO users (username, login, password_hash, registration_date) VALUES (?,?,?,?)", (username, login, password_hash, registration_date))
        self.__db.commit()

    def check_username(self, username):
        '''Повертає True якщо користувач з таким username існує в БД'''
        self.__cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        self.__cur.fetchone()
        if self.__cur.fetchone():
            return True
        else:
            return False

    def check_login(self, login):
        '''Повертає True якщо користувач з таким login існує в БД'''
        self.__cur.execute("SELECT * FROM users WHERE login = ?", (login,))
        self.__cur.fetchone()
        if self.__cur.fetchone():
            return True
        else:
            return False

    def getUser(self, user_id):
        self.__cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        res = self.__cur.fetchone()
        if not res:
            print('Користувач не знайдений')
            return False
        return res

    def getUserByLogin(self, login):
        self.__cur.execute("SELECT * FROM users WHERE login = ?", (login,))
        res = self.__cur.fetchone()
        if not res:
            print('Користувач не знайдений')
            return False
        return res

    def getAllPosts(self):
        self.__cur.execute("SELECT * FROM posts")
        res = self.__cur.fetchall()
        return res

    def getPost(self, post_id):
        self.__cur.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,))
        res = self.__cur.fetchone()
        return res

    def addPost(self, author_id, title, body, create_date=datetime.date.today()):
        self.__cur.execute("INSERT INTO posts (author_id, title, body, create_date) VALUES (?,?,?,?)", (author_id, title, body, create_date))
        self.__db.commit()

    def getPostsbyAuthorId(self, author_id):
        self.__cur.execute("SELECT * FROM posts WHERE author_id = ?", (author_id,))
        res = self.__cur.fetchall()
        return res