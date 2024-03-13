from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, number_range

from app.models import Reader, Admin, Book

#/////ЛОГИН///////
class LoginForm(FlaskForm):
    email = EmailField('Email адрес', validators=[DataRequired(), Email()])
    is_reader = BooleanField('Читатель')
    is_admin = BooleanField('Админ')
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('запомнить')
    submit = SubmitField('| ВОЙТИ |')


#/////РЕГИСТРАЦИЯ///////
class RegistrationForm(FlaskForm):
    email = StringField('Email адрес', validators=[DataRequired(), Email()])
    name = StringField('Ваше имя', validators=[DataRequired()])

    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('| ПОДТВЕРДИТЬ |')

    def validate_email(self, email):
        user = Reader.get_by_email(email.data)
        if user is not None:
            raise ValidationError('используйте другой email')
        
#//////ДОБАВИТЬ КНИГУ///////
class AddBookForm(FlaskForm):
    author = StringField('Введите инициалы и фамилию автора')
    book_name = StringField('Введите название книги в кавычках')
    image = StringField('Вставьте ссылку на изображение')

    genre = SelectField('Выберите жанр')
    submit = SubmitField('| Добавить книгу |')

    def validate_author(self, author):
        if author.data == '':
            raise ValidationError('Введите автора')
        else:
            return
        
    def validate_genre(self, genre):
        if genre.data == '':
            raise ValidationError('Выберите жанр произведения')
        else:
            return
        
    def validate_image(self, image):
        if image.data == '':
            raise ValidationError('Вставьте ссылку на изображение')
        else:
            return
        
    def validate_book_name(self, book_name):
        if book_name.data == '':
            raise ValidationError('Введите название произведения')
        elif len(book_name.data) > 50:
            raise ValidationError('Превышено количество символов в названии (макс: 50)')
        else:
            return
        


#//////ОБНОВИТЬ ИНФОРМАЦИЮ КНИГИ///////
class UpdateBook(FlaskForm):
    ID = SelectField('Выберите номер книги из списка')

    author = StringField('Введите инициалы и фамилию автора')
    book_name = StringField('Введите название книги в кавычках')
    image = StringField('Вставьте ссылку на изображение')

    genre = SelectField('Выберите жанр')
    submit = SubmitField('| Изменить информацию книги |')


#//////ЗАДАТЬ ВЫДАННУЮ КНИГУ ЧИТАТЕЛЮ///////
class AddReaderBook(FlaskForm):
    max_reader = Reader.max_reader()
    max_book = Book.max_book()

    print('MAXBOOK:_____________________________',max_book[0][0])

    reader_ID = IntegerField('Введите номер читателя из списка', validators=[DataRequired(), number_range(min=2, max=max_reader[0][0])])
    book_ID = IntegerField('Введите номер книги из списка', validators=[DataRequired(), number_range(min=1, max=max_book[0][0])])
    date_issue = DateField('Задайте дату выдачи книги')

    submit = SubmitField('| Задать выданную книгу |')

#//////УДАЛИТЬ КНИГУ ЧИТАТЕЛЯ///////
class DeleteReaderBook(FlaskForm):
    book_ID = SelectField('Выберите номер книги (ID книги читателя)')

    submit = SubmitField('| Убрать книгу читателя |')