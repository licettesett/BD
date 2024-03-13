import os

from flask import render_template, flash, redirect, url_for, request, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app

from app.forms import LoginForm, RegistrationForm, EditTrainerProfileForm, EditFavTrainerForm, InvitationAdminForm, InvitationTrainerForm, SetResult
from app.models import Trainer, Spectator, Pokemon_of_trainer, Pokemon_kind, Admin, TrainerProfile, Battle, Battlefield, Pokemon_in_battle, Trainer_in_battle


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



#//////ПОКЕМОН ЭНЦИКЛОПЕДИЯ//////
@app.route('/pokemon_pedia', methods=['GET', 'POST'])
def pokemon_pedia():
    kinds = Pokemon_kind.get_all_all()
    return render_template('pokemon_pedia.html', title = 'PokemonPedia', kinds = kinds)
    


#///////////////////////////////////////////////////////////////////////////
#////ПРОФИЛЬ ТРЕНЕРА/////
@app.route('/trainer/<trainer_id>')
@login_required
def trainer_profile(trainer_id):

    trainer = Trainer.get_by_id(trainer_id)

    #получение покемонов тренера (информации о них)
    pokemons = Pokemon_of_trainer.get_kind_by_trainer_id(trainer_id)
    print(pokemons)

    #подсчет количества приглашений на битвы (битв всего)
    invitations = Trainer_in_battle.count_of_invitations(trainer_id)
    print(invitations)

    #подсчет завершенных битв
    finished = Trainer_in_battle.count_of_finished(trainer_id)
    print(finished)

    if pokemons is None:
        pokemons = ''


    #получение ID покемонов участвующих в текущей битве
    get_battle_id = Trainer_in_battle.get_battle_id(trainer_id)
    if get_battle_id is None:
        battle_pokemons = ''
    else:
        id_battle = get_battle_id.id_battle

        id_battle_pokemons = Pokemon_in_battle.get_id_battle_pokemon(trainer_id,id_battle)
        print('IDDDD', id_battle_pokemons)
        if id_battle_pokemons is not None:
            battle_pokemons = [0] * 3
            i = 0 #счетчик

            for id in id_battle_pokemons:
                battle_pokemons[i] = Pokemon_of_trainer.get_db_kind_name_by_id(id[0])
                i = i + 1
            
            print('POKES!', battle_pokemons)
        else: 
            battle_pokemons = ''

    #есть ли у тренера сейчас битва
    in_battle = trainer.in_battle

    return render_template('trainer_profile.html', title='trainer profile',
                    trainer=trainer, pokemons = pokemons, invitations = invitations,
                    in_battle = in_battle, finished = finished,
                    battle_pokemons = battle_pokemons)


#////ИЗМЕНИТЬ ПРОФИЛЬ ТРЕНЕРА////
@app.route('/edit_trainer_profile', methods=['GET', 'POST'])
@login_required
def edit_trainer_profile():

    form = EditTrainerProfileForm() 

    pokemonAdd_choices = Pokemon_kind.get_all()
    if pokemonAdd_choices is None:
        pokemonAdd_choices = []

    form.pokemonAdd.choices = pokemonAdd_choices


    if form.validate_on_submit():

        trainer_name = form.trainer_name.data
        if trainer_name == '':
            trainer_name = current_user.trainer_name

        fav_pokemon = form.fav_pokemon.data
        if fav_pokemon == '':
            fav_pokemon = current_user.fav_pokemon

        biography = form.biography.data
        if biography == '':
            biography = current_user.biography

        pokemonAdd = form.pokemonAdd.data
        print(pokemonAdd)

        trainer_profile = TrainerProfile(current_user.id, 
                                        trainer_name, 
                                        fav_pokemon,
                                        biography)

        
        if form.add_pokemon.data:
            if (Pokemon_of_trainer.have_such_pokemon(pokemonAdd, current_user.id) is None):
                pokTr = Pokemon_of_trainer(pokemonAdd,current_user.id,0)
                if not Pokemon_of_trainer.add(pokTr):
                    abort(500)
                else:
                    flash('new pokemon added successfully')
            else: 
                flash('YOU ALREADY HAVE THIS POKEMON KIND')
                return redirect(url_for('edit_trainer_profile'))

        if not TrainerProfile.update_trainer(trainer_profile):
            abort(500)
        else:
            flash('profile changed successfully')
            return redirect(url_for('trainer_profile', trainer_id=current_user.id))
    
    return render_template('edit_trainer_profile.html', title='Edit Profile', form=form)



