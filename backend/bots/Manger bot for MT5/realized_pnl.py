

# COMMON_PNL = f'''
# WITH 
# vse_aki AS (
#     SELECT *
#     FROM mt5r1.mt5_users
#     WHERE Login NOT IN (
#         SELECT Login
#         FROM mt5r1.mt5_users
#         WHERE FirstName IN (
#             'First Admin', 
#             'FastMT Admin 1', 
#             'FastMT Admin 2', 
#             'FastMT Admin 3', 
#             'FastMT Admin 4', 
#             'FastMT Admin 5', 
#             'FastMT Admin 6', 
#             'Neobit Admin 1', 
#             'Neobit Admin 2', 
#             'FastMT Monitoring', 
#             'FastMT Backup', 
#             'TestVadim', 
#             'MT5 Monitor', 
#             'Web API Personal Area Account', 
#             'MT5BBProGateway', 
#             'MT5BBProFeeder', 
#             'FX manager sub', 
#             'FX manager din', 
#             'FX manager nak', 
#             'FX manager nov', 
#             'FX manager ova', 
#             'FX manager shin', 
#             'FX manager rnov', 
#             'FX manager hov', 
#             'Data Export Manager', 
#             'FX manager 2112', 
#             'FX manager 2114', 
#             'FX manager otov 2115', 
#             'FX manager 2116', 
#             'FX manager sich 2117', 
#             'FX manager 2118 up partner', 
#             'FX manager 2119 up2 clients', 
#             'FX manager 2120 Atimex', 
#             'Manager_view only', 
#             'Manager_Kuznecov Vladimir', 
#             'FX manager 2123', 
#             'FX manager 2124', 
#             'FX manager 2125', 
#             'FX manager 2126 lcov', 
#             'BrokerPilot', 
#             'FX manager 2128', 
#             'FX manager 2129', 
#             'FX manager 2130', 
#             'FX manager 2131', 
#             'FX_Manager_2132', 
#             'fsd gsdfg gdfs', 
#             'Test Test ', 
#             'Sabodin Aleksandr test Sergeevich', 
#             'TestIossub TestVadim Petrovich', 
#             'TestLukashin Dmitry Gennadievich', 
#             'Testov Test ', 
#             'Petukhov test Alexander test Alex test', 
#             'TestSmirnov Ivan Valerevich', 
#             'Test Aleksandr test ', 
#             'Petukhov Alexander sdfsdfsdf', 
#             'Test Test Follower', 
#             'Test Oleg Master', 
#             'TestIvan', 
#             'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс)', 
#             'A-Book Client Position', 
#             'B-Book Client Position', 
#             'A-Book and B-Book Client Position', 
#             'TestSmirnov Ivan', 
#             'Test Andrei ', 
#             'Test cent', 
#             'Monitor', 
#             'Bruver TestSergeyTest ', 
#             'B-Book cent Client Position', 
#             'Test Swap Free netting платно', 
#             'Test Centroid Trading', 
#             'Test admin', 
#             'Test Stopout Plugin', 
#             'Test Stopout Plugin 2', 
#             'Test Stopout Plugin 3', 
#             'Abook 50 процентов 345019', 
#             'Bbook 50 процентов 900778', 
#             'TestBruv Serg ', 
#             'Тест Бородина Ксения ', 
#             'Test Svetlana Fatima ', 
#             'Kagirova Venera Test ', 
#             'Te_s', 
#             'Test', 
#             'TestBruv TestSerg ', 
#             'Abook 20 процентов 345019', 
#             'Test PAMM 1', 
#             'Test PAMM 2', 
#             'Test PAMM 3', 
#             'gastinets', 
#             'gastinets+1', 
#             'gastinets+2', 
#             'kdronof', 
#             'kdronof+1', 
#             'kdronof+2', 
#             'testing.process', 
#             'testing.process+1', 
#             'testing.process+2', 
#             'sergey', 
#             'sergey 2', 
#             'sergey test deposit', 
#             'sergey deposit test 2', 
#             'sergey test 3', 
#             'Test Borodina Kseniya Vadimovna', 
#             'test1 as', 
#             'test D', 
#             'sergey test ', 
#             'For site (take swaps)', 
#             'FastMT_Test', 
#             'Abook ретрантсляция логина 901412_901396', 
#             'A S test test', 
#             'Sasha P test test', 
#             'Vladimir Test Test', 
#             'Serj Test Test', 
#             'Test Gusenkov Sergey ', 
#             'Serj', 
#             'Alex P Test1', 
#             'Ксю', 
#             'Gas test', 
#             'Gas test2', 
#             'Gas test3', 
#             'Serj2', 
#             'Test Sophia', 
#             'Test Kagirova Venera Ramzis', 
#             'Gas test5', 
#             'test21212', 
#             'test денег нет но вы держитесь', 
#             'Test Borodina ksenia test ', 
#             'Serj3', 
#             '123', 
#             'Test Redko Svetlana ', 
#             'Nik Test 1 Master', 
#             'Nik Test 2 Follower', 
#             'Serj4', 
#             'TestBruver TestSerg ', 
#             'Serj5', 
#             'test1', 
#             'B2B PL скольжения в карман компании(только плюсовые)XAUUSD.vol', 
#             'Денег нет но вы держитесь', 
#             'Serj8', 
#             'Serj9'
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
#     AND DATE(`Time`) BETWEEN {start} AND {end}
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
# INNER JOIN pl_comis_kompens ON pl_comis_kompens.Login = c_bbook_users.Login) AS PnL_CBOOK_USD_side_client_realized;'''

