
from config import host, user, password, db_name
from query_statements import connect_db, create_table, insert_data, select_atm_to_fix,\
     select_atm_to_withdraw, select_atm_to_fill


#just create db on your localhost with name 'atm_db'

#create table_1
connection = connect_db()
create_table_query = "CREATE TABLE `ATM_list` ("\
                    "id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,"\
                    "coordinates VARCHAR(22),"\
                    "model TINYINT UNSIGNED ZEROFILL NOT NULL,"\
                    "is_online BOOLEAN NULL);"
create_table(connection, create_table_query)

#create table_2
connection = connect_db()
create_table_query = "CREATE TABLE `cash_inside_ATM` ("\
                    "id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,"\
                    "banknote_100 TINYINT UNSIGNED NOT NULL,"\
                    "banknote_1000 TINYINT UNSIGNED NOT NULL,"\
                    "banknote_5000 TINYINT UNSIGNED NOT NULL,"\
                    "FOREIGN KEY (id) REFERENCES `ATM_list` (id) ON DELETE CASCADE);"
create_table(connection, create_table_query)

#create table_3
connection = connect_db()
create_table_query = "CREATE TABLE `ATM_types` ("\
                    "model TINYINT UNSIGNED ZEROFILL NOT NULL,"\
                    "cash_withdrawal BOOLEAN NULL,"\
                    "cash_slot TINYINT UNSIGNED NOT NULL);"
create_table(connection, create_table_query)

#insert data to table_1
connection = connect_db()
insert_query = "INSERT INTO `ATM_list` ("\
    "coordinates, model, is_online)"\
    "VALUES ('55.791119, 37.622757', 1, 0),"\
    "('55.776824, 37.581496', 3, 1),"\
    "('55.771003, 37.620469', 1, 1),"\
    "('55.779029, 37.665854', 1, 1),"\
    "('55.762472, 37.634821', 1, 1),"\
    "('55.755143, 37.620611', 2, 0),"\
    "('55.752054, 37.591975', 1, 1),"\
    "('55.749712, 37.542070', 1, 0),"\
    "('55.744000, 37.565178', 2, 1),"\
    "('55.741848, 37.600741', 3, 1);"
insert_data(connection, insert_query)

#insert data to table_2 (one-to-one relationship to save security about total cash)
connection = connect_db()
insert_query = "INSERT INTO `cash_inside_ATM` ("\
    "banknote_100, banknote_1000, banknote_5000)"\
    "VALUES (57, 65, 49),"\
    "(21, 35, 70),"\
    "(12, 9, 55),"\
    "(66, 83, 43),"\
    "(43, 87, 48),"\
    "(75, 94, 75),"\
    "(54, 47, 20),"\
    "(56, 58, 99),"\
    "(78, 49, 51),"\
    "(17, 19, 20);"
insert_data(connection, insert_query)

#insert data to table_3 (one-to-many), 3rd type of ATM for receive cash only
connection = connect_db()
insert_query = "INSERT INTO `ATM_types` ("\
    "model, cash_withdrawal, cash_slot)"\
    "VALUES (1, 1, 100),"\
    "(2, 1, 150),"\
    "(3, 0, 150);"
insert_data(connection, insert_query)

#select info about ATM's which needs to be fixed
connection = connect_db()
select_query = "SELECT id, coordinates FROM `ATM_list` WHERE is_online = 0;"
select_atm_to_fix(connection, select_query)

#select info about ATM's and cash slots which needs to be withdrawed (3rd type of ATM for receive cash only)
connection = connect_db()
select_query = "SELECT ATM_list.id, coordinates "\
    "FROM cash_inside_ATM JOIN ATM_list USING (id) "\
    "JOIN ATM_types ON ATM_list.model = ATM_types.model "\
    "WHERE (cash_slot * 0.8) <= banknote_100 OR "\
    "cash_slot * 0.8 <= banknote_1000 OR "\
    "cash_slot * 0.8 <= banknote_5000;"
select_atm_to_withdraw(connection, select_query)

#select info about ATM's and cash slots which needs to be filled (3rd type of ATM for receive cash only)
connection = connect_db()
select_query = "SELECT ATM_list.id, coordinates "\
    "FROM cash_inside_ATM JOIN ATM_list USING (id) "\
    "JOIN ATM_types ON ATM_list.model = ATM_types.model "\
    "WHERE (cash_slot * 0.2) >= banknote_100 OR "\
    "cash_slot * 0.2 >= banknote_1000 OR "\
    "cash_slot * 0.2 >= banknote_5000;"
select_atm_to_fill(connection, select_query)