#////ПРИГЛАШЕНИЕ ТРЕНЕРА НА БИТВУ////
@app.route('/trainer/<trainer_id>/all_trainer_invitations', methods=['GET', 'POST'])
@login_required
def all_trainer_invitations(trainer_id):

    battle = Trainer_in_battle.get_battle_id(current_user.id)

    battleInf = Trainer_in_battle.get_battle(battle.id_battle, current_user.id)
    if battleInf is None:
        battleInf = []

    print(battle)
    print(battleInf)

    #Заполнил ли тренер приглашение (есть ли покемоны в битве)
    if Pokemon_in_battle.have_pok_in_battle(battle.id_battle, current_user.id) is None:
        have_pok_in_battle = False #не заполнил
    else: 
        have_pok_in_battle = True #заполнил

    print(have_pok_in_battle)


    if battleInf is None:
        battleInf = []
    else:
        for inf in battleInf:
            enemy_id = inf[4]
            battlefield_id = inf[3]
    
        enemy = Trainer.get_by_id(enemy_id)
        if enemy is not None:
            enemy_name = enemy.trainer_name
            print(enemy_name)

        battlefield = Battlefield.get_by_id(battlefield_id)
        if  battlefield is not None:
            battlefield_adress = battlefield.adress
            print(battlefield_adress)


        #вывод покемонов в битве
        battle_pokemons = Pokemon_in_battle.get_id_battle_pokemon(current_user.id, battle.id_battle)
        if battle_pokemons is None:
            battle_pokemons = []

        battle_pok = [0] * 3 #покемоны в битве
        i = 0
        for poks in battle_pokemons:
            print(poks[0])
            battle_pok[i] = Pokemon_of_trainer.get_kind_name_by_id(poks[0])
            i = i + 1
            print(battle_pok)

        trainer = Trainer.get_by_id(trainer_id)


    return render_template('all_trainer_invitations.html', title = 'invitations', trainer = trainer, 
    battleInf = battleInf, enemy_name = enemy_name, battlefield_adress = battlefield_adress,
    have_pok_in_battle = have_pok_in_battle, battle_pok = battle_pok)



#////ЗАПОЛНИТЬ ПРИГЛАШЕНИЕ ТРЕНЕРА////
@app.route('/fill_trainer_invitation', methods=['GET', 'POST'])
def fill_trainer_invitation():

    battle = Trainer_in_battle.get_battle_id(current_user.id)
    battleInf = Trainer_in_battle.get_battle(battle.id_battle, current_user.id)

    for inf in battleInf:
        battle_id = inf[2]


    form = InvitationTrainerForm()
    #print(battle)


    pokemon_choices = Pokemon_of_trainer.get_choises(current_user.id)
    if pokemon_choices is None:
        pokemon_choices = []

    print(pokemon_choices)

    form.pokemon1.choices = pokemon_choices
    form.pokemon2.choices = pokemon_choices
    form.pokemon3.choices = pokemon_choices
    
    if form.validate_on_submit():

        pokemon1_id = form.pokemon1.data
        pokemon2_id = form.pokemon2.data
        pokemon3_id = form.pokemon3.data

        pokemon1 = Pokemon_in_battle(pokemon1_id, battle_id)
        pokemon2 = Pokemon_in_battle(pokemon2_id, battle_id)
        pokemon3 = Pokemon_in_battle(pokemon3_id, battle_id)

        if not (Pokemon_in_battle.add(pokemon1) 
        and Pokemon_in_battle.add(pokemon2)
        and Pokemon_in_battle.add(pokemon3)):
            abort(500)
        else:
            flash('invitation filled successfully')
            return redirect(url_for('all_trainer_invitations', trainer_id=current_user.id))

    return render_template('fill_trainer_invitation.html', title = 'fill invitation', form = form)





#///////////////////////////////////////////////////////////////////////
#////ПРОФИЛЬ ЗРИТЕЛЯ/////
@app.route('/spectator/<spectator_id>')
@login_required
def spectator_profile(spectator_id):
    spectator = Spectator.get_by_id(spectator_id)
    fav = Spectator.get_name_by_id_fav(spectator.id_fav)
    if fav is None:
        fav = ''
    return render_template('spectator_profile.html', title='spectator profile', 
    spectator=spectator, fav=fav)


