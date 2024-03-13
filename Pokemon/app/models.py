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

#///////ТРЕНЕР//////////
class Trainer(UserMixin):
    def __init__(self, 
                id: int,
                trainer_name: str,
                email: str,
                fav_pokemon: str,
                biography: str,
                password_hash: str = None,
                in_battle: bool = False):

        self.id = id
        self.trainer_name = trainer_name
        self.email = email
        self.fav_pokemon = fav_pokemon
        self.biography = biography
        self.password_hash = password_hash

        self.in_battle = in_battle


    def tuple(self):
        return ( self.trainer_name, self.email, self.fav_pokemon, 
                self.biography, self.password_hash, self.in_battle)

    @classmethod
    def get_all(cls):
        query = '''
        SELECT *
        FROM trainer
        ORDER BY id'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    @classmethod
    def get_by_id(cls, id: int):
        query = '''
        SELECT * FROM trainer
        WHERE id = {}'''.format(id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Trainer(* arguments)


    @classmethod
    def get_by_email(cls, email):
        query = '''
        SELECT * FROM trainer
        WHERE email = '{}' '''.format(email)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Trainer(* arguments)
    
    
    @classmethod
    def get_by_kind(cls, pokemon):
        query = '''
        SELECT kind_name FROM pokemon_kind
        WHERE kind_name = '{}' '''.format(pokemon)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return arguments

    @classmethod
    def count(cls):
        query = '''
        SELECT COUNT (*)
        FROM Trainer'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result


    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def add(cls, trainer):
        query = '''
        INSERT INTO trainer (trainer_name, email, fav_pokemon, biography, password_hash, in_battle)
        VALUES {}'''.format(trainer.tuple())
        return DataBase.execute_query(query)

    @classmethod
    def get_id_id(cls):
        query = '''
        SELECT id, id
        FROM trainer
        ORDER BY id'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result


    @classmethod
    def update_trainer(cls, in_battle, trainer_id):
        query = '''
        UPDATE trainer 
        SET in_battle = {}
        WHERE id = '{}' '''.format(in_battle, trainer_id)
        return DataBase.execute_query(query)

#//////ЗРИТЕЛЬ////////
class Spectator(UserMixin):
    def __init__(self, 
                id: int,
                id_fav: int,
                email: str,
                password_hash: str = None):
        self.id = id

        self.id_fav = id_fav

        self.email = email
        self.password_hash = password_hash

        self.fav = None

    def tuple(self):
        return (self.email, self.password_hash)

    @classmethod
    def get_all(cls):
        query = '''
        SELECT *
        FROM spectator
        ORDER BY id'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    @classmethod
    def get_by_id(cls, id: int):
        query = '''
        SELECT * FROM spectator
        WHERE id = {}'''.format(id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Spectator(* arguments)

    @classmethod
    def get_by_email(cls, email):
        query = '''
        SELECT * FROM spectator
        WHERE email = '{}' '''.format(email)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Spectator(* arguments)


    @classmethod
    def update_fav(cls, spectator):
        query = '''
        UPDATE spectator
        SET id_fav = {}
        WHERE id = '{}' '''.format(spectator.id_fav, spectator.id)
        return DataBase.execute_query(query)

    @classmethod
    def get_name_by_id_fav(cls, id_fav):
        query = '''
        SELECT * FROM trainer
        WHERE id = {} '''.format(id_fav)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result


    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def add(cls, spectator):
        query = '''
        INSERT INTO spectator (email, password_hash)
        VALUES {}'''.format(spectator.tuple())
        return DataBase.execute_query(query)


#///////ПОКЕМОН/////////
class Pokemon_of_trainer(object):
    def __init__(self,
                 id_kind: int,
                 id_trainer: int,
                 id: int):
        self.id_kind = id_kind
        self.id_trainer = id_trainer

        self.id = id

        self.kind = None
        self.trainer = None

    def tuple(self):
        return (self.id_kind,
                self.id_trainer)

    @classmethod
    def add(cls, pokemon_of_trainer):
        query = '''
        INSERT INTO pokemon_of_trainer (id_kind, id_trainer)
        VALUES {}'''.format(pokemon_of_trainer.tuple())
        return DataBase.execute_query(query)


    @classmethod
    def get_by_id(cls, id: int):
        query = '''
        SELECT * FROM pokemon_of_trainer
        WHERE id = {}'''.format(id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Pokemon_of_trainer(* arguments)

    @classmethod
    def get_kind_by_trainer_id(cls, id_trainer: int):
        query = '''
        SELECT DISTINCT kind_name, descr, image, "Type" 
        FROM pokemon_kind
        INNER JOIN pokemon_of_trainer 
        ON pokemon_kind.id = pokemon_of_trainer.id_kind
        WHERE pokemon_of_trainer.id_trainer = {}'''.format(id_trainer)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    #Получить ID и названия видов покемонов, которые есть у тренера
    #(выборы для SelectField)
    @classmethod
    def get_choises(cls, id_trainer: int):
        query = '''
        SELECT DISTINCT pokemon_of_trainer.id, kind_name 
        FROM pokemon_kind
        INNER JOIN pokemon_of_trainer 
        ON pokemon_kind.id = pokemon_of_trainer.id_kind
        WHERE pokemon_of_trainer.id_trainer = {}'''.format(id_trainer)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    
    #получить названия видов по айди тренера
    #(какие виды покемонов есть у тренера)
    @classmethod
    def get_kind_name_by_trainer_id(cls, id_trainer: int):
        query = '''
        SELECT DISTINCT kind_name
        FROM pokemon_kind
        INNER JOIN pokemon_of_trainer 
        ON pokemon_kind.id = pokemon_of_trainer.id_kind
        WHERE pokemon_of_trainer.id_trainer = {}'''.format(id_trainer)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    #получить название вида покемона по его айди
    @classmethod
    def get_kind_name_by_id(cls, id_pokemon):
        query = '''
        SELECT kind_name FROM pokemon_kind
        WHERE id = {}'''.format(id_pokemon)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result[0]
    
    #получить данные вида покемона по его айди
    @classmethod
    def get_db_kind_name_by_id(cls, id_pokemon):
        query = '''
        SELECT kind_name, descr, image, "Type" FROM pokemon_kind
        WHERE id = {}'''.format(id_pokemon)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result[0]

    @classmethod
    def have_such_pokemon(cls, id_pokemon, id_trainer):
        query = '''
        SELECT id_kind, kind_name FROM pokemon_kind
        INNER JOIN pokemon_of_trainer
        ON pokemon_kind.id = pokemon_of_trainer.id_kind
        WHERE id_kind = {} and id_trainer = {}'''.format(id_pokemon, id_trainer)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    
    @classmethod
    def get_id_by_kind_name(cls, kind):
        query = '''
        SELECT * FROM pokemon_kind
        WHERE kind_name = '{}' '''.format(kind)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Pokemon_kind(* arguments)


    @classmethod
    def update_pokemon_of_trainer(cls, pokemon):
        query = '''
        UPDATE pokemon_of_trainer
        SET id_kind = {}, id_trainer = {}
        WHERE id = {} '''.format(pokemon.id_kind, pokemon.id_trainer, pokemon.id)

        return DataBase.execute_query(query) 


#//////ПОКЕМОН (ВИД)////////
class Pokemon_kind(object):
    def __init__(self,
                 kind_name: str,
                 id: int,
                 descr: str,
                 image: str,
                 type: str):
        self.kind_name = kind_name
        self.id = id
        self.descr = descr
        self.image = image
        self.type = type
        
    @classmethod
    def get_all(cls):
        query = '''
        SELECT id, kind_name
        FROM pokemon_kind'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result


    @classmethod
    def get_all_all(cls):
        query = '''
        SELECT *
        FROM pokemon_kind'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
        

    @classmethod
    def get_by_id(cls, id: int):
        query = '''
        SELECT * FROM pokemon_kind
        WHERE id = {}'''.format(id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Pokemon_kind(* arguments)



#///////ПОКЕМОН В БИТВЕ/////////
class Pokemon_in_battle(object):
    def __init__(self,
                 id_pokemon: int,
                 id_battle: int):
        self.id_pokemon = id_pokemon
        self.id_battle = id_battle

        self.pokemon = None
        self.battlefield = None

    def tuple(self):
        return (self.id_pokemon,
                self.id_battle)

    
    @classmethod
    def add(cls, pokemon_in_battle):
        query = '''
        INSERT INTO pokemon_in_battle (id_pokemon, id_battle)
        VALUES {}'''.format(pokemon_in_battle.tuple())
        return DataBase.execute_query(query)

    
    #получить строки с покемонами в конкретной битве у тренера
    #(существуют ли они вообще)
    #(для проверки, заполнил ли тренер конкретное приглашение)
    @classmethod
    def have_pok_in_battle(cls, id_battle, id_trainer: int):
        query = '''
    SELECT *
    FROM pokemon_of_trainer
    WHERE id =
        (SELECT id_pokemon
        FROM pokemon_in_battle
        INNER JOIN pokemon_of_trainer
        ON pokemon_in_battle.id_pokemon = pokemon_of_trainer.id
        WHERE pokemon_in_battle.id_battle = {} 
        and pokemon_of_trainer.id_trainer = {} LIMIT 1)
    and id_trainer = {} '''.format(id_battle, id_trainer, id_trainer)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    #получить айди покемонов тренера в битве
    @classmethod
    def get_id_battle_pokemon(cls, id_trainer: int, id_battle):
        query = '''
        SELECT id_kind
        FROM pokemon_of_trainer
        INNER JOIN pokemon_in_battle
        ON pokemon_of_trainer.id = pokemon_in_battle.id_pokemon
        WHERE pokemon_of_trainer.id_trainer = {}
        and pokemon_in_battle.id_battle = {}'''.format(id_trainer, id_battle)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result



#///////ПОКЕМОН В БИТВЕ/////////
class Trainer_in_battle(object):
    def __init__(self,
                 id_trainer: int,
                 id_battle: int):
        self.id_trainer = id_trainer
        self.id_battle = id_battle

    def tuple(self):
        return (self.id_trainer,
                self.id_battle)

    
    @classmethod
    def add(cls, trainer):
        query = '''
        INSERT INTO trainer_in_battle (id_trainer, id_battle)
        VALUES {}'''.format(trainer.tuple())
        return DataBase.execute_query(query)

    #подсчет количества приглашений на битвы (всего битв)
    @classmethod
    def count_of_invitations(cls, id):
        query = '''
        SELECT COUNT (*)
        FROM trainer_in_battle
        WHERE id_trainer = {}'''.format(id)
        result = DataBase.execute_query(query, True)
        return result

    #подсчет завершенных битв
    @classmethod
    def count_of_finished(cls, id):
        query = '''
        SELECT COUNT (*)
        FROM trainer_in_battle
        INNER JOIN battle
        ON battle.id = trainer_in_battle.id_battle
        WHERE trainer_in_battle.id_trainer = {}
        and battle.result != '' '''.format(id)
        result = DataBase.execute_query(query, True)
        return result

    #получить ID тренера по ID битвы
    #(тренеров участвующих в этой битве)
    @classmethod
    def get_id_trainer(cls, id_battle: int):
        query = '''
        SELECT id_trainer
        FROM trainer_in_battle
        WHERE id_battle = {}'''.format(id_battle)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    #получить ID тренеров по ID битвы для формы
    #(тренеров участвующих в этой битве)
    @classmethod
    def get_id_trainer_choices(cls, id_battle: int):
        query = '''
        SELECT id_trainer, id_trainer
        FROM trainer_in_battle
        WHERE id_battle = {}'''.format(id_battle)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    
    #получить ID битвы по ID тренера
    #которая не завершена
    @classmethod
    def get_battle_id(cls, id_trainer: int):
        query = '''
        SELECT DISTINCT id_trainer, id_battle
        FROM trainer_in_battle
        INNER JOIN battle
        ON battle.id = trainer_in_battle.id_battle
        WHERE trainer_in_battle.id_trainer = {}
        and battle.result = '' '''.format(id_trainer)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Trainer_in_battle(* arguments)
   
   #Получить битвы без результата (еще не прошедшие)
    @classmethod
    def get_battle(cls, id_battle: int, tr_id: int):
        query = '''
        SELECT DISTINCT date_time, result, id, id_battlefield, id_trainer
        FROM battle
        INNER JOIN trainer_in_battle
        ON battle.id = trainer_in_battle.id_battle
        WHERE trainer_in_battle.id_battle = {} 
        and trainer_in_battle.id_trainer != {} 
        and battle.result = '' '''.format(id_battle, tr_id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

   #Получить битвы с результатом (уже законченные)
    @classmethod
    def get_battle_with_result(cls, id_battle: int, tr_id: int):
        query = '''
        SELECT DISTINCT date_time, result, id, id_battlefield, id_trainer
        FROM battle
        INNER JOIN trainer_in_battle
        ON battle.id = trainer_in_battle.id_battle
        WHERE trainer_in_battle.id_battle = {} 
        and trainer_in_battle.id_trainer != {} 
        and battle.result != '' '''.format(id_battle, tr_id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

#///////БИТВА////////
class Battle(object):
    def __init__(self,
                 date_time: str,
                 result: str,
                 id: int,
                 id_battlefield: int):
        self.date_time = date_time
        self.result = result
        self.id = id
        self.id_battlefield = id_battlefield

        self.battlefield = None
        
    def tuple(self):
        return ( self.date_time, self.result, self.id_battlefield)
    
    
    @classmethod 
    def get_all_id(cls):
        query = '''
        SELECT id
        FROM battle
        WHERE result ='' '''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result


    @classmethod
    def get_by_id(cls, id: int):
        query = '''
        SELECT * FROM battle
        WHERE id = {}'''.format(id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Battle(* arguments)

    #Получить строку битвы по времени и месту битвы,
    #а также проверка на ввод даты и времени (чтобы не повторялись)
    @classmethod 
    def get_id_battle(cls, date_time, id_battlefield):
        query = '''
        SELECT * FROM battle
        WHERE date_time = '{}' and id_battlefield = {}'''.format(date_time, id_battlefield)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Battle(* arguments)


    #получить все айди незавершенных битв
    @classmethod 
    def get_un_id(cls):
        query = '''
        SELECT id FROM battle
        WHERE result = '' '''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    #получить все айди завершенных битв
    @classmethod 
    def get_fin_id(cls):
        query = '''
        SELECT id FROM battle
        WHERE result != '' '''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result


    #добавить битву в БД
    @classmethod
    def add(cls, battle):
        query = '''
        INSERT INTO battle (date_time, result, id_battlefield)
        VALUES {}'''.format(battle.tuple())
        return DataBase.execute_query(query) 

    #проверка на ввод даты и времени (чтобы не повторялись)
    @classmethod 
    def get_check_date(cls, date_time, id_battlefield):
        query = '''
        SELECT * FROM battle
        WHERE date_time = '{}' 
        and id_battlefield = {}
        and id = {}'''.format(date_time, id_battlefield)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    #обновить результат битвы
    @classmethod
    def update_battle_result(cls, result, id_battle):
        query = '''
        UPDATE battle
        SET result = '{}'
        WHERE id = {} '''.format(result, id_battle)
        return DataBase.execute_query(query)  

    #есть ли по этой битве результат
    @classmethod 
    def have_result(cls, id_battle):
        query = '''
        SELECT * FROM battle
        WHERE result != ''
        and id = {}'''.format(id_battle)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    

#///////МЕСТО БИТВЫ////////
class Battlefield(object):
    def __init__(self,
                 adress: str,
                 number_seats: int,
                 id: int):
        self.adress = adress
        self.number_seats = number_seats
        self.id = id
        
    @classmethod
    def get_all(cls):
        query = '''
        SELECT *
        FROM battlefield'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    @classmethod
    def get_by_id(cls, id: int):
        query = '''
        SELECT * FROM battlefield
        WHERE id = {}'''.format(id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Battlefield(* arguments)

    @classmethod
    def get_adress(cls):
        query = '''
        SELECT id, adress
        FROM battlefield'''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result

    @classmethod
    def get_adress_by_id(cls, id_battlefield):
        query = '''
        SELECT adress
        FROM battlefield
        WHERE id = {}'''.format(id_battlefield)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result[0]

    #для селекта
    @classmethod
    def get_id(cls, adress):
        query = '''
        SELECT id
        FROM battlefield
        WHERE adress = {}'''.format(adress)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        return result
    

#///////Админ/////////
class Admin(UserMixin):
    def __init__(self, 
                id: int,
                id_fav: int,
                email: str,
                password_hash: str = None):
        self.id = id
        self.id_fav = id_fav
        self.email = email
        self.password_hash = password_hash

    def tuple(self):
        return (self.email, self.password_hash)

    @classmethod
    def get_by_id(cls, id: int):
        query = '''
        SELECT * FROM spectator
        WHERE id = 1 '''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Admin(* arguments)

    @classmethod
    def get_by_email(cls, email):
        query = '''
        SELECT * FROM spectator
        WHERE email = 'the_best_admin@mail.ru' '''
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        arguments = result[0]
        return Admin(* arguments)


    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)


class TrainerProfile(object):
    def __init__(self,
                trainer_id: int, 
                trainer_name: str,
                fav_pokemon: str,
                biography: str):
                
        self.trainer_id = trainer_id
        self.trainer_name = trainer_name
        self.fav_pokemon = fav_pokemon
        self.biography = biography

    def tuple(self):
        return (self.trainer_id,self.trainer_name, self.fav_pokemon, self.biography)


    @classmethod
    def update_trainer(cls, trainerprofile):
        query = '''
        UPDATE trainer
        SET trainer_name = '{}', fav_pokemon = '{}', biography = '{}'
        WHERE id = {} '''.format(trainerprofile.trainer_name,trainerprofile.fav_pokemon, trainerprofile.biography, trainerprofile.trainer_id)

        return DataBase.execute_query(query)  


    @classmethod
    def update_pokemon_of_trainer(cls):
        query = '''
        UPDATE pokemon_of_trainer
        SET id_kind = '{}', id_trainer = '{}'
        WHERE id = {} '''.format()

        return DataBase.execute_query(query)   

    @classmethod
    def get_by_trainer_id(cls, trainer_id):
        query = '''SELECT trainer_name, fav_pokemon, biography
        FROM trainer
        WHERE id = {} '''.format(trainer_id)
        result = DataBase.execute_query(query, True)
        if result is None or len(result) == 0:
            return None
        #arguments = result[0]
        return result



@login.user_loader
def load_user(id: str):
    if session['role'] == 'trainer':
        user = Trainer.get_by_id(int(id))

    elif session['role'] == 'spectator':
        user = Spectator.get_by_id(int(id))

    elif session['role'] == 'admin':
        user = Admin.get_by_id(int(id))
        
    else:
        user = None
    print(f'user {user} loaded')
    return user