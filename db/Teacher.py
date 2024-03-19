from dataclasses import dataclass


@dataclass
class Teacher(object):

    pk : int = None
    login : str = None
    fio : str = None
    phone : str = None
    email : str = None
    comment : str = None
    id_user : int = None

    