# # ABOOK_PNL = f'''
# # /*начало Блок Абук Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # select IFNULL(SUM(pl_comis_kompens.Profit+pl_comis_kompens.Storage+pl_comis_kompens.Commission+pl_comis_kompens.Fee),0) as PnL_ABOOK_USD_side_client_realized
# # FROM 
# #     (
# #     /*начало Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
# #         select vse_aki.*
# #         from (
# #                 /*конец Блок полные абук группы автоматика опеределения*/
# #                 SELECT `Group` 
# #                 FROM mt5r1.mt5_groups
# #                 WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` not like '%_percent' and Currency ='USD'
# #                 /*конец Блок полные абук группы автоматика опеределения*/
# #             ) as abook_ak 
# #         inner join (
# #                     /*начало Блок все логины с исключениями*/
# #                     select *
# #                     from mt5r1.mt5_users
# #                     where Login not in (
# #                                         /*начало Блок исключений из статистики*/
# #                                         select Login
# #                                         from mt5r1.mt5_users
# #                                         where FirstName in ( 
# #                                                             'First Admin', 
# #                                                             'FastMT Admin 1', 
# #                                                             'FastMT Admin 2', 
# #                                                             'FastMT Admin 3', 
# #                                                             'FastMT Admin 4', 
# #                                                             'FastMT Admin 5', 
# #                                                             'FastMT Admin 6', 
# #                                                             'Neobit Admin 1', 
# #                                                             'Neobit Admin 2', 
# #                                                             'FastMT Monitoring', 
# #                                                             'FastMT Backup', 
# #                                                             'TestVadim', 
# #                                                             'MT5 Monitor', 
# #                                                             'Web API Personal Area Account', 
# #                                                             'MT5BBProGateway', 
# #                                                             'MT5BBProFeeder', 
# #                                                             'FX manager sub', 
# #                                                             'FX manager din', 
# #                                                             'FX manager nak', 
# #                                                             'FX manager nov', 
# #                                                             'FX manager ova', 
# #                                                             'FX manager shin', 
# #                                                             'FX manager rnov', 
# #                                                             'FX manager hov', 
# #                                                             'Data Export Manager', 
# #                                                             'FX manager 2112', 
# #                                                             'FX manager 2114', 
# #                                                             'FX manager otov 2115', 
# #                                                             'FX manager 2116', 
# #                                                             'FX manager sich 2117', 
# #                                                             'FX manager 2118 up partner', 
# #                                                             'FX manager 2119 up2 clients', 
# #                                                             'FX manager 2120 Atimex', 
# #                                                             'Manager_view only', 
# #                                                             'Manager_Kuznecov Vladimir', 
# #                                                             'FX manager 2123', 
# #                                                             'FX manager 2124', 
# #                                                             'FX manager 2125', 
# #                                                             'FX manager 2126 lcov', 
# #                                                             'BrokerPilot', 
# #                                                             'FX manager 2128', 
# #                                                             'FX manager 2129', 
# #                                                             'FX manager 2130', 
# #                                                             'FX manager 2131', 
# #                                                             'FX_Manager_2132', 
# #                                                             'fsd gsdfg gdfs', 
# #                                                             'Test Test ', 
# #                                                             'Sabodin Aleksandr test Sergeevich', 
# #                                                             'TestIossub TestVadim Petrovich', 
# #                                                             'TestLukashin Dmitry Gennadievich', 
# #                                                             'Testov Test ', 
# #                                                             'Petukhov test Alexander test Alex test', 
# #                                                             'TestSmirnov Ivan Valerevich', 
# #                                                             'Test Aleksandr test ', 
# #                                                             'Petukhov Alexander sdfsdfsdf', 
# #                                                             'Test Test Follower', 
# #                                                             'Test Oleg Master', 
# #                                                             'TestIvan', 
# #                                                             'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс)', 
# #                                                             'A-Book Client Position', 
# #                                                             'B-Book Client Position', 
# #                                                             'A-Book and B-Book Client Position', 
# #                                                             'TestSmirnov Ivan', 
# #                                                             'Test Andrei ', 
# #                                                             'Test cent', 
# #                                                             'Monitor', 
# #                                                             'Bruver TestSergeyTest ', 
# #                                                             'B-Book cent Client Position', 
# #                                                             'Test Swap Free netting платно', 
# #                                                             'Test Centroid Trading', 
# #                                                             'Test admin', 
# #                                                             'Test Stopout Plugin', 
# #                                                             'Test Stopout Plugin 2', 
# #                                                             'Test Stopout Plugin 3', 
# #                                                             'Abook 50 процентов 345019', 
# #                                                             'Bbook 50 процентов 900778', 
# #                                                             'TestBruv Serg ', 
# #                                                             'Тест Бородина Ксения ', 
# #                                                             'Test Svetlana Fatima ', 
# #                                                             'Kagirova Venera Test ', 
# #                                                             'Te_s', 
# #                                                             'Test', 
# #                                                             'TestBruv TestSerg ', 
# #                                                             'Abook 20 процентов 345019', 
# #                                                             'Test PAMM 1', 
# #                                                             'Test PAMM 2', 
# #                                                             'Test PAMM 3', 
# #                                                             'gastinets', 
# #                                                             'gastinets+1', 
# #                                                             'gastinets+2', 
# #                                                             'kdronof', 
# #                                                             'kdronof+1', 
# #                                                             'kdronof+2', 
# #                                                             'testing.process', 
# #                                                             'testing.process+1', 
# #                                                             'testing.process+2', 
# #                                                             'sergey', 
# #                                                             'sergey 2', 
# #                                                             'sergey test deposit', 
# #                                                             'sergey deposit test 2', 
# #                                                             'sergey test 3', 
# #                                                             'Test Borodina Kseniya Vadimovna', 
# #                                                             'test1 as', 
# #                                                             'test D', 
# #                                                             'sergey test ', 
# #                                                             'For site (take swaps)', 
# #                                                             'FastMT_Test', 
# #                                                             'Abook ретрантсляция логина 901412_901396', 
# #                                                             'A S test test', 
# #                                                             'Sasha P test test', 
# #                                                             'Vladimir Test Test', 
# #                                                             'Serj Test Test', 
# #                                                             'Test Gusenkov Sergey ', 
# #                                                             'Serj', 
# #                                                             'Alex P Test1', 
# #                                                             'Ксю', 
# #                                                             'Gas test', 
# #                                                             'Gas test2', 
# #                                                             'Gas test3', 
# #                                                             'Serj2', 
# #                                                             'Test Sophia', 
# #                                                             'Test Kagirova Venera Ramzis', 
# #                                                             'Gas test5', 
# #                                                             'test21212', 
# #                                                             'test денег нет но вы держитесь', 
# #                                                             'Test Borodina ksenia test ', 
# #                                                             'Serj3', 
# #                                                             '123', 
# #                                                             'Test Redko Svetlana ', 
# #                                                             'Nik Test 1 Master', 
# #                                                             'Nik Test 2 Follower', 
# #                                                             'Serj4', 
# #                                                             'TestBruver TestSerg ', 
# #                                                             'Serj5', 
# #                                                             'test1', 
# #                                                             'B2B PL скольжения в карман компании(только плюсовые)XAUUSD.vol', 
# #                                                             'Денег нет но вы держитесь', 
# #                                                             'Serj8', 
# #                                                             'Serj9') 
# #                                             OR FirstName LIKE 'Bbook %' 
# #                                             OR FirstName LIKE 'Abook %' 
# #                                             OR FirstName LIKE 'test %' 
# #                                             OR FirstName LIKE '% test' 
# #                                             OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
# #                                             /*конец Блок исключений из статистики*/
# #                                         )
# #                     /*конец Блок все логины с исключениями*/) as vse_aki on vse_aki.`Group`=abook_ak.`Group`
# #         /*конец Блок все абук юзеры таблица мт5 юзерс на фильтрах*/
# #     ) as abook_users 
# # INNER JOIN (
# #             /*начало Блок Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# #             SELECT *
# #             FROM mt5r1.mt5_deals
# #             WHERE (
# #                 `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
# #                 OR (
# #                     `Action` = 2
# #                     AND (
# #                         Comment IN (
# #                             'indemnification',
# #                             'compensation',
# #                             'Drawdown compensation',
# #                             'Bonus transfer',
# #                             'bonus transfer',
# #                             'Swapfree compensation',
# #                             'balance indemnification',
# #                             'Balance indemnification'
# #                         )
# #                     )
# #                 )
# #                 OR (
# #                     `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2)
# #                     AND Comment LIKE '%Swap Free Commission'
# #                 )
# #             )
# #             AND DATE(`Time`) BETWEEN {start} AND {end}
# #             /*конец Блок Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # ) as pl_comis_kompens on pl_comis_kompens.Login=abook_users.Login
# # /*конец Блок Абук Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # ;'''

