START TRANSACTION;

/*-----------------------------------------------------------*/
create table problem(
    "id" serial not null primary key,
    f_title text,
    f_contents text not null,
    f_created timestamp not null default CURRENT_TIMESTAMP,
    id_author int not null references teacher("id")
);

comment on table problem is 'Задача';
comment on column problem.f_title is 'название задачи';
comment on column problem.f_contents is 'условие задачи';
comment on column problem.f_created is 'дата создания задачи';
comment on column problem.id_author is 'id автора задачи';
/*-----------------------------------------------------------*/

create table variant(
    "id" serial not null primary key,
    f_title text,
    f_created timestamp not null default CURRENT_TIMESTAMP,
    id_composer int not null references teacher("id")
);

comment on table variant is 'Задача';
comment on column variant.f_title is 'название варианта';
comment on column variant.f_created is 'дата создания варианта';
comment on column variant.id_composer is 'id автора варианта';
/*-----------------------------------------------------------*/

create table problem_variant(
    "id" serial not null primary key,
    id_variant int not null references variant("id"),
    id_problem int not null references problem("id"),
    f_ordinal int
);

comment on table problem_variant is 'Таблица для связки проблема-вариант';
comment on column problem_variant.id_variant is 'id варианта';
comment on column problem_variant.id_problem is 'id проблемы';
comment on column problem_variant.f_ordinal is 'порядковый номер задачи';
/*-----------------------------------------------------------*/

COMMIT TRANSACTION;