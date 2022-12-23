# 坦克类
import pygame
import random,start
from bullet import Bullet,Cannon
SCREEN_HIGHT=720
SCREEN_WIDTH=1200
last_shoot_time=0
shoot_delay=400
# 我方坦克类
class myTank(pygame.sprite.Sprite):
	def __init__(self, stage,kind=1):
		pygame.sprite.Sprite.__init__(self)
		self.kind = kind
		# 不同玩家用不同的坦克(不同等级对应不同的图)
		if self.kind == 1:
			self.tanks = ['images/myTank/tank_T1_0.png', 'images/myTank/tank_T1_1.png', 'images/myTank/tank_T1_2.png']
		elif self.kind == 2:
			self.tanks = ['images/myTank/tank_T2_0.png', 'images/myTank/tank_T2_1.png', 'images/myTank/tank_T2_2.png']
		# 坦克等级(初始0)
		self.level = 0
		self.stage=stage
		# 载入(两个tank是为了轮子特效)
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		self.rect = self.tank_0.get_rect()
		# 保护罩
		self.protected_mask = pygame.image.load('images/others/protect.png').convert_alpha()
		self.protected_mask1 = self.protected_mask.subsurface((0, 0), (48, 48))
		self.protected_mask2 = self.protected_mask.subsurface((48, 0), (48, 48))
		self.dead=False
		# 坦克方向
		self.direction_x, self.direction_y = 0, -1
		self.rect.left, self.rect.top =self.reset_position()
		# 坦克速度
		self.speed = 3
		# 是否存活
		self.being = True
		# 有几条命
		self.life = 5
		# 是否处于保护状态
		self.protected = False
		# 子弹
		self.bullet = Bullet()
			
	# 射击
	def shoot(self):
		global last_shoot_time
		global shoot_delay
		if pygame.time.get_ticks()-last_shoot_time>shoot_delay:
			last_shoot_time=pygame.time.get_ticks()
			self.bullet.being = True
			self.bullet.turn(self.direction_x, self.direction_y)
			if self.direction_x == 0 and self.direction_y == -1:
				self.bullet.rect.left = self.rect.left + 20
				self.bullet.rect.bottom = self.rect.top - 1
			elif self.direction_x == 0 and self.direction_y == 1:
				self.bullet.rect.left = self.rect.left + 20
				self.bullet.rect.top = self.rect.bottom + 1
			elif self.direction_x == -1 and self.direction_y == 0:
				self.bullet.rect.right = self.rect.left - 1
				self.bullet.rect.top = self.rect.top + 20
			elif self.direction_x == 1 and self.direction_y == 0:
				self.bullet.rect.left = self.rect.right + 1
				self.bullet.rect.top = self.rect.top + 20
			else:
				raise ValueError('myTank class -> direction value error.')
			if self.level == 0:
				self.bullet.speed = 8
				self.bullet.stronger = False
			elif self.level == 1:
				self.bullet.speed = 12
				self.bullet.stronger = False
			elif self.level == 2:
				self.bullet.speed = 12
				self.bullet.stronger = True
			elif self.level == 3:
				self.bullet.speed = 16
				self.bullet.stronger = True
			else:
				raise ValueError('myTank class -> level value error.')
			return True
		else:
			return False

	#重生位置
	def reset_position(self):
		if self.kind == 1:
			if self.stage == 2:
				return 24*25,24*21
			elif self.stage == 11:
				return 24*20,24*22
			elif self.stage == 13:
				return 24*25,24*26
			elif self.stage == 16:
				return 24*3,24*25
			else:
				return 24*20,24*26
		else:
			if self.stage == 2:
				return 24*27,24*21
			elif self.stage == 9:
				return 24*22,24*26
			elif self.stage == 11:
				return 24*26,24*22
			elif self.stage == 13:
				return 24*27,24*26
			elif self.stage == 16:
				return 24*45,24*25
			else:
				return 24*28,24*26
	# 等级提升
	def up_level(self):
		if self.level < 3:
			self.level += 1
		try:
			self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
		except:
			self.tank = pygame.image.load(self.tanks[-1]).convert_alpha()
	# 等级降低
	def down_level(self):
		if self.level > 0:
			self.level -= 1
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
	# 向上
	def move_up(self, tankGroup, brickGroup, ironGroup,riverGroup, myhome):
		self.direction_x, self.direction_y = 0, -1
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图顶端
		if self.rect.top < 0:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞石头/钢墙/河流
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
             pygame.sprite.spritecollide(self,riverGroup,False,None)\
			or pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他坦克
		if pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 大本营
		if pygame.sprite.collide_rect(self, myhome) and myhome.being:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向下
	def move_down(self, tankGroup, brickGroup, ironGroup, riverGroup,myhome):
		self.direction_x, self.direction_y = 0, 1
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图底端
		if self.rect.bottom > SCREEN_HIGHT :
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞石头/钢墙/河流
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
           pygame.sprite.spritecollide(self,riverGroup,False,None)\
			or pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他坦克
		if pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 大本营
		if pygame.sprite.collide_rect(self, myhome) and myhome.being:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向左
	def move_left(self, tankGroup, brickGroup, ironGroup,riverGroup, myhome):
		self.direction_x, self.direction_y = -1, 0
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图左端
		if self.rect.left < 0:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞石头/钢墙/河流
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
           pygame.sprite.spritecollide(self,riverGroup,False,None) \
			or pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他坦克
		if pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False		
		# 大本营
		if pygame.sprite.collide_rect(self, myhome) and myhome.being:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 向右
	def move_right(self, tankGroup, brickGroup, ironGroup,riverGroup ,myhome):
		self.direction_x, self.direction_y = 1, 0
		# 先移动后判断
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
		# 是否可以移动
		is_move = True
		# 地图右端
		if self.rect.right > SCREEN_WIDTH :
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞石头/钢墙
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self,riverGroup,False,None) or\
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 撞其他坦克
		if pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 大本营
		if pygame.sprite.collide_rect(self, myhome) and myhome.being:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 死后重置
	def reset(self):
		self.level = 0
		self.protected = False
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		self.rect = self.tank_0.get_rect()
		self.direction_x, self.direction_y = 0, -1
		self.rect.left, self.rect.top =  self.reset_position()
		self.speed = 3
		self.dead = False

