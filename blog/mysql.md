Title:   MySQL常用操作
Author: JinJay 靳杰
Date:    2015-04
description: MySQL常用操作，增删改查，视图，权限等等。
keywords: MySQL

# 授权
```mysql
grant insert, drop, update, select, create on database.table to 'username'@'host' indentified by 'password';
flush privileges;
```

# 视图
```mysql
create view myview(id, username, password) as select id, username, passwd from atable;
```

# 增删改查
```mysql
insert into atable (id, user, passwd) values (xx, xx, xx);
drop table atable;
update atable set (id, user,passwd) values (xx, xx, xx);
select * from atable;
```

# 创建表格
```mysql
create table if not exists atable(
    id int unsigned not null auto_increment,
    username varchar(128) not null,
    password varchar(128) not null,
    primary key (id)
) engine=innodb;
```

# 备份
```
mysqldump -hhost -Pport -uuser -ppassword --all-databases > all.sql
```

# 事件定时器
## 查看是否开启，三种方法
```
SHOW VARIABLES LIKE 'event_scheduler';
SELECT @@event_scheduler;
SHOW PROCESSLIST;
```

## 开启事件机制
```
SET GLOBAL event_scheduler = 1;
SET @@global.event_scheduler = 1;
SET GLOBAL event_scheduler = ON;
SET @@global.event_scheduler = ON;
```

## 事件权限查看
```
SELECT HOST,USER,Event_priv FROM mysql.user;
```

## 事件权限分配
```
UPDATE mysql.user SET Event_priv = 'Y' WHERE HOST='%' AND USER='auser';
```
## 创建事件
```
create event [if not exists] event_name
on schedule schedule
[on completion [not] preserve]
[enable | disable]
[comment 'comment']
do sql_statement;
```

## 事件开启与关闭
```
alter event e_test on completion preserve enable;
alter event e_test on completion preserve disable;
```

[TOC]