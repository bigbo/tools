class pair:
    def __init__(self,key='',val=''):
        self.key = key
        self.val = val

    def set_key(self,key):
        if not isinstance(key.str):
            raise ValueError('key should be string')
        if len(key.strip()) ==0:
            raise ValueError('key must be not null')
        self.key = key

    def set_val(self,val):
        if len(val.strip())==0:
            raise ValueError('val must be not null')
        self.val = val

    def get_key(self):
        return self.key

    def get_val(self):
        return self.val

    def get_pair(self):
        return (self.key , self.val)

    def __str_(self):
        pass

