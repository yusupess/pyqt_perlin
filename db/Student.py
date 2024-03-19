from dataclasses import dataclass


@dataclass
class Student(object):

    pk : int = None
    login : str = None
    fio : str = None
    email : str = None
    comment : str = None
    id_user : int = None
