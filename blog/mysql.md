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

[TOC]