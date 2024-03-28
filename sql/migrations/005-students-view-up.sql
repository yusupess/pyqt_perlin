START TRANSACTION;

create view v_student as
    select
            st.id as pk,
            au.f_fio as f_fio,
            au.f_email as f_email,
            au.f_comment as f_comment
        from appuser as au
        inner join student as st
            on au.id = st.id_user;

COMMIT TRANSACTION;