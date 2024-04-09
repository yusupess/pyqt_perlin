/*На этом этапе мы решили что соль должна добавляться автоматичсеки
а не как до етого мы в программе указали просто 1.
но так как база данных уже большая(типо) мы вынуждены писать этот
скрипт*/
START TRANSACTION;

alter table appuser
    alter column f_salt set default md5(random()::text);

update appuser set
    f_salt = md5(random()::text),
    f_password_hash = null
    where f_salt is null;

alter table appuser
    alter column f_salt set not null;

COMMIT TRANSACTION;