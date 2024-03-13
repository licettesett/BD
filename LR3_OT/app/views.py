import os

from flask import render_template, flash, redirect, url_for, request, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

import datetime

from app.forms import LoginForm, RegistrationForm, AddBookForm, AddReaderBook, DeleteReaderBook
from app.models import Reader, Admin, Book, Book_of_reader

from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#//////СПИСОК КНИГ//////
@app.route('/book_list', methods=['GET', 'POST'])
def book_list():
    books = Book.get_all()
    if books is None:
        books = ''

    return render_template('book_list.html', title = 'books', books = books)


#//////СПИСОК ЧИТАТЕЛЕЙ//////
@app.route('/reader_list', methods=['GET', 'POST'])
def reader_list():
    readers = Reader.get_all()
    if readers is None:
        readers = ''

    return render_template('reader_list.html', title = 'readers', readers = readers)

#///////////////////////////////////////////////////////////////////////
#////ПРОФИЛЬ ЧИТАТЕЛЯ/////
@app.route('/reader/<reader_id>')
@login_required
def reader_profile(reader_id):
    reader = Reader.get_by_id(reader_id)

    books = Reader.get_book_of_reader(reader_id)
    if books is None:
        books = ''
    print(books)
    
    return render_template('reader_profile.html', title='reader profile', 
    reader=reader, books = books)


#////ДОБАВИТЬ КНИГУ/////
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = AddBookForm()

    form.genre.choices = ['Роман', 'Рассказ', 'Новелла', 'Повесть', 'Стих', 'Сонет', 'Поэма', 'Хайку', 'Ода', 'Мелодрама', 'Трагикомедия', 'Трагедия', 'Комедия', 'Водевиль']

    if form.validate_on_submit():
        user = Book(0, form.author.data, form.book_name.data, form.image.data, form.genre.data)

        if not Book.add(user):
            abort(500)

        flash('Книга добавлена')

    return render_template('add_book.html', title='add book', form=form)


#////ВЫДАТЬ КНИГУ/////
@app.route('/add_reader_book', methods=['GET', 'POST'])
def add_reader_book():

    #выдать книгу
    form = AddReaderBook()

    if form.validate_on_submit():
        reader_id = form.reader_ID.data
        book_id = form.book_ID.data
        date_issue = form.date_issue.data

        print('DATA:', date_issue)

        issue_book = Book_of_reader(reader_id, book_id, str(date_issue))
        
        if (Book_of_reader.have_that_book(reader_id, book_id)) != None:
            flash('У читателя уже есть эта книга') 
        elif not Book_of_reader.add(issue_book):
            abort(500)
        else:
            flash('Читателю добавлена выданная книга')   

    return render_template('add_reader_book.html', title='add reader book', form=form)


#////ЗАБРАТЬ КНИГУ/////
@app.route('/reader/<reader_id>/delete_reader_book', methods=['GET', 'POST'])
def delete_reader_book(reader_id):

    #выдать книгу
    form = DeleteReaderBook()

    form.book_ID.choices = Book_of_reader.get_id_choices(reader_id)

    if form.validate_on_submit():
        book_id = form.book_ID.data
        if not Book_of_reader.delete(reader_id, book_id ):
            abort(500)
        else:
            flash('Книга удалена из выданных книг читателя')
            return redirect(url_for('reader_profile', reader_id=reader_id))   

    return render_template('delete_reader_book.html', title='delete reader book', form=form)


#////////////////////////////////////////////////////////////////////////////////
#ВОЙТИ В АККАУНТ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if not (form.is_reader.data or form.is_admin.data):
            flash('Выберите роль (отметить)')
            return redirect(url_for('login'))
        
        if (form.is_reader.data and form.is_admin.data):
            flash('Выберите только одну роль')
            return redirect(url_for('login'))
        
        if form.is_reader.data:
            # логинизация для читателя
            user = Reader.get_by_email(form.email.data)
            session['role'] = 'reader'
        
        if form.is_admin.data:
            # логинизация для Админа
            user = Reader.get_by_email(form.email.data)
            if user.email == 'admin@mail.ru':
                print('EMAIL:', user.email)
                session['role'] = 'admin'
            else:
                flash('Неверный email или пароль')
                return redirect(url_for('login'))

        if user is None or not user.check_password(form.password.data):
            flash('Неверный email или пароль')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='login', form=form)

#////ВЫЙТИ ИЗ АККАУНТА////
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['role'] = None
    return redirect(url_for('index'))

#////ЗАРЕГИСТРИРОВАТЬСЯ/////
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Reader(0, form.name.data, form.email.data)
        user.set_password(form.password.data)

        if not Reader.add(user):
            abort(500)

        flash('Вы успешно зарегистрировались')

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)