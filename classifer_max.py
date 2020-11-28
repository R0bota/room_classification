import pygame
pygame.init()

categories = ("bath_room","living_room","sleeping_room","empty_room","balcony","house","kitchen","floor_plan","corridor","other")
screen = pygame.display.set_mode((800,600))
path = "/Users/maximilian/Documents/python/room_classification/data/out/600_4E116827495442A18FA07F6DC281DFE8.jpg"
img = pygame.image.load(path)


pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)

button = pygame.Rect(100, 100, 50, 50)
buttons = []
texts = []
i = 0




for category in categories:
    i += 1
    buttons.append(pygame.Rect(10, 40 * i, 100, 30))
    texts.append(myfont.render('Some Text', False, (255, 0, 0)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button.collidepoint(mouse_pos):
                    # prints current location of mouse
                    print('button was pressed at {0}'.format(mouse_pos))


    screen.fill((0,0,0))
    screen.blit(img, (0,0))

    for b in buttons:
        pygame.draw.rect(screen, (0,0,0), b)  # draw button


    for t in texts:
        screen.blit(t,(0,0))

    #pygame.draw.rect(screen, [0, 0, 0], button)  # draw button

    pygame.display.update()

pygame.quit()