#////ПРОСМОТР ТРЕНЕРОВ//////
@app.route('/see_trainers', methods=['GET', 'POST'])
def see_trainers():
    usersT = Trainer.get_all()
    if usersT is None:
        usersT = []

    not_profile = True

    return render_template('see_trainers.html', title = 'Trainers', usersT = usersT, not_profile = not_profile)



#////////ИЗМЕНИТЬ ЛЮБИМОГО ТРЕНЕРА/////////
@app.route('/edit_fav_trainer', methods=['GET', 'POST'])
@login_required
def edit_fav_trainer():
    form = EditFavTrainerForm()

    id_fav_choices = Trainer.get_id_id()
    if id_fav_choices is None:
        id_fav_choices = []


    form.id_fav.choices = id_fav_choices


    if form.validate_on_submit():
        id_fav = form.id_fav.data

        spectator = Spectator(current_user.id, id_fav,
                            current_user.email, 
                            current_user.password_hash)

        if not Spectator.update_fav(spectator):
            abort(500)
        else:
            flash('favorite trainer changed successfully')
            return redirect(url_for('spectator_profile', spectator_id=current_user.id))

    return render_template('edit_fav_trainer.html', title='Edit Fav', form=form)






#//////////////////////////////////////////////////////////////////////////////////
#////ПРОСМОТР ПОЛЬЗОВАТЕЛЕЙ АДМИНОМ////
@app.route('/see_users', methods=['GET', 'POST'])
def see_users():
    usersT = Trainer.get_all()
    if usersT is None:
        usersT = []

    usersS = Spectator.get_all()
    if usersS is None:
        usersS = []
    
    return render_template('see_users.html', title = 'Users', usersT = usersT, usersS = usersS)



#////СОЗДАНИЕ ПРИГЛАШЕНИЯ НА БИТВУ АДМИНОМ////
@app.route('/invite_admin', methods=['GET', 'POST'])
@login_required
def invite_admin():
    form = InvitationAdminForm()
    usersT = Trainer.get_all()
    if usersT is None:
        usersT = []

    id_trainers = Trainer.get_id_id()
    battlefields = Battlefield.get_adress()

    if id_trainers is None:
        id_trainers = []

    if battlefields is None:
        battlefields = []
   

    form.id_trainer1.choices = id_trainers
    form.id_trainer2.choices = id_trainers

    form.battlefield.choices = battlefields

    if form.validate_on_submit():
        id_trainer1 = form.id_trainer1.data
        id_trainer2 = form.id_trainer2.data
        id_battlefield = form.battlefield.data
        print(id_battlefield)
        datetime = form.datetime.data

        battle = Battle(datetime, '', 0, id_battlefield)
        
        trainer1 = Trainer.get_by_id(id_trainer1)
        trainer2 = Trainer.get_by_id(id_trainer2)

        if not (trainer1.in_battle or trainer2.in_battle):
            if not Battle.add(battle):
                abort(500)
            else:
                flash('battle created successfully')

                if not (Trainer.update_trainer(True, id_trainer1) and
                Trainer.update_trainer(True, id_trainer2)):
                    abort(500)
                else:
                    id_battle = Battle.get_id_battle(datetime, id_battlefield)
                    trainerB1 = Trainer_in_battle(id_trainer1,id_battle.id)
                    trainerB2 = Trainer_in_battle(id_trainer2,id_battle.id)
                    print(trainerB1)
                    print(trainerB1)

            if not (Trainer_in_battle.add(trainerB1) 
                    and Trainer_in_battle.add(trainerB2)):
                abort(500)
            else:
                flash('invitation created successfully')
                #return redirect(url_for('invite_admin'))
        else : flash('ONE OF THE TRAINERS IS BUSY (ALREADY HAS BATTLE)')


    return render_template('invite_admin.html', title='create invitation', form = form, usersT = usersT)


