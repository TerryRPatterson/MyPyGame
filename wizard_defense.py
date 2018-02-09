import pygame, random, os

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.HWSURFACE)
def main():
    pygame.init()
    enemy_list_location = "enemy_names.txt"
    enemy_names = import_list(enemy_list_location)
    origin = (0,0)
    player = PlayerCharacter( health=10, power=10, name="Test", image_set="Assests/wizard",pos=(0,0),move_rate=5)
    done = False
    background = pygame.image.load("Assets/Background.png")
    while not done:
        screen.blit(pygame.transform.scale(background,screen.get_size()),origin)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(change_vel=(0,-player.move_rate))

                if event.key == pygame.K_DOWN:
                    player.move(change_vel=(0,player.move_rate))

                if event.key == pygame.K_RIGHT:
                    player.move(change_vel=(player.move_rate,0))

                if event.key == pygame.K_LEFT:
                    player.move(change_vel=(-player.move_rate,0))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.move(change_vel=(0,player.move_rate))

                if event.key == pygame.K_DOWN:
                    player.move(change_vel=(0,-player.move_rate))

                if event.key == pygame.K_RIGHT:
                    player.move(change_vel=(-player.move_rate,0))

                if event.key == pygame.K_LEFT:
                    player.move(change_vel=(player.move_rate,0))

        screen.blit(player.image_set,player.position)
        player.update()
        pygame.display.update()
    pygame.quit()

class Character(pygame.sprite.Sprite):
    def __init__(self, health, power, name, image_set,pos,vel,move_rate):
        super().__init__()
        self.health = health
        self.power = power
        self.name = name
        self.image_set = image_set
        self.position = pos
        self.velocity = vel
        self.animating =  False
        self.move_rate = move_rate
        self.image_current = pygame.transform.scale(pygame.image.load("Assets/wizard/idle/1_IDLE_000.png"),(int(screen.get_size()[0]*0.1),int(screen.get_size()[1]*0.1)))

        #Loading sprites
        idles = []
        attacks = []
        walking = []
        death = []
        for image in os.listdir(os.path("".join(image_set,"/idle"))):
            current_image = pygame.image.load(image)
            idles.append(pygame.transform.scale(current_image,int(screen.get_size()[0]*0.1),int(screen.get_size()[1]*0.1)))

        for image in os.listdir(os.path("".join(image_set,"/attack"))):
            current_image = pygame.image.load(image)
            attacks.append(pygame.transform.scale(current_image,int(screen.get_size()[0]*0.1),int(screen.get_size()[1]*0.1)))

        for image in os.listdir(os.path("".join(image_set,"/walk"))):
            current_image = pygame.image.load(image)
            idles.append(pygame.transform.scale(current_image,int(screen.get_size()[0]*0.1),int(screen.get_size()[1]*0.1)))

        for image in os.listdir(os.path("".join(image_set,"/die"))):
            current_image = pygame.image.load(image)
            death.append(pygame.transform.scale(current_image,int(screen.get_size()[0]*0.1),int(screen.get_size()[1]*0.1)))

    def attack(self,target):
        if self.alive and target.alive:
            target.health -= self.power
    def move(self, change_vel=(0,0)):
        self.velocity = (self.velocity[0] + change_vel[0], self.velocity[1] + change_vel[1])
    def update(self):
        self.position = (self.velocity[0] + self.position[0], self.velocity[1] + self.position[1])

    def animate(self,type,duration):

    def animating():
        if animating == True:
            pass


class PlayerCharacter(Character):
    def __init__(self, health=0 ,power=0, name="Test", image_set=None, points=0, lives=0, pos=(0,0), vel=(0,0), move_rate=10):
        super().__init__(health, power, name, image_set, pos, vel, move_rate)
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