# 敌方坦克类
class enemyTank(pygame.sprite.Sprite):
	def __init__(self, x=None, kind=None, is_red=None):
		pygame.sprite.Sprite.__init__(self)
		# 用于给刚生成的坦克播放出生特效
		self.born = True
		self.times = 90
		# 坦克的种类编号
		if kind is None:
			self.kind = random.randint(0, 3)
		else:
			self.kind = kind
		# 所有坦克
		self.tanks1 = ['images/enemyTank/enemy_1_0.png', 'images/enemyTank/enemy_1_1.png', 'images/enemyTank/enemy_1_2.png', 'images/enemyTank/enemy_1_3.png']
		self.tanks2 = ['images/enemyTank/enemy_2_0.png', 'images/enemyTank/enemy_2_1.png', 'images/enemyTank/enemy_2_2.png', 'images/enemyTank/enemy_2_3.png']
		self.tanks3 = ['images/enemyTank/enemy_3_0.png', 'images/enemyTank/enemy_3_1.png', 'images/enemyTank/enemy_3_2.png', 'images/enemyTank/enemy_3_3.png']
		self.tanks4 = ['images/enemyTank/enemy_4_0.png', 'images/enemyTank/enemy_4_1.png', 'images/enemyTank/enemy_4_2.png', 'images/enemyTank/enemy_4_3.png']
		self.tanks = [self.tanks1, self.tanks2, self.tanks3, self.tanks4]
		# 是否携带食物(红色的坦克携带食物)
		if is_red is None:
			self.is_red = random.choice((True, False, False, False, False))
		else:
			self.is_red = is_red
		# 同一种类的坦克具有不同的颜色, 红色的坦克比同类坦克多一点血量
		if self.is_red:
			self.color = 3
		else:
			self.color = random.randint(0, 2)
		# 血量
		self.blood = self.color
		# 载入(两个tank是为了轮子特效)
		self.tank = pygame.image.load(self.tanks[self.kind][self.color]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
		self.rect = self.tank_0.get_rect()
		# 坦克位置
		if x is None:
			self.x = random.randint(0, 2)
		else:
			self.x = x
		self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3
		# 坦克是否可以行动
		self.can_move = True
		# 坦克速度
		self.speed = max(3 - self.kind, 1)
		# 方向
		self.direction_x, self.direction_y = 0, 1
		# 是否存活
		self.being = True
		# 子弹
		self.bullet = Bullet()
	#射击
	def shoot(self):
		self.bullet.being = True
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('enemyTank class -> direction value error.')
		
	# 随机移动
	def move(self, tankGroup, brickGroup, ironGroup, riverGroup,myhome):
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		is_move = True
		randi = random.randint(0,100)
		if randi <1:
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			return False
		if self.direction_x == 0 and self.direction_y == -1:
			self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
			if self.rect.top < 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 0 and self.direction_y == 1:
			self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
			if self.rect.bottom > SCREEN_HIGHT - 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == -1 and self.direction_y == 0:
			self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
			if self.rect.left < 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 1 and self.direction_y == 0:
			self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
			if self.rect.right > SCREEN_WIDTH - 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		else:
			raise ValueError('enemyTank class -> direction value error.')
		if pygame.sprite.spritecollide(self, brickGroup, False, None) \
			or pygame.sprite.spritecollide(self, ironGroup, False, None) \
			or pygame.sprite.spritecollide(self,riverGroup,False,None)\
			or pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		if pygame.sprite.collide_rect(self, myhome):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		return is_move
	# 重新载入坦克
	def reload(self):
		self.tank = pygame.image.load(self.tanks[self.kind][self.color]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 48), (48, 48))

