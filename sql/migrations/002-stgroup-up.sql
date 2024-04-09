START TRANSACTION;

create table student_group (
    "id" serial not null primary key,
    id_student int not null references student("id"),
    id_group int not null references stgroup("id"),
    -- пара студент-группа не должна повторяться
    constraint un_student_group unique(id_student, id_group)
);

COMMIT TRANSACTION;