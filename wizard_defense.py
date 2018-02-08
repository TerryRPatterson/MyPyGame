import pygame, random
def main():

    pygame.init()
    origin = (0,0)
    enemy_list_location = "enemy_names.txt"
    enemy_names = import_list(enemy_list_location)
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.HWSURFACE)
    done = False
    background = pygame.image.load("Assets/Background.png")
    while not done:
        screen.blit(pygame.transform.scale(background,screen.get_size()),origin)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.update()
    pygame.quit()

class Character(pygame.sprite.Sprite):
    def __init__(self, health=0, power=0, name=None, sprite=None):
        pygame.sprite.Sprite.__init__(self)
        self.health = health
        self.power = power
        self.name = name
        self.sprite = sprite
def import_list(file):
    output = []
    open_file = open(file, "r")
    for line in open_file:
        output.append(line.strip())
    #Removes duplicate names
    output = list(set(output))
    return output

main()
