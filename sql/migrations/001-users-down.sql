-- скрипт для отката базы данных. Выполняется с конца очереди создания таблиц. По принципу все или ничего

START TRANSACTION;

drop table if exists stgroup ;
drop table if exists student ;
drop table if exists teacher ;
drop table if exists appuser ;

drop type if exists user_role ;

COMMIT TRANSACTION ;
