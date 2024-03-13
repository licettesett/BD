from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email

from app.models import Trainer, Spectator, Battle, Trainer_in_battle


#/////ЛОГИН///////
class LoginForm(FlaskForm):
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    is_trainer = BooleanField('is Trainer')
    is_admin = BooleanField('is Admin')
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember')
    submit = SubmitField('Log In')

#/////РЕГИСТРАЦИЯ///////
class RegistrationForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])

    is_trainer = BooleanField('is Trainer')
    name = StringField('Trainer name')
    fav_pokemon = StringField('Write your favorite pokemon if you are Trainer')
    biography = StringField('Write smth about yourself if you are Trainer')
    
    pokemon1 = SelectField('1st Pokemon', coerce=int)
    pokemon2 = SelectField('2nd Pokemon', coerce=int)
    pokemon3 = SelectField('3rd Pokemon', coerce=int)

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('| Submit |')

    def validate_email(self, email):
        if self.is_trainer:
            user = Trainer.get_by_email(email.data)
        else:
            user = Spectator.get_by_email(email.data)
        if user is not None:
            raise ValidationError('use different email')

    def validate_fav_pokemon(self, fav_pokemon):
        if self.is_trainer.data and fav_pokemon.data == '':
            raise ValidationError('if you are Trainer, you should write your favorite pokemon')
        elif self.is_trainer.data and Trainer.get_by_kind(fav_pokemon.data) is None:
            raise ValidationError('please enter a real pokemon (you can see them on PokemonPedia)')
        else:
            return

     
    def validate_pokemon1(self, pokemon1):
        if self.is_trainer.data and (pokemon1.data == self.pokemon2.data  
        or pokemon1.data == self.pokemon3.data):
            raise ValidationError('To register as a trainer, you must have at least THREE DIFFERENT Pokemon to battle')
        else:
            return   

    def validate_pokemon2(self, pokemon2):
        if self.is_trainer.data and (pokemon2.data == self.pokemon1.data  
        or pokemon2.data == self.pokemon3.data):
            raise ValidationError('To register as a trainer, you must have at least THREE DIFFERENT Pokemon to battle')
        else:
            return  

    def validate_pokemon3(self, pokemon3):
        if self.is_trainer.data and (pokemon3.data == self.pokemon1.data  
        or pokemon3.data == self.pokemon2.data):
            raise ValidationError('To register as a trainer, you must have at least THREE DIFFERENT Pokemon to battle')
        else:
            return  

    def validate_biography(self, biography):
        if self.is_trainer.data and biography.data == '':
            raise ValidationError('if you are Trainer, you should write smth about yourself')
        else:
            return

    def validate_trainer_name(self, name):
        if self.is_trainer.data and name.data == '':
            raise ValidationError('if you are Trainer, you must write your name')
        else:
            return


#////////ИЗМЕНИТЬ ПРОФИЛЬ ТРЕНЕРА////////
class EditTrainerProfileForm(FlaskForm):
    trainer_name = StringField('Write your trainer name')
    
    fav_pokemon = StringField('Write name of your favorite pokemon')

    biography = StringField('Write smth about yourself')

    pokemonAdd = SelectField('Select name of your new pokemon', coerce=int)
    add_pokemon = BooleanField('add_pokemon')
    
    submit = SubmitField('| Edit Profile |')
    
    def validate_fav_pokemon(self, fav_pokemon):
        if (fav_pokemon.data != ''):
            if Trainer.get_by_kind(fav_pokemon.data) is None:
                raise ValidationError('please enter an existing pokemon (you can see them on PokemonPedia)')
        else:
            return



#////////ИЗМЕНИТЬ ПРОФИЛЬ ЗРИТЕЛЯ (ФАВОРИТ)////////
class EditFavTrainerForm(FlaskForm):
    
    id_fav = SelectField('Write your favorite trainer ID', coerce = int)

    submit = SubmitField('| Edit |')

    def validate_id_fav(self, id_fav):
        if Trainer.get_by_id(id_fav.data) is None:
            raise ValidationError('please enter a existing Trainer (you can see them on View Trainers)')
        else:
            return


#////////СОЗДАТЬ ПРИГЛАШЕНИЕ НА БИТВУ АДМИНОМ////////
class InvitationAdminForm(FlaskForm):

    id_trainer1 = SelectField('Select ID of 1st trainer', coerce=int)
    id_trainer2 = SelectField('Select ID of 2nd trainer', coerce=int)

    battlefield = SelectField('Select battlefield', coerce=int)
    datetime = StringField('Write datetime of the Battle (format: yy-mm-dd hh:mm)')

    submit = SubmitField('| Create invitation |')
    
    def validate_id_trainer1(self, id_trainer1):
        if id_trainer1.data == self.id_trainer2.data:
            raise ValidationError('Please select DIFFERENT trainer IDs')
        else:
            return  

    def validate_datetime(self, datetime):
        if datetime.data == '':
            raise ValidationError('Please write date and time of the Battle')
        elif Battle.get_id_battle(datetime.data, self.battlefield.data) is not None:
            raise ValidationError('Such a battle is already existing. Choose another time, date or battlefield')
        else:
            return  


#////////ЗАПОЛНИТЬ ПРИГЛАШЕНИЕ НА БИТВУ ТРЕНЕРОМ////////
class InvitationTrainerForm(FlaskForm):

    pokemon1 = SelectField('1st Pokemon for battle', coerce=int)
    pokemon2 = SelectField('2nd Pokemon for battle', coerce=int)
    pokemon3 = SelectField('3rd Pokemon for battle', coerce=int)

    submit = SubmitField('| Fill invitation |')
    
    def validate_pokemon1(self, pokemon1):
        if (pokemon1.data == self.pokemon2.data  
        or pokemon1.data == self.pokemon3.data
        or self.pokemon2.data == self.pokemon1.data):
            raise ValidationError('You must have at least THREE DIFFERENT Pokemon for battle')
        else:
            return   

#/////УСТАНОВИТЬ РЕЗУЛЬТАТ БИТВЫ////////
class SetResult(FlaskForm):

    result1 = SelectField('Select ID of winner')
    result2 = SelectField('Select ID of NOT winner')
    clean_result = BooleanField('clean result (mark the battle as unfinished)')
    submit = SubmitField('| Set result |')

    def validate_result1(self, result1):
        if result1.data == self.result2.data:
            raise ValidationError('Please select DIFFERENT trainer IDs')
        else:
            return  
