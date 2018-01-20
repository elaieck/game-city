import socket
import threading
import database
import json

srv_sock = socket.socket()
ip = "0.0.0.0" # means local
port = 60000
srv_sock.bind((ip, port))
srv_sock.listen(10)
threads = []

def server(sock):
    while True:
        username = get_authen()
        if username is not None:
            break
    # game = get_choice()
    # send_game_info(game)
    # send_posts(game)
    while True:
        data = new_sock.recv(1024)

while True:
    cli_s, addr = srv_sock.accept()
    t = threading.Thread(target=server, args=(cli_s,))
    print "hi"
    t.start()
    threads.append(t)

def parts(message):
    return message.split("~")


def get_authen(sock):
    data = sock.recv(1024)
    message = parts(data)
    if message[0] == "LOGIN":
        user = database.get_user(message[1])
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
        if database.get_user(message[1]) is not None:
            sock.send("SUF")
            return ""
        else:
            database.create_new_user(message[1], message[2])
            return ""


def recv_choice(sock):
    game = sock.recv(1024)
    game = database.get_game(game)
    sock.send("GINFO~" + game.price + "~" + game.image_base64)
    posts = database.get_game_posts(game)
    string_posts = []
    for post in posts:
        string_posts.append(json.dumps(post))
    sock.send("GINFO~" + "~".join(posts))



