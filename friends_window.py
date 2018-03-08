import pygame
import graphics

window_width = 750
window_height = 538
window = pygame.display.set_mode((window_width, window_height))
friends_background = pygame.image.load("images\\friends.png")

text_box = graphics.TextBox(window, 0, window_height/2, window_width-100, window_height/2, "enter message")
button = graphics.DrawButton(window, window_width-100, window_height/2, 100, window_height/2, (0,255,255), "send")
messages = []
def main():

    while True:
        window.fill((255,255,255))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if button.is_pressed(events):
            messages.append()
            text_box.clear()
        text_box.update(events)
        button.show()
        pygame.display.flip()


if __name__ == '__main__':
    main()