from dataclasses import dataclass
import psycopg2
import settings as st

INSERT_USER = """
    insert into appuser(f_login, f_salt, f_role )
    values( %s, %s, 'teacher' )
    returning id ;
    """

INSERT_TEACHER = """
    insert into teacher ( f_fio, f_phone, f_email, f_comment, id_user )
    values( %s, %s, %s, %s, %s)
    returning id ;
    """

@dataclass
class Teacher(object):

    pk : int = None
    login : str = None
    fio : str = None
    phone : str = None
    email : str = None
    comment : str = None
    id_user : int = None

    @property   
    def user_data(self):
        return (self.login, '1')
    
    @property
    def teacher_data(self):
        return ( self.fio, self.phone, self.email,
                self.comment, self.id_user)

    def insert(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        # data = (self.fio, self.phone, self.email, self.comment, self.id_user)
        cursor.execute(INSERT_USER, self.user_data)
        (self.id_user, ) = next(cursor)
        cursor.execute(INSERT_TEACHER, self.teacher_data)
        (self.pk, ) = next(cursor)
        conn.commit()
        conn.close()
    