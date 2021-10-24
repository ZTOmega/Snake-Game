import pygame, sys
from random import choice, randint

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screenWidth / 2),(screenHeight / 2))]
        self.direction = choice([up, down, left, right])
        self.color = (245, 245, 0)
        self.score = 0

        self.musicToggle = True
        self.music = pygame.mixer.Sound("../Snake/Audio/8_bit_nice_music_loop.wav")
        self.music.set_volume(0.1)
        self.music.play(loops=-1)

        self.gameOverSound = pygame.mixer.Sound("../Snake/Audio/8_bit_error_sound.wav")
        self.gameOverSound.set_volume(0.4)

    def getHeadPosicion(self):
        return self.positions[0]

    def turn(self, dir):
        if self.length > 1 and (dir[0] * -1, dir[1] * -1) == self.direction:
            return
        else:
            self.direction = dir

    def move(self):
        curPos = self.getHeadPosicion()
        x, y = self.direction
        newPos = (((curPos[0] + (x*gridSize)) % screenWidth), (curPos[1] + (y*gridSize)) % screenHeight)
        if len(self.positions) > 2 and newPos in self.positions[2:]:
            self.reset()
            food.reset()
            self.gameOverSound.play()
        else:
            self.positions.insert(0, newPos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screenWidth / 2), (screenHeight / 2))]
        self.direction = choice([up, down, left, right])
        self.score = 0

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect((pos[0], pos[1]), (gridSize,gridSize))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, (0, 100, 0), rect, 1)

    def imputKeys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                if event.key == pygame.K_DOWN:
                    self.turn(down)
                if event.key == pygame.K_LEFT:
                    self.turn(left)
                if event.key == pygame.K_RIGHT:
                    self.turn(right)

                if self.musicToggle == True:
                    if event.key == pygame.K_LCTRL:
                        self.music.stop()
                        self.musicToggle = False
                elif self.musicToggle == False:
                    if event.key == pygame.K_LCTRL:
                        self.music.play(loops = -1)
                        self.musicToggle = True

class Food():
    def __init__(self):
        self.foods = []
        self.color = (255, 100, 0)
        self.randomizePosicion()

    def randomizePosicion(self):
        for fruit in range(1, 6):
            self.position = (randint(0, gridWidth - 1) * gridSize, randint(0, gridHeight - 1) * gridSize)
            self.foods.insert(0, self.position)

    def reset(self):
        self.foods.clear()
        self.randomizePosicion()

    def draw(self, surface):
        for pos in self.foods:
            rect = pygame.Rect((pos[0], pos[1]), (gridSize, gridSize))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, (0, 100, 0), rect, 1)


def drawGrid(surface):
    for y in range(0, int(gridHeight)):
        for x in range(0, int(gridWidth)):
            if (x + y) % 2 == 0:
                greenRect = pygame.Rect((x * gridSize, y * gridSize), (gridSize, gridSize))
                pygame.draw.rect(surface, (0, 100, 0), greenRect)

            else:
                darkGreenRect = pygame.Rect((x * gridSize, y * gridSize), (gridSize, gridSize))
                pygame.draw.rect(surface, (0, 70, 0), darkGreenRect)


screenWidth = 640
screenHeight = 640

gridSize = 20
gridWidth = screenWidth / gridSize
gridHeight = screenWidth / gridSize

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

food = Food()


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    
    myFont = pygame.font.Font("..\Snake\Font\Aldrich-Regular.ttf", 25)
    eatSound = pygame.mixer.Sound("..\Snake\Audio\sine_click.wav")
    eatSound.set_volume(0.8)

    while True:
        clock.tick(10)
        snake.imputKeys()
        drawGrid(surface)
        snake.move()
        for pos in food.foods:
            if snake.getHeadPosicion() == pos:
                snake.length += 1
                snake.score += 1
                food.foods.pop(food.foods.index(pos))
                eatSound.play()
            if snake.getHeadPosicion() == pos and len(food.foods) == 0:
                food.randomizePosicion()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        scoreSurf = myFont.render("Score {0}".format(snake.score), 1, "white")
        screen.blit(scoreSurf, (10, 10))
        pygame.display.update()

main()