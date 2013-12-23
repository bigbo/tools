import os

def list(dir_path):
    if not exist(dir_path):
        raise ValueError('%s not exist !'%dir_path)
    list = os.listdir(dir_path)
    return list

def current_path(abs=True):
    current_path= os.getcwd()

    if abs:
        return os.path.abspath(current_path)
    else:
        return current_path



def exist(path):
    if os.path.exists(path):return True
    else:return False

def readline(file):
    pass


def 