#////ПРОСМОТР БИТВ//////
@app.route('/see_battles', methods=['GET', 'POST'])
def see_battles():

    #получить все айди предстоящих битв (чтобы перечислить битвы по айди)
    ids_up_battle = Battle.get_un_id()
    if ids_up_battle is None:
        ids_up_battle = []


    #подсчет размера списка и создание массива для хранения айди тренеров в битве
    idsUp_mass = [0] * len(ids_up_battle)#айди тренеров (по 2) в незавершенных битвах

    i: int #счетчик
    i = 0
    #айди тренеров в конкретной незавершенной битве 
    #по два заносятся в массив по айди битвы 
    #(какой тренер (айди) участвует в битве с таким-то айди)
    for ids_up in ids_up_battle:
        idsUp_mass[i] = Trainer_in_battle.get_id_trainer(ids_up[0])
        i = i + 1

    if idsUp_mass is None:
        idsUp_mass = []

    
    #айди первых тренеров в битвах 
    trainers1u = [0] * len(ids_up_battle) 
    #айди вторых тренеров в битвах 
    trainers2u = [0] * len(ids_up_battle)
    i = 0
    #массивы с 
    # 1) инф-ей о первых тренеров в каждой битве
    # 2) инф-ей о вторых тренеров в каждой битве

    for ids in idsUp_mass:
        trainers1u[i] = Trainer.get_by_id(ids[0][0])
        trainers2u[i] = Trainer.get_by_id(ids[1][0])
        i = i + 1


#///////ВСЕ ТО ЖЕ САМОЕ ТОЛЬКО С ЗАВЕРШЕННЫМИ БИТВАМИ////////
    #получить все айди завершенных битв (чтобы перечислить битвы по айди)
    ids_fin_battle = Battle.get_fin_id()
    if ids_fin_battle is None:
        ids_fin_battle = []

    idsFin_mass = [0] * len(ids_fin_battle)#айди тренеров (по 2) в завершенных битвах


    i = 0
    #айди тренеров в конкретной завершенной битве 
    #по два заносятся в массив по айди битвы 
    for ids_fin in ids_fin_battle:
        idsFin_mass[i] = Trainer_in_battle.get_id_trainer(ids_fin[0])
        i = i + 1

    if idsFin_mass is None:
        idsFin_mass = []


    #айди первых тренеров в битвах 
    trainers1f = [0] * len(ids_fin_battle) 
    #айди вторых тренеров в битвах 
    trainers2f = [0] * len(ids_fin_battle)

    i = 0
    for ids in idsFin_mass:
        trainers1f[i] = Trainer.get_by_id(ids[0][0])
        trainers2f[i] = Trainer.get_by_id(ids[1][0])
        i = i + 1


#///////////////////ИНФ-ИЯ ПО БИТВАМ////////////////////////////////////////
#ПО НЕЗАВЕРШЕННЫМ:
    #массив для хранения строк с информацией по предстоящим битвам
    battleInfUp = [0] * len(ids_up_battle) 
    
    i = 0
    for ids_up in ids_up_battle:
        battleInfUp[i] = Trainer_in_battle.get_battle(ids_up[0], trainers1u[i].id )
        i = i + 1

    #записать айди мест битв в массив
    fields_id = [0] * len(ids_up_battle) 
    i = 0
    for inf in  battleInfUp:
        fields_id[i] = inf[0][3]
        i = i + 1

    fieldsUp = [0] * len(ids_up_battle) 
    #получить название места по его айди и записать их в массив
    i = 0
    for f in  fields_id:
        fieldsUp[i] = Battlefield.get_adress_by_id(f)
        i = i + 1



#ПО ЗАВЕРШЕННЫМ:
    #массив для хранения строк с информацией по предстоящим битвам
    battleInfFin = [0] * len(ids_fin_battle) 
    
    i = 0
    for ids_fin in ids_fin_battle:
        battleInfFin[i] = Trainer_in_battle.get_battle_with_result(ids_fin[0], trainers1f[i].id )
        i = i + 1

    #записать айди мест битв в массив
    fields_id = [0] * len(ids_fin_battle) 
    i = 0
    for inf in  battleInfFin:
        fields_id[i] = inf[0][3]
        i = i + 1

    fieldsFin = [0] * len(ids_fin_battle) 
    #получить название места по его айди и записать их в массив
    i = 0
    for f in  fields_id:
        fieldsFin[i] = Battlefield.get_adress_by_id(f)
        i = i + 1

    for f in  fieldsFin:
        print('Fields', f[0])

    return render_template('see_battles.html', title = 'battles', 
        trainers1u = trainers1u, trainers2u = trainers2u, 
        trainers1f = trainers1f, trainers2f = trainers2f, 
        ids_up_battle = ids_up_battle, ids_fin_battle = ids_fin_battle,
        battleInfUp = battleInfUp, battleInfFin = battleInfFin,
        fieldsFin = fieldsFin, fieldsUp = fieldsUp)


