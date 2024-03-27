START TRANSACTION;
/*------------------------------------------------------------*/

create type user_role as enum ('admin', 'student', 'teacher');

comment on type user_role is 'Права пользователя в приложении';

/*------------------------------------------------------------*/

create table appuser (
    "id" serial not null primary key,
    f_login text not null unique,
    f_password_hash text,
    f_salt text,
    f_enabled boolean not null default true,
    f_created timestamp not null default CURRENT_TIMESTAMP,
    f_expire timestamp,
    f_role user_role not null,
    f_fio text not null,
    f_email text,
    f_comment text
) ;

comment on table appuser is 'Общие сведения о пользователе';
comment on column appuser.f_login is 'логин пользователя';
comment on column appuser.f_password_hash is 'хэш пароля с солью';
comment on column appuser.f_salt is 'соль пароля';
comment on column appuser.f_enabled is 'пользователю разрешено подкдючение';
comment on column appuser.f_created is 'время создания пользователя';
comment on column appuser.f_expire is 'истечение срока действия логина';
comment on column appuser.f_role is 'права пользователя';
comment on column appuser.f_email is 'почтовый адрес';
comment on column appuser.f_comment is 'примечание';

/*----------------------------------------------------------------*/
/*serial - автоматически генерируемое целое число*/
create table teacher (
    "id" serial not null primary key,
    f_phone text,
    id_user int not null references appuser("id")
);

comment on table teacher is 'Сведения о преподователях';
comment on column teacher.f_phone is 'номер телефона';

/*----------------------------------------------------------------*/

create table student (
    "id" serial not null primary key,
    id_user int not null references appuser("id")
);

comment on table student is 'Сведения об учениках';

/*----------------------------------------------------------------*/

create table stgroup(
    "id" serial not null primary key,
    f_title text not null,
    f_comment text
);

comment on table stgroup is 'Группы студентов';
comment on column stgroup.f_title is 'наименование группы';
comment on column stgroup.f_comment is 'примечание';

/*----------------------------------------------------------------*/
COMMIT TRANSACTION ;