# # BBOOK_PNL = f'''
# # /*начало Блок Ббук Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # select IFNULL(SUM(pl_comis_kompens.Profit+pl_comis_kompens.Storage+pl_comis_kompens.Commission+pl_comis_kompens.Fee),0) as PnL_BBOOK_USD_side_client_realized
# # FROM 
# #     (
# #     /*начало Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/
# #     SELECT vse_aki.*
# #     FROM (
# #             /*конец Блок ббук группы автоматика опеределения*/
# #             SELECT `Group` 
# #             FROM mt5r1.mt5_groups
# #             WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' and Currency ='USD'
# #             /*конец Блок ббук группы автоматика опеределения*/
# #         ) as bbook_ak 
# #     INNER JOIN (
# #                 /*начало Блок все логины с исключениями*/
# #                 SELECT *
# #                 FROM mt5r1.mt5_users
# #                 WHERE Login NOT IN (
# #                                     /*начало Блок исключений из статистики*/
# #                                     SELECT Login
# #                                     FROM mt5r1.mt5_users
# #                                     WHERE FirstName IN ( 
# #                                                         'First Admin', 
# #                                                         'FastMT Admin 1', 
# #                                                         'FastMT Admin 2', 
# #                                                         'FastMT Admin 3', 
# #                                                         'FastMT Admin 4', 
# #                                                         'FastMT Admin 5', 
# #                                                         'FastMT Admin 6', 
# #                                                         'Neobit Admin 1', 
# #                                                         'Neobit Admin 2', 
# #                                                         'FastMT Monitoring', 
# #                                                         'FastMT Backup', 
# #                                                         'TestVadim', 
# #                                                         'MT5 Monitor', 
# #                                                         'Web API Personal Area Account', 
# #                                                         'MT5BBProGateway', 
# #                                                         'MT5BBProFeeder', 
# #                                                         'FX manager sub', 
# #                                                         'FX manager din', 
# #                                                         'FX manager nak', 
# #                                                         'FX manager nov', 
# #                                                         'FX manager ova', 
# #                                                         'FX manager shin', 
# #                                                         'FX manager rnov', 
# #                                                         'FX manager hov', 
# #                                                         'Data Export Manager', 
# #                                                         'FX manager 2112', 
# #                                                         'FX manager 2114', 
# #                                                         'FX manager otov 2115', 
# #                                                         'FX manager 2116', 
# #                                                         'FX manager sich 2117', 
# #                                                         'FX manager 2118 up partner', 
# #                                                         'FX manager 2119 up2 clients', 
# #                                                         'FX manager 2120 Atimex', 
# #                                                         'Manager_view only', 
# #                                                         'Manager_Kuznecov Vladimir', 
# #                                                         'FX manager 2123', 
# #                                                         'FX manager 2124', 
# #                                                         'FX manager 2125', 
# #                                                         'FX manager 2126 lcov', 
# #                                                         'BrokerPilot', 
# #                                                         'FX manager 2128', 
# #                                                         'FX manager 2129', 
# #                                                         'FX manager 2130', 
# #                                                         'FX manager 2131', 
# #                                                         'FX_Manager_2132', 
# #                                                         'fsd gsdfg gdfs', 
# #                                                         'Test Test ', 
# #                                                         'Sabodin Aleksandr test Sergeevich', 
# #                                                         'TestIossub TestVadim Petrovich', 
# #                                                         'TestLukashin Dmitry Gennadievich', 
# #                                                         'Testov Test ', 
# #                                                         'Petukhov test Alexander test Alex test', 
# #                                                         'TestSmirnov Ivan Valerevich', 
# #                                                         'Test Aleksandr test ', 
# #                                                         'Petukhov Alexander sdfsdfsdf', 
# #                                                         'Test Test Follower', 
# #                                                         'Test Oleg Master', 
# #                                                         'TestIvan', 
# #                                                         'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс)', 
# #                                                         'A-Book Client Position', 
# #                                                         'B-Book Client Position', 
# #                                                         'A-Book and B-Book Client Position', 
# #                                                         'TestSmirnov Ivan', 
# #                                                         'Test Andrei ', 
# #                                                         'Test cent', 
# #                                                         'Monitor', 
# #                                                         'Bruver TestSergeyTest ', 
# #                                                         'B-Book cent Client Position', 
# #                                                         'Test Swap Free netting платно', 
# #                                                         'Test Centroid Trading', 
# #                                                         'Test admin', 
# #                                                         'Test Stopout Plugin', 
# #                                                         'Test Stopout Plugin 2', 
# #                                                         'Test Stopout Plugin 3', 
# #                                                         'Abook 50 процентов 345019', 
# #                                                         'Bbook 50 процентов 900778', 
# #                                                         'TestBruv Serg ', 
# #                                                         'Тест Бородина Ксения ', 
# #                                                         'Test Svetlana Fatima ', 
# #                                                         'Kagirova Venera Test ', 
# #                                                         'Te_s', 
# #                                                         'Test', 
# #                                                         'TestBruv TestSerg ', 
# #                                                         'Abook 20 процентов 345019', 
# #                                                         'Test PAMM 1', 
# #                                                         'Test PAMM 2', 
# #                                                         'Test PAMM 3', 
# #                                                         'gastinets', 
# #                                                         'gastinets+1', 
# #                                                         'gastinets+2', 
# #                                                         'kdronof', 
# #                                                         'kdronof+1', 
# #                                                         'kdronof+2', 
# #                                                         'testing.process', 
# #                                                         'testing.process+1', 
# #                                                         'testing.process+2', 
# #                                                         'sergey', 
# #                                                         'sergey 2', 
# #                                                         'sergey test deposit', 
# #                                                         'sergey deposit test 2', 
# #                                                         'sergey test 3', 
# #                                                         'Test Borodina Kseniya Vadimovna', 
# #                                                         'test1 as', 
# #                                                         'test D', 
# #                                                         'sergey test ', 
# #                                                         'For site (take swaps)', 
# #                                                         'FastMT_Test', 
# #                                                         'Abook ретрантсляция логина 901412_901396', 
# #                                                         'A S test test', 
# #                                                         'Sasha P test test', 
# #                                                         'Vladimir Test Test', 
# #                                                         'Serj Test Test', 
# #                                                         'Test Gusenkov Sergey ', 
# #                                                         'Serj', 
# #                                                         'Alex P Test1', 
# #                                                         'Ксю', 
# #                                                         'Gas test', 
# #                                                         'Gas test2', 
# #                                                         'Gas test3', 
# #                                                         'Serj2', 
# #                                                         'Test Sophia', 
# #                                                         'Test Kagirova Venera Ramzis', 
# #                                                         'Gas test5', 
# #                                                         'test21212', 
# #                                                         'test денег нет но вы держитесь', 
# #                                                         'Test Borodina ksenia test ', 
# #                                                         'Serj3', 
# #                                                         '123', 
# #                                                         'Test Redko Svetlana ', 
# #                                                         'Nik Test 1 Master', 
# #                                                         'Nik Test 2 Follower', 
# #                                                         'Serj4', 
# #                                                         'TestBruver TestSerg ', 
# #                                                         'Serj5', 
# #                                                         'test1', 
# #                                                         'B2B PL скольжения в карман компании(только плюсовые)XAUUSD.vol', 
# #                                                         'Денег нет но вы держитесь', 
# #                                                         'Serj8', 
# #                                                         'Serj9') 
# #                                         OR FirstName LIKE 'Bbook %' 
# #                                         OR FirstName LIKE 'Abook %' 
# #                                         OR FirstName LIKE 'test %' 
# #                                         OR FirstName LIKE '% test' 
# #                                         OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
# #                                         /*конец Блок исключений из статистики*/
# #                                     )
# #                 /*конец Блок все логины с исключениями*/) as vse_aki on vse_aki.`Group`=bbook_ak.`Group`
# #     /*конец Блок все ббук юзеры таблица мт5 юзерс на фильтрах*/) as bbook_users 
# # INNER JOIN (
# #             /*начало Блок Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# #             SELECT *
# #             FROM mt5r1.mt5_deals
# #             WHERE (
# #                 `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
# #                 OR (
# #                     `Action` = 2
# #                     AND (
# #                         Comment IN (
# #                             'indemnification',
# #                             'compensation',
# #                             'Drawdown compensation',
# #                             'Bonus transfer',
# #                             'bonus transfer',
# #                             'Swapfree compensation',
# #                             'balance indemnification',
# #                             'Balance indemnification'
# #                         )
# #                     )
# #                 )
# #                 OR (
# #                     `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2)
# #                     AND Comment LIKE '%Swap Free Commission'
# #                 )
# #             )
# #             AND DATE(`Time`) BETWEEN {start} AND {end}
# #             /*конец Блок Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # ) as pl_comis_kompens on pl_comis_kompens.Login=bbook_users.Login
# # /*конец Блок Ббук Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # ;'''

