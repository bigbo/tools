import MySQLdb

class MySQLdb(object):
    def __init__(self,host = 'localhost',user = None,pawd = 3306,debug=False):
        try :
            self.db = MySQLdb.connect(
                                    host=host,
                                    user=user,
                                    pawd=pawd)
            print "connect ok"
        except:
            print "connect error!"

    def insert(self,str_sql):
        cur_write = self.db.cursor()
        try:
            cur_write.execute(str_sql)
            self.db.commit()
        except Exception as e:
            print("run Mysql save data: %s error: %s" % (sql, e))

    def select(self,str_sql):
        conn = self.db.cursor()
        try:
            datas = conn.execute(str_sql)
        except MySQLdb.Error,e:
            print "Mysql error %d : %s." % (e.args[0], e.args[1])
        return datas,conn


    def close(self,conn):
        conn.close()


