START TRANSACTION;

drop function if exists new_student(text, text, text, text, text);
drop function if exists new_teacher(text, text, text, text, text);

drop view if exists v_teacher;
drop view if exists v_student;

COMMIT TRANSACTION;