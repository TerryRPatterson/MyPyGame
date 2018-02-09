import pygame, random


def main():
    pygame.init()
    enemy_list_location = "enemy_names.txt"
    enemy_names = import_list(enemy_list_location)
    origin = (0,0)
    player = PlayerCharacter( health=10, power=10, name="Test", image_set="Assets/wizard/idle/1_IDLE_000.png",pos_x=0,pos_y=0)
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.HWSURFACE)
    done = False
    background = pygame.image.load("Assets/Background.png")
    while not done:
        screen.blit(pygame.transform.scale(background,screen.get_size()),origin)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(change_vel_y=-10)
                if event.key == pygame.K_DOWN:
                    player.move(change_vel_y=10)
                if event.key == pygame.K_RIGHT:
                    player.move(change_vel_x=10)
                if event.key == pygame.K_LEFT:
                    player.move(change_vel_x=-10)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.move(change_vel_y=10)
                if event.key == pygame.K_DOWN:
                    player.move(change_vel_y=-10)
                if event.key == pygame.K_RIGHT:
                    player.move(change_vel_x=-10)
                if event.key == pygame.K_LEFT:
                    player.move(change_vel_x=10)
        screen.blit(player.image_set,(player.pos_x,player.pos_y))
        player.update()
        pygame.display.update()
    pygame.quit()

class Character(pygame.sprite.Sprite):
    def __init__(self, health, power, name, image_set,pos_x,pos_y,vel_x,vel_y):
        super().__init__()
        self.health = health
        self.power = power
        self.name = name
        self.image_set = pygame.image.load(image_set)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
    def attack(self,target):
        if self.alive and target.alive:
            target.health -= self.power
    def move(self, change_vel_x=0, change_vel_y=0):
        self.vel_x += change_vel_x
        self.vel_y += change_vel_y
    def update(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

class PlayerCharacter(Character):
    def __init__(self, health=0 ,power=0, name="Test", image_set=None, points=0, lives=0,pos_x=0,pos_y=0,vel_x=0, vel_y=0):
        super().__init__(health, power, name, image_set, pos_x, pos_y, vel_x,vel_y)
        self.points = points
        self.lives = lives

# class Enemy(Character):
#     def init(self,health=random.randint(1,10), power=1, name=random.choice(enemy_names), image_set=None):
#         Character.__init__(self, health, power, name, image_set)
def import_list(file):
    output = []
    open_file = open(file, "r")
    for line in open_file:
        output.append(line.strip())
    #Removes duplicate entries
    output = list(set(output))
    return output

main()
