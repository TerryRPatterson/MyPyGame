#! /usr/bin/env python3
import random
import glob
import pygame
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)


def main():
    pygame.init()
    origin = (0, 0)
    wizard = SpriteGroup("Assets/wizard")
    skeleton = SpriteGroup("Assets/skeleton")
    RoundControl()
    player = PlayerCharacter(health=10, power=10, name="Test",
                             image_set=wizard, pos=(0, 0),
                             move_rate=5)
    # skeleton.position = (screen.get_width()-skeleton.current_image.get_width(),
    #                      random.randint(0,
    #                      screen.get_height()
    #                      - skeleton.current_image.get_height()))
    done = False
    background = pygame.image.load("Assets/Background.png")
    while not done:
        screen.blit(pygame.transform.scale(background,
                                           screen.get_size()), origin)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_UP:
                    player.move(change_vel=(0, -player.move_rate))

                if event.key == pygame.K_DOWN:
                    player.move(change_vel=(0, player.move_rate))

                if event.key == pygame.K_RIGHT:
                    player.move(change_vel=(player.move_rate, 0))

                if event.key == pygame.K_LEFT:
                    player.move(change_vel=(-player.move_rate, 0))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.move(change_vel=(0, player.move_rate))

                if event.key == pygame.K_DOWN:
                    player.move(change_vel=(0, -player.move_rate))

                if event.key == pygame.K_RIGHT:
                    player.move(change_vel=(-player.move_rate, 0))

                if event.key == pygame.K_LEFT:
                    player.move(change_vel=(player.move_rate, 0))

        skeleton.update()
        player.update()
        pygame.display.update()
    pygame.quit()


class Character(pygame.sprite.Sprite):
    def __init__(self, health, power, name, image_set, pos, move_rate):
        """Intializes Character."""
        super().__init__()
        self.health = health
        self.power = power
        self.name = name
        self.image_set = image_set
        self.position = pos
        self.velocity = (0, 0)
        self.animating = False
        self.move_rate = move_rate

        # Loading sprites
        self.current_image = self.image_set.idles[0]

        self.animate()

    def attack(self, target):
        if self.alive and target.alive:
            target.health -= self.power

    def move(self, change_vel=(0, 0)):
        """
        Used to change the velocity of the player.

        Velocity is applied to player postion every frame.
        """
        self.velocity = (self.velocity[0] + change_vel[0], self.velocity[1]
                         + change_vel[1])

    def update(self):
        self.position = (self.velocity[0] + self.position[0], self.velocity[1]
                         + self.position[1])
        self.update_animation()
        screen.blit(self.current_image, self.position)

    def animate(self, type="idle", duration=0.5):
        if type == "death":
            self.anim_list = self.image_set.death
            self.animating = True

        if type == "walk":
            self.anim_list = self.image_set.walking
            self.animating = True

        if type == "attack":
            self.animating = True
            self.anim_list = self.image_set.attacks

        if type == "idle":
            self.anim_list = self.image_set.idles
            self.animating = False

        self.start_time = pygame.time.get_ticks()
        self.stop_time = self.start_time + (duration * 1000)
        self.frames = len(self.anim_list)
        self.frame_rate = (duration * 1000) / self.frames

    def update_animation(self):
        if self.stop_time <= pygame.time.get_ticks():
            self.animating = False
            self.animate()
        else:
            frame_index = int((pygame.time.get_ticks()-self.start_time)
                              // self.frame_rate)
            if frame_index == len(self.anim_list):
                self.current_image = self.anim_list[-1]
            else:
                self.current_image = self.anim_list[frame_index]


class PlayerCharacter(Character):
    def __init__(self, health=10, power=2, name="Player",
                 image_set=wizard, points=0, lives=3, pos=(0, 0),
                 vel=(0, 0), move_rate=10):
        super().__init__(health, power, name, image_set, pos, move_rate)
        self.points = points
        self.lives = lives


class Enemy(Character):
    def __init__(self, health=random.randint(1, 10), power=1, name=None,
                 image_set=skeleton, pos=(0, 0), move_rate=random.randint(1, 3)):
        super().__init__(health, power, name, image_set, pos, move_rate)
        print(self.name, self.position)
        self.move(change_vel=(-move_rate, 0))


def import_list(file):
    output = []
    open_file = open(file, "r")
    for line in open_file:
        if line.strip() not in output:
            output.append(line.strip())
    # Removes duplicate entries
    output = list(set(output))
    return output


def load_image(image):
    pre_scaled_image = pygame.image.load(image).convert_alpha()
    scaled_image = pygame.transform.scale(pre_scaled_image,
                                          (int(screen.get_size()[0]*0.1),
                                           int(screen.get_size()[1]*0.1)))
    return scaled_image


class SpriteGroup():
    def __init__(self, image_set):
        self.idles = []
        self.attacks = []
        self.walking = []
        self.death = []
        idle_paths = glob.glob(image_set + "/idle/*.png")
        attack_paths = glob.glob(image_set + "/attack/*.png")
        walk_paths = glob.glob(image_set + "/walk/*.png")
        death_paths = glob.glob(image_set + "/die/*.png")

        for image in idle_paths:
            self.idles.append(load_image(image))

        for image in attack_paths:
            self.attacks.append(load_image(image))

        for image in walk_paths:
            self.walking.append(load_image(image))

        for image in death_paths:
            self.death.append(load_image(image))


class RoundControl():
    def __init__(self):
        self.round = 1
        self.enemies = pygame.sprite.Group()
        round_start()
        enemy_list_location = "enemy_names.txt"
        self.name_list = import_list(enemy_list_location)

    def update(self):
        if self.enemies:
            self.enemies.update()
        else:
            self.round += 1
            self.round_start()

    def round_start(self):
        number_of_enemies = random.randint(1, self.round)
        while number_of_enemies > 0:
            enemy = Enemy(pos=(screen.get_width(), random.randint(0,
                               screen.get_height())),
                          name=random.choice(self.name_list))
            self.enemies.add(enemy)
            number_of_enemies -= 1


main()
