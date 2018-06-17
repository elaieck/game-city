import sqlite3
import json
import datetime


class user(object):
    #user data-base info object
    def __init__(self, name, password, friends=[], games=[]):
        self.name = name
        self.password = password
        self.friends = friends
        self.games = games


class game(object):
    #game data-base info object
    def __init__(self, id, name, price, image):
        self.id = id
        self.name = name
        self.price = price
        self.image = image


class post(object):
    #post data-base info object
    def __init__(self, game_id, content, username, datetime):
        self.game_id = game_id
        self.content = content
        self.username = username
        self.datetime = datetime


class ORM():
    #all data-base related functions - functions that require set and get from db

    def __init__(self):
        #constractor: stores - connection variable to db and db connection cursor
        self.conn = None  # will store the DB connection
        self.cursor = None   # will store the DB connection cursor

    def open_DB(self):
        # will open DB file and put value in:
        # self.conn (need DB file name)
        # and self.cursor
        self.conn = sqlite3.connect('GCDB.db')
        self.cursor = self.conn.cursor()

    def close_DB(self):
        #closes connection to db
        self.conn.close()

    def commit(self):
        #saves changes
        self.conn.commit()

    def get_user(self, name):
        #get user object from db with his username

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
        #get game object from db with game id

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
        # get list of post objects with all posts of the wanted game with game id

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
        #add a new user to users table in db
        #inserts the chosen username and password
        # puts empty lists in friends and games columns
        self.open_DB()
        sql = "INSERT INTO users (name, password, friends, games) VALUES " \
              "('%s', '%s', '%s', '%s')" % (username, password, '[]', '[]')
        self.cursor.execute(sql)
        self.commit()
        self.close_DB()

    def insert_new_post(self, game_id, content, username, datetime):
        #add a new post to posts table in db
        # inserts the chosen game id, post content, username of the writer, datetime published
        sql = "INSERT INTO posts (game_id, content, username, datetime) VALUES " \
              "(%d, '%s', '%s', '%s')" % (game_id, content, username, datetime)
        self.open_DB()
        self.cursor.execute(sql)
        self.commit()
        self.close_DB()


    def buy_game(self, username, game_id):
        #adds a game with the chosen id to the user with the chosen username's game list
        games = self.get_user(username).games
        game_info = str(game_id)+str(datetime.datetime.now().strftime("%d.%m.%Y"))
        games.append(game_info)
        games = json.dumps(games)
        sql = "UPDATE users SET games = \'%s\' WHERE name IS \'%s\'" % (games, username)
        self.open_DB()
        self.cursor.execute(sql)
        self.commit()
        self.close_DB()

    def attach_friends(self, friend1, friend2):
        # adds one friend to the list of friends of the other, and the other way around

        if friend1 == friend2:
            return
        friends_list = self.get_user(friend1).friends
        if friend2 not in friends_list:
            friends_list.append(friend2)
        sql = "UPDATE users SET friends = \'%s\' WHERE name IS \'%s\'" % (json.dumps(friends_list), friend1)
        self.open_DB()
        self.cursor.execute(sql)
        self.commit()
        self.close_DB()

        friends_list = self.get_user(friend2).friends
        if friend1 not in friends_list:
            friends_list.append(friend1)
        sql = "UPDATE users SET friends = \'%s\' WHERE name IS \'%s\'" % (json.dumps(friends_list), friend2)
        self.open_DB()
        self.cursor.execute(sql)
        self.commit()
        self.close_DB()



