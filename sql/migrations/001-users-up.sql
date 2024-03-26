
create type user_role as enum ('admin', 'student', 'teacher');

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
)