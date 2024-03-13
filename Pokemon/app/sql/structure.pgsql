DROP TABLE IF EXISTS Pokemon_in_battle;
DROP TABLE IF EXISTS Trainer_in_battle;
DROP TABLE IF EXISTS Pokemon_of_trainer;
DROP TABLE IF EXISTS Pokemon_kind;
DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS Spectator;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Battle;
DROP TABLE IF EXISTS Battlefield;


CREATE TABLE Trainer
(
    ID INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY, --key
    Trainer_name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Fav_pokemon VARCHAR(100),
    Biography TEXT,
    password_hash VARCHAR(150) NOT NULL,
    in_battle boolean
);


CREATE TABLE Pokemon_kind
(
    Kind_name VARCHAR(100) NOT NULL, 
    ID INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,--key
    Descr TEXT,
    Image VARCHAR(600),
    "Type" VARCHAR(100)
);

CREATE TABLE Pokemon_of_trainer
(
    ID_kind INTEGER REFERENCES Pokemon_kind(ID),--ref
    ID_trainer INTEGER REFERENCES Trainer(ID), --ref
    ID INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY --key
);

CREATE TABLE Battlefield
(
    Adress VARCHAR(100) NOT NULL,
    Number_seats INTEGER NOT NULL,
    ID INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY --key
);

CREATE TABLE Battle
(
    Date_time timestamp, 
    Result VARCHAR(100),
    ID INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY, --key
    ID_battlefield INTEGER REFERENCES Battlefield(ID) --ref
);


CREATE TABLE Trainer_in_battle
(
    ID_trainer INTEGER REFERENCES Trainer(ID), --ref --key
    ID_battle INTEGER REFERENCES Battle(ID),--ref key
    PRIMARY KEY(ID_trainer,ID_battle)
);


CREATE TABLE Pokemon_in_battle
(
    ID_pokemon INTEGER REFERENCES Pokemon_of_trainer(ID), --ref =-key
    ID_battle INTEGER REFERENCES Battle(ID),--ref key
    PRIMARY KEY(ID_pokemon,ID_battle)
);

CREATE TABLE Spectator
(
    ID INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY, --key
    ID_fav INTEGER REFERENCES Trainer(ID),--ref
    Email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(150) NOT NULL
);

CREATE TABLE Ticket
(
    "Row" INTEGER,
    Seat INTEGER,
    Ticket_number INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY, --key
    ID_spectator INTEGER REFERENCES Spectator(ID), --ref
    ID_battle INTEGER REFERENCES Battle(ID) --ref
);


--CREATE TABLE "User"
--(
    --UUID CHAR(32) PRIMARY KEY,
    --login VARCHAR(100) NOT NULL,
    --password_hash VARCHAR(500) NOT NULL
--);

GRANT ALL ON DATABASE prob_db TO user1;
GRANT ALL ON SCHEMA public TO user1;
GRANT ALL ON ALL TABLES IN SCHEMA public TO user1;