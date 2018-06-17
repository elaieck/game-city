import socket
import pygame
import graphics
import hashlib
import pickle
import subprocess
import datetime
import threading
from sys import argv
from os import _exit

pygame.init()
screen_width = 750
screen_height = 538
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

done = False
bye = False

admin_ip = "127.0.0.1"
admin_port = 61234

sock = socket.socket()
ip = argv[1]
port = int(argv[2])
sock.connect((ip, port))

shoot_image = pygame.image.load("images\shoot_image.jpg")

username = ""

#authentication screen
login_background = pygame.image.load("authen.jpg")
login_username_box = graphics.TextBox(screen, 200, 175, 350, 40, "username")
login_password_box = graphics.TextBox(screen, 200, 241, 350, 40, "password", hide=True)
login_button = graphics.Button(195, 307, 360, 43, "sign in")
create_account_button = graphics.Button(394, 371, 151, 20, "create account")
login_error_box = graphics.DialogBox(screen, 195, 123, "wrong password or username")

#register screen
signup_background = pygame.image.load("signup.jpg")
signup_username_box = graphics.TextBox(screen, 200, 170, 350, 40, "username")
signup_password_box = graphics.TextBox(screen, 200, 236, 350, 40, "password", hide=True)
signup_confirm_box = graphics.TextBox(screen, 200, 300, 350, 40, "confirm password", hide=True)
sign_up_button = graphics.Button(196, 366, 360, 43, "sign up")
signup_back_button = graphics.Button(0, 0, 72, 72, "back")

#menu screen
menu_background = pygame.image.load("games_menu.jpg")
game_buttons = [
    graphics.ImageButton(screen, 37, 117, "images\shoot.jpg", "00"),
    graphics.ImageButton(screen, 379, 117, "images\shoot.jpg", "00"),
    graphics.ImageButton(screen, 37, 322, "images\shoot.jpg", "00"),
    graphics.ImageButton(screen, 379, 322, "images\shoot.jpg", "00")
]
friends_bar = graphics.FriendsBar(screen, 0, 0)
friends_button = graphics.Button(576, 25, 81, 67, "friends")
logout_button = graphics.Button(664, 29, 52, 63, "logout")

#game page
page_background = pygame.image.load("images\game_page_background.jpg")
page_bar = pygame.image.load("images\page_bar.jpg")
page_back_button = graphics.Button(50, 30, 65, 21, "back")
page_write_post = graphics.WritePostBar(screen)
page_scroll_box = graphics.ScrollBox(screen, 0, page_bar.get_height(), screen_width,
                                     screen_height - page_bar.get_height() - 58, [])
page_buy_prompt = graphics.PromptBox(screen, 195, 123, 30, "Credit Card Details")
page_bought_message = graphics.DialogBox(screen, 195, 123, "you already purchased this game")
page_need_to_buy = graphics.DialogBox(screen, 195, 123, "you have to purchase this game")
game_id = "00"
game_name = ""
game_price = ""
game_image = ""
posts_info = ""
play_button = None
buy_button = None
posts = []

# info lists
processes = []
group = []
messages = []
threads = []
messages_to_send = []

in_group = False
said_yes = True

def chat_server():
    #open a multiclient connection with a chat window
    chat_sock = socket.socket()
    chat_sock.bind(("0.0.0.0", 61005))
    chat_sock.listen(10)
    while True:
        cli_s, addr = chat_sock.accept()
        t = threading.Thread(target=chat_manage, args=(cli_s,))
        t.start()
        threads.append(t)


def chat_manage(chat):
    # communicates with the chat window
    # sends the messages from the window to the server
    friend = chat.recv(1024)
    while True:
        recv = chat.recv(1024)
        if recv == "":
            break
        elif recv == "CHTMSG":
            to_send = "=%#nothing#%="
            for msg in messages:
                if msg[0] == friend:
                    to_send = msg[1]
                    messages.remove(msg)
                    break
            chat.send(to_send)
        msg = chat.recv(10100)
        if msg == "":
            break
        msg = msg.split("~")
        if msg[0] == "INVT":
            messages_to_send.append((friend, "=%#00#%=", ))
        elif msg[1] != "=%#nothing#%=":
            messages_to_send.append((friend, msg[1]))
        chat.send("OK")


def pop_error(text):
    # pop a dialog box with and error
    error_box = graphics.DialogBox(screen, 195, 123, text)
    return error_box.activate(processes)

def check_new_message():
    # check for a new message
    # if a new message arrived, append it to the messages list
    sock.send("GETMSG")
    data = sock.recv(10111)
    if data != "NOMSG":
        data = data.split("~")
        messages.append([data[1], data[2]])
    if len(messages_to_send) != 0:
        sock.send("SNDMSG~%s~%s" % (messages_to_send[0][0], messages_to_send[0][1]))
        messages_to_send.pop(0)

def check_new_requests():
    # check for a new friend request
    # if a new message arrived, pop a dialog box
    sock.send("GETREQ")
    data = sock.recv(1024)
    if data != "NOREQ":
        data = data.split("~")
        answer = pop_error(data[1]+" wants to be your friend")
        if answer:
            sock.send("ADDFRND~"+data[1])

def check_new_accpets():
    #ask server if there are any group acceptances
    # if there are, open group and open game server
    global in_group
    sock.send("GETACPT")
    recv = sock.recv(1024)
    if recv != "NOACPT" and not in_group:
        recv = recv.split("~")
        in_group = True
        group.append(recv[0])
        proc = subprocess.Popen(["python", "shoot\\server.py"])
        processes.append(proc)