# # CBOOK_PNL = f'''
# # /*начало Блок цент ббук Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # select IFNULL(SUM(pl_comis_kompens.Profit+pl_comis_kompens.Storage+pl_comis_kompens.Commission+pl_comis_kompens.Fee),0) as PnL_CBOOK_USD_side_client_realized
# # FROM 
# #     (
# #     /*начало Блок все цбук группы юзеры таблица мт5 юзерс на фильтрах*/
# #         select vse_aki.*
# #         from (
# #                 /*конец Блок все цбук группы автоматика опеределения*/
# #                 SELECT `Group` 
# #                 FROM mt5r1.mt5_groups
# #                 WHERE `group` LIKE 'real\\\\abook\\\\abook%' and `group` like '%_percent' and Currency ='USD'
# #                 /*конец все цбук группы автоматика опеределения*/
# #             ) as c_bbook_ak 
# #         inner join (
# #                     /*начало Блок все логины с исключениями*/
# #                     select *
# #                     from mt5r1.mt5_users
# #                     where Login not in (
# #                                         /*начало Блок исключений из статистики*/
# #                                         select Login
# #                                         from mt5r1.mt5_users
# #                                         where FirstName in ( 
# #                                                             'First Admin', 
# #                                                             'FastMT Admin 1', 
# #                                                             'FastMT Admin 2', 
# #                                                             'FastMT Admin 3', 
# #                                                             'FastMT Admin 4', 
# #                                                             'FastMT Admin 5', 
# #                                                             'FastMT Admin 6', 
# #                                                             'Neobit Admin 1', 
# #                                                             'Neobit Admin 2', 
# #                                                             'FastMT Monitoring', 
# #                                                             'FastMT Backup', 
# #                                                             'TestVadim', 
# #                                                             'MT5 Monitor', 
# #                                                             'Web API Personal Area Account', 
# #                                                             'MT5BBProGateway', 
# #                                                             'MT5BBProFeeder', 
# #                                                             'FX manager sub', 
# #                                                             'FX manager din', 
# #                                                             'FX manager nak', 
# #                                                             'FX manager nov', 
# #                                                             'FX manager ova', 
# #                                                             'FX manager shin', 
# #                                                             'FX manager rnov', 
# #                                                             'FX manager hov', 
# #                                                             'Data Export Manager', 
# #                                                             'FX manager 2112', 
# #                                                             'FX manager 2114', 
# #                                                             'FX manager otov 2115', 
# #                                                             'FX manager 2116', 
# #                                                             'FX manager sich 2117', 
# #                                                             'FX manager 2118 up partner', 
# #                                                             'FX manager 2119 up2 clients', 
# #                                                             'FX manager 2120 Atimex', 
# #                                                             'Manager_view only', 
# #                                                             'Manager_Kuznecov Vladimir', 
# #                                                             'FX manager 2123', 
# #                                                             'FX manager 2124', 
# #                                                             'FX manager 2125', 
# #                                                             'FX manager 2126 lcov', 
# #                                                             'BrokerPilot', 
# #                                                             'FX manager 2128', 
# #                                                             'FX manager 2129', 
# #                                                             'FX manager 2130', 
# #                                                             'FX manager 2131', 
# #                                                             'FX_Manager_2132', 
# #                                                             'fsd gsdfg gdfs', 
# #                                                             'Test Test ', 
# #                                                             'Sabodin Aleksandr test Sergeevich', 
# #                                                             'TestIossub TestVadim Petrovich', 
# #                                                             'TestLukashin Dmitry Gennadievich', 
# #                                                             'Testov Test ', 
# #                                                             'Petukhov test Alexander test Alex test', 
# #                                                             'TestSmirnov Ivan Valerevich', 
# #                                                             'Test Aleksandr test ', 
# #                                                             'Petukhov Alexander sdfsdfsdf', 
# #                                                             'Test Test Follower', 
# #                                                             'Test Oleg Master', 
# #                                                             'TestIvan', 
# #                                                             'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс)', 
# #                                                             'A-Book Client Position', 
# #                                                             'B-Book Client Position', 
# #                                                             'A-Book and B-Book Client Position', 
# #                                                             'TestSmirnov Ivan', 
# #                                                             'Test Andrei ', 
# #                                                             'Test cent', 
# #                                                             'Monitor', 
# #                                                             'Bruver TestSergeyTest ', 
# #                                                             'B-Book cent Client Position', 
# #                                                             'Test Swap Free netting платно', 
# #                                                             'Test Centroid Trading', 
# #                                                             'Test admin', 
# #                                                             'Test Stopout Plugin', 
# #                                                             'Test Stopout Plugin 2', 
# #                                                             'Test Stopout Plugin 3', 
# #                                                             'Abook 50 процентов 345019', 
# #                                                             'Bbook 50 процентов 900778', 
# #                                                             'TestBruv Serg ', 
# #                                                             'Тест Бородина Ксения ', 
# #                                                             'Test Svetlana Fatima ', 
# #                                                             'Kagirova Venera Test ', 
# #                                                             'Te_s', 
# #                                                             'Test', 
# #                                                             'TestBruv TestSerg ', 
# #                                                             'Abook 20 процентов 345019', 
# #                                                             'Test PAMM 1', 
# #                                                             'Test PAMM 2', 
# #                                                             'Test PAMM 3', 
# #                                                             'gastinets', 
# #                                                             'gastinets+1', 
# #                                                             'gastinets+2', 
# #                                                             'kdronof', 
# #                                                             'kdronof+1', 
# #                                                             'kdronof+2', 
# #                                                             'testing.process', 
# #                                                             'testing.process+1', 
# #                                                             'testing.process+2', 
# #                                                             'sergey', 
# #                                                             'sergey 2', 
# #                                                             'sergey test deposit', 
# #                                                             'sergey deposit test 2', 
# #                                                             'sergey test 3', 
# #                                                             'Test Borodina Kseniya Vadimovna', 
# #                                                             'test1 as', 
# #                                                             'test D', 
# #                                                             'sergey test ', 
# #                                                             'For site (take swaps)', 
# #                                                             'FastMT_Test', 
# #                                                             'Abook ретрантсляция логина 901412_901396', 
# #                                                             'A S test test', 
# #                                                             'Sasha P test test', 
# #                                                             'Vladimir Test Test', 
# #                                                             'Serj Test Test', 
# #                                                             'Test Gusenkov Sergey ', 
# #                                                             'Serj', 
# #                                                             'Alex P Test1', 
# #                                                             'Ксю', 
# #                                                             'Gas test', 
# #                                                             'Gas test2', 
# #                                                             'Gas test3', 
# #                                                             'Serj2', 
# #                                                             'Test Sophia', 
# #                                                             'Test Kagirova Venera Ramzis', 
# #                                                             'Gas test5', 
# #                                                             'test21212', 
# #                                                             'test денег нет но вы держитесь', 
# #                                                             'Test Borodina ksenia test ', 
# #                                                             'Serj3', 
# #                                                             '123', 
# #                                                             'Test Redko Svetlana ', 
# #                                                             'Nik Test 1 Master', 
# #                                                             'Nik Test 2 Follower', 
# #                                                             'Serj4', 
# #                                                             'TestBruver TestSerg ', 
# #                                                             'Serj5', 
# #                                                             'test1', 
# #                                                             'B2B PL скольжения в карман компании(только плюсовые)XAUUSD.vol', 
# #                                                             'Денег нет но вы держитесь', 
# #                                                             'Serj8', 
# #                                                             'Serj9') 
# #                                             OR FirstName LIKE 'Bbook %' 
# #                                             OR FirstName LIKE 'Abook %' 
# #                                             OR FirstName LIKE 'test %' 
# #                                             OR FirstName LIKE '% test' 
# #                                             OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
# #                                             /*конец Блок исключений из статистики*/
# #                                         )
# #                     /*конец Блок все логины с исключениями*/) as vse_aki on vse_aki.`Group`=c_bbook_ak.`Group`
# #         /*конец Блок все цбук юзеры таблица мт5 юзерс на фильтрах*/
# #     ) as c_bbook_users
# # /*конец Блок балансы все цбук на фильтрах*/ 
# # INNER JOIN (
# #             /*начало Блок Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# #             SELECT *
# #             FROM mt5r1.mt5_deals
# #             WHERE (
# #                 `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
# #                 OR (
# #                     `Action` = 2
# #                     AND (
# #                         Comment IN (
# #                             'indemnification',
# #                             'compensation',
# #                             'Drawdown compensation',
# #                             'Bonus transfer',
# #                             'bonus transfer',
# #                             'Swapfree compensation',
# #                             'balance indemnification',
# #                             'Balance indemnification'
# #                         )
# #                     )
# #                 )
# #                 OR (
# #                     `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2)
# #                     AND Comment LIKE '%Swap Free Commission'
# #                 )
# #             )
# #             AND DATE(`Time`) BETWEEN {start} AND {end}
# #             /*конец Блок Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # ) as pl_comis_kompens on pl_comis_kompens.Login=c_bbook_users.Login
# # /*конец Блок цент ббук Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # ;'''

