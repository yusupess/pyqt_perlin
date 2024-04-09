select st.pk, st.f_fio, st.f_comment
    from student_group as sg 
    inner join v_student as st
        on st.pk = sg.id_student
    where id_group = 1;