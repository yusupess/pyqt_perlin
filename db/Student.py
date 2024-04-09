from dataclasses import dataclass
import psycopg2
import settings as st

# INSERT_USER = """
#     insert into appuser(f_login, f_salt, f_role )
#     values( %s, %s, 'teacher' )
#     returning id ;
#     """

# INSERT_STUDENT = """
#     insert into student ( f_fio, f_email, f_comment, id_user )
#     values( %s, %s, %s, %s)
#     returning id ;
#     """

# f_login, f_fio, f_email, f_comment
INSERT_ONE = """select new_student(%s, %s, %s, %s);"""
# pk, f_fio ,f_email, f_comment
UPDATE_ONE = """select upd_student(%s, %s, %s, %s)"""
DELETE_ONE = """select del_student(%s)"""

SELECT_ONE = """
                select f_login, f_fio, f_email,
                f_comment, id_user from v_student
                where pk = %s ;"""


@dataclass
class Student(object):

    pk : int = None
    login : str = None
    fio : str = None
    email : str = None
    comment : str = None
    id_user : int = None

    # @property   
    # def user_data(self):
    #     return (self.login, '1')
    
    @property
    def student_data(self):
        return ( self.login, self.fio,
                 self.email, self.comment)
    
    @property
    def student_upd_data(self):
        # вспомогательное свойство
        return (self.pk, self.fio, self.email,
                self.comment)

    def insert(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        # data = (self.fio, self.phone, self.email, self.comment, self.id_user)
        cursor.execute(INSERT_ONE, self.student_data)
        (self.pk, ) = next(cursor)
        conn.commit()
        conn.close()

    def update(self):
        # обновление данных в БД
        conn = psycopg2.connect(**st.db_params)
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(UPDATE_ONE, self.student_upd_data)
        finally:
            conn.close()

    def save(self):
        # если пк равен None это значт что студент только создается ведб пк присваивает БД
        # а если пк есть значит мы делаем изменение в уже существующей записи
        if self.pk is None:
            return self.insert()
        else:
            return self.update()


    def load(self):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        cursor.execute(SELECT_ONE, (self.pk,))
        (self.login, self.fio, self.email,
         self.comment, self.id_user) = next(cursor)
        conn.commit()
        conn.close()
        return self
    
    def delete(self):
        conn = psycopg2.connect(**st.db_params)
        try:
            with conn:
                with conn.cursor() as cursor:
                    data = (self.pk, )
                    cursor.execute(DELETE_ONE, data)
        finally:
            conn.close()