def check_new_invites():
    # check for a new invitation to play
    # if there is ,pop a dialog box
    # if agreed, send it to the server
    global in_group
    global admin
    global admin_ip
    global admin_port
    sock.send("GETINVT")
    recv = sock.recv(1024)
    if recv != "NOINVT":
        recv = recv.split("~")
        if pop_error(recv[1]+" invited you to play"):
            sock.send("SNDACPT~"+recv[1]+"~"+recv[2])
            in_group = True
            admin = recv[1]
            admin_ip = recv[3]
            admin_port = recv[4]

def get_menu():
        # show menu and check if any of tha games are pressed
        # if any game is pressed, get all its data from the server
        global current_screen
        global game_id
        global game_name
        global game_price
        global game_image
        global posts_info
        global play_button
        global buy_button
        global posts
        screen.blit(menu_background, (0, 0))
        for game in game_buttons:
            game.show()
            if game.is_pressed(events):
                sock.send("CHSGM~" + game.description)
                current_screen = "game_page"
                game_info = sock.recv(1024).split("~")
                data = sock.recv(100000).split("~")

                game_id = game.description
                game_name = game_info[1]
                game_price = game_info[2]
                game_image = pygame.image.load("images\\"+game_name+"_image.jpg")
                posts_info = pickle.loads(data[1])
                play_button = graphics.DrawButton(screen, 0, 0, 120, 36, (137, 255, 223), "PLAY NOW")
                buy_button = graphics.DrawButton(screen, 0, 0, 120, 36, (137, 255, 223), "BUY - " + game_price)
                posts = [graphics.Post(screen, 0, 0, screen_width - 80, post.username, post.content)
                         for post in posts_info[::-1]]
                page_scroll_box.surfaces = [game_image] + [play_button] + [buy_button] + posts

def do_events():
    # get ptgmae events
    # if window is closed, all processes are killed
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            for proc in processes:
                proc.kill()
            _exit(1)
    return events

current_screen = "login"
while True:

    while current_screen == "login":    #============ login page =================
        events = do_events()

        screen.blit(login_background, (0, 0))
        login_username_box.update(events)
        login_password_box.update(events)

        if create_account_button.is_pressed(events):
            current_screen = "signup"

        elif login_button.is_pressed(events):
            username = login_username_box.get_text()
            password = hashlib.md5(login_password_box.get_text()).hexdigest()
            sock.send("LOGIN~%s~%s" % (username, password))

            recv = sock.recv(3)
            if recv == "LOS":
                current_screen = "menu"
                t = threading.Thread(target=chat_server)
                t.start()
            else:
                print "FAILED LOGIN :("
                login_error_box.activate(processes)

        pygame.display.flip()

    while current_screen == "signup":   #============== sign up page ==================
        events = do_events()

        screen.blit(signup_background, (0, 0))
        signup_username_box.update(events)
        signup_password_box.update(events)
        signup_confirm_box.update(events)

        if sign_up_button.is_pressed(events):
            if signup_password_box.get_text() != signup_confirm_box.get_text():
                pop_error("password different than verified")
                break
            new_username = signup_username_box.get_text()
            password = hashlib.md5(signup_password_box.get_text()).hexdigest()
            sock.send("SIGNUP~%s~%s" % (new_username, password))
            recv = sock.recv(3)
            if recv == "SUS":
                current_screen = "login"
            else:
                pop_error("username already exists")

        if signup_back_button.is_pressed(events):
            current_screen = "login"

        pygame.display.flip()

    while current_screen == "menu":     #============= menu page ======================
        events = do_events()

        check_new_message()

        if friends_button.is_pressed(events):
            sock.send("GETFRNDS")
            friends_list = sock.recv(1024).split("~")
            if len(friends_list) != 1:
                friends_bar.set_friends(friends_list[1:])
            for friend_button in friends_bar.scroll_box.surfaces:
                if friend_button.description in [x[0] for x in messages]:
                    friend_button.color = (0, 255, 255)
                    friend_button.text_color = (255, 255, 255)

            chat_friend = friends_bar.activate(processes)
            if chat_friend is not None:
                proc = subprocess.Popen(["python", "chat.py", username, chat_friend])
                processes.append(proc)

        check_new_accpets()
        get_menu()
        check_new_invites()
        check_new_requests()

        pygame.display.flip()

    while current_screen == "game_page":    #=========== game page ==================
        events = events = do_events()

        check_new_message()
        check_new_requests()

        if page_back_button.is_pressed(events):
            current_screen = "menu"

        elif play_button.is_pressed(events):
            sock.send("PLAY~"+game_id)
            answer = sock.recv(1024)
            if answer == "approved":
                proc = subprocess.Popen(["python", "shoot\\client.py", admin_ip])
                processes.append(proc)
            else:
                page_need_to_buy.activate(processes)


        elif buy_button.is_pressed(events):
            sock.send("BUY~"+game_id)
            recv = sock.recv(1024)
            if recv == "ALBUY":
                page_bought_message.activate(processes)
            else:
                page_buy_prompt.activate(processes)

        for surface in page_scroll_box.surfaces:
            if surface.__class__ == graphics.Post:
                if surface.friend_button.is_pressed(events):
                    sock.send("ASKFRND~"+surface.user)

        screen.blit(page_background, (0, 0))
        page_scroll_box.show(events)
        screen.blit(page_bar, (0, 0))
        post_content = page_write_post.update(events, processes)
        if post_content != "":
            sock.send("POST~"+game_id+"~"+post_content+"~"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        pygame.display.flip()


