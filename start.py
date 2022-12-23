import sys
import pygame,random
import scene, tank, food,explode,display,bullet
from ui import Ui
SCREEN_WIDTH=1200
SCREEN_HIGHT=720
tile_size = 24

class MainGame:
	def __init__(self,stage):
		# 初始化
		
		# 暂停图片加载
		self.rad = None
		self.game_pause_image = pygame.image.load(r"images\ui\game_pause.png")
		#关卡结束
		self.game_over_win = pygame.image.load(r"images\ui\game_over_win.png")
		self.game_over_fail = pygame.image.load(r"images\ui\game_over_fail.png")
		self.moving1 = 0
		self.move_dir1 = 0
		self.moving2 = 0
		self.move_dir2 = 0
		#敌方坦克静止
		self.is_still = 0
		self.last_still_time=0
		self.still_delay=4000
		#食物类型
		self.food_kind = -1
		#食物提示文本
		self.last_food_time = 0
		self.food_delay = 3000
		self.game_tip_image1=pygame.image.load(r"images\ui\game_tip_image1.png")
		self.game_tip_image2=pygame.image.load(r"images\ui\game_tip_image2.png")
		self.game_tip_image3=pygame.image.load(r"images\ui\game_tip_image3.png")
	# 主函数
	def main(self,stage,num_player=1):
		pygame.init()
		pygame.mixer.init()
		UI=Ui()
		screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
		pygame.display.set_caption("坦克大战")
		Display = display.Display()
		# 加载图片
		self.bg_img = pygame.image.load("images/others/background.png")
		# 加载音效
		add_sound = pygame.mixer.Sound("audios/add.wav")
		add_sound.set_volume(1)
		bang_sound = pygame.mixer.Sound("audios/bang.wav")
		bang_sound.set_volume(1)
		blast_sound = pygame.mixer.Sound("audios/blast.wav")
		blast_sound.set_volume(1)
		fire_sound = pygame.mixer.Sound("audios/fire.wav")
		fire_sound.set_volume(1)
		Gunfire_sound = pygame.mixer.Sound("audios/Gunfire.wav")
		Gunfire_sound.set_volume(1)
		hit_sound = pygame.mixer.Sound("audios/hit.wav")
		hit_sound.set_volume(1)
		self.start_sound = pygame.mixer.Sound("audios/start.wav")
  		# 场上存在的敌方坦克总数量
		enemytanks_now = 0
  		# 该关卡坦克总数量
		enemytanks_total = min(15+stage*3 , 40)
		# 场上可以存在的敌方坦克总数量
		enemytanks_now_max = 7
		# 精灵组
		explodeGroup=[]
		bossGroup= pygame.sprite.Group()
		tanksGroup = pygame.sprite.Group()
		mytanksGroup = pygame.sprite.Group()
		enemytanksGroup = pygame.sprite.Group()
		enemybulletsGroup = pygame.sprite.Group()
		bossbulletGroup=[]
		myfoodsGroup = pygame.sprite.Group()
		self.start_sound.set_volume(1)
		# 播放游戏开始的音乐
		self.start_sound.play()
		left_time=300
		# 游戏是否结束
		is_gameover = False
		# 关卡
		kind=1
		Display.show_switch_stage(screen, SCREEN_WIDTH, SCREEN_HIGHT, stage)
		
		
		# 自定义事件
		# 	-生成敌方坦克事件
		genEnemyEvent = pygame.constants.USEREVENT + 0
		pygame.time.set_timer(genEnemyEvent, 100)
		# 	-敌方坦克静止恢复事件
		recoverEnemyEvent = pygame.constants.USEREVENT + 1
		pygame.time.set_timer(recoverEnemyEvent, 800)
		# 	-我方坦克无敌恢复事件
		noprotectMytankEvent = pygame.constants.USEREVENT + 2
		pygame.time.set_timer(noprotectMytankEvent, 900)
		# 关卡地图
		map_stage = scene.World(stage)
		# 我方坦克
		tank_player1 = tank.myTank(stage,1)
		tanksGroup.add(tank_player1)
		mytanksGroup.add(tank_player1)
		if num_player > 1:
			tank_player2 = tank.myTank(stage,2)
			tanksGroup.add(tank_player2)
			mytanksGroup.add(tank_player2)
		is_switch_tank = True
		player1_moving = False
		player2_moving = False
		# 为了轮胎的动画效果
		time = 0
		# 敌方坦克
		if stage==16:
			boss=tank.boss()
			tanksGroup.add(boss)
			bossGroup.add(boss)
			enemytanks_now += 1
			enemytanks_total -= 1
		for i in range(0, 5):
			if enemytanks_total > 0:
				enemytank = tank.enemyTank(i)
				tanksGroup.add(enemytank)
				enemytanksGroup.add(enemytank)
				enemytanks_now += 1
				enemytanks_total -= 1
		# 大本营
		myhome = scene.Home()	
		# 出场特效
		appearance_img = pygame.image.load("images/others/appear.png").convert_alpha()
		appearances = []
		appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
		appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
		appearances.append(appearance_img.subsurface((96, 0), (48, 48)))
		clock = pygame.time.Clock()
		# 背景
		screen.blit(self.bg_img, (0, 0))
		#关卡提示
		mid = self.game_tip(screen,stage)
		# 关卡主循环
		while True:
			if is_gameover:
				break
			if enemytanks_total < 1 and enemytanks_now < 1:
				is_gameover = False
				break
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == genEnemyEvent:
					if enemytanks_total > 0:
						if enemytanks_now < enemytanks_now_max:
							enemytank = tank.enemyTank()
							if not pygame.sprite.spritecollide(enemytank, tanksGroup, False, None):
								tanksGroup.add(enemytank)
								enemytanksGroup.add(enemytank)
								enemytanks_now += 1
								enemytanks_total -= 1
				if event.type == recoverEnemyEvent:
					for each in enemytanksGroup:
						each.can_move = True
				if event.type == noprotectMytankEvent:
					for each in mytanksGroup:
						mytanksGroup.protected = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					mid = self.game_pause(screen)
					if mid == 0:
						return
			# 检查用户键盘操作
			key_pressed = pygame.key.get_pressed()
			if not self.moving1:
				# 玩家一
				if key_pressed[pygame.K_w]:
					self.moving1 = 7
					self.move_dir1 = 0
					tanksGroup.remove(tank_player1)
					if not tank_player1.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome):
						self.moving1 = 0
					tanksGroup.add(tank_player1)
					player1_moving = True
				elif key_pressed[pygame.K_s]:
					self.moving1 = 7
					self.move_dir1 = 1
					tanksGroup.remove(tank_player1)
					if not tank_player1.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup,  map_stage.riverGroup,myhome):
						self.moving1 = 0
					tanksGroup.add(tank_player1)
					player1_moving = True
				elif key_pressed[pygame.K_a]:
					self.moving1 = 7
					self.move_dir1 = 2
					tanksGroup.remove(tank_player1)
					if not tank_player1.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup, myhome):
						self.moving1 = 0
					tanksGroup.add(tank_player1)
					player1_moving = True
				elif key_pressed[pygame.K_d]:
					self.moving1 = 7
					self.move_dir1 = 3
					tanksGroup.remove(tank_player1)
					if not tank_player1.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup, myhome):
						self.moving1 = 0
					tanksGroup.add(tank_player1)
					player1_moving = True
				elif key_pressed[pygame.K_F1]:
					if tank_player1.dead==True:
						tank_player1.reset()
				if key_pressed[pygame.K_j]:
					if not tank_player1.bullet.being :
						if tank_player1.shoot():
							fire_sound.play()
			else:
				self.moving1 -=1
				if self.move_dir1 == 0:
					tanksGroup.remove(tank_player1)
					tank_player1.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome)
					tanksGroup.add(tank_player1)
					player1_moving = True
				elif self.move_dir1 == 1:
					tanksGroup.remove(tank_player1)
					tank_player1.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome)
					tanksGroup.add(tank_player1)
					player1_moving = True
				elif self.move_dir1 == 2:
					tanksGroup.remove(tank_player1)
					tank_player1.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome)
					tanksGroup.add(tank_player1)
					player1_moving = True
				elif self.move_dir1 == 3:
					tanksGroup.remove(tank_player1)
					tank_player1.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome)
					tanksGroup.add(tank_player1)
					player1_moving = True
			if num_player>1:
				if not self.moving2:
					# 玩家一
					if key_pressed[pygame.K_UP]:
						self.moving2 = 7
						self.move_dir2 = 0
						tanksGroup.remove(tank_player2)
						if not tank_player2.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome):
							self.moving2 = 0
						tanksGroup.add(tank_player2)
						player2_moving = True
					elif key_pressed[pygame.K_DOWN]:
						self.moving2 = 7
						self.move_dir2 = 1
						tanksGroup.remove(tank_player2)
						if not tank_player2.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup,  map_stage.riverGroup,myhome):
							self.moving2 = 0
						tanksGroup.add(tank_player2)
						player2_moving = True
					elif key_pressed[pygame.K_LEFT]:
						self.moving2 = 7
						self.move_dir2 = 2
						tanksGroup.remove(tank_player2)
						if not tank_player2.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup, myhome):
							self.moving2 = 0
						tanksGroup.add(tank_player2)
						player2_moving = True
					elif key_pressed[pygame.K_RIGHT]:
						self.moving2 = 7
						self.move_dir2 = 3
						tanksGroup.remove(tank_player2)
						if not tank_player2.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup, myhome):
							self.moving2 = 0
						tanksGroup.add(tank_player2)
						player2_moving = True
					elif key_pressed[pygame.K_KP9]:
						if tank_player2.dead==True:
							tank_player2.reset()
					if key_pressed[pygame.K_KP0]:
						if not tank_player2.bullet.being :
							if tank_player2.shoot():
								fire_sound.play()
				else:
					self.moving2 -=1
					if self.move_dir2 == 0:
						tanksGroup.remove(tank_player2)
						tank_player2.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome)
						tanksGroup.add(tank_player2)
						player2_moving = True
					elif self.move_dir2 == 1:
						tanksGroup.remove(tank_player2)
						tank_player2.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome)
						tanksGroup.add(tank_player2)
						player2_moving = True
					elif self.move_dir2 == 2:
						tanksGroup.remove(tank_player2)
						tank_player2.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome)
						tanksGroup.add(tank_player2)
						player2_moving = True
					elif self.move_dir2 == 3:
						tanksGroup.remove(tank_player2)
						tank_player2.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup,myhome)
						tanksGroup.add(tank_player2)
						player2_moving = True
			# 背景
			screen.blit(self.bg_img, (0, 0))
			Display.display_object(screen,map_stage)
			Display.displayexplode(screen,explodeGroup)
			time += 1
			if time == 5:
				time = 0
				is_switch_tank = not is_switch_tank
			
			# 我方坦克
			if not tank_player1.dead and tank_player1 in mytanksGroup:
				if  is_switch_tank and player1_moving:
					screen.blit(tank_player1.tank_0, (tank_player1.rect.left, tank_player1.rect.top))
					player1_moving = False
				else:
					screen.blit(tank_player1.tank_1, (tank_player1.rect.left, tank_player1.rect.top))
				if tank_player1.protected:
					screen.blit(tank_player1.protected_mask1, (tank_player1.rect.left, tank_player1.rect.top))
			if num_player>1:
				if not tank_player2.dead and tank_player2 in mytanksGroup:
					if  is_switch_tank and player2_moving:
						screen.blit(tank_player2.tank_0, (tank_player2.rect.left, tank_player2.rect.top))
						player2_moving = False
					else:
						screen.blit(tank_player2.tank_1, (tank_player2.rect.left, tank_player2.rect.top))
					if tank_player2.protected:
						screen.blit(tank_player2.protected_mask1, (tank_player2.rect.left, tank_player2.rect.top))
			# 敌方坦克
			for each in enemytanksGroup:
				# 出生特效
				if each.born:
					Display.display_enemyTank(screen,each,appearances)
				else:
					if is_switch_tank:
						screen.blit(each.tank_0, (each.rect.left, each.rect.top))
					else:
						screen.blit(each.tank_1, (each.rect.left, each.rect.top))
					if each.can_move and not self.is_still:
						tanksGroup.remove(each)
						each.move(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, map_stage.riverGroup, myhome)
						tanksGroup.add(each)
			if self.is_still:
				if pygame.time.get_ticks()-self.last_still_time>self.still_delay:
					self.last_still_time=pygame.time.get_ticks()
					self.is_still = 0
			for each in bossGroup:
				if each.born:
					Display.display_enemyTank(screen, each, appearances)
				else:
					screen.blit(each.image, (each.rect.left, each.rect.top))
					if each.can_move:
						tanksGroup.remove(each)
						each.move(tanksGroup, map_stage.brickGroup, map_stage.ironGroup ,map_stage.riverGroup)
						tanksGroup.add(each)
			# 我方子弹
			for tank_player in mytanksGroup:
				if tank_player.bullet.being:
					tank_player.bullet.move()
					screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
					# 子弹碰撞敌方子弹
					for each in enemybulletsGroup:
						if each.being:
							if pygame.sprite.collide_rect(tank_player.bullet, each):
								tank_player.bullet.being = False
								each.being = False
								enemybulletsGroup.remove(each)
								break
						else:
							enemybulletsGroup.remove(each)
					# 子弹碰撞敌方坦克
					for each in enemytanksGroup:
						if each.being:
							if pygame.sprite.collide_rect(tank_player.bullet, each):
								if each.is_red == True:
									myfood = food.Food()
									myfood.generate()
									while True:
										if pygame.sprite.spritecollide(myfood, map_stage.brickGroup, False, None):
											myfood.generate()
										elif pygame.sprite.spritecollide(myfood, map_stage.ironGroup, False, None):
											myfood.generate()
										elif pygame.sprite.spritecollide(myfood, map_stage.iceGroup, False, None):
											myfood.generate()
										elif pygame.sprite.spritecollide(myfood, map_stage.riverGroup, False, None):
											myfood.generate()
										break
									myfoodsGroup.add(myfood)
									each.is_red = False
								each.blood -= 1
								each.color -= 1
								bang_sound.play()
								if each.blood < 0:
									explodeGroup.append(explode.Explode(each))
									bang_sound.play()
									each.being = False
									enemytanksGroup.remove(each)
									enemytanks_now -= 1
									tanksGroup.remove(each)
								else:
									each.reload()
								tank_player.bullet.being = False
								break
						else:
							enemytanksGroup.remove(each)
							tanksGroup.remove(each)
					Display.check_wall(map_stage,tank_player)
					# 子弹碰撞boss
					for each in bossGroup:
						if each.being:
							if pygame.sprite.collide_rect(tank_player.bullet, each):
								each.blood -= 1
								print(each.blood)
								if each.blood < 0:
									explodeGroup.append(explode.big_explode(each))
									bang_sound.play()
									each.being = False
									bossGroup.remove(each)
									enemytanks_now -= 1
									tanksGroup.remove(each)
								else:
									each.reload()
								tank_player.bullet.being = False
								break
						else:
							bossGroup.remove(each)
							tanksGroup.remove(each)
					Display.check_wall(map_stage, tank_player)

			# 敌方子弹
			for each in enemytanksGroup:
				if each.being:
					randi=random.randint(0,100)
					if randi<1:
						enemybulletsGroup.remove(each.bullet)
						each.shoot()
						enemybulletsGroup.add(each.bullet)
					if not each.born:
						if each.bullet.being:
							each.bullet.move()
							screen.blit(each.bullet.bullet, each.bullet.rect)
							# 子弹碰撞我方坦克
							for tank_player in mytanksGroup:
								if pygame.sprite.collide_rect(each.bullet, tank_player):
									if not tank_player.protected:
										tank_player.life -= 1
										if tank_player.life < 0:
											mytanksGroup.remove(tank_player)
											tanksGroup.remove(tank_player)
											if len(mytanksGroup) < 1:
												is_gameover = True
										else:
											tank_player.dead=True
											tank_player.rect.left, tank_player.rect.top =  24 * 100,  24 * 100
									each.bullet.being = False
									enemybulletsGroup.remove(each.bullet)
									break
							# 子弹碰撞石头墙
							for one in map_stage.brickGroup:
								if pygame.sprite.collide_rect(each.bullet, one):
									each.bullet.being = False
									one.being = False
									map_stage.brickGroup.remove(one)
									enemybulletsGroup.remove(each)
									break
							# 子弹碰钢墙
							for one in map_stage.ironGroup:
								if pygame.sprite.collide_rect(each.bullet, one):
									each.bullet.being = False
									if each.bullet.stronger:
										one.being = False
										map_stage.ironGroup.remove(one)
									break
							# 子弹碰大本营
							if stage =="1":
								if pygame.sprite.collide_rect(each.bullet, myhome):
									each.bullet.being = False
									myhome.set_dead()
									is_gameover = True
				else:
					enemytanksGroup.remove(each)
					tanksGroup.remove(each)
			#boss子弹
			for each in bossGroup:
				if each.being:
					randi=random.randint(0,50)
					if randi<1:
						each.shoot()
						self.rad=random.randint(0,20)
						if self.rad<2:
							each.bullet.kind = 1
							if num_player>1 and self.rad == 1:
								each.bullet.tank = tank_player2
							else:
								each.bullet.tank = tank_player1
						bossbulletGroup.append(each.bullet)
				else:
					bossGroup.remove(each)
					tanksGroup.remove(each)
			for each in bossbulletGroup:
				is_killed=0
				if not each.kind:
					each.move()
					screen.blit(each.bullet, each.rect)
				else:
					each.bullet_track(each.tank)
					screen.blit(each.missiled,each.rect)
				# 子弹碰撞我方坦克
				for tank_player in mytanksGroup:
					if pygame.sprite.collide_rect(each, tank_player):
						if not tank_player.protected:
							tank_player.life -= 1
							if tank_player.life < 0:
								mytanksGroup.remove(tank_player)
								tanksGroup.remove(tank_player)
								if len(mytanksGroup) < 1:
									is_gameover = True
							else:
								tank_player.dead=True
								tank_player.rect.left, tank_player.rect.top =  24 * 100,  24 * 100
						boss.bullet.num -=1
						bossbulletGroup.remove(each)
						is_killed = 1
						break
				if each.being == False and is_killed == 0:
					bossbulletGroup.remove(each)
				# 子弹碰撞石头墙
				if is_killed == 0:
					for one in map_stage.brickGroup:
						if pygame.sprite.collide_rect(each, one):
							boss.bullet.num -= 1
							one.being = False
							map_stage.brickGroup.remove(one)
							bossbulletGroup.remove(each)
							break
				# 子弹碰钢墙
				if is_killed == 0:
					for one in map_stage.ironGroup:
						if pygame.sprite.collide_rect(each, one):
							boss.bullet.num -= 1
							if each.stronger:
								one.being = False
								map_stage.ironGroup.remove(one)
							break
			# 家
			if map_stage.home_being:
				myhome.being = True
				screen.blit(myhome.home, myhome.rect)
			#最后显示树丛，以达到进入树丛隐藏的目的
			for each in map_stage.treeGroup:
				screen.blit(each.tree, each.rect)
			screen.blit(UI.getTextSurface("玩家一坦克剩余生命：{:}".format(tank_player1.life)),(10,10))
			if num_player >1:
				screen.blit(UI.getTextSurface("玩家二坦克剩余生命：{:}".format(tank_player2.life)),(10,30))
				screen.blit(UI.getTextSurface("敌方坦克剩余数量：{:}".format(enemytanks_total+enemytanks_now)),(10,50))
			else:
				screen.blit(UI.getTextSurface("敌方坦克剩余数量：{:}".format(enemytanks_total+enemytanks_now)),(10,30))

			if tank_player1.dead:
				UI.display(screen)
			if num_player>1 and tank_player2.dead:
				UI.display_2(screen)
			# 食物
			for myfood in myfoodsGroup:
				if myfood.being and myfood.time > 0:
					screen.blit(myfood.food, myfood.rect)
					myfood.time -= 1
					for tank_player in mytanksGroup:
						if pygame.sprite.collide_rect(tank_player, myfood):
							self.last_food_time=pygame.time.get_ticks()
							# 消灭当前所有敌人
							if myfood.kind == 0:
								self.food_kind = 0
								for _ in enemytanksGroup:
									bang_sound.play()
								enemytanksGroup = pygame.sprite.Group()
								enemytanks_now = len(bossGroup)
							# 敌人静止
							if myfood.kind == 1:
								self.is_still = 1
								self.food_kind = 1
								self.last_still_time = pygame.time.get_ticks()
								for each in enemytanksGroup:
									each.can_move = False
							# 子弹增强
							if myfood.kind == 2:
								self.food_kind = 2
								add_sound.play()
								Display.bullet_stronger = True
							# 坦克获得一段时间的保护罩
							if myfood.kind == 3:
								self.food_kind = 3
								add_sound.play()
								for tank_player in mytanksGroup:
									tank_player.protected = True
							# 坦克升级
							if myfood.kind == 4:
								self.food_kind = 4
								add_sound.play()
								tank_player.up_level()
							# 坦克生命+1
							if myfood.kind == 5:
								self.food_kind = 5
								add_sound.play()
								tank_player.life += 1
							myfood.being = False
							myfoodsGroup.remove(myfood)
							break
				else:
					myfood.being = False
					myfoodsGroup.remove(myfood)
			if self.food_kind !=-1:
				if pygame.time.get_ticks()-self.last_food_time>self.food_delay:
					self.last_food_time=pygame.time.get_ticks()
					self.food_kind = -1
				if self.food_kind == 0:
					screen.blit(UI.getTextSurface("消灭敌方坦克",60,1),(430,600))
				elif self.food_kind == 1:
					screen.blit(UI.getTextSurface("敌军静止一段时间",60,1),(400,600))
				elif self.food_kind == 2:
					screen.blit(UI.getTextSurface("子弹增强",60,1),(450,600))
				elif self.food_kind == 3:
					screen.blit(UI.getTextSurface("坦克获得保护罩",60,1),(430,600))
				elif self.food_kind == 4:
					screen.blit(UI.getTextSurface("子弹射速升级",60,1),(430,600))
				elif self.food_kind == 5:
					screen.blit(UI.getTextSurface("坦克生命+1",60,1),(440,600))
			pygame.display.flip()
			clock.tick(60)
		Display.displayexplode(screen,explodeGroup)
		if not is_gameover:
			mid = self.game_over(screen,1)
			if mid == 0:
				self.start_sound.stop()
				return
		else:
			mid = self.game_over(screen,0)
			if mid == 0:
				self.start_sound.stop()
				return

	def game_pause(self,screen):
		self.start_sound.stop()
		while True:
            # 显示图片
			screen.blit(self.game_pause_image, (360, 230))
			pygame.display.flip()
			key_pressed = pygame.key.get_pressed()
            # 按esc退出游戏
			if key_pressed[pygame.K_ESCAPE]:
				return 0
            # 如果点击鼠标就暂停结束
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					return 1
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
	def game_over(self,screen,is_win):
		while True:
            # 根据游戏结局不同 选择不同图片显示
			if is_win == 1:
				screen.blit(self.bg_img,(0,0))
				screen.blit(self.game_over_win, (360, 230))
			elif is_win == 0:
				screen.blit(self.bg_img,(0,0))
				screen.blit(self.game_over_fail, (360, 230))

			pygame.display.flip()
			key_pressed = pygame.key.get_pressed()
            # 按esc退出游戏
			if key_pressed[pygame.K_ESCAPE]:
				self.start_sound.stop()
				return 0
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
	def game_tip(self,screen,stage):
		while True:
			# 显示图片
			if stage == 2 or stage == 6 or stage == 9 or stage == 10 or stage == 11 or stage == 13:
				screen.blit(self.game_tip_image1, (280, 220))
			elif stage == 16:
				screen.blit(self.game_tip_image2, (280, 220))
			else:
				screen.blit(self.game_tip_image3, (280, 220))
			pygame.display.flip()
			key_pressed = pygame.key.get_pressed()
			# 按esc退出游戏
			if key_pressed[pygame.K_ESCAPE]:
				return 0
			# 如果点击鼠标就暂停结束
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					return 1
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
if __name__ == '__main__':
     Display=display.Display()
     Display.show_start_interface(SCREEN_WIDTH,SCREEN_HIGHT)