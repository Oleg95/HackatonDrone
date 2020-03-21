import pygame
import random
import math

pygame.init()

map = pygame.image.load(r'images/abstract_map.jpg')
display_width, display_height = map.get_rect().size

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Drone')
clock = pygame.time.Clock()

drone_img = [pygame.image.load(r'images/drone1.png'), pygame.image.load(r'images/drone2.png')]

base_img = [pygame.image.load(r'images/trash1.png'), pygame.image.load(r'images/trash2.png'),
            pygame.image.load(r'images/trash3.png'), pygame.image.load(r'images/trash4.png'),
            pygame.image.load(r'images/trash5.png')]
img_counter = 0

trash = [{'paper': []}, {'plastic': []}, {'organic': []}]


class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self):
        display.blit(self.image, (self.x - self.image.get_rect().size[0] // 2, self.y - self.image.get_rect().size[1] // 2))


class Base(Object):
    def __init__(self, x, y, image, capacity):
        Object.__init__(self, x, y, image)
        self.capacity = capacity
        self.current_capacity = 0

    def draw(self):
        display.blit(base_img[self.current_capacity], (self.x, self.y))

    def change_capacity(self, size):
        if 1 <= size <= self.capacity - self.current_capacity:
            self.current_capacity += size
        elif size == -1:
            self.current_capacity = 0


class Drone(Object):
    def __init__(self, x, y, image):
        Object.__init__(self, x, y, image)
        self.move_to = False
        self.targetXY = ()

    def draw(self):
        global img_counter
        if img_counter == 12:
            img_counter = 0

        if self.move_to:
            if self.x - self.image.get_rect().size[0] // 2 < self.targetXY[0]:
                self.x += 1
            elif self.x - self.image.get_rect().size[0] // 2 > self.targetXY[0]:
                self.x -= 1
            if self.y + self.image.get_rect().size[1] // 2 < self.targetXY[1]:
                self.y += 1
            elif self.y + self.image.get_rect().size[1] // 2 > self.targetXY[1]:
                self.y -= 1
        else:
            self.move_to = False
            self.targetXY = ()

        display.blit(drone_img[img_counter // 6], (self.x, self.y))
        img_counter += 1

    def go_to(self, x, y):
        self.move_to = True
        self.targetXY = (x, y)

    def get_closest_type(self):
        the_closest_type = ''
        the_closest_range = 1000
        gg = []
        for i in range(len(trash)):
            min = 1000
            for key, value in trash[i].items():
                print(key)
                for elem in value:
                    elemX = elem.x
                    elemY = elem.y
                    if min > ((abs(elemX - self.x) ** 2 + abs(elemY - self.y) ** 2) ** 1/2):
                        min = (abs(elemX - self.x) ** 2 + abs(elemY - self.y) ** 2) ** 1/2
                        gg = elemX, elemY
                    print(elemX, elemY, min)
            self.go_to(gg[0], gg[1])
            if the_closest_range > min:
                the_closest_type = key
                the_closest_range = min
        print(the_closest_type, int(the_closest_range))


def create_trash(array):
    for i in range(len(array)):
        for key in array[i].keys():
            for _ in range(4):
                array[i][key].append(Object(random.randrange(50, display_width - 50), random.randrange(50, display_height - 50),
                                      pygame.image.load(r'images/{}.png'.format(key))))


def draw_trash(array):
    for i in range(len(array)):
        for key in array[i].keys():
            for obj in array[i][key]:
                obj.draw()

def main():
    create_trash(trash)
    base = Base(display_width // 2, display_height // 2, base_img[0], 4)
    drone = Drone(display_width // 2, display_height // 2 - 60, drone_img[0])
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    base.change_capacity(1)
                    drone.get_closest_type()
        display.blit(map, (0, 0))
        base.draw()
        draw_trash(trash)
        drone.draw()
        pygame.display.update()
        clock.tick(30)


main()