#//ИЗМЕНИТЬ РЕЗУЛЬТАТ БИТВЫ АДМИНОМ/////
@app.route('/set_result/<battle_id>', methods=['GET', 'POST'])
def set_result(battle_id):
    
    form = SetResult()
    #возвращает айди конкретной битвы
    b_id = battle_id

    form.result1.choices = Trainer_in_battle.get_id_trainer_choices(battle_id)
    form.result2.choices = Trainer_in_battle.get_id_trainer_choices(battle_id)
    
    if form.validate_on_submit():
        #в результат заносится айди выбранного тренера в строковом виде
        result1 = str(form.result1.data)
        result2 = str(form.result2.data)

        id_trainer1 = int(result1)
        id_trainer2 = int(result2)

        #если не нажата кнопка очистить данные о результате битвы
        if not (form.clean_result.data):
            #в результат битвы заносится айди тренера победителя
            if not Battle.update_battle_result(result1,battle_id):
                abort(500)
            else:
                #если у битвы задан результат
                if Battle.have_result(battle_id) is not None:
                #тренеру присваивается значение, что он свободен
                #(можно назначить новую битву)
                    if not (Trainer.update_trainer(False, id_trainer1)
                        and Trainer.update_trainer(False, id_trainer2)):
                        abort(500)
                    flash('Result set successfully') 
                else:
                    #у тренера не меняется ничего, меняется только результат битвы
                    flash('Result changed successfully') 
         
        else: #если нажата
            if (Trainer_in_battle.get_battle_id(form.result1.data) is None
                    and Trainer_in_battle.get_battle_id(form.result2.data) is None):
                #в результат битвы заносится пустая строка
                # (битва еще не провелась)
                if not Battle.update_battle_result('',battle_id):
                    abort(500)
                else:
                    #тренеру присваивается значение, что он в битве
                    #(нельзя назначить новую битву)
                    if not (Trainer.update_trainer(True, id_trainer1)
                    and Trainer.update_trainer(True, id_trainer2)):
                        abort(500)
                    flash('Result cleaned successfully') 
            else:
                flash('TRAINER HAS UNCOMPLETE BATTLE. Before changing the result of completed battles, finish unfinished battles.') 


    return render_template('set_result.html', title = 'set result', form = form, b_id = b_id)




#////////////////////////////////////////////////////////////////////////////////
#ВОЙТИ В АККАУНТ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.is_trainer.data:
            # логинизация для Тренера
            user = Trainer.get_by_email(form.email.data)
            session['role'] = 'trainer'
        else:
            # логинизация для Зрителя
            user = Spectator.get_by_email(form.email.data)
            session['role'] = 'spectator'
        
        if form.is_admin.data:
            # логинизация для Админа
            user = Admin.get_by_email(form.email.data)
            session['role'] = 'admin'

        if user is None or not user.check_password(form.password.data):
            flash('invalid email or password')
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

    pokemonAdd_choices = Pokemon_kind.get_all()
    if pokemonAdd_choices is None:
        pokemonAdd_choices = []

    form.pokemon1.choices = pokemonAdd_choices
    form.pokemon2.choices = pokemonAdd_choices
    form.pokemon3.choices = pokemonAdd_choices

    if form.validate_on_submit():
        if form.is_trainer.data:
            print('tr')
            user = Trainer(0, form.name.data, form.email.data, form.fav_pokemon.data, form.biography.data,0)
            user.set_password(form.password.data)
            if not Trainer.add(user):
                abort(500)
            else:
                us = Trainer.get_by_email(form.email.data)

                pokemon1 = form.pokemon1.data
                pokTr1 = Pokemon_of_trainer(pokemon1,us.id,0)
                Pokemon_of_trainer.add(pokTr1)

                pokemon2 = form.pokemon2.data
                pokTr2 = Pokemon_of_trainer(pokemon2,us.id,0)
                Pokemon_of_trainer.add(pokTr2)

                pokemon3 = form.pokemon3.data
                pokTr3 = Pokemon_of_trainer(pokemon3,us.id,0)
                Pokemon_of_trainer.add(pokTr3)

        else:
            print('spec')
            user = Spectator(0, 0, form.email.data)
            user.set_password(form.password.data)
            if not Spectator.add(user):
                abort(500)
        flash('you are registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



#/////////////////////////////////////////////////////////////////////////// 
#////БЕДНЫЙ СТУДЕНТ/////
@app.route('/poor_student', methods=['GET', 'POST'])
def poor_student():
    return render_template('poor_student.html', title = 'POKEMON - About Us')



