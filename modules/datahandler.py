# coding: utf-8
import sqlite3
import datetime
import itertools

class Datahandler(object):
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        c = self.connection.cursor()
        c.execute("create table if not exists users \
            (id INTEGER PRIMARY KEY, name text, reg timestamp, last timestamp)")
        c.execute("create table if not exists matches \
            (id INTEGER PRIMARY KEY, pid1 integer, pid2 integer, team1 text, team2 text, goals1 integer, goals2 integer, date timestamp)")
        self.connection.commit()
        c.close()

    def insert_user(self, name):
        c = self.connection.cursor()
        c.execute("insert into users values (NULL, ?, ?, ?)", ( name, datetime.datetime.now().strftime("%d.%m.20%y"), None))
        self.connection.commit()
        c.close()

    def update_user(self, id, name, last=None):
        c = self.connection.cursor()
        if last:
            c.execute("update users set name=?, last=? where id=?", ( name, last, id, ))
        else:
            c.execute("UPDATE users SET name=? WHERE id=?", ( name, id, ))
        self.connection.commit()
        c.close()

    def delete_user(self, id):
        c = self.connection.cursor()
        c.execute("delete from users where id=?", (id, ))
        self.connection.commit()
        c.close()

    def get_users(self, id=None):
        c = self.connection.cursor()
        if id:
            c.execute("select name from users where id=?", (id, ))
        else:
            c.execute("select * from users")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data

    def get_user_names(self):
        c = self.connection.cursor()
        c.execute("select name from users")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data

    def insert_match(self, id1, id2, team1, team2, goals1, goals2, date):
        c = self.connection.cursor()
        c.execute("insert into matches values(NULL, ?, ?, ?, ?, ?, ?, ?)", (id1, id2, team1, team2, goals1, goals2, date))
        self.connection.commit()
        c.close()

    def delete_match(self, id):
        c = self.connection.cursor()
        c.execute("delete from matches where id=?", (id,))
        self.connection.commit()
        c.close()

    def get_matches(self, id=None):
        c = self.connection.cursor()
        if id:
            c.execute("select * from matches where pid1=? or pid2=?", (id, id))
        else:
            c.execute("select * from matches")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data

    def get_diff(self, id):
        c = self.connection.cursor()

        c.execute("select goals1, goals2 from matches where pid1=?", (id,))
        self.connection.commit()
        first = c.fetchall()

        c.execute("select goals1, goals2 from matches where pid2=?", (id,))
        self.connection.commit()
        sec = c.fetchall()
        c.close()

        pos = sum([a for a,b in first]) + sum([b for a,b in sec])
        neg = sum([b for a,b in first]) + sum([a for a,b in sec])

        return pos - neg

    def get_fav_team(self, id):
        c = self.connection.cursor()
        c.execute("select team1 from matches where pid1=?", (id,))
        self.connection.commit()
        first = c.fetchall()

        c.execute("select team2 from matches where pid2=?", (id,))
        self.connection.commit()
        sec = c.fetchall()
        c.close()

        team_count = {}

        for t1, t2 in itertools.izip_longest(first, sec):
            team_count[t1] = team_count.get(t1, 0) + 1
            team_count[t2] = team_count.get(t2, 0) + 1

        team_count.pop(None)
        m = max(team_count.values())

        for k, v in team_count.items():
            if v == m:
                return k[0]

    def get_teams(self):
        c = self.connection.cursor()
        c.execute("select team1, team2 from matches")
        self.connection.commit()
        data = c.fetchall()

        teams = []

        for t1, t2 in data:
            if t1 not in teams: teams.append(t1)
            if t2 not in teams: teams.append(t2)
        return sorted(teams)

    def close(self):
        self.connection.close()