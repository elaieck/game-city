# -*- coding: utf-8 -*-
import pygame

def main():
    window_width = 287
    window_height = 538
    window = pygame.display.set_mode((window_width, window_height))
    friends_background = pygame.image.load("images\\friends.png")
    window.blit(friends_background, (0, 0))
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        pygame.display.flip()


if __name__ == '__main__':
    main()