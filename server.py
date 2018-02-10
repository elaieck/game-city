import socket
import threading
from SQL_ORM import ORM
import pickle

db = ORM()
srv_sock = socket.socket()
ip = "0.0.0.0" # means local
port = 60000
srv_sock.bind((ip, port))
srv_sock.listen(10)
threads = []


def parts(message):
    return message.split("~")


def get_authen(sock):
    data = sock.recv(1024)
    print "~"+data+"~"
    message = parts(data)
    print message
    if message[0] == "LOGIN":
        print "login is here"
        user = db.get_user(message[1])
        if user is None:
            sock.send("LOF")
            return ""
        elif user.password != message[2]:
            sock.send("LOF")
            return ""
        else:
            sock.send("LOS")
            return user
    else:
        if db.get_user(message[1]) is not None:
            sock.send("SUF")
            return ""
        else:
            db.insert_new_user(message[1], message[2])
            sock.send("SUS")
            return ""


def recv_choice(sock):
    game_id = parts(sock.recv(1024))[1]
    return db.get_game(game_id)

def send_game_info(sock, game):
    sock.send("GINFO~" + str(game.name) + "~" + str(game.price))
    posts = db.get_game_posts(game.id)
    str_posts = pickle.dumps(posts)
    sock.send("GPOSTS~" + str_posts)


def server(sock):
    while True:
        username = get_authen(sock)
        if username is not "":
            break
    while True:
        game = recv_choice(sock)
        send_game_info(sock, game)

    # while True:
    #     data = sock.recv(1024)

while True:
    cli_s, addr = srv_sock.accept()
    t = threading.Thread(target=server, args=(cli_s,))
    t.start()
    threads.append(t)

