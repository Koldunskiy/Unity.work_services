# Балансы Перцева сейчас (подставляем нужный коммент в счетах)
Balanc = '''
select 
SUM(case 
	when mt5r1.mt5_users.`Group` LIKE 'real\\\\cent\\\\bbook%' then Balance * 0.01
	when mt5r1.mt5_users.`Group` not LIKE 'real\\\\cent\\\\bbook%' then Balance
	else 0
end) as Balance 
from mt5r1.mt5_users
inner join (
	        /*конец Блок ббук группы автоматика опеределения*/
	        SELECT `Group` 
	        FROM mt5r1.mt5_groups
	        WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' and Currency ='USD' 
	            or (`group` LIKE 'real\\\\abook\\\\abook%' and Currency ='USD') 
	            or (`group` like 'real\\\\abook\\\\300023_netting_USD' and Currency ='USD')
	            or (`group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC')
            ) as real_group on real_group.`Group` = mt5r1.mt5_users.`Group`
where comment LIKE '%Percev%' -- тут указать поиск по ключевому слову в комментариях, поиск не по логину!!!
      -- OR comment LIKE '%Nitsan234%' -- доп условие через OR
;'''






# Эквити Перцев сейчас(подставляем нужный коммент в счетах)
Equity = '''
select 
SUM( case
	when real_group.`Group` LIKE 'real\\\\cent\\\\bbook%' then (IFNULL(position_online.Profit, 0) + IFNULL(position_online.Storage, 0) + mt5r1.mt5_users.Balance) * 0.01
	else IFNULL(position_online.Profit, 0) + IFNULL(position_online.Storage, 0) + mt5r1.mt5_users.Balance
end) as Equity_no_credit
from mt5r1.mt5_users
inner join (
	        /*конец Блок ббук группы автоматика опеределения*/
	        SELECT `Group` 
	        FROM mt5r1.mt5_groups
	        WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' and Currency ='USD' 
	            or (`group` LIKE 'real\\\\abook\\\\abook%' and Currency ='USD') 
	            or (`group` like 'real\\\\abook\\\\300023_netting_USD' and Currency ='USD')
	            or (`group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC')
            ) as real_group on real_group.`Group` = mt5r1.mt5_users.`Group`
left join (select Login, SUM(Profit) as Profit, SUM(Storage) as Storage from mt5r1.mt5_positions group by Login) as position_online on position_online.Login = mt5r1.mt5_users.Login
where mt5r1.mt5_users.comment LIKE '%Percev%' -- тут указать поиск по ключевому слову в комментариях, поиск не по логину!!!
      -- OR mt5r1.mt5_users.comment LIKE '%Nitsan234%' -- доп условие через OR
;'''


# Реализованный ПЛ по счёту/счетам, за всё время или промежуток (подставляем нужный коммент в счетах)
Realized_pnl = lambda start, end: f'''
select 
ROUND(SUM( case
	when real_group.`Group` LIKE 'real\\\\cent\\\\bbook%' then (IFNULL((real_deals.Profit + real_deals.Storage + real_deals.Commission + real_deals.Fee), 0)) * 0.01
	else IFNULL((real_deals.Profit + real_deals.Storage + real_deals.Commission + real_deals.Fee), 0)
end), 2) as Profit_all
from mt5r1.mt5_users
inner join (
	        /*конец Блок ббук группы автоматика опеределения*/
	        SELECT `Group` 
	        FROM mt5r1.mt5_groups
	        WHERE `group` LIKE 'real\\\\neobit\\\\bbook%' and Currency ='USD' 
	            or (`group` LIKE 'real\\\\abook\\\\abook%' and Currency ='USD') 
	            or (`group` like 'real\\\\abook\\\\300023_netting_USD' and Currency ='USD')
	            or (`group` LIKE 'real\\\\cent\\\\bbook%' and Currency ='USC')
            ) as real_group on real_group.`Group` = mt5r1.mt5_users.`Group`
left join (select Login, SUM(Profit) as Profit, SUM(Storage) as Storage, SUM(Commission) as Commission, SUM(Fee) as Fee
		   from mt5r1.mt5_deals 
		   where 
				    (mt5r1.mt5_deals.`Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19)
				    OR (
				        mt5r1.mt5_deals.`Action` = 2
				        AND (
				            mt5r1.mt5_deals.Comment IN (
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
				        mt5r1.mt5_deals.`Action` IN (0, 1, 7, 8, 9, 12, 15, 16, 17, 19, 2)
				        AND mt5r1.mt5_deals.Comment LIKE '%Swap Free Commission'
				    )
				) 
				and DATE(`Time`) BETWEEN {start} and {end} -- тут указываем промежуток дат, если нужно
			group by Login
			)as real_deals
		   on real_deals.Login = mt5r1.mt5_users.Login
where mt5r1.mt5_users.comment like '%Percev%' -- тут указать поиск по ключевому слову в комментариях, поиск не по логину!!!
	  -- OR mt5r1.mt5_users.comment LIKE '%Nitsan%'
	  -- OR mt5r1.mt5_users.comment LIKE '%Nitsan234%' -- доп условие через OR
;'''