import sqlite3 as sq
from flask import Flask,render_template,redirect
class login:
    def __init__(self):
        
        con = sq.connect("Main.db")

        cur = con.cursor()

        Query = """
        create table if not exists keys(password text primary key);
        """
        cur.execute(Query)

        #self.createkeys()

        con.close()

    def createkeys(self):

        con = sq.connect("Main.db")

        cur = con.cursor()
 # executemany expects a list of tuples. Each string needs to be
        # wrapped in a tuple, indicated by the trailing comma.
        Ids = [
            ("admin",),
            ("co_admin",),
            ("member",)
        ]
        
        Query = """insert into keys(password) values(?);"""
        try:
            cur.executemany(Query,Ids)
            con.commit()
        except sq.OperationalError:
            pass     
        finally:
            con.close()
    
    def checkPassword(self,password):

        con = sq.connect("Main.db")

        cur = con.cursor()

        data = cur.execute("select * from keys")

        entries = data.fetchall()
        filtered = []
        for tuple in entries:
            filtered.extend(tuple)

        print("data = ",filtered)
        if password in filtered:
            return True

        con.close()
        return False
        
    
        


