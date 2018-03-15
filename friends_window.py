import pygame
import graphics

window_width = 750
window_height = 538
window = pygame.display.set_mode((window_width, window_height))
friends_background = pygame.image.load("images\\friends.png")
font = pygame.font.SysFont('', 30)

messages = []
messages_box = graphics.ScrollBox(window, 0, 0, window_height, window_height/2, messages)
text_box = graphics.TextBox(window, 0, window_height/2, window_width-100, window_height/2, "enter message")
button = graphics.DrawButton(window, window_width-100, window_height/2, 100, window_height/2, (0, 255, 255), "send")

def to_surface(string):
    s = graphics.line_up(string, window_width, font)
    lines = s.split("\n")
    surface = pygame.Surface(window_width ,30*len(lines), pygame.SRCALPHA, 32).convert_alpha()
    for i in range(len(lines)):
        sur = font.render(lines[i], True, (0, 0, 0))
        surface.blit(sur, (0, i*30))

def show_messages(screen):

    for i in range(len(messages)):
        text = font.render(messages[i], True, (0, 0, 0))
        screen.blit(text, (10, 10 + i * 30))

def main():

    while True:
        window.fill((200,200,200))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if button.is_pressed(events):
            messages.append(text_box.get_text())
            print messages
            text_box.clear()
        pygame.draw.rect(window, (255, 255, 255), (text_box.x, text_box.y, text_box.width, text_box.height))
        text_box.update(events)
        show_messages(window)
        button.show()
        pygame.display.flip()




if __name__ == '__main__':
    main()