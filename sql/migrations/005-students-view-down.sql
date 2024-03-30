START TRANSACTION;

drop function if exists  del_teacher(int);
drop function if exists  upd_teacher(int, text, text, text, text);
drop function if exists new_teacher(text, text, text, text, text);
drop view if exists v_teacher;

drop function if exists  del_student(int);
drop function if exists  upd_student(int, text, text, text);
drop function if exists new_student(text, text, text, text);
drop view if exists v_student;

COMMIT TRANSACTION;