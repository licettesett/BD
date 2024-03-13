INSERT INTO Reader (email, password_hash) VALUES
('admin@mail.ru','pbkdf2:sha256:260000$mjIFp8XjC47vFZaU$6502d2d216a45afbdbc3b7bb89e58df1b490eee33871543ecab98b3f78e8fc18');

INSERT INTO Book (author, book_name, genre, image) VALUES
('А.С. Грибоедов','"Горе от ума"', 'Комедия',
'https://img3.labirint.ru/rc/b0048ff25a08d14c7ed72660762812db/363x561q80/books60/591695/cover.png?1575448043'),

('А.С. Пушкин','"Капитанская дочка"', 'Роман',
'https://img4.labirint.ru/rc/4b2c8f582617d8d7465d6746c99180e4/363x561q80/books81/800560/cover.jpg?1618471547'),

('Ф.М. Достоевский','"Преступление и наказание"', 'Роман',
'https://book-cover.ru/sites/default/files/styles/osn_530x/public/field/image/dostoevskiy-prestuplenie-i-nakazanie.jpg?itok=oRvP308I'),

('Ф.М. Достоевский','"Идиот"', 'Роман',
'https://book-cover.ru/sites/default/files/styles/osn_530x/public/field/image/dostoevskiy-idiot-4.jpg?itok=bHGCpGc0'),

('М. Булгаков','"Мастер и Маргарита"', 'Роман',
'https://book-cover.ru/sites/default/files/styles/osn_530x/public/field/image/bulgakov-master-i-margarita.jpg?itok=sWDsInBY'),

('Уильям Шекспир','"Макбет"', 'Трагедия',
'https://img3.labirint.ru/rc/a244cccbcff227762190887fc89cca5d/363x561q80/books63/623275/cover.png?1575390445'),

('Уильям Шекспир','"Ромео и Джульетта"', 'Трагедия',
'https://book-cover.ru/sites/default/files/styles/osn_530x/public/field/image/shekspir-romeo-i-djuljetta.jpg?itok=D5oXRQ4G'),

('Уильям Шекспир','"Гамлет"', 'Трагедия',
'https://img3.labirint.ru/rc/c050d2ffa2c9ccb9321131e9c84a3dfa/363x561q80/books59/587569/cover.png?1575447954'),

('Евгений Замятин','"Мы"', 'Роман',
'https://book-cover.ru/sites/default/files/styles/osn_530x/public/field/image/zamyatin-mi.jpg?itok=9cyS1ZbA'),

('Рэй Брэдбери','"451 градус по Фаренгейту"', 'Роман',
'https://book-cover.ru/sites/default/files/styles/osn_530x/public/field/image/bredberi-451-gradus-po-farengeytu-2.jpg?itok=KyfvhPHT'),

('Уильям Шекспир','"Укрощение строптивой"', 'Комедия',
'https://img3.labirint.ru/rc/3ed6e78acde9669055173a36af61b8ca/363x561q80/books81/803851/cover.jpg?1620365141'),

('Уильям Шекспир','"Отелло"', 'Трагедия', 
'https://img3.labirint.ru/rc/80241d7c4717b3bf7452bceb8a147e98/363x561q80/books48/474421/cover.jpg?1563806894');

--https://img4.labirint.ru/rc/0d7106bb99a6b71c15016194066f5fc0/363x561q80/books98/972396/cover.jpg?1694021196 #кафка превращение

-- UPDATE book
-- set image = 'https://img3.labirint.ru/rc/a244cccbcff227762190887fc89cca5d/363x561q80/books63/623275/cover.png?1575390445'
-- where id = 6

-- INSERT INTO book_of_reader (id_reader, id_book) VALUES
-- (2,1),
-- (2,2),
-- (2,3),
-- (2,4),
-- (2,5),
-- (3,1),
-- (3,5),
-- (3,6),
-- (3,7),
-- (3,8);
