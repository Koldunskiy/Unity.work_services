COMMON_EQVITY = '''
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

ABBOK_EQVITY = '''
/*начало Блок эквити абук с кредитами на фильтрах*/
select ROUND(((SUM(abook_users.balance))+(SUM(abook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2) as Equity_s_credit_USD_ABOOK
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
		inner join (
					/*начало Блок все логины с исключениями*/
					select *
					from mt5r1.mt5_users
					where Login not in (
										/*начало Блок исключений из статистики*/
										select Login
										from mt5r1.mt5_users
										where FirstName in ( 
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
															'Serj9') 
											  OR FirstName LIKE 'Bbook %' 
										      OR FirstName LIKE 'Abook %' 
										      OR FirstName LIKE 'test %' 
										      OR FirstName LIKE '% test' 
										      OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
										      /*конец Блок исключений из статистики*/
										)
					/*конец Блок все логины с исключениями*/) as vse_aki on vse_aki.`Group`=abook_ak.`Group`
		/*конец Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
	) as abook_users
Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=abook_users.Login
/*конецБлок эквити абук с кредитами на фильтрах*/
;'''

BBOOK_EQVITY = '''
/*начало Блок эквити с кредитом ббук на фильтрах*/
select ROUND(((SUM(bbook_users.Balance))+(SUM(bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2) as Equity_s_credit_USD_BBOOK
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
		inner join (
					/*начало Блок все логины с исключениями*/
					select *
					from mt5r1.mt5_users
					where Login not in (
										/*начало Блок исключений из статистики*/
										select Login
										from mt5r1.mt5_users
										where FirstName in ( 
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
															'Serj9') 
											  OR FirstName LIKE 'Bbook %' 
										      OR FirstName LIKE 'Abook %' 
										      OR FirstName LIKE 'test %' 
										      OR FirstName LIKE '% test' 
										      OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
										      /*конец Блок исключений из статистики*/
										)
					/*конец Блок все логины с исключениями*/) as vse_aki on vse_aki.`Group`=bbook_ak.`Group`
		/*конец Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
	) as bbook_users 
Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=bbook_users.Login
/*конец Блок эквити с кредитом ббук на фильтрах*/
;
'''

CBOOK_EQVITY = '''
/*начало Блок эквити цбук все цбук на фильтрах*/
select ROUND(((SUM(c_bbook_users.Balance))+(SUM(c_bbook_users.Credit)))+IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0),2) as Equity_s_credit_USD_CBOOK
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
		inner join (
					/*начало Блок все логины с исключениями*/
					select *
					from mt5r1.mt5_users
					where Login not in (
										/*начало Блок исключений из статистики*/
										select Login
										from mt5r1.mt5_users
										where FirstName in ( 
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
															'Serj9') 
											  OR FirstName LIKE 'Bbook %' 
										      OR FirstName LIKE 'Abook %' 
										      OR FirstName LIKE 'test %' 
										      OR FirstName LIKE '% test' 
										      OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
										      /*конец Блок исключений из статистики*/
										)
					/*конец Блок все логины с исключениями*/) as vse_aki on vse_aki.`Group`=c_bbook_ak.`Group`
		/*конец Блок все цбук юзеры таблица мт5 юзерс на фильтрах*/
	) as c_bbook_users
Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=c_bbook_users.Login
/*конец Блок эквити цбук все цбук на фильтрах*/
;
'''

CENT_BOOK_EQVITY = '''
/*начало Блок эквити с кредитом цент ббук на фильтрах*/
select ROUND((((SUM(cent_bbook_users.balance))+(SUM(cent_bbook_users.Credit))+(IFNULL((SUM(mt5_positions_group.profit_storage_pos)),0)))*0.01),2) as Equity_s_credit_USD_Cent_BBOOK
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
		inner join (
					/*начало Блок все логины с исключениями*/
					select *
					from mt5r1.mt5_users
					where Login not in (
										/*начало Блок исключений из статистики*/
										select Login
										from mt5r1.mt5_users
										where FirstName in ( 
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
															'Serj9') 
											  OR FirstName LIKE 'Bbook %' 
										      OR FirstName LIKE 'Abook %' 
										      OR FirstName LIKE 'test %' 
										      OR FirstName LIKE '% test' 
										      OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
										      /*конец Блок исключений из статистики*/
										)
					/*конец Блок все логины с исключениями*/) as vse_aki on vse_aki.`Group`=cent_bbook_ak.`Group`
		/*конец Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
	) as cent_bbook_users 
Left join (select Login, (IFNULL(SUM(Profit),0))+(IFNULL(SUM(Storage),0)) as profit_storage_pos from mt5r1.mt5_positions group by Login) as mt5_positions_group on mt5_positions_group.Login=cent_bbook_users.Login
/*конец Блок эквити с кредитом цент ббук на фильтрах*/
;
'''