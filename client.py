import socket
import pygame
import graphics
import hashlib
import pickle
import subprocess
import datetime
import threading
from os import _exit

pygame.init()
screen_width = 750
screen_height = 538
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

done = False
bye = False

sock = socket.socket()
ip = "127.0.0.1"    # means local
port = 59567
sock.connect((ip, port))

shoot_image = pygame.image.load("images\shoot_image.jpg")

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

messages = []
threads = []
messages_to_send = []

def chat_server():
    chat_sock = socket.socket()
    chat_sock.bind(("0.0.0.0", 61002))
    chat_sock.listen(10)
    while True:
        cli_s, addr = chat_sock.accept()
        t = threading.Thread(target=chat_manage, args=(cli_s,))
        t.start()
        threads.append(t)


def chat_manage(chat):
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
        elif msg != "=%#nothing#%=":
            messages_to_send.append((friend, msg))
        chat.send("ok")



def check_new_message():
    sock.send("GETMSG")
    data = sock.recv(10111)
    if data != "NOMSG":
        data = data.split("~")
        messages.append([data[1], data[2]])
    if len(messages_to_send) != 0:
        sock.send("SNDMSG~%s~%s" % (messages_to_send[0][0], messages_to_send[0][1]))
        messages_to_send.pop(0)

def do_events():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            _exit(1)
    return events

current_screen = "login"
while True:

    while current_screen == "login":    #==========================================================================
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
                login_error_box.activate()

        pygame.display.flip()

    while current_screen == "signup":   #==========================================================================
        events = events = do_events()

        screen.blit(signup_background, (0, 0))
        signup_username_box.update(events)
        signup_password_box.update(events)
        signup_confirm_box.update(events)

        if sign_up_button.is_pressed(events):
            username = signup_username_box.get_text()
            password = hashlib.md5(signup_password_box.get_text()).hexdigest()
            sock.send("SIGNUP~%s~%s" % (username, password))
            recv = sock.recv(3)
            if recv == "SUS":
                current_screen = "login"
            else:
                print "SIGN UP FAILED :("
        if signup_back_button.is_pressed(events):
            current_screen = "login"

        pygame.display.flip()

    while current_screen == "menu":     #==========================================================================
        events = events = do_events()

        check_new_message()

        if friends_button.is_pressed(events):
            sock.send("GETFRNDS")
            friends23 = sock.recv(1024)
            print friends23
            chat_friend = friends_bar.activate()
            if chat_friend is not None:
                subprocess.Popen(["python", "friends_window.py", username, chat_friend])


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

        pygame.display.flip()

    while current_screen == "game_page":    #==========================================================================
        events = events = do_events()

        check_new_message()

        if page_back_button.is_pressed(events):
            current_screen = "menu"

        elif play_button.is_pressed(events):
            sock.send("PLAY~"+game_id)
            answer = sock.recv(1024)
            if answer == "approved":
                subprocess.Popen(["python", "shoot\\server.py"])
                subprocess.Popen(["python", "shoot\\client.py"])
            else:
                page_need_to_buy.activate()


        elif buy_button.is_pressed(events):
            sock.send("BUY~"+game_id)
            recv = sock.recv(1024)
            if recv == "ALBUY":
                page_bought_message.activate()
            else:
                page_buy_prompt.activate()

        for surface in page_scroll_box.surfaces:
            if surface.__class__ == graphics.Post:
                if surface.friend_button.is_pressed(events):
                    print "press"
                    sock.send("ADDFRND~"+surface.user)

        screen.blit(page_background, (0, 0))
        page_scroll_box.show(events)
        page_scroll_box.surfaces[3].show()
        screen.blit(page_bar, (0, 0))
        post_content = page_write_post.update(events)
        if post_content != "":
            sock.send("POST~"+game_id+"~"+post_content+"~"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        # graphics.screen_print(screen, pygame.mouse.get_pos())
        pygame.display.flip()


