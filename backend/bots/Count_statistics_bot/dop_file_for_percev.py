CONFIG_1 = {
    'user': 'neo_reports',
    'password': 'gh2uyti56hgk2h',
    'host': '92.38.186.22',
    'port': '3306',
    'raise_on_warnings': True
}
import warnings
import mysql.connector
connection = mysql.connector.connect(**CONFIG_1)
import datetime
warnings.filterwarnings("ignore")
import pandas as pd

from new_sql_qwer_Percev import Balanc, Equity, Realized_pnl

def get_today():
    return datetime.date.today().strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')

def get_yesterday():
    return (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'), (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def get_week():
    start_of_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
    return start_of_week.strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')

def get_month():
    start_of_month = datetime.date.today().replace(day=1)
    return start_of_month.strftime('%Y-%m-%d'), datetime.date.today().strftime('%Y-%m-%d')


def get_azpros(zapros:str, start:str = None, end:str = None):
    connection = mysql.connector.connect(**CONFIG_1)
    # dict_zap = {
    # "Equity" :'''
    # WITH vse_aki AS (
    #     /*начало Блок все логины с исключениями*/
    #     SELECT *
    #     FROM mt5r1.mt5_users
    #     WHERE Login NOT IN (
    #         /*начало Блок исключений из статистики*/
    #         SELECT Login
    #         FROM mt5r1.mt5_users
    #         WHERE FirstName IN (
    #                         'Chartex P 900969',
    #                         'Chartex P Agr 901066',
    #                         'Chartex Own 901507'
    #         ) 
    #         OR FirstName LIKE 'Bbook %' 
    #         OR FirstName LIKE 'Abook %' 
    #         OR FirstName LIKE 'test %' 
    #         OR FirstName LIKE '% test' 
    #         OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
    #         /*конец Блок исключений из статистики*/
    #     )
    #     /*конец Блок все логины с исключениями*/
    # ) 
    # select 
    # ((
    # /*начало Блок эквити с кредитом ббук на фильтрах*/
    # select ROUND(((SUM(bbook_users.Balance))+(SUM(bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
    # from (
    #         /*начало Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
    #         select vse_aki.*
    #         from (
    #                 /*начало Блок ббук группы автоматика опеределения*/
    #                 SELECT `Group` 
    #                 FROM mt5r1.mt5_groups
    #                 WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' and Currency ='USD'
    #                 /*конец Блок ббук группы автоматика опеределения*/
    #             ) as bbook_ak 
    #         inner join vse_aki on vse_aki.`Group`=bbook_ak.`Group`
    #         /*конец Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
    #     ) as bbook_users 
    # Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=bbook_users.Login
    # /*конец Блок эквити с кредитом ббук на фильтрах*/) + 
    # /**/
    # (
    # /*начало Блок эквити абук с кредитами на фильтрах*/
    # select ROUND(((SUM(abook_users.balance))+(SUM(abook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
    # from (
    #         /*начало Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
    #         select vse_aki.*
    #         from (
    #                 /*конец Блок полные абук группы автоматика опеределения*/
    #                 SELECT `Group` 
    #                 FROM mt5r1.mt5_groups
    #                 WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` not like '%_percent' and Currency ='USD'
    #                 /*конец Блок полные абук группы автоматика опеределения*/
    #             ) as abook_ak 
    #         inner join vse_aki on vse_aki.`Group`=abook_ak.`Group`
    #         /*конец Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
    #     ) as abook_users
    # Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=abook_users.Login
    # /*конецБлок эквити абук с кредитами на фильтрах*/) +  
    # /**/
    # (
    # /*начало Блок эквити с кредитом цент ббук на фильтрах*/
    # select ROUND((((SUM(cent_bbook_users.balance))+(SUM(cent_bbook_users.Credit))+(IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0)))*0.01),2)
    # from (
    #         /*начало Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
    #         select vse_aki.*
    #         from (
    #                 /*конец Блок цент ббук группы автоматика опеределения*/
    #                 SELECT `Group` 
    #                 FROM mt5r1.mt5_groups
    #                 WHERE `group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC'
    #                 /*конец Блок цент ббук группы автоматика опеределения*/
    #             ) as cent_bbook_ak 
    #         inner join vse_aki on vse_aki.`Group`=cent_bbook_ak.`Group`
    #         /*конец Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
    #     ) as cent_bbook_users 
    # Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=cent_bbook_users.Login
    # /*конец Блок эквити с кредитом цент ббук на фильтрах*/) +  
    # /**/ 
    # (
    # /*начало Блок эквити цбук все цбук на фильтрах*/
    # select ROUND(((SUM(c_bbook_users.Balance))+(SUM(c_bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2) 
    # from (
    #         /*начало Блок все цбук группы юзеры таблица мт5 юзерс на фильтрах*/
    #         select vse_aki.*
    #         from (
    #                 /*конец Блок все цбук группы автоматика опеределения*/
    #                 SELECT `Group` 
    #                 FROM mt5r1.mt5_groups
    #                 WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` like '%_percent' and Currency ='USD'
    #                 /*конец все цбук группы автоматика опеределения*/
    #             ) as c_bbook_ak 
    #         inner join vse_aki on vse_aki.`Group`=c_bbook_ak.`Group`
    #         /*конец Блок все цбук юзеры таблица мт5 юзерс на фильтрах*/
    #     ) as c_bbook_users
    # Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=c_bbook_users.Login
    # /*конец Блок эквити цбук все цбук на фильтрах*/)) as total_equity_s_credit_USD, 
    # (
    # /*начало Блок эквити с кредитом ббук на фильтрах*/
    # select ROUND(((SUM(bbook_users.Balance))+(SUM(bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
    # from (
    #         /*начало Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
    #         select vse_aki.*
    #         from (
    #                 /*начало Блок ббук группы автоматика опеределения*/
    #                 SELECT `Group` 
    #                 FROM mt5r1.mt5_groups
    #                 WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' and Currency ='USD'
    #                 /*конец Блок ббук группы автоматика опеределения*/
    #             ) as bbook_ak 
    #         inner join vse_aki on vse_aki.`Group`=bbook_ak.`Group`
    #         /*конец Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
    #     ) as bbook_users 
    # Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=bbook_users.Login
    # /*конец Блок эквити с кредитом ббук на фильтрах*/) as Equity_s_credit_USD_BBOOK, 
    # /**/
    # (
    # /*начало Блок эквити абук с кредитами на фильтрах*/
    # select ROUND(((SUM(abook_users.balance))+(SUM(abook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
    # from (
    #         /*начало Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
    #         select vse_aki.*
    #         from (
    #                 /*конец Блок полные абук группы автоматика опеределения*/
    #                 SELECT `Group` 
    #                 FROM mt5r1.mt5_groups
    #                 WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` not like '%_percent' and Currency ='USD'
    #                 /*конец Блок полные абук группы автоматика опеределения*/
    #             ) as abook_ak 
    #         inner join vse_aki on vse_aki.`Group`=abook_ak.`Group`
    #         /*конец Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
    #     ) as abook_users
    # Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=abook_users.Login
    # /*конецБлок эквити абук с кредитами на фильтрах*/) as Equity_s_credit_USD_ABOOK, 
    # /**/
    # (
    # /*начало Блок эквити с кредитом цент ббук на фильтрах*/
    # select ROUND((((SUM(cent_bbook_users.balance))+(SUM(cent_bbook_users.Credit))+(IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0)))*0.01),2)
    # from (
    #         /*начало Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
    #         select vse_aki.*
    #         from (
    #                 /*конец Блок цент ббук группы автоматика опеределения*/
    #                 SELECT `Group` 
    #                 FROM mt5r1.mt5_groups
    #                 WHERE `group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC'
    #                 /*конец Блок цент ббук группы автоматика опеределения*/
    #             ) as cent_bbook_ak 
    #         inner join vse_aki on vse_aki.`Group`=cent_bbook_ak.`Group`
    #         /*конец Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
    #     ) as cent_bbook_users 
    # Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=cent_bbook_users.Login
    # /*конец Блок эквити с кредитом цент ббук на фильтрах*/) as Equity_s_credit_USD_Cent_BBOOK, 
    # /**/ 
    # (
    # /*начало Блок эквити цбук все цбук на фильтрах*/
    # select ROUND(((SUM(c_bbook_users.Balance))+(SUM(c_bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2) 
    # from (
    #         /*начало Блок все цбук группы юзеры таблица мт5 юзерс на фильтрах*/
    #         select vse_aki.*
    #         from (
    #                 /*конец Блок все цбук группы автоматика опеределения*/
    #                 SELECT `Group` 
    #                 FROM mt5r1.mt5_groups
    #                 WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` like '%_percent' and Currency ='USD'
    #                 /*конец все цбук группы автоматика опеределения*/
    #             ) as c_bbook_ak 
    #         inner join vse_aki on vse_aki.`Group`=c_bbook_ak.`Group`
    #         /*конец Блок все цбук юзеры таблица мт5 юзерс на фильтрах*/
    #     ) as c_bbook_users
    # Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=c_bbook_users.Login
    # /*конец Блок эквити цбук все цбук на фильтрах*/) as Equity_s_credit_USD_CBOOK
    # ;
    # ''',

    # "Realized_pnl" : f'''
    # WITH 
    # vse_aki AS (
    #     SELECT *
    #     FROM mt5r1.mt5_users
    #     WHERE Login NOT IN (
    #         SELECT Login
    #         FROM mt5r1.mt5_users
    #         WHERE FirstName IN (
    #             'Chartex P 900969',
    #             'Chartex P Agr 901066',
    #             'Chartex Own 901507'
    #         ) 
    #         OR FirstName LIKE 'Bbook %' 
    #         OR FirstName LIKE 'Abook %' 
    #         OR FirstName LIKE 'test %' 
    #         OR FirstName LIKE '% test' 
    #         OR Login IN ('')
    #     )
    # ),
    # pl_comis_kompens AS (
    #     SELECT *
    #     FROM mt5r1.mt5_deals
    #     WHERE (
    #         `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
    #         OR (
    #             `Action` = 2
    #             AND (
    #                 Comment IN (
    #                     'indemnification',
    #                     'compensation',
    #                     'Drawdown compensation',
    #                     'Bonus transfer',
    #                     'bonus transfer',
    #                     'Swapfree compensation',
    #                     'balance indemnification',
    #                     'Balance indemnification'
    #                 )
    #             )
    #         )
    #         OR (
    #             `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2)
    #             AND Comment LIKE '%Swap Free Commission'
    #         )
    #     )
    #     AND DATE(`Time`) BETWEEN '{start}' AND '{end}'
    # )
    # select 
    # ((SELECT 
    #     IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    # FROM (
    #     SELECT vse_aki.*
    #     FROM (
    #         SELECT `Group` 
    #         FROM mt5r1.mt5_groups
    #         WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' AND Currency = 'USD'
    #     ) AS bbook_ak 
    #     INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
    # ) AS bbook_users 
    # INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = bbook_users.Login) + 
    # (SELECT 
    #     IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    # FROM (
    #     SELECT vse_aki.*
    #     FROM (
    #         SELECT `Group` 
    #         FROM mt5r1.mt5_groups
    #         WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` NOT LIKE '%_percent' AND Currency = 'USD'
    #     ) AS abook_ak 
    #     INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
    # ) AS abook_users 
    # INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = abook_users.Login) + 
    # (SELECT 
    #     ROUND(IFNULL((SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee)) * 0.01, 0), 2)
    # FROM (
    #     SELECT vse_aki.*
    #     FROM (
    #         SELECT `Group` 
    #         FROM mt5r1.mt5_groups
    #         WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency = 'USC'
    #     ) AS cent_bbook_ak 
    #     INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
    # ) AS cent_bbook_users 
    # INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = cent_bbook_users.Login) + 
    # (SELECT 
    #     IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    # FROM (
    #     SELECT vse_aki.*
    #     FROM (
    #         SELECT `Group` 
    #         FROM mt5r1.mt5_groups
    #         WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` LIKE '%_percent' AND Currency = 'USD'
    #     ) AS c_bbook_ak 
    #     INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
    # ) AS c_bbook_users 
    # INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = c_bbook_users.Login)) as Total_PnL_USD_side_client_realized, 
    # (SELECT 
    #     IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    # FROM (
    #     SELECT vse_aki.*
    #     FROM (
    #         SELECT `Group` 
    #         FROM mt5r1.mt5_groups
    #         WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' AND Currency = 'USD'
    #     ) AS bbook_ak 
    #     INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
    # ) AS bbook_users 
    # INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = bbook_users.Login) AS PnL_BBOOK_USD_side_client_realized, 
    # /**/
    # (SELECT 
    #     IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    # FROM (
    #     SELECT vse_aki.*
    #     FROM (
    #         SELECT `Group` 
    #         FROM mt5r1.mt5_groups
    #         WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` NOT LIKE '%_percent' AND Currency = 'USD'
    #     ) AS abook_ak 
    #     INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
    # ) AS abook_users 
    # INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = abook_users.Login) AS PnL_ABOOK_USD_side_client_realized, 
    # /**/
    # (SELECT 
    #     ROUND(IFNULL((SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee)) * 0.01, 0), 2)
    # FROM (
    #     SELECT vse_aki.*
    #     FROM (
    #         SELECT `Group` 
    #         FROM mt5r1.mt5_groups
    #         WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency = 'USC'
    #     ) AS cent_bbook_ak 
    #     INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
    # ) AS cent_bbook_users 
    # INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = cent_bbook_users.Login) AS PnL_Cent_BBOOK_USD_side_client_realized, 
    # /**/
    # (SELECT 
    #     IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    # FROM (
    #     SELECT vse_aki.*
    #     FROM (
    #         SELECT `Group` 
    #         FROM mt5r1.mt5_groups
    #         WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` LIKE '%_percent' AND Currency = 'USD'
    #     ) AS c_bbook_ak 
    #     INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
    # ) AS c_bbook_users 
    # INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = c_bbook_users.Login) AS PnL_CBOOK_USD_side_client_realized;''',

    # "Balanc" : '''
    # WITH vse_aki AS (
    #     /*начало Блок все логины с исключениями*/
    #     SELECT *
    #     FROM mt5r1.mt5_users
    #     WHERE Login NOT IN (
    #         /*начало Блок исключений из статистики*/
    #         SELECT Login
    #         FROM mt5r1.mt5_users
    #         WHERE FirstName IN (
    # 'Chartex P 900969',
    # 'Chartex P Agr 901066',
    # 'Chartex Own 901507'
    #         ) 
    #         OR FirstName LIKE 'Bbook %' 
    #         OR FirstName LIKE 'Abook %' 
    #         OR FirstName LIKE 'test %' 
    #         OR FirstName LIKE '% test' 
    #         OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
    #         /*конец Блок исключений из статистики*/
    #     )
    #     /*конец Блок все логины с исключениями*/
    # )
    # SELECT 
    #     ROUND((SELECT SUM(bbook_users.balance) 
    #     FROM (
    #         SELECT vse_aki.*
    #         FROM (
    #             SELECT `Group` 
    #             FROM mt5r1.mt5_groups
    #             WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' AND Currency ='USD'
    #         ) AS bbook_ak 
    #         INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
    #     ) AS bbook_users) +
    #     (SELECT SUM(abook_users.balance) 
    #     FROM (
    #         SELECT vse_aki.*
    #         FROM (
    #             SELECT `Group` 
    #             FROM mt5r1.mt5_groups
    #             WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` NOT LIKE '%_percent' AND Currency ='USD'
    #         ) AS abook_ak 
    #         INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
    #     ) AS abook_users) +
    #     (SELECT ROUND(SUM(cent_bbook_users.balance) * 0.01, 2) 
    #     FROM (
    #         SELECT vse_aki.*
    #         FROM (
    #             SELECT `Group` 
    #             FROM mt5r1.mt5_groups
    #             WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency ='USC'
    #         ) AS cent_bbook_ak 
    #         INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
    #     ) AS cent_bbook_users) +
    #     (SELECT SUM(c_bbook_users.balance) 
    #     FROM (
    #         SELECT vse_aki.*
    #         FROM (
    #             SELECT `Group` 
    #             FROM mt5r1.mt5_groups
    #             WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` LIKE '%_percent' AND Currency ='USD'
    #         ) AS c_bbook_ak 
    #         INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
    #     ) AS c_bbook_users), 2) AS total_balance_USD,
    # /**/     
    #     (SELECT SUM(bbook_users.balance) 
    #     FROM (
    #         SELECT vse_aki.*
    #         FROM (
    #             SELECT `Group` 
    #             FROM mt5r1.mt5_groups
    #             WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' AND Currency ='USD'
    #         ) AS bbook_ak 
    #         INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
    #     ) AS bbook_users) AS balance_USD_BBOOK,
    # /**/      
    #     (SELECT SUM(abook_users.balance) 
    #     FROM (
    #         SELECT vse_aki.*
    #         FROM (
    #             SELECT `Group` 
    #             FROM mt5r1.mt5_groups
    #             WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` NOT LIKE '%_percent' AND Currency ='USD'
    #         ) AS abook_ak 
    #         INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
    #     ) AS abook_users) AS balance_USD_ABOOK,
    # /**/      
    #     (SELECT ROUND(SUM(cent_bbook_users.balance) * 0.01, 2) 
    #     FROM (
    #         SELECT vse_aki.*
    #         FROM (
    #             SELECT `Group` 
    #             FROM mt5r1.mt5_groups
    #             WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency ='USC'
    #         ) AS cent_bbook_ak 
    #         INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
    #     ) AS cent_bbook_users) AS balance_USD_Cent_BBOOK,
    # /**/      
    #     (SELECT SUM(c_bbook_users.balance) 
    #     FROM (
    #         SELECT vse_aki.*
    #         FROM (
    #             SELECT `Group` 
    #             FROM mt5r1.mt5_groups
    #             WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` LIKE '%_percent' AND Currency ='USD'
    #         ) AS c_bbook_ak 
    #         INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
    #     ) AS c_bbook_users) AS balance_USD_CBOOK;
    # '''
    # }

    dict_zap = {
        "Equity": Equity,
        "Realized_pnl": Realized_pnl(start=start, end=end),
        "Balanc": Balanc
    }

    df = pd.read_sql_query(dict_zap[zapros].replace("\\", "\\\\"), con=connection)
    d = dict(zip(df.columns, *df.values))
    res = []
    connection.close()
    return f'{zapros}: {list(d.values())[0]}'
    # for key, value in d.items():
    #     if 'BBOOK' in key:
    #         return (f"{key}: {value:,.2f} USD \n".replace(',', ' '))
        # if 'Cent' in key:
        #     value = value / 100
        # res.append((f"{key}: {value:,.2f} USD \n".replace(',', ' ')))
    


    # return ''.join(res)
        
# print(get_azpros('Realized_pnl', '2025-03-01', '2025-03-01'))