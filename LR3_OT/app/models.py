import os
from datetime import datetime

from flask import session
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import login, app

import psycopg2

class DataBase(object):
    _db_name = app.config['DB_NAME']
    _db_user = app.config['DB_USER']
    _user_password = app.config['USER_PASSWORD']
    _db_host = app.config['DB_HOST']
    _db_port = app.config['DB_PORT']

    _connection: psycopg2 = None

    @classmethod
    def _to_connect(cls):
        try:
            cls._connection = psycopg2.connect(
                database=cls._db_name,
                user=cls._db_user,
                password=cls._user_password,
                host=cls._db_host,
                port=cls._db_port,
            )
        except psycopg2.OperationalError as ex:
            print(f"{ex}")
        except Exception as ex:
            print(f'{ex}')
        else:
            print("connection is successful")
        return

    @classmethod
    def execute_query(cls, query: str, is_returning: bool = False):
        print(query)
        if cls._connection is None:
            cls._to_connect()
        cls._connection.autocommit = True
        cursor = cls._connection.cursor()
        try:
            cursor.execute(query)
            if is_returning:
                result = cursor.fetchall()
        except psycopg2.OperationalError as ex:
            print(f'{ex}')
        except Exception as ex:
            print(f'{ex}')
        else:
            print("the query is executed")
            if is_returning:
                return result
            else:
                return True
        finally:
            cursor.close()
        return None

#///////Книга/////////
class Book(object):
    def __init__(self, 
                id: int,
                author: str,
                book_name: str,
                image: str,
                genre: str):
        self.id = id
        self.author = author
        self.book_name = book_name
        self.image = image
        self.genre = genre

    def tuple(self):
        return (self.author, self.book_name, self.image, self.genre)
    
    #все книги
    @classmethod
    def get_all(cls):
        query = '''
        SELECT * FROM book'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    
    #все книги
    @classmethod
    def max_book(cls):
        query = '''
        SELECT COUNT(*) FROM book'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    
    #добавить новую книгу
    @classmethod
    def add(cls, book):
        query = '''
        INSERT INTO book (author, book_name, image, genre)
        VALUES {}'''.format(book.tuple())
        return DataBase.execute_query(query)


#///////ЧИТАТЕЛЬ//////////
class Reader(UserMixin):
    def __init__(self, 
                id: int,
                sn: str,
                email: str,
                password_hash: str = None):

        self.id = id
        self.sn = sn
        self.email = email
        self.password_hash = password_hash


    def tuple(self):
        return ( self.sn, self.email, self.password_hash)

    #поиск по ID
    @classmethod
    def get_by_id(cls, id: int):
        query = '''
        SELECT * FROM reader
        WHERE id = {}'''.format(id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Reader(* arguments)
    
    #поиск по адресу почты
    @classmethod
    def get_by_email(cls, email):
        query = '''
        SELECT * FROM reader
        WHERE email = '{}' '''.format(email)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Reader(* arguments)
    
    #добавить нового читателя
    @classmethod
    def add(cls, reader):
        query = '''
        INSERT INTO reader (sn, email, password_hash)
        VALUES {}'''.format(reader.tuple())
        return DataBase.execute_query(query)
    
    #все читатели
    @classmethod
    def get_all(cls):
        query = '''
        SELECT * FROM reader'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    #все книги
    @classmethod
    def max_reader(cls):
        query = '''
        SELECT COUNT(*) FROM reader'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    #выданные книги читателя
    @classmethod
    def get_book_of_reader(cls, id_reader):
        query = '''
        SELECT DISTINCT id, book_name, author, image, genre 
        FROM book
        INNER JOIN book_of_reader
        ON book.id = book_of_reader.id_book
        WHERE book_of_reader.id_reader = '{}' '''.format(id_reader)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    
    #получить ID читателей для формы
    @classmethod
    def get_id_choices(cls):
        query = '''
        SELECT id, id
        FROM reader'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
    

#///////КНИГА ЧИТАТЕЛЯ/////////
class Book_of_reader(object):
    def __init__(self, 
                id_reader: int,
                id_book: int,
                date_issue: datetime):
        self.id_reader = id_reader
        self.id_book = id_book
        self.date_issue = date_issue

    def tuple(self):
        return (self.id_reader, self.id_book, self.date_issue)
    
    #все книги
    @classmethod
    def get_all(cls):
        query = '''
        SELECT * FROM book_of_reader'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    
    #добавить новую книгу читателя
    @classmethod
    def add(cls, book_of_reader):
        query = '''
        INSERT INTO book_of_reader (id_reader, id_book, date_issue)
        VALUES {}'''.format(book_of_reader.tuple())
        return DataBase.execute_query(query)

    #проверка есть ли уже такая выданная книга у читателя
    @classmethod
    def have_that_book(cls, id_reader, id_book):
        query = '''
        SELECT *
        FROM book_of_reader
        WHERE id_reader = {} and id_book = {}
        '''.format(id_reader, id_book)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    
    #получить ID книг читателя для формы
    @classmethod
    def get_id_choices(cls, id_reader):
        query = '''
        SELECT id_book, id_book
        FROM book_of_reader
        WHERE id_reader = {}
        ORDER BY id_book'''.format(id_reader)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    
    #удалить (забрать) книгу читателя
    @classmethod
    def delete(cls, id_reader, id_book):
        query = '''
        DELETE FROM book_of_reader
        WHERE id_reader = {} and id_book = {}
        '''.format(id_reader, id_book)
        return DataBase.execute_query(query)

#///////Админ/////////
class Admin(UserMixin):
    def __init__(self, 
                id: int,
                sn: str,
                email: str,
                password_hash: str = None):
        self.id = id
        self.sn = sn
        self.email = email
        self.password_hash = password_hash

    def tuple(self):
        return (self.email, self.password_hash)

    #поиск по ID
    @classmethod
    def get_by_id(cls, id):
        query = '''
        SELECT * FROM reader
        WHERE id = 1 '''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Admin(* arguments)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)


#///////////////////////////////////
@login.user_loader
def load_user(id: str):
    if session['role'] == 'reader':
        user = Reader.get_by_id(int(id))

    elif session['role'] == 'admin':
        user = Admin.get_by_id(int(id))
        
    else:
        user = None
    print(f'user {user} loaded')
    return user