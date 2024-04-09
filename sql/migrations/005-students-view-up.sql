START TRANSACTION;

/*=======================================*/

create view v_student as
    select
            st.id as pk,
            st.id_user as id_user,
            au.f_login as f_login,
            au.f_enabled as f_enabled,
            au.f_created as f_created,
            au.f_expire as f_expire,
            au.f_role as f_role,
            au.f_fio as f_fio,
            au.f_email as f_email,
            au.f_comment as f_comment
        from appuser as au
        inner join student as st
            on au.id = st.id_user;

/*-----------------------------------------------------*/
create function new_student(p_login text, p_fio text,
                            p_email text, p_comment text) returns int

language plpgsql
security definer -- те же права что и владелец функции
-- что делать если в параметры ф-ии попадаются null
called on null input
volatile
as $BODY$
DECLARE
    d_id_user int;
    d_pk int;
BEGIN
    insert into appuser(f_login, f_role, f_fio, 
                        f_email, f_comment)
        values (p_login, 'student', p_fio, p_email, p_comment)
        returning id
        into strict d_id_user;
    insert into student(id_user)
        values(d_id_user)
        returning id
        into strict d_pk;
    return d_pk;
END;
$BODY$;

/*-----------------------------------------------------*/
create function upd_student(pk int, p_fio text, p_email text,
                            p_comment text) returns int
language plpgsql
security definer
called on null input
volatile
as $BODY$
DECLARE
    d_id_user int;
BEGIN
    select id_user from student
        where id = pk
        into strict d_id_user;
    update appuser set 
        f_fio = p_fio,
        f_email = p_email,
        f_comment = p_comment
        where id = d_id_user;
    return pk;

END;
$BODY$;

/*-------------------------------------------*/
create function del_student(pk int ) returns int
language plpgsql
security definer
called on null input
volatile
as $BODY$
DECLARE
    d_id_user int;
BEGIN
    select id_user from student
        where id = pk
        into strict d_id_user;
    delete from student where id = pk;
    delete from appuser where id = d_id_user;
    return pk;

END;
$BODY$;


/*=======================================*/

create view v_teacher as
    select
            t.id as pk,
            t.id_user as id_user,
            t.f_phone as f_phone,
            au.f_login as f_login,
            au.f_enabled as f_enabled,
            au.f_created as f_created,
            au.f_expire as f_expire,
            au.f_role as f_role,
            au.f_fio as f_fio,
            au.f_email as f_email,
            au.f_comment as f_comment
        from appuser as au
        inner join teacher as t
            on au.id = t.id_user;

/*-----------------------------------------------------*/
create function new_teacher(p_login text, p_fio text,
                            p_phone text, p_email text,
                            p_comment text) returns int

language plpgsql
security definer -- те же права что и владелец функции
-- что делать если в параметры ф-ии попадаются null
called on null input
volatile
as $BODY$
DECLARE
    d_id_user int;
    d_pk int;
BEGIN
    insert into appuser(f_login, f_role, f_fio, 
                        f_email, f_comment)
        values (p_login, 'teacher', p_fio, p_email, p_comment)
        returning id
        into strict d_id_user;
    insert into teacher(f_phone, id_user)
        values(p_phone, d_id_user)
        returning id
        into strict d_pk;
    return d_pk;
END;
$BODY$;

/*-----------------------------------------------------*/

create function upd_teacher(pk int, p_fio text,
                            p_phone text, p_email text,
                            p_comment text) returns int
language plpgsql
security definer
called on null input
volatile
as $BODY$
DECLARE
    d_id_user int;
BEGIN
    select id_user from teacher
        where id = pk
        into strict d_id_user;
    update appuser set 
        f_fio = p_fio,
        f_email = p_email,
        f_comment = p_comment
        where id = d_id_user;
    update teacher set
        f_phone = p_phone
        where id = pk;
    return pk;

END;
$BODY$;

/*-------------------------------------------*/
create function del_teacher(pk int ) returns int
language plpgsql
security definer
called on null input
volatile
as $BODY$
DECLARE
    d_id_user int;
BEGIN
    select id_user from teacher
        where id = pk
        into strict d_id_user;
    delete from teacher where id = pk;
    delete from appuser where id = d_id_user;
    return pk;

END;
$BODY$;

/*=======================================*/

COMMIT TRANSACTION;