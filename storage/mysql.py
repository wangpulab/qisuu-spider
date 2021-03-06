#! /bin/python
# coding: utf-8

from logs.QisuuLog import QisuuLog
import MySQLdb

class MySQL(object):

    def __init__(self, dbname, host='127.0.0.1', user='root', passwd='root'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.log = QisuuLog()
        self.connect()

    def connect(self):
        try:
            self.db = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname)
        except Exception, e:
            message = 'connect db {name} failure for {message}'.format(
                name=self.dbname,
                message=e.message,
            )
            self.log.error(message)
        else:
            self.cursor = self.db.cursor()

    def select(self, sql):
        try:
            self.cursor.execute(sql)
            self.results = self.cursor.fetchall()
        except Exception, e:
            self.log.error(e.message)
            print 'query data failuer for {0}'.format(e.message)

    def insert(self, sql):
        self.change(sql, 'insert')

    def update(self, sql):
        self.change(sql, 'update')

    def delete(self, sql):
        self.change(sql, 'delete')

    def change(self, sql, opt):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            self.log.error(e.message)
            print '\033[31m {0} \033[0m data failuer for {1}'.format(opt, e.message)