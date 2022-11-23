-- SQLite
-- select strftime('%s','now') 
-- select strftime('%Y-%m-%d %H:%M:%f','now')
select * from jpwords

update jpwords set lasttime = strftime('%s','now') - 86400  where id = 2
-- update jpwords set lasttime = strftime('%Y-%m-%d %H:%M:%f','now') where id = 1


SELECT * FROM jpwords where strftime('%s','now') - lasttime > 86400

SELECT * FROM jpwords where lesson like '%m2-1-14%'

SELECT kana FROM jpwords where lesson like '%w-1-05%'
SELECT kana FROM jpstats  where increase > decrease

update jpstats set decrease = increase where kana in (SELECT kana FROM jpwords where lesson like '%w-1-03%')

select kana,decrease,increase from jpstats where increase > decrease and kana in (SELECT kana FROM jpwords where lesson like '%w-1-05%')
select kana,increase,decrease from jpstats where increase > decrease


SELECT kana, increase FROM jpstats where increase > decrease

SELECT chinese FROM jpwords where lesson like '%w-1-03%'