# 场景类
import pygame
import random
import os
import csv
import start
tile_size=24
# 石头墙
class Brick(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.brick = pygame.image.load('images/scene/brick.png')
		self.rect = self.brick.get_rect()
		self.being = False


# 钢墙
class Iron(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.iron = pygame.image.load('images/scene/iron.png')
		self.rect = self.iron.get_rect()
		self.being = False


# 冰
class Ice(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ice = pygame.image.load('images/scene/ice.png')
		self.rect = self.ice.get_rect()
		self.being = False


# 河流
class River(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.kind=1
		self.rivers = ['images/scene/river1.png', 'images/scene/river2.png']
		self.river1 = pygame.image.load(self.rivers[0])
		self.river2 = pygame.image.load(self.rivers[1])
		self.rect = self.river1.get_rect()
		self.being = False


# 树
class Tree(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.tree = pygame.image.load('images/scene/tree.png')
		self.rect = self.tree.get_rect()
		self.being = False

class Home(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.homes = ['images/home/home1.png', 'images/home/home2.png', 'images/home/home_destroyed.png']
		self.home = pygame.image.load(self.homes[0])
		self.being = False
		self.rect = self.home.get_rect()
		self.rect.left, self.rect.top = 24*24,24*26
		self.alive = True
	# 大本营置为摧毁状态
	def set_dead(self):
		self.home = pygame.image.load(self.homes[-1])
		self.alive = False
# 地图
class World():
	def __init__(self,stage):
		self.tile_list = []
		self.home_being = False
		self.brickGroup = pygame.sprite.Group()
		self.ironGroup = pygame.sprite.Group()
		self.iceGroup = pygame.sprite.Group()
		self.riverGroup = pygame.sprite.Group()
		self.treeGroup = pygame.sprite.Group()
		stage_map="./maps/stage"+str(stage)+".csv"
		self.data=self.load_data(stage_map)
		self.load_map()
		if stage == 2 or stage == 6 or stage == 9 or stage == 10 or stage == 11 or stage == 13 or stage == 16:
			self.home_being = False
		else:
			self.home_being = True

	def load_map(self):
			row_count = 0
			for row in self.data:
				col_count = 0
				for tile in row:
					if tile == "0":
						self.brick = Brick()
						self.brick.rect.left, self.brick.rect.top = col_count * 24,row_count * 24
						self.brick.being = True
						self.brickGroup.add(self.brick)
					elif tile == "5":
						self.tree = Tree()
						self.tree.rect.left, self.tree.rect.top = col_count * 24, row_count * 24
						self.tree.being = True
						self.treeGroup.add(self.tree)
					elif tile == "2":
						self.iron = Iron()
						self.iron.rect.left, self.iron.rect.top = col_count * 24, row_count * 24
						self.iron.being = True
						self.ironGroup.add(self.iron)
					elif tile == "3":
						self.river = River()
						self.river.rect.left, self.river.rect.top = col_count * 24, row_count * 24
						self.river.being = True
						self.riverGroup.add(self.river)
					elif tile == "1":
						self.ice = Ice()
						self.ice.rect.left, self.ice.rect.top = col_count * 24, row_count * 24
						self.ice.being = True
						self.iceGroup.add(self.ice)
					col_count += 1
				row_count += 1

	def load_data(self, filename):
		map = []
		with open(os.path.join(filename)) as data:
			data = csv.reader(data, delimiter=',')
			for row in data:
				map.append(list(row))
		return map


