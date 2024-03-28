/*На этом этапе мы решили что соль должна добавляться автоматичсеки
а не как до етого мы в программе указали просто 1.
но так как база данных уже большая(типо) мы вынуждены писать этот
скрипт*/
START TRANSACTION;

alter table appuser
    alter column f_salt drop not null;

alter table appuser
    alter column f_salt drop default;

COMMIT TRANSACTION;