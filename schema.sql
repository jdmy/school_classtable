use class_table;
CREATE TABLE IF NOT EXISTS classtable (
  id int(11) NOT NULL AUTO_INCREMENT,
  class_order int(11) NOT NULL,
  class_weekday int(7) NOT NULL,/*星期几*/
  class_name varchar(1024) NOT NULL,
  class_teacher varchar(1024) NOT NULL,
  class_place varchar(1024) NOT NULL,
  class_whichweek varchar(1024) NOT NULL,
  user_id varchar(1024) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
insert into classtable(class_order,class_weekday,class_name,
class_teacher,class_place,class_whichweek,user_id) values(1,2,
'高数','高数老师A','教三202','单周,第一周到第15周',"S1000");

use class_table;
CREATE TABLE IF NOT EXISTS publishes (
  id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(1024) NOT NULL,
  class_name varchar(1024) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
insert into publishes(title,class_name)
values('完成高数','高数');

use class_table;
CREATE TABLE IF NOT EXISTS `todolist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(1024) NOT NULL,
  `title` varchar(1024) NOT NULL,
  `status` int(2) NOT NULL COMMENT '是否完成',
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
insert into todolist(id, user_id, title, status, create_time)
values(3, 'S1000', '完成离散', 0, 1);

use class_table;
CREATE TABLE IF NOT EXISTS usertable (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id varchar(1024) NOT NULL unique,
  user_name varchar(1024) NOT NULL,
  user_type varchar(1024) NOT NULL,
  user_password varchar(1024) NOT NULL default 12345,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
insert into usertable(user_id,user_name,user_type,user_password) values("S1000","扬帆","student","qwert");
insert into usertable(user_id,user_name,user_type,user_password) values("T1000","刘一木","teacher","12345");
insert into usertable(user_id,user_name,user_type) values("S1001","文杰","student");