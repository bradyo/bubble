#!/usr/bin/env python
import sys, pygame, math, random
from pygame.locals import *

pygame.init()
random.seed()

clock = pygame.time.Clock()
size = width, height = 700, 700
black = 0, 0, 0
white = 255, 255, 255
screen = pygame.display.set_mode(size)

class Player:
  def __init__(self, x, y, radius=5, velocity=0, color=(255,255,255), ai='food'):
    self.r = radius
    self.x = x
    self.y = y
    self.dir = (0, 0)
    self.v = velocity
    self.color = color
    self.ai = ai
    pass
  
  def update(self, dt):
    self.x = self.x + self.dir[0] * self.v * dt;
    self.y = self.y + self.dir[1] * self.v * dt;
    pass
  
  
player1 = Player(0, 0);

# set up world
foods = []
for i in range(200):
  x = random.gauss(width / 2, 100)
  y = random.gauss(height / 2, 100)
  foods.append(Player(x, y, 2))
  
startR = width / 2 * 0.90; # start 80% from center
enemies = []
for i in range(10):
  theta = 2 * math.pi * random.random();
  x = width/2 + startR * math.cos(theta)
  y = height/2 + startR * math.sin(theta)
  enemy = Player(x, y, 5, 1, (random.randint(0, 255), random.randint(0,255), random.randint(0,255)))
  
  dirx = random.random()
  diry = random.random()
  enemy.dir = [dirx, diry]
  
  enemies.append(enemy)


while 1:
  dt = clock.tick(30)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    
    if hasattr(event, 'key'):
      dirx = player1.dir[0]
      diry = player1.dir[1]
      if event.key == K_RIGHT: dirx = 1
      elif event.key == K_LEFT: dirx = -1      
      if event.key == K_UP: diry = -1
      elif event.key == K_DOWN: diry = 1
      player1.dir = (dirx, diry)

  for enemy in enemies:
    dirx = random.random() - 0.5 
    diry = random.random() - 0.5
    enemy.dir = [dirx, diry]
    if enemy.x - enemy.r < 0:
      enemy.x = enemy.r
      enemy.dir[0] *= -1
    if enemy.x + enemy.r > width:
      enemy.x = width - enemy.r
      enemy.dir[0] *= -1
    if enemy.y - enemy.r < 0:
      enemy.y = enemy.r
      enemy.dir[1] *= -1
    if enemy.y + enemy.r > height:
      enemy.y = height - enemy.r
      enemy.dir[1] *= -1
    enemy.update(dt)

  for enemy in enemies:
    x = enemy.x - enemy.r
    y = enemy.y - enemy.r
    s = h = 2 * enemy.r
    rect = pygame.Rect(x, y, s, s)
    
    for otherEnemy in enemies:
      x = otherEnemy.x - otherEnemy.r
      y = otherEnemy.y - otherEnemy.r
      s = h = 2 * otherEnemy.r
      otherRect = pygame.Rect(x, y, s, s)
      if (enemy != otherEnemy and rect.colliderect(otherRect)):
        if (enemy.r > otherEnemy.r):
          enemy.r += math.sqrt(otherEnemy.r / math.pi)
          enemies.remove(otherEnemy)
        else:
          otherEnemy.r += math.sqrt(enemy.r / math.pi)
          enemies.remove(enemy)
          
    for food in foods:
      x = food.x - food.r
      y = food.y - food.r
      s = h = 2 * food.r
      otherRect = pygame.Rect(x, y, s, s)
      if (rect.colliderect(otherRect)):
        enemy.r += math.sqrt(food.r / math.pi)
        foods.remove(food)
    

  screen.fill(black)
  for food in foods:
    pygame.draw.circle(screen, food.color, (int(food.x), int(food.y)), int(food.r))
  for enemy in enemies:
    pygame.draw.circle(screen, enemy.color, (int(enemy.x), int(enemy.y)), int(enemy.r))
  pygame.display.flip()