class boss(pygame.sprite.Sprite):
	def __init__(self):
		self.boss1 = [pygame.image.load('images/enemyTank/boss31.png').convert_alpha(),
					  pygame.image.load('images/enemyTank/boss32.png').convert_alpha(),
					  pygame.image.load('images/enemyTank/boss33.png').convert_alpha(),
					  pygame.image.load('images/enemyTank/boss34.png').convert_alpha(),]
		pygame.sprite.Sprite.__init__(self)
		# 用于给刚生成的坦克播放出生特效
		self.born = True
		self.x=2
		self.times = 90
		self.dir=0
		self.image=self.boss1[self.dir]
		# 血量
		self.blood = 30
		# 载入(两个tank是为了轮子特效)
		self.rect =self.boss1[0].get_rect()
		# 坦克位置
		self.rect.left, self.rect.top = 25 * 24, 25*15
		# 坦克是否可以行动
		self.can_move = True
		# 坦克速度
		self.speed = 1
		# 方向
		self.direction_x, self.direction_y = 0, 1
		# 是否存活
		self.being = True
		# 子弹
		self.bullet = Cannon()
	# 射击
	def shoot(self):
		self.bullet=Cannon()
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet.rect.left = self.rect.left + 42
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet.rect.left = self.rect.left + 42
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 42
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 42
		else:
			raise ValueError('enemyTank class -> direction value error.')
		self.bullet.x1,self.bullet.y1=self.bullet.rect.left,self.bullet.rect.top

	# 随机移动
	def move(self, tankGroup, brickGroup, ironGroup,riverGroup):
		self.rect = self.rect.move(self.speed * self.direction_x, self.speed * self.direction_y)
		is_move = True
		if self.direction_x == 0 and self.direction_y == -1:
			self.dir=0
			self.image = self.boss1[self.dir]
			if self.rect.top < 3:
				self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 0 and self.direction_y == 1:
			self.dir = 1
			self.image = self.boss1[self.dir]
			if self.rect.bottom > SCREEN_HIGHT - 3:
				self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == -1 and self.direction_y == 0:
			self.dir = 2
			self.image = self.boss1[self.dir]
			if self.rect.left < 3:
				self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 1 and self.direction_y == 0:
			self.dir = 3
			self.image = self.boss1[self.dir]
			if self.rect.right > SCREEN_WIDTH - 3:
				self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		else:
			raise ValueError('enemyTank class -> direction value error.')
		if pygame.sprite.spritecollide(self, brickGroup, False, None) \
				or pygame.sprite.spritecollide(self, ironGroup, False, None) \
                or pygame.sprite.spritecollide(self,riverGroup,False,None)\
				or pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		return is_move

	# 重新载入坦克
	def reload(self):
		self.image=self.boss1[self.dir]

