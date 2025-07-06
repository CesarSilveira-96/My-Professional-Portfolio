import pygame
import sys
import random
import math

pygame.init()

# >>>>>> SCREEN CONFIG >>>>>>
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")

# >>>>>> COLORS >>>>>>
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (50, 205, 50)
BLUE = (30, 144, 255)
PURPLE = (186, 85, 211)
COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

# >>>>>> FONTS >>>>>>
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)


# >>>>>> CLASSES >>>>>>
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 10
        self.color = WHITE
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # 3D EFFECTS
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, 4))
        pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, 4, self.height))
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y + self.height - 4, self.width, 4))
        
    def move(self, direction):
        if direction == "left" and self.x > 10:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width - 10:
            self.x += self.speed
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self):
        self.radius = 10
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = 4
        self.dy = -4
        self.speed = 5
        self.color = WHITE
        self.active = True
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # LIGHTING EFFECTS
        pygame.draw.circle(screen, (200, 200, 255), (self.x - 3, self.y - 3), self.radius // 3)
        
    def move(self):
        if not self.active:
            return
            
        self.x += self.dx
        self.y += self.dy
        
        # WALL COLLISIONS
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.dx *= -1
            pygame.mixer.Sound.play(wall_sound)
            
        if self.y <= self.radius:
            self.dy *= -1
            pygame.mixer.Sound.play(wall_sound)
            
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = random.choice([-4, 4])
        self.dy = -4
        self.active = True
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Block:
    def __init__(self, x, y, color):
        self.width = 60
        self.height = 25
        self.x = x
        self.y = y
        self.color = color
        self.visible = True
        
    def draw(self):
        if not self.visible:
            return
            
        # MAIN BLOCK
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # 3D EFFECTS WITH LIGHTER AND DARKER BORDER EFFECTS
        pygame.draw.rect(screen, self.lighten_color(self.color), 
                         (self.x, self.y, self.width, 3))
        pygame.draw.rect(screen, self.lighten_color(self.color), 
                         (self.x, self.y, 3, self.height))
        pygame.draw.rect(screen, self.darken_color(self.color), 
                         (self.x, self.y + self.height - 3, self.width, 3))
        pygame.draw.rect(screen, self.darken_color(self.color), 
                         (self.x + self.width - 3, self.y, 3, self.height))
    
    def lighten_color(self, color):
        return (min(color[0] + 40, 255), min(color[1] + 40, 255), min(color[2] + 40, 255))
    
    def darken_color(self, color):
        return (max(color[0] - 40, 0), max(color[1] - 40, 0), max(color[2] - 40, 0))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.game_won = False
        self.create_blocks()
        
    def create_blocks(self):
        self.blocks = []
        rows = 6 + self.level - 1
        cols = 10
        
        block_width = 60
        block_height = 25
        horizontal_gap = 10
        vertical_gap = 5
        start_x = (SCREEN_WIDTH - (cols * (block_width + horizontal_gap))) // 2
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (block_width + horizontal_gap)
                y = 80 + row * (block_height + vertical_gap)
                color = COLORS[row % len(COLORS)]
                self.blocks.append(Block(x, y, color))
    
    def handle_collisions(self):
        ball_rect = self.ball.get_rect()
        paddle_rect = self.paddle.get_rect()
        
        # PADDLE COLLISION
        if ball_rect.colliderect(paddle_rect) and self.ball.dy > 0:
            relative_x = (self.ball.x - self.paddle.x) / self.paddle.width
            angle = relative_x * 140 + 20
            self.ball.dx = self.ball.speed * math.cos(math.radians(angle))
            self.ball.dy = -self.ball.speed * math.sin(math.radians(angle))
            if paddle_sound: paddle_sound.play()
        
        # BLOCKS COLLISION
        for block in [b for b in self.blocks if b.visible]:
            block_rect = block.get_rect()
            if not ball_rect.colliderect(block_rect):
                continue
                
            block.visible = False
            self.score += 10
            if block_sound: block_sound.play()
            
            # CALCULATES OVERLAP
            overlap_x = min(ball_rect.right, block_rect.right) - max(ball_rect.left, block_rect.left)
            overlap_y = min(ball_rect.bottom, block_rect.bottom) - max(ball_rect.top, block_rect.top)
            
            # DETERMINES COLLISION SIDE
            if overlap_y < overlap_x:
                # VERTICAL COLLISIONS
                if self.ball.dy > 0: 
                    self.ball.y = block_rect.top - self.ball.radius
                else:
                    self.ball.y = block_rect.bottom + self.ball.radius
                self.ball.dy *= -1
            else:
                # HORIZONTAL COLLISIONS
                if self.ball.dx > 0: # TO THE RIGHT
                    self.ball.x = block_rect.left - self.ball.radius
                else:  # TO THE LEFT
                    self.ball.x = block_rect.right + self.ball.radius
                self.ball.dx *= -1
            if abs(self.ball.dy) < 1.0:  # AT SHARP ANGLES
                self.ball.dy = -1.0 if self.ball.dy < 0 else 1.0
                self.ball.dx *= 0.8
            break
        
        # LIFES CHECK
        if self.ball.y > SCREEN_HEIGHT:
            self.lives -= 1
            pygame.mixer.Sound.play(life_lost_sound)
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.reset()
        
        # LEVEL FINISHED CHECK
        if all(not block.visible for block in self.blocks):
            self.level += 1
            if self.level > 5:
                self.game_won = True
            else:
                self.create_blocks()
                self.ball.reset()
                self.paddle = Paddle()
                pygame.mixer.Sound.play(level_complete_sound)
    
    def draw(self):
        # BACKGROUND
        screen.fill(BLACK)
        
        # BORDERS
        pygame.draw.rect(screen, (50, 50, 100), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)
        
        # ELEMENTS
        self.paddle.draw()
        self.ball.draw()
        
        for block in self.blocks:
            block.draw()
        
        # GAME INFO AND SCOREBOARD
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 20))
        
        # GAME OVER AND GAME WON MESSAGES
        if self.game_over:
            game_over_text = big_font.render("GAME OVER", True, RED)
            restart_text = font.render("Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                        SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                      SCREEN_HEIGHT // 2 + 30))
        
        if self.game_won:
            win_text = big_font.render("YOU WIN!", True, GREEN)
            restart_text = font.render("Press R to Restart", True, WHITE)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 
                                  SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                      SCREEN_HEIGHT // 2 + 30))

# SOUNDS
try:
    pygame.mixer.init()
    paddle_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytes(random.randint(0, 255) for _ in range(44))))
    paddle_sound.set_volume(0.3)
    
    wall_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytes(random.randint(0, 255) for _ in range(44))))
    wall_sound.set_volume(0.2)
    
    block_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytes(random.randint(0, 255) for _ in range(44))))
    block_sound.set_volume(0.4)
    
    life_lost_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytes(random.randint(0, 255) for _ in range(44))))
    life_lost_sound.set_volume(0.5)
    
    level_complete_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytes(random.randint(0, 255) for _ in range(44))))
    level_complete_sound.set_volume(0.6)
except:
    # FALLBACK IF SOUNDS DO NOT WORK
    paddle_sound = wall_sound = block_sound = life_lost_sound = level_complete_sound = None

# GAME START
game = Game()
clock = pygame.time.Clock()

# MAIN GAME LOOP
while True:
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game.game_over or game.game_won):
                # GAME RESET
                game = Game()
    
    # PRESSED KEYS AND ELEMENTS MOVEMENT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game.paddle.move("left")
    if keys[pygame.K_RIGHT]:
        game.paddle.move("right")
    
    game.ball.move()
    
    if not game.game_over and not game.game_won:
        game.handle_collisions()
    
    game.draw()
    
    # SCREEN UPDATE
    pygame.display.flip()
    
    clock.tick(60)