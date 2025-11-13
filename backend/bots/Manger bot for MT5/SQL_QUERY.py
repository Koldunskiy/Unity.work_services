
def get_sql_query(zapros: str, start:str = None, end:str = None) -> str:


    DICT = { 
    'EKTIV_BALANCE': '''
# Balanc Aktiv
WITH vse_aki AS (
/*начало Блок все логины с исключениями*/
select *
from mt5r2.mt5_users
where Login not in (
					/*начало Блок исключений из статистики*/
					select Login
					from mt5r2.mt5_users
					where FirstName in ( 
										'FirstName', 
										'First Admin', 
										'Шлюз OPICS-MT5', 
										'MT5Replicator', 
										'For delete partners', 
										'Поддержка MetaQuotes', 
										'Технический Дилер для Уведомления и закрытия позиций по CFD', 
										'Тех логин для доступа MT5OpicsImport', 
										'Тех. логин для доступа MT5ARobotImport', 
										'Тех. дилер для MT5GroupChanger', 
										'MT5PammUploader TEST', 
										'MT5OpicsConvertation', 
										'MT5 Summary 2 OPICS', 
										'TESTMT5OpicsConvertation', 
										'MT5ARobotGateway', 
										'FX Best Feeder Rezerv', 
										'ARobot Feeder', 
										'ARobot Get-Accounts', 
										'MT5SoapProvider', 
										'Alfa-Robot-MT5-Gateway-LD4', 
										'MT5FeederAlfaRobot-LD4', 
										'MT5BBProGateway', 
										'BBProDealService ', 
										'BBProGatewayX ', 
										'MT5GatewayUnity', 
										'MT5GatewayActiveBBook', 
										'FastMT Admins', 
										'TPS (Trading Platform Service)', 
										'WEB Gate', 
										'MT5 Pamm Uploader', 
										'Alfa Forex Site', 
										'MT5SwapsFree(тех. пользователь)', 
										'MT5DataPro', 
										'MT5 Monitor', 
										'MT5 Pamm Info', 
										'AF Online IOS', 
										'Тех. логин для доступа MT5PartnerShip', 
										'Casual Investment', 
										'Technical AlfaFinance', 
										'Alfa-Finance Get Quotes', 
										'MT5WebAPIExtension Plugin', 
										'MT5Monitor64', 
										'MT5PartnerShip для EuroTrader', 
										'MatchLiquidityDealService', 
										'MT5DataPro TEST', 
										'MT5PammInfo TEST', 
										'MT5Partnership TEST', 
										'ACM_MT5RegulatoryReporting', 
										'MT5PositionManager', 
										'AF Online Android', 
										'MTServiceTools', 
										'Dealer 7', 
										'MT5ServiceReports', 
										'1C Galament Integration', 
										'ADEALING', 
										'MT5FeederAR_RFD', 
										'MT5FeederAR_RFD_LD4', 
										'MT5TicksExport', 
										'MT5FeederNTPro64_RFD', 
										'Kaz Retail CRM', 
										'ACM_MT5FloatLeverageService ', 
										'MT5 Quotex view-only', 
										'MT5FeederProvider', 
										'ACM_MT5PropTrading', 
										'MT5CreditActiveService', 
										'MT5SwapFreeActive', 
										'RFD-Gateway tick manager', 
										'ACM_MT5FloatLeverageService_Kval', 
										'FastMT Monitoring', 
										'FastMT Backup', 
										'Dealer 1', 
										'Dealer 4', 
										'Dealer 2', 
										'Dealer 5', 
										'Dealer 6', 
										'Dealer 3', 
										'Менеджер ZuluTrade', 
										'Dealer 8', 
										'RobotMoveAB', 
										'Dealer 9', 
										'Dealer 10', 
										'Dealer 11', 
										'Dealer 12', 
										'I-FO', 
										'Dealer 13', 
										'CySEC', 
										'View manager', 
										'Cappitech', 
										'FX View Only', 
										'Murat', 
										'FX manager', 
										'FX Manager 2 nov', 
										'FX Manager 3 din', 
										'FX Manager 4 sub', 
										'FX Manager 5 nak', 
										'FX Manager 6 lov', 
										'FX Manager 7 rnov', 
										'FX Manager 8 ova', 
										'FX web manager', 
										'FX Manager 9 ikov', 
										'FX Manager 10 shin', 
										'FX Manager 11 up1', 
										'FX Manager 12 SF', 
										'FX Manager sich 13', 
										'FX Manager 14 up2', 
										'FX Manager 15 rou', 
										'FX Manager 16', 
										'FX Manager 17', 
										'FX Manager 18', 
										'View account', 
										'FX_Manager_Sofia', 
										'FX_Manager _Venera', 
										'Дежурный дилер АСМ', 
										'Dealer 14', 
										'FX admin hov', 
										'audit 1', 
										'TestNewIossub TestNewVadim ', 
										'TestIossub TestVadim ll', 
										'yvayvayvav yvayvavya ', 
										'test test ', 
										'TestIossub TestVadim Petrovich', 
										'test fsdfsdf fsdfsf gfdsgsdg тест', 
										'TestIossub TestVadim Test', 
										'fgsd gfsdsdf ', 
										'Ggg Fff Ff', 
										'fsdfsd fsdfs ', 
										'SeletskiTest Kirill Borisovich', 
										'BruvTest SergTest ', 
										'TestSmirnov TestIvan ', 
										'Test  Sergei  ', 
										'Test Andrei ', 
										'TestSmirnov Ivan Valerevich', 
										'Indicative', 
										'TestIvan', 
										'Andrei BbN', 
										'Andrei BbH', 
										'Andrei AbN', 
										'Andrei AbH', 
										'Test Swapfree netting', 
										'Test Swapfree hedge', 
										'Test Swapfree Pilot hedge', 
										'PL abook', 
										'testing for FastMT', 
										'test abook hedge', 
										'Test Kagirova Venera Ramzisovna', 
										'FastMT Test', 
										'Test Sophia ssss', 
										'Test Test Artyom Lyutikov', 
										'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс' 
										) 
						  OR FirstName LIKE 'Bbook %' 
					      OR FirstName LIKE 'Abook %' 
					      OR FirstName LIKE 'test %' 
					      OR FirstName LIKE '% test' 
					      OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
					      /*конец Блок исключений из статистики*/
					)
/*конец Блок все логины с исключениями*/
)
SELECT 
    ROUND((SELECT IFNULL(SUM(bbook_users.balance), 0) 
     FROM (
         SELECT vse_aki.*
         FROM (
				/*конец Блок ббук группы автоматика опеределения*/
				SELECT `Group` 
				FROM mt5r2.mt5_groups
				WHERE `group` LIKE 'real\\\\active\\\\Bbook%' and Currency ='USD'
				/*конец Блок ббук группы автоматика опеределения*/
         ) AS bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
     ) AS bbook_users) +
    (SELECT IFNULL(SUM(abook_users.balance), 0) 
     FROM (
         SELECT vse_aki.*
         FROM (
				/*конец Блок полные абук группы автоматика опеределения*/
				SELECT `Group` 
				FROM mt5r2.mt5_groups
				WHERE `group` LIKE 'real\\\\active_Abook\\\\Abook%' and `group` not like '%_percent' and Currency ='USD'
				/*конец Блок полные абук группы автоматика опеределения*/
         ) AS abook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
     ) AS abook_users) +
    (SELECT IFNULL(ROUND(SUM(cent_bbook_users.balance) * 0.01, 2), 0) 
     FROM (
         SELECT vse_aki.*
         FROM (
				/*конец Блок цент ббук группы автоматика опеределения*/
				SELECT `Group` 
				FROM mt5r2.mt5_groups
				WHERE `group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC'
				/*конец Блок цент ббук группы автоматика опеределения*/
         ) AS cent_bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
     ) AS cent_bbook_users) +
    (SELECT IFNULL(SUM(c_bbook_users.balance), 0) 
     FROM (
         SELECT vse_aki.*
         FROM (
				/*конец Блок цбук группы в USD автоматика опеределения*/
				SELECT `Group` 
				FROM mt5r2.mt5_groups
				WHERE `group` LIKE 'real\\\\active_Abook\\\\Abook%' and `group` like '%_percent' and Currency ='USD'
				/*конец Блок цбук группы в USD автоматика опеределения*/
         ) AS c_bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
     ) AS c_bbook_users), 2) AS total_balance_USD;
''',

"EKTIV_EKVITY" : '''
WITH vse_aki AS (
/*начало Блок все логины с исключениями*/
select *
from mt5r2.mt5_users
where Login not in (
					/*начало Блок исключений из статистики*/
					select Login
					from mt5r2.mt5_users
					where FirstName in ( 
										'FirstName', 
										'First Admin', 
										'Шлюз OPICS-MT5', 
										'MT5Replicator', 
										'For delete partners', 
										'Поддержка MetaQuotes', 
										'Технический Дилер для Уведомления и закрытия позиций по CFD', 
										'Тех логин для доступа MT5OpicsImport', 
										'Тех. логин для доступа MT5ARobotImport', 
										'Тех. дилер для MT5GroupChanger', 
										'MT5PammUploader TEST', 
										'MT5OpicsConvertation', 
										'MT5 Summary 2 OPICS', 
										'TESTMT5OpicsConvertation', 
										'MT5ARobotGateway', 
										'FX Best Feeder Rezerv', 
										'ARobot Feeder', 
										'ARobot Get-Accounts', 
										'MT5SoapProvider', 
										'Alfa-Robot-MT5-Gateway-LD4', 
										'MT5FeederAlfaRobot-LD4', 
										'MT5BBProGateway', 
										'BBProDealService ', 
										'BBProGatewayX ', 
										'MT5GatewayUnity', 
										'MT5GatewayActiveBBook', 
										'FastMT Admins', 
										'TPS (Trading Platform Service)', 
										'WEB Gate', 
										'MT5 Pamm Uploader', 
										'Alfa Forex Site', 
										'MT5SwapsFree(тех. пользователь)', 
										'MT5DataPro', 
										'MT5 Monitor', 
										'MT5 Pamm Info', 
										'AF Online IOS', 
										'Тех. логин для доступа MT5PartnerShip', 
										'Casual Investment', 
										'Technical AlfaFinance', 
										'Alfa-Finance Get Quotes', 
										'MT5WebAPIExtension Plugin', 
										'MT5Monitor64', 
										'MT5PartnerShip для EuroTrader', 
										'MatchLiquidityDealService', 
										'MT5DataPro TEST', 
										'MT5PammInfo TEST', 
										'MT5Partnership TEST', 
										'ACM_MT5RegulatoryReporting', 
										'MT5PositionManager', 
										'AF Online Android', 
										'MTServiceTools', 
										'Dealer 7', 
										'MT5ServiceReports', 
										'1C Galament Integration', 
										'ADEALING', 
										'MT5FeederAR_RFD', 
										'MT5FeederAR_RFD_LD4', 
										'MT5TicksExport', 
										'MT5FeederNTPro64_RFD', 
										'Kaz Retail CRM', 
										'ACM_MT5FloatLeverageService ', 
										'MT5 Quotex view-only', 
										'MT5FeederProvider', 
										'ACM_MT5PropTrading', 
										'MT5CreditActiveService', 
										'MT5SwapFreeActive', 
										'RFD-Gateway tick manager', 
										'ACM_MT5FloatLeverageService_Kval', 
										'FastMT Monitoring', 
										'FastMT Backup', 
										'Dealer 1', 
										'Dealer 4', 
										'Dealer 2', 
										'Dealer 5', 
										'Dealer 6', 
										'Dealer 3', 
										'Менеджер ZuluTrade', 
										'Dealer 8', 
										'RobotMoveAB', 
										'Dealer 9', 
										'Dealer 10', 
										'Dealer 11', 
										'Dealer 12', 
										'I-FO', 
										'Dealer 13', 
										'CySEC', 
										'View manager', 
										'Cappitech', 
										'FX View Only', 
										'Murat', 
										'FX manager', 
										'FX Manager 2 nov', 
										'FX Manager 3 din', 
										'FX Manager 4 sub', 
										'FX Manager 5 nak', 
										'FX Manager 6 lov', 
										'FX Manager 7 rnov', 
										'FX Manager 8 ova', 
										'FX web manager', 
										'FX Manager 9 ikov', 
										'FX Manager 10 shin', 
										'FX Manager 11 up1', 
										'FX Manager 12 SF', 
										'FX Manager sich 13', 
										'FX Manager 14 up2', 
										'FX Manager 15 rou', 
										'FX Manager 16', 
										'FX Manager 17', 
										'FX Manager 18', 
										'View account', 
										'FX_Manager_Sofia', 
										'FX_Manager _Venera', 
										'Дежурный дилер АСМ', 
										'Dealer 14', 
										'FX admin hov', 
										'audit 1', 
										'TestNewIossub TestNewVadim ', 
										'TestIossub TestVadim ll', 
										'yvayvayvav yvayvavya ', 
										'test test ', 
										'TestIossub TestVadim Petrovich', 
										'test fsdfsdf fsdfsf gfdsgsdg тест', 
										'TestIossub TestVadim Test', 
										'fgsd gfsdsdf ', 
										'Ggg Fff Ff', 
										'fsdfsd fsdfs ', 
										'SeletskiTest Kirill Borisovich', 
										'BruvTest SergTest ', 
										'TestSmirnov TestIvan ', 
										'Test  Sergei  ', 
										'Test Andrei ', 
										'TestSmirnov Ivan Valerevich', 
										'Indicative', 
										'TestIvan', 
										'Andrei BbN', 
										'Andrei BbH', 
										'Andrei AbN', 
										'Andrei AbH', 
										'Test Swapfree netting', 
										'Test Swapfree hedge', 
										'Test Swapfree Pilot hedge', 
										'PL abook', 
										'testing for FastMT', 
										'test abook hedge', 
										'Test Kagirova Venera Ramzisovna', 
										'FastMT Test', 
										'Test Sophia ssss', 
										'Test Test Artyom Lyutikov', 
										'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс' 
										) 
						  OR FirstName LIKE 'Bbook %' 
					      OR FirstName LIKE 'Abook %' 
					      OR FirstName LIKE 'test %' 
					      OR FirstName LIKE '% test' 
					      OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
					      /*конец Блок исключений из статистики*/
					)
/*конец Блок все логины с исключениями*/
) 
select 
((
/*начало Блок эквити с кредитом ббук на фильтрах*/
select ROUND(((SUM(bbook_users.Balance))+(SUM(bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
from (
		/*начало Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
		select vse_aki.*
		from (
				/*конец Блок ббук группы автоматика опеределения*/
				SELECT `Group` 
				FROM mt5r2.mt5_groups
				WHERE `group` LIKE 'real\\\\active\\\\Bbook%' and Currency ='USD'
				/*конец Блок ббук группы автоматика опеределения*/
			) as bbook_ak 
		inner join vse_aki on vse_aki.`Group`=bbook_ak.`Group`
		/*конец Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
	) as bbook_users 
Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r2.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=bbook_users.Login
/*конец Блок эквити с кредитом ббук на фильтрах*/) + 
/**/
(
/*начало Блок эквити абук с кредитами на фильтрах*/
select ROUND(((SUM(abook_users.balance))+(SUM(abook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
from (
		/*начало Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
		select vse_aki.*
		from (
				/*конец Блок полные абук группы автоматика опеределения*/
				SELECT `Group` 
				FROM mt5r2.mt5_groups
				WHERE `group` LIKE 'real\\\\active_Abook\\\\Abook%' and `group` not like '%_percent' and Currency ='USD'
				/*конец Блок полные абук группы автоматика опеределения*/
			) as abook_ak 
		inner join vse_aki on vse_aki.`Group`=abook_ak.`Group`
		/*конец Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
	) as abook_users
Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r2.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=abook_users.Login
/*конецБлок эквити абук с кредитами на фильтрах*/) +  
/**/
(
/*начало Блок эквити с кредитом цент ббук на фильтрах*/
select IFNULL(ROUND((((SUM(cent_bbook_users.balance))+(SUM(cent_bbook_users.Credit))+(IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0)))*0.01),2),0)
from (
		/*начало Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
		select vse_aki.*
		from (
				/*конец Блок цент ббук группы автоматика опеределения*/
				SELECT `Group` 
				FROM mt5r2.mt5_groups
				WHERE `group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC'
				/*конец Блок цент ббук группы автоматика опеределения*/
			) as cent_bbook_ak 
		inner join vse_aki on vse_aki.`Group`=cent_bbook_ak.`Group`
		/*конец Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
	) as cent_bbook_users 
Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r2.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=cent_bbook_users.Login
/*конец Блок эквити с кредитом цент ббук на фильтрах*/) +  
/**/ 
(
/*начало Блок эквити цбук все цбук на фильтрах*/
select IFNULL(ROUND(((SUM(c_bbook_users.Balance))+(SUM(c_bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2),0) 
from (
		/*начало Блок все цбук группы юзеры таблица мт5 юзерс на фильтрах*/
		select vse_aki.*
		from (
				/*конец Блок цбук группы в USD автоматика опеределения*/
				SELECT `Group` 
				FROM mt5r2.mt5_groups
				WHERE `group` LIKE 'real\\\\active_Abook\\\\Abook%' and `group` like '%_percent' and Currency ='USD'
				/*конец Блок цбук группы в USD автоматика опеределения*/
			) as c_bbook_ak 
		inner join vse_aki on vse_aki.`Group`=c_bbook_ak.`Group`
		/*конец Блок все цбук юзеры таблица мт5 юзерс на фильтрах*/
	) as c_bbook_users
Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r2.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=c_bbook_users.Login
/*конец Блок эквити цбук все цбук на фильтрах*/)) as total_equity_s_credit_USD
;
'''
,

"EKTIV_PNL" : f'''SELECT
    /* PnL для Cent BBOOK */
    (
        SELECT 
            ROUND(IFNULL(SUM((pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee) * 0.01), 0), 2) AS PnL_Cent_BBOOK_USD_side_client_realized
        FROM 
            (
                SELECT vse_aki.*
                FROM (
                    SELECT `Group`
                    FROM mt5r2.mt5_groups
                    WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency = 'USC'
                ) AS cent_bbook_ak
                INNER JOIN (
                    SELECT *
                    FROM mt5r2.mt5_users
                    WHERE Login NOT IN (
                        SELECT Login
                        FROM mt5r2.mt5_users
                        WHERE FirstName IN ('FirstName', 'First Admin' /* добавьте все исключения */) 
                            OR FirstName LIKE 'Bbook %'
                            OR FirstName LIKE 'Abook %'
                            OR FirstName LIKE 'test %'
                            OR FirstName LIKE '% test'
                            OR Login IN ('') /* список исключаемых логинов */
                    )
                ) AS vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
            ) AS cent_bbook_users
        INNER JOIN (
            SELECT *
            FROM mt5r2.mt5_deals
            WHERE (
                `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
                OR (`Action` = 2 AND Comment IN ('indemnification', 'compensation', 'Drawdown compensation', 'Bonus transfer', 'Swapfree compensation', 'Balance indemnification'))
                OR (`Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2) AND Comment LIKE '%Swap Free Commission')
            ) AND DATE(`Time`) BETWEEN '{start}' AND '{end}'
        ) AS pl_comis_kompens ON pl_comis_kompens.Login = cent_bbook_users.Login
    ) AS PnL_Cent_BBOOK_USD_side_client_realized,

    /* PnL для BBOOK */
    (
        SELECT 
            IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0) AS PnL_BBOOK_USD_side_client_realized
        FROM 
            (
                SELECT vse_aki.*
                FROM (
                    SELECT `Group`
                    FROM mt5r2.mt5_groups
                    WHERE `group` LIKE 'real\\\\active\\\\Bbook%' AND Currency = 'USD'
                ) AS bbook_ak
                INNER JOIN (
                    SELECT *
                    FROM mt5r2.mt5_users
                    WHERE Login NOT IN (
                        SELECT Login
                        FROM mt5r2.mt5_users
                        WHERE FirstName IN ('FirstName', 'First Admin' /* добавьте все исключения */) 
                            OR FirstName LIKE 'Bbook %'
                            OR FirstName LIKE 'Abook %'
                            OR FirstName LIKE 'test %'
                            OR FirstName LIKE '% test'
                            OR Login IN ('') /* список исключаемых логинов */
                    )
                ) AS vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
            ) AS bbook_users
        INNER JOIN (
            SELECT *
            FROM mt5r2.mt5_deals
            WHERE (
                `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
                OR (`Action` = 2 AND Comment IN ('indemnification', 'compensation', 'Drawdown compensation', 'Bonus transfer', 'Swapfree compensation', 'Balance indemnification'))
                OR (`Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2) AND Comment LIKE '%Swap Free Commission')
            ) AND DATE(`Time`) BETWEEN '{start}' AND '{end}'
        ) AS pl_comis_kompens ON pl_comis_kompens.Login = bbook_users.Login
    ) AS PnL_BBOOK_USD_side_client_realized,

    /* PnL для ABOOK */
    (
        SELECT 
            IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0) AS PnL_ABOOK_USD_side_client_realized
        FROM 
            (
                SELECT vse_aki.*
                FROM (
                    SELECT `Group`
                    FROM mt5r2.mt5_groups
                    WHERE `group` LIKE 'real\\\\active_Abook\\\\Abook%' AND `group` NOT LIKE '%_percent' AND Currency = 'USD'
                ) AS abook_ak
                INNER JOIN (
                    SELECT *
                    FROM mt5r2.mt5_users
                    WHERE Login NOT IN (
                        SELECT Login
                        FROM mt5r2.mt5_users
                        WHERE FirstName IN ('FirstName', 'First Admin' /* добавьте все исключения */) 
                            OR FirstName LIKE 'Bbook %'
                            OR FirstName LIKE 'Abook %'
                            OR FirstName LIKE 'test %'
                            OR FirstName LIKE '% test'
                            OR Login IN ('') /* список исключаемых логинов */
                    )
                ) AS vse_aki ON vse_aki.`Group` = abook_ak.`Group`
            ) AS abook_users
        INNER JOIN (
            SELECT *
            FROM mt5r2.mt5_deals
            WHERE (
                `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
                OR (`Action` = 2 AND Comment IN ('indemnification', 'compensation', 'Drawdown compensation', 'Bonus transfer', 'Swapfree compensation', 'Balance indemnification'))
                OR (`Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2) AND Comment LIKE '%Swap Free Commission')
            ) AND DATE(`Time`) BETWEEN '{start}' AND '{end}'
        ) AS pl_comis_kompens ON pl_comis_kompens.Login = abook_users.Login
    ) AS PnL_ABOOK_USD_side_client_realized,

    /* PnL для CBOOK */
    (
        SELECT 
            IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0) AS PnL_CBOOK_USD_side_client_realized
        FROM 
            (
                SELECT vse_aki.*
                FROM (
                    SELECT `Group`
                    FROM mt5r2.mt5_groups
                    WHERE `group` LIKE 'real\\\\active_Abook\\\\Abook%' AND `group` LIKE '%_percent' AND Currency = 'USD'
                ) AS c_bbook_ak
                INNER JOIN (
                    SELECT *
                    FROM mt5r2.mt5_users
                    WHERE Login NOT IN (
                        SELECT Login
                        FROM mt5r2.mt5_users
                        WHERE FirstName IN ('FirstName', 'First Admin' /* добавьте все исключения */) 
                            OR FirstName LIKE 'Bbook %'
                            OR FirstName LIKE 'Abook %'
                            OR FirstName LIKE 'test %'
                            OR FirstName LIKE '% test'
                            OR Login IN ('') /* список исключаемых логинов */
                    )
                ) AS vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
            ) AS c_bbook_users
        INNER JOIN (
            SELECT *
            FROM mt5r2.mt5_deals
            WHERE (
                `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
                OR (`Action` = 2 AND Comment IN ('indemnification', 'compensation', 'Drawdown compensation', 'Bonus transfer', 'Swapfree compensation', 'Balance indemnification'))
                OR (`Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2) AND Comment LIKE '%Swap Free Commission')
            ) AND DATE(`Time`) BETWEEN '{start}' AND '{end}'
        ) AS pl_comis_kompens ON pl_comis_kompens.Login = c_bbook_users.Login
    ) AS PnL_CBOOK_USD_side_client_realized;
'''
,

"NEO_BALANCE" : '''
WITH vse_aki AS (
    /*начало Блок все логины с исключениями*/
    SELECT *
    FROM mt5r1.mt5_users
    WHERE Login NOT IN (
        /*начало Блок исключений из статистики*/
        SELECT Login
        FROM mt5r1.mt5_users
        WHERE FirstName IN (
            'First Admin', 
            'FastMT Admin 1', 
            'FastMT Admin 2', 
            'FastMT Admin 3', 
            'FastMT Admin 4', 
            'FastMT Admin 5', 
            'FastMT Admin 6', 
            'Neobit Admin 1', 
            'Neobit Admin 2', 
            'FastMT Monitoring', 
            'FastMT Backup', 
            'TestVadim', 
            'MT5 Monitor', 
            'Web API Personal Area Account', 
            'MT5BBProGateway', 
            'MT5BBProFeeder', 
            'FX manager sub', 
            'FX manager din', 
            'FX manager nak', 
            'FX manager nov', 
            'FX manager ova', 
            'FX manager shin', 
            'FX manager rnov', 
            'FX manager hov', 
            'Data Export Manager', 
            'FX manager 2112', 
            'FX manager 2114', 
            'FX manager otov 2115', 
            'FX manager 2116', 
            'FX manager sich 2117', 
            'FX manager 2118 up partner', 
            'FX manager 2119 up2 clients', 
            'FX manager 2120 Atimex', 
            'Manager_view only', 
            'Manager_Kuznecov Vladimir', 
            'FX manager 2123', 
            'FX manager 2124', 
            'FX manager 2125', 
            'FX manager 2126 lcov', 
            'BrokerPilot', 
            'FX manager 2128', 
            'FX manager 2129', 
            'FX manager 2130', 
            'FX manager 2131', 
            'FX_Manager_2132', 
            'fsd gsdfg gdfs', 
            'Test Test ', 
            'Sabodin Aleksandr test Sergeevich', 
            'TestIossub TestVadim Petrovich', 
            'TestLukashin Dmitry Gennadievich', 
            'Testov Test ', 
            'Petukhov test Alexander test Alex test', 
            'TestSmirnov Ivan Valerevich', 
            'Test Aleksandr test ', 
            'Petukhov Alexander sdfsdfsdf', 
            'Test Test Follower', 
            'Test Oleg Master', 
            'TestIvan', 
            'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс)', 
            'A-Book Client Position', 
            'B-Book Client Position', 
            'A-Book and B-Book Client Position', 
            'TestSmirnov Ivan', 
            'Test Andrei ', 
            'Test cent', 
            'Monitor', 
            'Bruver TestSergeyTest ', 
            'B-Book cent Client Position', 
            'Test Swap Free netting платно', 
            'Test Centroid Trading', 
            'Test admin', 
            'Test Stopout Plugin', 
            'Test Stopout Plugin 2', 
            'Test Stopout Plugin 3', 
            'Abook 50 процентов 345019', 
            'Bbook 50 процентов 900778', 
            'TestBruv Serg ', 
            'Тест Бородина Ксения ', 
            'Test Svetlana Fatima ', 
            'Kagirova Venera Test ', 
            'Te_s', 
            'Test', 
            'TestBruv TestSerg ', 
            'Abook 20 процентов 345019', 
            'Test PAMM 1', 
            'Test PAMM 2', 
            'Test PAMM 3', 
            'gastinets', 
            'gastinets+1', 
            'gastinets+2', 
            'kdronof', 
            'kdronof+1', 
            'kdronof+2', 
            'testing.process', 
            'testing.process+1', 
            'testing.process+2', 
            'sergey', 
            'sergey 2', 
            'sergey test deposit', 
            'sergey deposit test 2', 
            'sergey test 3', 
            'Test Borodina Kseniya Vadimovna', 
            'test1 as', 
            'test D', 
            'sergey test ', 
            'For site (take swaps)', 
            'FastMT_Test', 
            'Abook ретрантсляция логина 901412_901396', 
            'A S test test', 
            'Sasha P test test', 
            'Vladimir Test Test', 
            'Serj Test Test', 
            'Test Gusenkov Sergey ', 
            'Serj', 
            'Alex P Test1', 
            'Ксю', 
            'Gas test', 
            'Gas test2', 
            'Gas test3', 
            'Serj2', 
            'Test Sophia', 
            'Test Kagirova Venera Ramzis', 
            'Gas test5', 
            'test21212', 
            'test денег нет но вы держитесь', 
            'Test Borodina ksenia test ', 
            'Serj3', 
            '123', 
            'Test Redko Svetlana ', 
            'Nik Test 1 Master', 
            'Nik Test 2 Follower', 
            'Serj4', 
            'TestBruver TestSerg ', 
            'Serj5', 
            'test1', 
            'B2B PL скольжения в карман компании(только плюсовые)XAUUSD.vol', 
            'Денег нет но вы держитесь', 
            'Serj8', 
            'Serj9'
        ) 
        OR FirstName LIKE 'Bbook %' 
        OR FirstName LIKE 'Abook %' 
        OR FirstName LIKE 'test %' 
        OR FirstName LIKE '% test' 
        OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
        /*конец Блок исключений из статистики*/
    )
    /*конец Блок все логины с исключениями*/
)
SELECT 
    ROUND((SELECT SUM(bbook_users.balance) 
     FROM (
         SELECT vse_aki.*
         FROM (
             SELECT `Group` 
             FROM mt5r1.mt5_groups
             WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' AND Currency ='USD'
         ) AS bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
     ) AS bbook_users) +
    (SELECT SUM(abook_users.balance) 
     FROM (
         SELECT vse_aki.*
         FROM (
             SELECT `Group` 
             FROM mt5r1.mt5_groups
             WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` NOT LIKE '%_percent' AND Currency ='USD'
         ) AS abook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
     ) AS abook_users) +
    (SELECT ROUND(SUM(cent_bbook_users.balance) * 0.01, 2) 
     FROM (
         SELECT vse_aki.*
         FROM (
             SELECT `Group` 
             FROM mt5r1.mt5_groups
             WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency ='USC'
         ) AS cent_bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
     ) AS cent_bbook_users) +
    (SELECT SUM(c_bbook_users.balance) 
     FROM (
         SELECT vse_aki.*
         FROM (
             SELECT `Group` 
             FROM mt5r1.mt5_groups
             WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` LIKE '%_percent' AND Currency ='USD'
         ) AS c_bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
     ) AS c_bbook_users), 2) AS total_balance_USD,
/**/     
    (SELECT SUM(bbook_users.balance) 
     FROM (
         SELECT vse_aki.*
         FROM (
             SELECT `Group` 
             FROM mt5r1.mt5_groups
             WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' AND Currency ='USD'
         ) AS bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
     ) AS bbook_users) AS balance_USD_BBOOK,
/**/      
    (SELECT SUM(abook_users.balance) 
     FROM (
         SELECT vse_aki.*
         FROM (
             SELECT `Group` 
             FROM mt5r1.mt5_groups
             WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` NOT LIKE '%_percent' AND Currency ='USD'
         ) AS abook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
     ) AS abook_users) AS balance_USD_ABOOK,
/**/      
    (SELECT ROUND(SUM(cent_bbook_users.balance) * 0.01, 2) 
     FROM (
         SELECT vse_aki.*
         FROM (
             SELECT `Group` 
             FROM mt5r1.mt5_groups
             WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency ='USC'
         ) AS cent_bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
     ) AS cent_bbook_users) AS balance_USD_Cent_BBOOK,
/**/      
    (SELECT SUM(c_bbook_users.balance) 
     FROM (
         SELECT vse_aki.*
         FROM (
             SELECT `Group` 
             FROM mt5r1.mt5_groups
             WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` LIKE '%_percent' AND Currency ='USD'
         ) AS c_bbook_ak 
         INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
     ) AS c_bbook_users) AS balance_USD_CBOOK;'''
,

"NEO_EKVITY" : '''
    WITH vse_aki AS (
        /*начало Блок все логины с исключениями*/
        SELECT *
        FROM mt5r1.mt5_users
        WHERE Login NOT IN (
            /*начало Блок исключений из статистики*/
            SELECT Login
            FROM mt5r1.mt5_users
            WHERE FirstName IN (
                'First Admin', 
                'FastMT Admin 1', 
                'FastMT Admin 2', 
                'FastMT Admin 3', 
                'FastMT Admin 4', 
                'FastMT Admin 5', 
                'FastMT Admin 6', 
                'Neobit Admin 1', 
                'Neobit Admin 2', 
                'FastMT Monitoring', 
                'FastMT Backup', 
                'TestVadim', 
                'MT5 Monitor', 
                'Web API Personal Area Account', 
                'MT5BBProGateway', 
                'MT5BBProFeeder', 
                'FX manager sub', 
                'FX manager din', 
                'FX manager nak', 
                'FX manager nov', 
                'FX manager ova', 
                'FX manager shin', 
                'FX manager rnov', 
                'FX manager hov', 
                'Data Export Manager', 
                'FX manager 2112', 
                'FX manager 2114', 
                'FX manager otov 2115', 
                'FX manager 2116', 
                'FX manager sich 2117', 
                'FX manager 2118 up partner', 
                'FX manager 2119 up2 clients', 
                'FX manager 2120 Atimex', 
                'Manager_view only', 
                'Manager_Kuznecov Vladimir', 
                'FX manager 2123', 
                'FX manager 2124', 
                'FX manager 2125', 
                'FX manager 2126 lcov', 
                'BrokerPilot', 
                'FX manager 2128', 
                'FX manager 2129', 
                'FX manager 2130', 
                'FX manager 2131', 
                'FX_Manager_2132', 
                'fsd gsdfg gdfs', 
                'Test Test ', 
                'Sabodin Aleksandr test Sergeevich', 
                'TestIossub TestVadim Petrovich', 
                'TestLukashin Dmitry Gennadievich', 
                'Testov Test ', 
                'Petukhov test Alexander test Alex test', 
                'TestSmirnov Ivan Valerevich', 
                'Test Aleksandr test ', 
                'Petukhov Alexander sdfsdfsdf', 
                'Test Test Follower', 
                'Test Oleg Master', 
                'TestIvan', 
                'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс)', 
                'A-Book Client Position', 
                'B-Book Client Position', 
                'A-Book and B-Book Client Position', 
                'TestSmirnov Ivan', 
                'Test Andrei ', 
                'Test cent', 
                'Monitor', 
                'Bruver TestSergeyTest ', 
                'B-Book cent Client Position', 
                'Test Swap Free netting платно', 
                'Test Centroid Trading', 
                'Test admin', 
                'Test Stopout Plugin', 
                'Test Stopout Plugin 2', 
                'Test Stopout Plugin 3', 
                'Abook 50 процентов 345019', 
                'Bbook 50 процентов 900778', 
                'TestBruv Serg ', 
                'Тест Бородина Ксения ', 
                'Test Svetlana Fatima ', 
                'Kagirova Venera Test ', 
                'Te_s', 
                'Test', 
                'TestBruv TestSerg ', 
                'Abook 20 процентов 345019', 
                'Test PAMM 1', 
                'Test PAMM 2', 
                'Test PAMM 3', 
                'gastinets', 
                'gastinets+1', 
                'gastinets+2', 
                'kdronof', 
                'kdronof+1', 
                'kdronof+2', 
                'testing.process', 
                'testing.process+1', 
                'testing.process+2', 
                'sergey', 
                'sergey 2', 
                'sergey test deposit', 
                'sergey deposit test 2', 
                'sergey test 3', 
                'Test Borodina Kseniya Vadimovna', 
                'test1 as', 
                'test D', 
                'sergey test ', 
                'For site (take swaps)', 
                'FastMT_Test', 
                'Abook ретрантсляция логина 901412_901396', 
                'A S test test', 
                'Sasha P test test', 
                'Vladimir Test Test', 
                'Serj Test Test', 
                'Test Gusenkov Sergey ', 
                'Serj', 
                'Alex P Test1', 
                'Ксю', 
                'Gas test', 
                'Gas test2', 
                'Gas test3', 
                'Serj2', 
                'Test Sophia', 
                'Test Kagirova Venera Ramzis', 
                'Gas test5', 
                'test21212', 
                'test денег нет но вы держитесь', 
                'Test Borodina ksenia test ', 
                'Serj3', 
                '123', 
                'Test Redko Svetlana ', 
                'Nik Test 1 Master', 
                'Nik Test 2 Follower', 
                'Serj4', 
                'TestBruver TestSerg ', 
                'Serj5', 
                'test1', 
                'B2B PL скольжения в карман компании(только плюсовые)XAUUSD.vol', 
                'Денег нет но вы держитесь', 
                'Serj8', 
                'Serj9'
            ) 
            OR FirstName LIKE 'Bbook %' 
            OR FirstName LIKE 'Abook %' 
            OR FirstName LIKE 'test %' 
            OR FirstName LIKE '% test' 
            OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
            /*конец Блок исключений из статистики*/
        )
        /*конец Блок все логины с исключениями*/
    ) 
    select 
    ((
    /*начало Блок эквити с кредитом ббук на фильтрах*/
    select ROUND(((SUM(bbook_users.Balance))+(SUM(bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
    from (
    		/*начало Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
    		select vse_aki.*
    		from (
    				/*начало Блок ббук группы автоматика опеределения*/
    				SELECT `Group` 
    				FROM mt5r1.mt5_groups
    				WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' and Currency ='USD'
    				/*конец Блок ббук группы автоматика опеределения*/
    			) as bbook_ak 
    		inner join vse_aki on vse_aki.`Group`=bbook_ak.`Group`
    		/*конец Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
    	) as bbook_users 
    Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=bbook_users.Login
    /*конец Блок эквити с кредитом ббук на фильтрах*/) + 
    /**/
    (
    /*начало Блок эквити абук с кредитами на фильтрах*/
    select ROUND(((SUM(abook_users.balance))+(SUM(abook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
    from (
    		/*начало Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
    		select vse_aki.*
    		from (
    				/*конец Блок полные абук группы автоматика опеределения*/
    				SELECT `Group` 
    				FROM mt5r1.mt5_groups
    				WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` not like '%_percent' and Currency ='USD'
    				/*конец Блок полные абук группы автоматика опеределения*/
    			) as abook_ak 
    		inner join vse_aki on vse_aki.`Group`=abook_ak.`Group`
    		/*конец Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
    	) as abook_users
    Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=abook_users.Login
    /*конецБлок эквити абук с кредитами на фильтрах*/) +  
    /**/
    (
    /*начало Блок эквити с кредитом цент ббук на фильтрах*/
    select ROUND((((SUM(cent_bbook_users.balance))+(SUM(cent_bbook_users.Credit))+(IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0)))*0.01),2)
    from (
    		/*начало Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
    		select vse_aki.*
    		from (
    				/*конец Блок цент ббук группы автоматика опеределения*/
    				SELECT `Group` 
    				FROM mt5r1.mt5_groups
    				WHERE `group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC'
    				/*конец Блок цент ббук группы автоматика опеределения*/
    			) as cent_bbook_ak 
    		inner join vse_aki on vse_aki.`Group`=cent_bbook_ak.`Group`
    		/*конец Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
    	) as cent_bbook_users 
    Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=cent_bbook_users.Login
    /*конец Блок эквити с кредитом цент ббук на фильтрах*/) +  
    /**/ 
    (
    /*начало Блок эквити цбук все цбук на фильтрах*/
    select ROUND(((SUM(c_bbook_users.Balance))+(SUM(c_bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2) 
    from (
    		/*начало Блок все цбук группы юзеры таблица мт5 юзерс на фильтрах*/
    		select vse_aki.*
    		from (
    				/*конец Блок все цбук группы автоматика опеределения*/
    				SELECT `Group` 
    				FROM mt5r1.mt5_groups
    				WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` like '%_percent' and Currency ='USD'
    				/*конец все цбук группы автоматика опеределения*/
    			) as c_bbook_ak 
    		inner join vse_aki on vse_aki.`Group`=c_bbook_ak.`Group`
    		/*конец Блок все цбук юзеры таблица мт5 юзерс на фильтрах*/
    	) as c_bbook_users
    Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=c_bbook_users.Login
    /*конец Блок эквити цбук все цбук на фильтрах*/)) as total_equity_s_credit_USD, 
    (
    /*начало Блок эквити с кредитом ббук на фильтрах*/
    select ROUND(((SUM(bbook_users.Balance))+(SUM(bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
    from (
    		/*начало Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
    		select vse_aki.*
    		from (
    				/*начало Блок ббук группы автоматика опеределения*/
    				SELECT `Group` 
    				FROM mt5r1.mt5_groups
    				WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' and Currency ='USD'
    				/*конец Блок ббук группы автоматика опеределения*/
    			) as bbook_ak 
    		inner join vse_aki on vse_aki.`Group`=bbook_ak.`Group`
    		/*конец Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
    	) as bbook_users 
    Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=bbook_users.Login
    /*конец Блок эквити с кредитом ббук на фильтрах*/) as Equity_s_credit_USD_BBOOK, 
    /**/
    (
    /*начало Блок эквити абук с кредитами на фильтрах*/
    select ROUND(((SUM(abook_users.balance))+(SUM(abook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2)
    from (
    		/*начало Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
    		select vse_aki.*
    		from (
    				/*конец Блок полные абук группы автоматика опеределения*/
    				SELECT `Group` 
    				FROM mt5r1.mt5_groups
    				WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` not like '%_percent' and Currency ='USD'
    				/*конец Блок полные абук группы автоматика опеределения*/
    			) as abook_ak 
    		inner join vse_aki on vse_aki.`Group`=abook_ak.`Group`
    		/*конец Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
    	) as abook_users
    Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=abook_users.Login
    /*конецБлок эквити абук с кредитами на фильтрах*/) as Equity_s_credit_USD_ABOOK, 
    /**/
    (
    /*начало Блок эквити с кредитом цент ббук на фильтрах*/
    select ROUND((((SUM(cent_bbook_users.balance))+(SUM(cent_bbook_users.Credit))+(IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0)))*0.01),2)
    from (
    		/*начало Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
    		select vse_aki.*
    		from (
    				/*конец Блок цент ббук группы автоматика опеределения*/
    				SELECT `Group` 
    				FROM mt5r1.mt5_groups
    				WHERE `group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC'
    				/*конец Блок цент ббук группы автоматика опеределения*/
    			) as cent_bbook_ak 
    		inner join vse_aki on vse_aki.`Group`=cent_bbook_ak.`Group`
    		/*конец Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
    	) as cent_bbook_users 
    Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=cent_bbook_users.Login
    /*конец Блок эквити с кредитом цент ббук на фильтрах*/) as Equity_s_credit_USD_Cent_BBOOK, 
    /**/ 
    (
    /*начало Блок эквити цбук все цбук на фильтрах*/
    select ROUND(((SUM(c_bbook_users.Balance))+(SUM(c_bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2) 
    from (
    		/*начало Блок все цбук группы юзеры таблица мт5 юзерс на фильтрах*/
    		select vse_aki.*
    		from (
    				/*конец Блок все цбук группы автоматика опеределения*/
    				SELECT `Group` 
    				FROM mt5r1.mt5_groups
    				WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` like '%_percent' and Currency ='USD'
    				/*конец все цбук группы автоматика опеределения*/
    			) as c_bbook_ak 
    		inner join vse_aki on vse_aki.`Group`=c_bbook_ak.`Group`
    		/*конец Блок все цбук юзеры таблица мт5 юзерс на фильтрах*/
    	) as c_bbook_users
    Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=c_bbook_users.Login
    /*конец Блок эквити цбук все цбук на фильтрах*/) as Equity_s_credit_USD_CBOOK
    ;'''
,
"NEO_PNL" : f'''
    WITH 
    vse_aki AS (
        SELECT *
        FROM mt5r1.mt5_users
        WHERE Login NOT IN (
            SELECT Login
            FROM mt5r1.mt5_users
            WHERE FirstName IN (
                'First Admin', 
                'FastMT Admin 1', 
                'FastMT Admin 2', 
                'FastMT Admin 3', 
                'FastMT Admin 4', 
                'FastMT Admin 5', 
                'FastMT Admin 6', 
                'Neobit Admin 1', 
                'Neobit Admin 2', 
                'FastMT Monitoring', 
                'FastMT Backup', 
                'TestVadim', 
                'MT5 Monitor', 
                'Web API Personal Area Account', 
                'MT5BBProGateway', 
                'MT5BBProFeeder', 
                'FX manager sub', 
                'FX manager din', 
                'FX manager nak', 
                'FX manager nov', 
                'FX manager ova', 
                'FX manager shin', 
                'FX manager rnov', 
                'FX manager hov', 
                'Data Export Manager', 
                'FX manager 2112', 
                'FX manager 2114', 
                'FX manager otov 2115', 
                'FX manager 2116', 
                'FX manager sich 2117', 
                'FX manager 2118 up partner', 
                'FX manager 2119 up2 clients', 
                'FX manager 2120 Atimex', 
                'Manager_view only', 
                'Manager_Kuznecov Vladimir', 
                'FX manager 2123', 
                'FX manager 2124', 
                'FX manager 2125', 
                'FX manager 2126 lcov', 
                'BrokerPilot', 
                'FX manager 2128', 
                'FX manager 2129', 
                'FX manager 2130', 
                'FX manager 2131', 
                'FX_Manager_2132', 
                'fsd gsdfg gdfs', 
                'Test Test ', 
                'Sabodin Aleksandr test Sergeevich', 
                'TestIossub TestVadim Petrovich', 
                'TestLukashin Dmitry Gennadievich', 
                'Testov Test ', 
                'Petukhov test Alexander test Alex test', 
                'TestSmirnov Ivan Valerevich', 
                'Test Aleksandr test ', 
                'Petukhov Alexander sdfsdfsdf', 
                'Test Test Follower', 
                'Test Oleg Master', 
                'TestIvan', 
                'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс)', 
                'A-Book Client Position', 
                'B-Book Client Position', 
                'A-Book and B-Book Client Position', 
                'TestSmirnov Ivan', 
                'Test Andrei ', 
                'Test cent', 
                'Monitor', 
                'Bruver TestSergeyTest ', 
                'B-Book cent Client Position', 
                'Test Swap Free netting платно', 
                'Test Centroid Trading', 
                'Test admin', 
                'Test Stopout Plugin', 
                'Test Stopout Plugin 2', 
                'Test Stopout Plugin 3', 
                'Abook 50 процентов 345019', 
                'Bbook 50 процентов 900778', 
                'TestBruv Serg ', 
                'Тест Бородина Ксения ', 
                'Test Svetlana Fatima ', 
                'Kagirova Venera Test ', 
                'Te_s', 
                'Test', 
                'TestBruv TestSerg ', 
                'Abook 20 процентов 345019', 
                'Test PAMM 1', 
                'Test PAMM 2', 
                'Test PAMM 3', 
                'gastinets', 
                'gastinets+1', 
                'gastinets+2', 
                'kdronof', 
                'kdronof+1', 
                'kdronof+2', 
                'testing.process', 
                'testing.process+1', 
                'testing.process+2', 
                'sergey', 
                'sergey 2', 
                'sergey test deposit', 
                'sergey deposit test 2', 
                'sergey test 3', 
                'Test Borodina Kseniya Vadimovna', 
                'test1 as', 
                'test D', 
                'sergey test ', 
                'For site (take swaps)', 
                'FastMT_Test', 
                'Abook ретрантсляция логина 901412_901396', 
                'A S test test', 
                'Sasha P test test', 
                'Vladimir Test Test', 
                'Serj Test Test', 
                'Test Gusenkov Sergey ', 
                'Serj', 
                'Alex P Test1', 
                'Ксю', 
                'Gas test', 
                'Gas test2', 
                'Gas test3', 
                'Serj2', 
                'Test Sophia', 
                'Test Kagirova Venera Ramzis', 
                'Gas test5', 
                'test21212', 
                'test денег нет но вы держитесь', 
                'Test Borodina ksenia test ', 
                'Serj3', 
                '123', 
                'Test Redko Svetlana ', 
                'Nik Test 1 Master', 
                'Nik Test 2 Follower', 
                'Serj4', 
                'TestBruver TestSerg ', 
                'Serj5', 
                'test1', 
                'B2B PL скольжения в карман компании(только плюсовые)XAUUSD.vol', 
                'Денег нет но вы держитесь', 
                'Serj8', 
                'Serj9'
            ) 
            OR FirstName LIKE 'Bbook %' 
            OR FirstName LIKE 'Abook %' 
            OR FirstName LIKE 'test %' 
            OR FirstName LIKE '% test' 
            OR Login IN ('')
        )
    ),
    pl_comis_kompens AS (
        SELECT *
        FROM mt5r1.mt5_deals
        WHERE (
            `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
            OR (
                `Action` = 2
                AND (
                    Comment IN (
                        'indemnification',
                        'compensation',
                        'Drawdown compensation',
                        'Bonus transfer',
                        'bonus transfer',
                        'Swapfree compensation',
                        'balance indemnification',
                        'Balance indemnification'
                    )
                )
            )
            OR (
                `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2)
                AND Comment LIKE '%Swap Free Commission'
            )
        )
        AND DATE(`Time`) BETWEEN '{start}' AND '{end}'
    )
    select 
    ((SELECT 
        IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    FROM (
        SELECT vse_aki.*
        FROM (
            SELECT `Group` 
            FROM mt5r1.mt5_groups
            WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' AND Currency = 'USD'
        ) AS bbook_ak 
        INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
    ) AS bbook_users 
    INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = bbook_users.Login) + 
    (SELECT 
        IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    FROM (
        SELECT vse_aki.*
        FROM (
            SELECT `Group` 
            FROM mt5r1.mt5_groups
            WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` NOT LIKE '%_percent' AND Currency = 'USD'
        ) AS abook_ak 
        INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
    ) AS abook_users 
    INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = abook_users.Login) + 
    (SELECT 
        ROUND(IFNULL((SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee)) * 0.01, 0), 2)
    FROM (
        SELECT vse_aki.*
        FROM (
            SELECT `Group` 
            FROM mt5r1.mt5_groups
            WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency = 'USC'
        ) AS cent_bbook_ak 
        INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
    ) AS cent_bbook_users 
    INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = cent_bbook_users.Login) + 
    (SELECT 
        IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    FROM (
        SELECT vse_aki.*
        FROM (
            SELECT `Group` 
            FROM mt5r1.mt5_groups
            WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` LIKE '%_percent' AND Currency = 'USD'
        ) AS c_bbook_ak 
        INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
    ) AS c_bbook_users 
    INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = c_bbook_users.Login)) as Total_PnL_USD_side_client_realized, 
    (SELECT 
        IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    FROM (
        SELECT vse_aki.*
        FROM (
            SELECT `Group` 
            FROM mt5r1.mt5_groups
            WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' AND Currency = 'USD'
        ) AS bbook_ak 
        INNER JOIN vse_aki ON vse_aki.`Group` = bbook_ak.`Group`
    ) AS bbook_users 
    INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = bbook_users.Login) AS PnL_BBOOK_USD_side_client_realized, 
    /**/
    (SELECT 
        IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    FROM (
        SELECT vse_aki.*
        FROM (
            SELECT `Group` 
            FROM mt5r1.mt5_groups
            WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` NOT LIKE '%_percent' AND Currency = 'USD'
        ) AS abook_ak 
        INNER JOIN vse_aki ON vse_aki.`Group` = abook_ak.`Group`
    ) AS abook_users 
    INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = abook_users.Login) AS PnL_ABOOK_USD_side_client_realized, 
    /**/
    (SELECT 
        ROUND(IFNULL((SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee)) * 0.01, 0), 2)
    FROM (
        SELECT vse_aki.*
        FROM (
            SELECT `Group` 
            FROM mt5r1.mt5_groups
            WHERE `group` LIKE 'real\\\\cent\\\\bbook%' AND Currency = 'USC'
        ) AS cent_bbook_ak 
        INNER JOIN vse_aki ON vse_aki.`Group` = cent_bbook_ak.`Group`
    ) AS cent_bbook_users 
    INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = cent_bbook_users.Login) AS PnL_Cent_BBOOK_USD_side_client_realized, 
    /**/
    (SELECT 
        IFNULL(SUM(pl_comis_kompens.Profit + pl_comis_kompens.Storage + pl_comis_kompens.Commission + pl_comis_kompens.Fee), 0)
    FROM (
        SELECT vse_aki.*
        FROM (
            SELECT `Group` 
            FROM mt5r1.mt5_groups
            WHERE `group` LIKE 'real\\\\abook\\\\abook%' AND `group` LIKE '%_percent' AND Currency = 'USD'
        ) AS c_bbook_ak 
        INNER JOIN vse_aki ON vse_aki.`Group` = c_bbook_ak.`Group`
    ) AS c_bbook_users 
    INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = c_bbook_users.Login) AS PnL_CBOOK_USD_side_client_realized;'''

}

    return DICT[zapros]
