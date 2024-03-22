from dataclasses import dataclass
import psycopg2
import settings as st

INSERT_USER = """
    insert into appuser(f_login, f_salt, f_role )
    values( %s, %s, 'teacher' )
    returning id ;
    """

INSERT_STUDENT = """
    insert into student ( f_fio, f_email, f_comment, id_user )
    values( %s, %s, %s, %s)
    returning id ;
    """

SELECT_ONE = """select u.f_login, t.f_fio,
                    t.f_email,
                    t.f_comment, t.id_user
                from appuser as u
                inner join student as t
                on u.id = t.id_user
                where t.id = %s ;"""


@dataclass
class Student(object):

    pk : int = None
    login : str = None
    fio : str = None
    email : str = None
    comment : str = None
    id_user : int = None

    @property   
    def user_data(self):
        return (self.login, '1')
    
    @property
    def student_data(self):
        return ( self.fio, self.email,
                self.comment, self.id_user)

    def insert(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        # data = (self.fio, self.phone, self.email, self.comment, self.id_user)
        cursor.execute(INSERT_USER, self.user_data)
        (self.id_user, ) = next(cursor)
        cursor.execute(INSERT_STUDENT, self.teacher_data)
        (self.pk, ) = next(cursor)
        conn.commit()
        conn.close()

    def load(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(SELECT_ONE, (self.pk,))
        (self.login, self.fio, self.email,
         self.comment, self.id_user) = next(cursor)
        conn.commit()
        conn.close()
        return self