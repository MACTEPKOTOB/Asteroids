from pygame import*
from random import*
import json

w, h = 700, 500
window = display.set_mode((w, h))

m,f = 0.2,0.2
speed_game = 1
num_E = 3

r,g,b = randint(0, 255),randint(0, 255),randint(0, 255)

clock = time.Clock()

game = True
finish = False

class GameSprite(sprite.Sprite):
	def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
		sprite.Sprite.__init__(self)
		self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
		self.speed = pSpeed
		self.rect = self.image.get_rect()
		self.rect.x = pX
		self.rect.y = pY
		self.sizeX = sizeX

	def draw(self):
		window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
	def update(self):
		keys = key.get_pressed()
		if keys[K_a] and self.rect.x >= 0:
			self.rect.x -= self.speed
		if keys[K_d] and self.rect.x <= w-self.sizeX:
			self.rect.x += self.speed
	def fire(self):
		bullet = Bullet("sprite/bullet.png", self.rect.centerx, self.rect.top, 15, 30, 15)
		bullets.add(bullet)

ship = Player("sprite/rocket.png", 10, h-100, 85, 85, 4)
background = transform.scale(image.load("detalis/galaxy.jpg"), (w, h))
batary = GameSprite("sprite/batary.png", 540, 340, 160, 160, 0)
GameOver = transform.scale(image.load("detalis/gameover.png"), (w, h))

lost = 0
class Enemy(GameSprite):
	def update(self):
		self.rect.y += self.speed
		global lost
		global hearts
		if self.rect.y >= h:
			try:
				hearts.pop(0)
			except:
				pass
			self.rect.y = 0
			self.rect.x = randint(0, w-self.sizeX)
			lost += 1

asteroids = sprite.Group()
for i in range(num_E):
	randpic = randint(1,4)
	if randpic == 1:
		pic = "sprite/asteroid.png"
	if randpic == 2:
		pic = "sprite/musor.png"
	if randpic == 3:
		pic = "sprite/sputnik.png"
	if randpic == 4:
		pic = "sprite/iron.png"
	asteroid = Enemy(pic, randint(0, w-50), -40, 50, 50, speed_game)
	asteroids.add(asteroid)

class Bullet(GameSprite):
	def update(self):
		self.rect.y -= self.speed
		if self.rect.y <= 0:
			self.kill()
mixer.init()

num = randint(1,2)
if num == 1:
	num_music = "music/music.mp3"
if num == 2:
	num_music = "music/two_music.mp3"
mixer.music.load(num_music)
mixer.music.play(-1)
mixer.music.set_volume(m)
bullets = sprite.Group()
fire_sound = mixer.Sound("music/fire.mp3")
fire_sound.set_volume(f)

font.init()
mainfont = font.Font("detalis/Washington Eagles.ttf", 40)
mainfont_mini = font.Font("detalis/Washington Eagles.ttf", 17)
mainfont1 = font.Font("detalis/Washington Eagles.ttf", 80)

score = 0

from time import time as timer
num_fire = 0
reload_time = False

hearts = []
lives = 5
heart_X = 500
for i in range(lives):
	#heart = GameSprite("sprite/heart.png", heart_X, 10, 40, 35, 0)
	heart = GameSprite("sprite/heart.png", heart_X, 10, 40, 35, 0)
	hearts.append(heart)
	heart_X += 40

with open('data.json', 'r', encoding = 'utf-8') as file:
	previous_num = json.load(file)
previous_score = previous_num["previous_score"]

while game:
	for e in event.get():
		if e.type == QUIT:
			game = False

		if e.type == MOUSEBUTTONDOWN and e.button == 1:
			r,g,b = randint(0, 255),randint(0, 255),randint(0, 255)
			if num_fire < 30 and reload_time == False:
				ship.fire()
				fire_sound.play()
				num_fire += 1

			if num_fire >= 30 and reload_time == False:
				reload_time = True
				reload_start = timer()

		if e.type == KEYDOWN:
			if e.key == K_r:
				for a in asteroids:
					a.rect.x = randint(0, 600)
					a.rect.y = -100
				finish, lost, score = 0,0,0
				start_warning = True
				hearts = []
				lives = 5
				heart_X = 500
				num_fire = 0
				for i in range(lives):
					#heart = GameSprite("sprite/heart.png", heart_X, 10, 40, 35, 0)
					heart = GameSprite("sprite/heart.png", heart_X, 10, 40, 35, 0)
					hearts.append(heart)
					heart_X += 40

	if not finish:
		
		window.blit(background, (0, 0))
		score_text = mainfont.render("Kelled:"+str(score), True, (r,g,b))
		previous_text = mainfont.render("Previous", True, (r,g,b))
		previous_twu_text = mainfont.render("score:"+str(previous_score), True, (r,g,b))
		lost_text = mainfont.render("Missed:"+str(lost), True, (r,g,b))
		patron_text = mainfont.render("30/"+str(num_fire), True, (r,g,b))

		warning = mainfont_mini.render("When restarting (r button), the previous record (previous score) will not be recorded!", True, (220,10,10))
		window.blit(warning, (95, 483))
		window.blit(score_text, (5, 10))
		window.blit(previous_text, (5, 60))
		window.blit(previous_twu_text, (5, 90))
		window.blit(lost_text, (5, 135))
		window.blit(patron_text, (5, 460))
		asteroids.draw(window)
		asteroids.update()

		bullets.draw(window)
		bullets.update()

		collides = sprite.groupcollide(bullets, asteroids, True, True)
		for c in collides:
			randpic = randint(1,4)
			if randpic == 1:
				pic = "sprite/asteroid.png"
			if randpic == 2:
				pic = "sprite/musor.png"
			if randpic == 3:
				pic = "sprite/sputnik.png"
			if randpic == 4:
				pic = "sprite/iron.png"
			score += 1
			asteroid = Enemy(pic, randint(0, w-50), -40, 50, 50, speed_game)
			asteroids.add(asteroid)

		if sprite.spritecollide(ship, asteroids, False):
			window.blit(GameOver, (0, 0))
			finish = True

		if reload_time:
			now_time = timer()
			if now_time - reload_start < 2:
				speed_game == 0.6
				batary.draw()
			else:
				num_fire = 0
				reload_time = False
				speed_game == 1

		for heart in hearts:
			heart.draw()

		if len(hearts) <= 0:
			window.blit(GameOver, (0, 0))
			finish = True

		ship.draw()
		ship.update()
	display.update()
	clock.tick(80)

data = {
"previous_score" : [score]
}


with open('data.json', 'w', encoding = 'utf-8') as file:
	json.dump(data, file, indent = 4)
