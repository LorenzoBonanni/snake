import pygame
from pygame.locals import *
from random import randint as ri

pygame.init()

GAME_RES = WIDTH, HEIGHT = 1280, 700
FPS = 13
GAME_TITLE = 'Snake'

window = pygame.display.set_mode(GAME_RES, HWACCEL | HWSURFACE | DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 50)


images = {
    'head_img': pygame.image.load('./snake_head.png'),
    'block_img': pygame.image.load('./snake_block.png'),
    'bgd': pygame.image.load('./background.png'),
    'apple': pygame.image.load('./apple.png')
}
images['bgd'] = pygame.transform.scale(
    images['bgd'],
    (
        images['block_img'].get_rect().width,
        images['block_img'].get_rect().height
    )
)


def draw_background():
    for h in range(0, HEIGHT, images['bgd'].get_height()):
        for w in range(0, WIDTH, images['bgd'].get_width()):
            window.blit(images['bgd'], (w, h))

# Game Values


class Head(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.last_x = None
        self.last_y = None
        self.width = self.rect.width
        self.height = self.rect.height
        self.direction = 'right'
        self.prev_direction = None

    def move(self, index):
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        if self.direction == 'right':
            self.rect.x += self.width
        elif self.direction == 'left':
            self.rect.x -= self.width
        elif self.direction == 'up':
            self.rect.y -= self.height
        elif self.direction == 'down':
            self.rect.y += self.height

    def collide(self):
        return pygame.sprite.spritecollide(head, tail_group, False, False)


class Block(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.last_x = None
        self.last_y = None
        self.width = self.rect.width
        self.height = self.rect.height
        # self.get_position()

    def move(self, index):
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.rect.x = snake[index-1].last_x
        self.rect.y = snake[index-1].last_y


class Apple(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.rect.x = 0
        self.rect.y = 0
        self.ate = False
        self.respawn()

    def respawn(self):
        self.rect.x = ri(0+self.width, WIDTH-self.width)
        self.rect.y = ri(0+self.height, HEIGHT-self.height)

    def collide(self):
        return pygame.sprite.spritecollide(head, apple_group, False, False)

head = Head(images['head_img'])
apple = Apple(images['apple'])

snake = [
    head,
    # *[Block(images['block_img']) for _ in range(0, 5)]
]

apple_group = pygame.sprite.GroupSingle(apple)
snake_group = pygame.sprite.Group(*snake)
tail_group = pygame.sprite.Group(*snake[1::])
# End of Game Values

# Game loop
game_ended = False
while not game_ended:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended = True
                break
            # movement keys
            elif event.key == K_w:
                head.direction = 'up'
            elif event.key == K_s:
                head.direction = 'down'
            elif event.key == K_d:
                head.direction = 'right'
            elif event.key == K_a:
                head.direction = 'left'
    # collisions
    for piece in snake:
        # collide right
        if piece.rect.x > WIDTH:
            piece.rect.x = 0 - piece.width
        # collide left
        elif piece.rect.x + piece.width < 0:
            piece.rect.x = WIDTH
        # collide up
        elif piece.rect.y + piece.height < 0:
            piece.rect.y = HEIGHT
        # collide down
        elif piece.rect.y > HEIGHT:
            piece.rect.y = 0 - piece.width

    # Game logic
    if head.collide():
        game_ended = True
    if apple.collide():
        block = Block(images['block_img'])
        snake.append(block)
        tail_group.add(block)
        snake_group.add(block)
        apple.respawn()

    for i in range(len(snake)):
        snake[i].move(i)

    # Display update
    draw_background()
    snake_group.draw(window)
    apple_group.draw(window)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
