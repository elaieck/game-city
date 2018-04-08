import socket
import threading
from SQL_ORM import ORM
import pickle
import subprocess


db = ORM()
srv_sock = socket.socket()
ip = "0.0.0.0" # means local
port = 60000
srv_sock.bind((ip, port))
srv_sock.listen(10)
threads = []
game_is_open = False


def parts(message):
    return message.split("~")


def get_authen(sock):
    data = sock.recv(1024)
    message = parts(data)
    if message[0] == "LOGIN":
        user = db.get_user(message[1])
        if user is None:
            sock.send("LOF")
            return None
        elif user.password != message[2]:
            sock.send("LOF")
            return None
        else:
            sock.send("LOS")
            return user
    else:
        if db.get_user(message[1]) is not None:
            sock.send("SUF")
            return None
        else:
            db.insert_new_user(message[1], message[2])
            sock.send("SUS")
            return None


def send_game_info(sock, game):
    sock.send("GINFO~" + str(game.name) + "~" + str(game.price))
    posts = db.get_game_posts(game.id)
    str_posts = pickle.dumps(posts)
    sock.send("GPOSTS~" + str_posts)

def game_bought(game_id, username):
    purchased_games_info = db.get_user(username).games
    purchased_games = [game_info[:2] for game_info in purchased_games_info]
    return game_id in purchased_games



def server(sock):
    while True:
        user = get_authen(sock)
        if user is not None:
            break
    while True:
        info = parts(sock.recv(1024))
        action = info[0]
        if action == "":
            break
        elif action == "CHSGM":
            game = db.get_game(info[1])
            send_game_info(sock, game)
        elif action == "POST":
            db.insert_new_post(int(info[1]), info[2], user.name, info[3])
        elif action == "PLAY":
            if game_bought(info[1], user.name):
                sock.send("approved")
            else:

                sock.send("BUYPLZ")
        elif action == "BUY":
            if game_bought(info[1], user.name):
                sock.send("ALBUY")
            else:
                db.buy_game(user.name, info[1])
                sock.send("BUYSUC")





# while True:
    #     data = sock.recv(1024)



subprocess.Popen(["python", "shoot\\server.py"])
while True:
    cli_s, addr = srv_sock.accept()
    t = threading.Thread(target=server, args=(cli_s,))
    t.start()
    threads.append(t)

