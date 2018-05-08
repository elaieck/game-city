import pygame
import graphics
import socket

window_width = 750
window_height = 538
window = pygame.display.set_mode((window_width, window_height))
friends_background = pygame.image.load("images\\friends.png")
font = pygame.font.SysFont('', 30)
online = True
username = "elaieck"
GREEN = (137, 255, 223)
GREY = (127, 127, 127)

messages = []
chat_box = graphics.ScrollBox(window, 0, 0, window_width, window_height/2, margin=5)
text_box = graphics.TextBox(window, 0, window_height/2, window_width-100, window_height/2, "enter message")
button = graphics.DrawButton(window, window_width-100, window_height/2, 100, window_height/2, (0, 255, 255), "send")

sock = socket.socket()

def to_surface(message):
    if type(message) is tuple:
        s = graphics.line_up(message[0]+": "+message[1], window_width, font)
        lines = s.split("\n")
        surface = pygame.Surface((window_width, 30*len(lines)), pygame.SRCALPHA, 32).convert_alpha()
        name_width = font.size(message[0]+": ")[0]
        sur = font.render(message[0]+": ", True, GREEN)
        surface.blit(sur, (0, 0))
        sur = font.render(lines[0][len(message[0])+2:], True, (0, 0, 0))
        surface.blit(sur, (name_width, 0))
        if len(lines) > 1:
            for i in range(len(lines)-1):
                sur = font.render(lines[i+1], True, (0, 0, 0))
                surface.blit(sur, (0, (i+1)*30))
    else:
        s = graphics.line_up(message, window_width, font)
        lines = s.split("\n")
        surface = pygame.Surface((window_width, 30*len(lines)), pygame.SRCALPHA, 32).convert_alpha()
        for i in range(len(lines)):
            sur = font.render(lines[i], True, GREY)
            surface.blit(sur, (0, i*30))
    
    return surface

# def show_messages(screen):
#
#     for i in range(len(messages)):
#         text = font.render(messages[i], True, (0, 0, 0))
#         screen.blit(text, (10, 10 + i * 30))

def main():

    while True:
        window.fill((200, 200, 200))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if button.is_pressed(events):
            if online:
                messages.append((username, text_box.get_text()))
                text_box.clear()
            else:
                messages.append("Your friend is not online")

        chat_box.surfaces = [to_surface(x) for x in messages]
        chat_box.show(events)
        pygame.draw.rect(window, (255, 255, 255), (text_box.x, text_box.y, text_box.width, text_box.height))
        text_box.update(events)
        button.show()
        pygame.display.flip()




if __name__ == '__main__':
    main()