-- SQLite
-- select strftime('%s','now') 
-- select strftime('%Y-%m-%d %H:%M:%f','now')
select * from jpwords

update jpwords set lasttime = strftime('%s','now') - 86400  where id = 2
-- update jpwords set lasttime = strftime('%Y-%m-%d %H:%M:%f','now') where id = 1


SELECT * FROM jpwords where strftime('%s','now') - lasttime > 86400