# # CENT_BOOK = f'''
# # /*начало Блок цент ббук Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # select ROUND(IFNULL((SUM(pl_comis_kompens.Profit+pl_comis_kompens.Storage+pl_comis_kompens.Commission+pl_comis_kompens.Fee))*0.01,0),2) as PnL_Cent_BBOOK_USD_side_client_realized
# # FROM 
# #     (
# #     /*начало Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
# #         select vse_aki.*
# #         from (
# #                 /*конец Блок цент ббук группы автоматика опеределения*/
# #                 SELECT `Group` 
# #                 FROM mt5r1.mt5_groups
# #                 WHERE `group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC'
# #                 /*конец Блок цент ббук группы автоматика опеределения*/
# #             ) as cent_bbook_ak 
# #         inner join (
# #                     /*начало Блок все логины с исключениями*/
# #                     select *
# #                     from mt5r1.mt5_users
# #                     where Login not in (
# #                                         /*начало Блок исключений из статистики*/
# #                                         select Login
# #                                         from mt5r1.mt5_users
# #                                         where FirstName in ( 
# #                                                             'First Admin', 
# #                                                             'FastMT Admin 1', 
# #                                                             'FastMT Admin 2', 
# #                                                             'FastMT Admin 3', 
# #                                                             'FastMT Admin 4', 
# #                                                             'FastMT Admin 5', 
# #                                                             'FastMT Admin 6', 
# #                                                             'Neobit Admin 1', 
# #                                                             'Neobit Admin 2', 
# #                                                             'FastMT Monitoring', 
# #                                                             'FastMT Backup', 
# #                                                             'TestVadim', 
# #                                                             'MT5 Monitor', 
# #                                                             'Web API Personal Area Account', 
# #                                                             'MT5BBProGateway', 
# #                                                             'MT5BBProFeeder', 
# #                                                             'FX manager sub', 
# #                                                             'FX manager din', 
# #                                                             'FX manager nak', 
# #                                                             'FX manager nov', 
# #                                                             'FX manager ova', 
# #                                                             'FX manager shin', 
# #                                                             'FX manager rnov', 
# #                                                             'FX manager hov', 
# #                                                             'Data Export Manager', 
# #                                                             'FX manager 2112', 
# #                                                             'FX manager 2114', 
# #                                                             'FX manager otov 2115', 
# #                                                             'FX manager 2116', 
# #                                                             'FX manager sich 2117', 
# #                                                             'FX manager 2118 up partner', 
# #                                                             'FX manager 2119 up2 clients', 
# #                                                             'FX manager 2120 Atimex', 
# #                                                             'Manager_view only', 
# #                                                             'Manager_Kuznecov Vladimir', 
# #                                                             'FX manager 2123', 
# #                                                             'FX manager 2124', 
# #                                                             'FX manager 2125', 
# #                                                             'FX manager 2126 lcov', 
# #                                                             'BrokerPilot', 
# #                                                             'FX manager 2128', 
# #                                                             'FX manager 2129', 
# #                                                             'FX manager 2130', 
# #                                                             'FX manager 2131', 
# #                                                             'FX_Manager_2132', 
# #                                                             'fsd gsdfg gdfs', 
# #                                                             'Test Test ', 
# #                                                             'Sabodin Aleksandr test Sergeevich', 
# #                                                             'TestIossub TestVadim Petrovich', 
# #                                                             'TestLukashin Dmitry Gennadievich', 
# #                                                             'Testov Test ', 
# #                                                             'Petukhov test Alexander test Alex test', 
# #                                                             'TestSmirnov Ivan Valerevich', 
# #                                                             'Test Aleksandr test ', 
# #                                                             'Petukhov Alexander sdfsdfsdf', 
# #                                                             'Test Test Follower', 
# #                                                             'Test Oleg Master', 
# #                                                             'TestIvan', 
# #                                                             'A-Book Client PnL (открытие-сделка на LP, закрытие-цена клиента, наша сторона, всегда должен быть плюс)', 
# #                                                             'A-Book Client Position', 
# #                                                             'B-Book Client Position', 
# #                                                             'A-Book and B-Book Client Position', 
# #                                                             'TestSmirnov Ivan', 
# #                                                             'Test Andrei ', 
# #                                                             'Test cent', 
# #                                                             'Monitor', 
# #                                                             'Bruver TestSergeyTest ', 
# #                                                             'B-Book cent Client Position', 
# #                                                             'Test Swap Free netting платно', 
# #                                                             'Test Centroid Trading', 
# #                                                             'Test admin', 
# #                                                             'Test Stopout Plugin', 
# #                                                             'Test Stopout Plugin 2', 
# #                                                             'Test Stopout Plugin 3', 
# #                                                             'Abook 50 процентов 345019', 
# #                                                             'Bbook 50 процентов 900778', 
# #                                                             'TestBruv Serg ', 
# #                                                             'Тест Бородина Ксения ', 
# #                                                             'Test Svetlana Fatima ', 
# #                                                             'Kagirova Venera Test ', 
# #                                                             'Te_s', 
# #                                                             'Test', 
# #                                                             'TestBruv TestSerg ', 
# #                                                             'Abook 20 процентов 345019', 
# #                                                             'Test PAMM 1', 
# #                                                             'Test PAMM 2', 
# #                                                             'Test PAMM 3', 
# #                                                             'gastinets', 
# #                                                             'gastinets+1', 
# #                                                             'gastinets+2', 
# #                                                             'kdronof', 
# #                                                             'kdronof+1', 
# #                                                             'kdronof+2', 
# #                                                             'testing.process', 
# #                                                             'testing.process+1', 
# #                                                             'testing.process+2', 
# #                                                             'sergey', 
# #                                                             'sergey 2', 
# #                                                             'sergey test deposit', 
# #                                                             'sergey deposit test 2', 
# #                                                             'sergey test 3', 
# #                                                             'Test Borodina Kseniya Vadimovna', 
# #                                                             'test1 as', 
# #                                                             'test D', 
# #                                                             'sergey test ', 
# #                                                             'For site (take swaps)', 
# #                                                             'FastMT_Test', 
# #                                                             'Abook ретрантсляция логина 901412_901396', 
# #                                                             'A S test test', 
# #                                                             'Sasha P test test', 
# #                                                             'Vladimir Test Test', 
# #                                                             'Serj Test Test', 
# #                                                             'Test Gusenkov Sergey ', 
# #                                                             'Serj', 
# #                                                             'Alex P Test1', 
# #                                                             'Ксю', 
# #                                                             'Gas test', 
# #                                                             'Gas test2', 
# #                                                             'Gas test3', 
# #                                                             'Serj2', 
# #                                                             'Test Sophia', 
# #                                                             'Test Kagirova Venera Ramzis', 
# #                                                             'Gas test5', 
# #                                                             'test21212', 
# #                                                             'test денег нет но вы держитесь', 
# #                                                             'Test Borodina ksenia test ', 
# #                                                             'Serj3', 
# #                                                             '123', 
# #                                                             'Test Redko Svetlana ', 
# #                                                             'Nik Test 1 Master', 
# #                                                             'Nik Test 2 Follower', 
# #                                                             'Serj4', 
# #                                                             'TestBruver TestSerg ', 
# #                                                             'Serj5', 
# #                                                             'test1', 
# #                                                             'B2B PL скольжения в карман компании(только плюсовые)XAUUSD.vol', 
# #                                                             'Денег нет но вы держитесь', 
# #                                                             'Serj8', 
# #                                                             'Serj9') 
# #                                             OR FirstName LIKE 'Bbook %' 
# #                                             OR FirstName LIKE 'Abook %' 
# #                                             OR FirstName LIKE 'test %' 
# #                                             OR FirstName LIKE '% test' 
# #                                             OR Login IN /*начало Здесь указать логины исключения*/ ('') /*конец Здесь указать логины исключения*/
# #                                             /*конец Блок исключений из статистики*/
# #                                         )
# #                     /*конец Блок все логины с исключениями*/) as vse_aki on vse_aki.`Group`=cent_bbook_ak.`Group`
# #         /*конец Блок все цент ббук юзеры таблица мт5 юзерс на фильтрах*/
# #     ) as cent_bbook_users 
# # INNER JOIN (
# #             /*начало Блок Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# #             SELECT *
# #             FROM mt5r1.mt5_deals
# #             WHERE (
# #                 `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
# #                 OR (
# #                     `Action` = 2
# #                     AND (
# #                         Comment IN (
# #                             'indemnification',
# #                             'compensation',
# #                             'Drawdown compensation',
# #                             'Bonus transfer',
# #                             'bonus transfer',
# #                             'Swapfree compensation',
# #                             'balance indemnification',
# #                             'Balance indemnification'
# #                         )
# #                     )
# #                 )
# #                 OR (
# #                     `Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2)
# #                     AND Comment LIKE '%Swap Free Commission'
# #                 )
# #             )
# #             AND DATE(`Time`) BETWEEN {start} AND {end}
# #             /*конец Блок Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # ) as pl_comis_kompens on pl_comis_kompens.Login=cent_bbook_users.Login
# # /*конец Блок цент ббук Общий ПЛ реализованный со всеми комиссиями компенсациями, дивидендами и т.д.*/
# # ;'''

