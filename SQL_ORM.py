import sqlite3
import json
import datetime
    # https://docs.python.org/2/library/sqlite3.html
    # https://www.youtube.com/watch?v=U7nfe4adDw8


class user(object):
    def __init__(self, name, password, friends=[], games=[]):
        self.name = name
        self.password = password
        self.friends = friends
        self.games = games


class game(object):
    def __init__(self, id, name, price, image):
        self.id = id
        self.name = name
        self.price = price
        self.image = image


class post(object):
    def __init__(self, game_id, content, username, datetime):
        self.game_id = game_id
        self.content = content
        self.username = username
        self.datetime = datetime

    
class ORM():
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor
        # print str(self.GetCountries())
        # print str(self.GetPresidents())

    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('GCDB.db')
        self.cursor = self.conn.cursor()
        
    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    #All read SQL
    def get_user(self, name):
        self.open_DB()

        self.cursor.execute("SELECT * FROM users WHERE name IS \"" + name + "\"; ")
        res = self.cursor.fetchall()

        if len(res) == 0:
            return None

        res = res[0]

        games_list = [x for x in json.loads(res[3])]

        usr = user( str(res[0]), str(res[1]), json.loads(res[2]), games_list )

        self.close_DB()
        return usr

    def get_game(self, game_id):
        self.open_DB()

        self.cursor.execute("SELECT * FROM games WHERE id IS \"" + str(game_id) + "\"; ")
        res = self.cursor.fetchall()

        if len(res) == 0:
            return None

        res = res[0]

        game_obj = game(int(res[0]), str(res[1]), float(res[2]), str(res[3]))

        self.close_DB()
        return game_obj

    def get_game_posts(self, game_id):
        self.open_DB()

        self.cursor.execute("SELECT * FROM posts WHERE game_id IS \""+str(game_id)+"\"; ")
        res = self.cursor.fetchall()

        if len(res) == 0:
            return None

        posts = []
        for post_list in res:
            posts.append(post(int(post_list[0]), str(post_list[1]), str(post_list[2]), str(post_list[3])))

        self.close_DB()
        return posts



    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #______end of read start write ____________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________



    def insert_new_user(self, username, password):

        self.open_DB()
        sql = "INSERT INTO users (name, password, friends, games) VALUES " \
              "('%s', '%s', '%s', '%s')" % (username, password, '[]', '[]')
        self.cursor.execute(sql)
        self.commit()
        self.close_DB()

    def insert_new_post(self, game_id, content, username, datetime):
        sql = "INSERT INTO posts (game_id, content, username, datetime) VALUES " \
              "(%d, '%s', '%s', '%s')" % (game_id, content, username, datetime)
        self.open_DB()
        self.cursor.execute(sql)
        self.commit()
        self.close_DB()

    def remove_game(self, username, game_id):
        self.open_DB()

        self.commit()
        self.close_DB()

    def buy_game(self, username, game_id):
        print "username: " + str(username)
        print "id: " + str(game_id)
        games = self.get_user(username).games
        print "games: " + str(games)
        game_info = str(game_id)+str(datetime.datetime.now().strftime("%d.%m.%Y"))
        print "infp: " + str(game_info)
        games.append(game_info)
        games = json.dumps(games)
        print "json: " + str(games)
        sql = "UPDATE users SET games = \'%s\' WHERE name IS \'%s\'" % (games, username)
        self.open_DB()
        self.cursor.execute(sql)
        self.commit()
        self.close_DB()

    def attach_friends(self, friend1, friend2):
        self.open_DB()

        self.commit()
        self.close_DB()

    def detach_friends(self, friend1, friend2):
        self.open_DB()

        self.commit()
        self.close_DB()


def main_test():

    db = ORM()
    print db.get_user("elaieck")
    db.insert_new_post(0, "hi guys!", "elaieck", "22.1.2018")
    # db.insert_new_user("food_lover", "bc815654dd7ce41e836a6ca7b0786b26")

if __name__ == "__main__":
    main_test()


