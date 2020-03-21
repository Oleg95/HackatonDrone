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
drone_img2 = [pygame.image.load(r'images/drone1.png'), pygame.image.load(r'images/drone2.png')]

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
        display.blit(base_img[self.current_capacity], (self.x - self.image.get_rect().size[0] // 2, self.y - self.image.get_rect().size[1]))

    def change_capacity(self, size):
        if 1 <= size <= self.capacity - self.current_capacity:
            self.current_capacity += size
        if size == -1:
            self.current_capacity = 0


class Drone(Object):
    def __init__(self, x, y, image):
        Object.__init__(self, x, y, image)
        self.goals = []
        self.speed = 1
        self.based = False

    def draw(self):
        global img_counter
        if img_counter == 12:
            img_counter = 0

        if self.goals and not self.based:
            if self.x + self.image.get_rect().size[0] // 2 < self.goals[0][0]:
                self.x += self.speed
            elif self.x + self.image.get_rect().size[0] // 2 > self.goals[0][0]:
                self.x -= self.speed
            if self.y + self.image.get_rect().size[1] // 2 < self.goals[0][1]:
                self.y += self.speed
            elif self.y + self.image.get_rect().size[1] // 2 > self.goals[0][1]:
                self.y -= self.speed
            if self.x + self.image.get_rect().size[0] // 2 == self.goals[0][0] and self.y + self.image.get_rect().size[1] // 2 == self.goals[0][1]:
                if self.goals[0][0] == display_width // 2 and self.goals[0][1] == display_height // 2:
                    self.based = True
                    self.goals = self.goals[1:]
                else:
                    delete_trash(self.goals[0][0], self.goals[0][1])
                    self.goals = self.goals[1:]
        display.blit(drone_img[img_counter // 6], (self.x, self.y))
        img_counter += 1

    def go_to(self, x, y):
        self.goals.append((x, y))

    def get_trash(self):
        for i in range(len(trash)):
            for key, value in trash[i].items():
                cords = []
                for elem in value:
                    cords.append((elem.x, elem.y))
                sorted_cords = sort_cords(self.x, self.y, cords)
                print(sorted_cords)
                for i in range(len(sorted_cords) // 2):
                    self.go_to(sorted_cords[i * 2], sorted_cords[i * 2 + 1])
            self.go_to(display_width // 2, display_height // 2)

        return


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


def sort_cords(x, y, array):
    if len(array) <= 1:
        return array[0][0], array[0][1]
    min = 1000
    result = []
    current = ()
    for elem in array:
        if min > math.sqrt(abs(x - elem[0]) ** 2 + abs(y - elem[1]) ** 2):
            min = math.sqrt(abs(x - elem[0]) ** 2 + abs(y - elem[1]) ** 2)
            current = elem[0], elem[1]
    array.pop(array.index(current))
    result = current + sort_cords(current[0], current[1], array)
    return result


def delete_trash(x, y):
    global trash
    for i in range(len(trash)):
        for key, value in trash[i].items():
            temp_i = -1
            for i in range(len(value)):
                if value[i].x == x and value[i].y == y:
                    temp_i = i
            if temp_i != -1:
                value.pop(temp_i)



def main():
    create_trash(trash)
    second = False
    base = Base(display_width // 2, display_height // 2, base_img[0], 4)
    #drone = Drone(display_width // 2, display_height // 2 - 60, drone_img[0])
    drone = Drone(100, 100, drone_img[0])
    drone2 = Drone(display_width // 2, -100, drone_img[0])
    drone2.speed = 2
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    drone.get_trash()
        display.blit(map, (0, 0))
        base.draw()
        draw_trash(trash)
        drone.draw()
        if drone.based:
            second = True
            base.change_capacity(4)
            if len(drone2.goals) == 0:
                drone2.go_to(display_width // 2, display_height // 2 - 90)
            if drone2.y == 226:
                base.change_capacity(-1)
                drone2.goals = []
                drone2.go_to(display_width // 2, - 170)
                drone.based = False
        if second:
            drone2.draw()
            if drone2.y == -214:
                second = False
                drone2.goals = []
        pygame.display.update()
        clock.tick(80)


main()
