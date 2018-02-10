import socket
import pygame
import graphics
import hashlib
import pickle
import subprocess

pygame.init()
screen_width = 750
screen_height = 538
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


sock = socket.socket()
ip = "127.0.0.1"    # means local
port = 60000
sock.connect((ip, port))

#authentication screen
login_background = pygame.image.load("authen.jpg")
login_username_box = graphics.TextBox(screen, 200, 175, 350, 40, "username")
login_password_box = graphics.TextBox(screen, 200, 241, 350, 40, "password")
login_button = graphics.Button(195, 307, 360, 43, "sign in")
create_account_button = graphics.Button(394, 371, 151, 20, "create account")
login_error_box = graphics.DialogBox(screen, 195, 123, "wrong password or username")

#register screen
signup_background = pygame.image.load("signup.jpg")
signup_username_box = graphics.TextBox(screen, 200, 170, 350, 40, "username")
signup_password_box = graphics.TextBox(screen, 200, 236, 350, 40, "password")
signup_confirm_box = graphics.TextBox(screen, 200, 300, 350, 40, "confirm password")
sign_up_button = graphics.Button(196, 366, 360, 43, "sign up")

#menu screen
menu_background = pygame.image.load("games_menu.jpg")
game_buttons = [
    graphics.ImageButton(screen, 37, 117, "images\shoot.jpg", "0"),
    graphics.ImageButton(screen, 379, 117, "images\shoot.jpg", "0"),
    graphics.ImageButton(screen, 37, 322, "images\shoot.jpg", "0"),
    graphics.ImageButton(screen, 379, 322, "images\shoot.jpg", "0")
]

#game page
page_background = pygame.image.load("images\game_page_background.jpg")
page_bar = pygame.image.load("images\page_bar.jpg")

page_scroll_box = graphics.ScrollBox(screen, 0, page_bar.get_height(), screen_width, screen_height - page_bar.get_height(),
                                     [
                                         graphics.Post(screen,0,0,screen_width - 150, "a random post about a really important subject"),
                                         graphics.Post(screen,0,0,screen_width - 150, "a random post about a really important subject"),
                                         graphics.Post(screen,0,0,screen_width - 150, "a random post about a really important subject"),
                                         graphics.Post(screen,0,0,screen_width - 150, "a random post about a really important subject"),
                                         graphics.Post(screen,0,0,screen_width - 150, "a random post about a really important subject")
                                     ])


current_screen = "login"
while True:

    while current_screen == "login":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

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
            else:
                print "FAILED LOGIN :("
                login_error_box.activate()

        pygame.display.flip()

    while current_screen == "signup":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

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
        pygame.display.flip()

    while current_screen == "menu":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        screen.blit(menu_background, (0, 0))
        for game in game_buttons:
            game.show()
            if game.is_pressed(events):
                sock.send("CHSGM~" + game.description)
                current_screen = "game_page"
                game_info = sock.recv(1024).split("~")
                chosen_game = game_info[1]
                game_price = game_info[2]
                data = sock.recv(1024).split("~")
                posts_info = pickle.loads(data[1])
                posts = [graphics.Post(screen, 0, 0, screen_width - 150, post.content) for post in posts_info]
                page_scroll_box.surfaces = posts
                # subprocess.Popen(["python", "shoot\\server.py"])
                # subprocess.Popen(["python", "shoot\\client.py"])
        pygame.display.flip()

    while current_screen == "game_page":
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        screen.blit(page_background, (0, 0))
        page_scroll_box.show(events)

        screen.blit(page_bar, (0, 0))
        pygame.display.flip()

