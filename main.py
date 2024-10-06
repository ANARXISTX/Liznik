import pygame as pg
import random 

pg.init()
sc = pg.display.set_mode((640,640))
clock = pg.time.Clock()
running = True

class SkierClass(pg.sprite.Sprite):
  def __init__(self):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.image.load('skier_down.png')
    self.image.set_colorkey((0,0,0))
    self.rect = self.image.get_rect()
    self.rect.center = [320, 100]
    self.angle = 0
    
  def turn(self, direction):
    self.angle += direction
    if self.angle < -2:
      self.angle = -2
    else:
      self.angle
    if self.angle > 2:
      self.angle = 2
    else:
      self.angle
    center = self.rect.center
    self.image = pg.image.load(skier_images[self.angle])
    self.image.set_colorkey((0,0,0))
    self.rect = self.image.get_rect()
    self.rect.center = center
    speed = [-self.angle, 6 - abs(self.angle) *2]
    return speed
  
  def move(self, speed) : 
    self.rect.centerx += speed[0]
    if self.rect.centerx < 20:
      self.rect.centerx = 20
    if self.rect.centerx > 620:
      self.rect.centerx = 620

class ObstacleClass(pg.sprite.Sprite):
  def __init__(self, image_file, location, type):
    pg.sprite.Sprite.__init__(self)
    self.image_file = image_file
    self.image = pg.image.load(image_file)
    self.rect = self.image.get_rect()
    self.rect.center = location
    self.passed = False
    self.type = type
  def update(self):
    global speed
    self.rect.centery -= speed[1]
    if self.rect.centery < -32 : self.kill()
    
def create_map():
  global obstacles
  locations = []
  for i in range(10):
    row = random.randrange(0,9)
    col = random.randrange(0,9)
    location = [col * 64 + 32,row * 64 + 32 + 640]
    if not(location in locations):
      locations.append(location)
      type = random.choice(['tree','flag'])
      img = 'skier_tree.png' if type == 'tree' else 'skier_flag.png'
      obstacle = ObstacleClass(img,location,type)
      obstacles.add(obstacle)
      
  
def animate():
  sc.fill((255,255,255))
  sc.blit(skier.image, skier.rect)
  sc.blit(point_text, [10,10])
  obstacles.draw(sc)
  pg.display.flip()

def end_game():
  font = pg.font.Font(None, 50)
  end_text = font.render('Game Over', 1, (0, 0, 0))
  sc.blit(end_text, [320, 320])
  pg.display.flip()
  pg.time.delay(3000)
  running = False

skier = SkierClass()
skier_images = ['skier_down.png', 'skier_right1.png', 'skier_right2.png', 'skier_left2.png', 'skier_left1.png']

speed = [0, 6]
running = True
obstacles = pg.sprite.Group()
create_map()

map_position = 0
points = 0
font = pg.font.Font(None, 50)
while running:
  clock.tick(30)
  point_text = font.render('Points - ' + str(points), 1, (0, 0, 0))
  for i in pg.event.get():
    if i.type == pg.QUIT:
      running = False
    if i.type == pg.KEYDOWN:
      if i.key == pg.K_LEFT:
        speed = skier.turn(1)
      if i.key == pg.K_RIGHT:
        speed = skier.turn(-1)
  map_position += speed[1]
  if map_position > 640:
    create_map()
    map_position = 0
  hit = pg.sprite.spritecollide(skier, obstacles, False)
  if hit:
    if hit[0].type == 'tree' and not hit[0].passed:
      points -= 30
      skier.image = pg.image.load('skier_crash.png')
      animate()
      pg.time.delay(1000)
      skier.image = pg.image.load('skier_down.png')
      skier.angle = 0
      speed = [0,6]
      hit[0].passed = True
    elif hit[0].type == 'flag' and not hit[0].passed:
      points += 30
      hit[0].kill()
        
  if points < 0:
    end_game()
  skier.move(speed)
  animate()
  obstacles.update()
pg.quit()