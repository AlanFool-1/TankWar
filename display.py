import pygame,pygame_menu
import sys

import ui,start
SCREEN_WIDTH=1200
SCREEN_HIGHT=720

class Display:
    def __init__(self):
        self.kind=0
        self.time=0
        self.ui= ui.Ui()   
        self.bullet_stronger = False 
    def displayexplode(self,screen,explodeGroup):
        for each in explodeGroup:
            each.time -= 1
            if each.kind==0:
                if each.time >= 24:
                    screen.blit(each.images[0], each.rect)
                elif each.time >= 21:
                    screen.blit(each.images[1], each.rect)
                elif each.time >= 18:
                    screen.blit(each.images[2], each.rect)
                elif each.time >= 15:
                    screen.blit(each.images[3], each.rect)
                elif each.time >= 12:
                    screen.blit(each.images[4], each.rect)
                elif each.time >= 9:
                    screen.blit(each.images[5], each.rect)
                elif each.time >= 6:
                    screen.blit(each.images[6], each.rect)
                elif each.time >= 3:
                    screen.blit(each.images[7], each.rect)
                elif each.time >= 0:
                    screen.blit(each.images[8], each.rect)
                if each.time < 0:
                    explodeGroup.remove(each)
            else:
                if each.time>=0:
                    screen.blit(each.images[each.time],each.rect)
                else:
                    explodeGroup.remove(each)
    def display_enemyTank(self,screen,each,appearances):
        if each.times > 0:
            each.times -= 1
            if each.times <= 10:
                screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
            elif each.times <= 20:
                screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
            elif each.times <= 30:
                screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
            elif each.times <= 40:
                screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
            elif each.times <= 50:
                screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
            elif each.times <= 60:
                screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
            elif each.times <= 70:
                screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
            elif each.times <= 80:
                screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
            elif each.times <= 90:
                screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
        else:
            each.born = False
    def check_wall(self,map_stage,tank_player):
        # 子弹碰撞石头墙
        for each in map_stage.brickGroup:
            if pygame.sprite.collide_rect(tank_player.bullet, each):
                tank_player.bullet.being = False
                each.being = False
                map_stage.brickGroup.remove(each)
                break

        # 子弹碰钢墙
        for each in map_stage.ironGroup:
            if pygame.sprite.collide_rect(tank_player.bullet, each):
                tank_player.bullet.being = False
                if  self.bullet_stronger:
                    each.being = False
                    map_stage.ironGroup.remove(each)
                break
    def display_object(self,screen,map_stage):
        # 石头墙
        for each in map_stage.brickGroup:
            screen.blit(each.brick, each.rect)
        # 钢墙
        for each in map_stage.ironGroup:
            screen.blit(each.iron, each.rect)
        # 冰
        for each in map_stage.iceGroup:
            screen.blit(each.ice, each.rect)
        # 河流
        if self.time == 70:
            self.time = 0
            self.kind ^= 1
        # is_switch_tank = not is_switch_tank
        self.time += 1
        for each in map_stage.riverGroup:
            each.kind ^= 1
            if self.kind == 0:
                screen.blit(each.river1, each.rect)
            elif self.kind == 1:
                screen.blit(each.river2, each.rect)
        # 树
       

    def show_start_interface(self, width, height):
        pygame.init()
        screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        pygame.display.set_caption("坦克大战")
        bg_img = pygame.image.load("images/others/start.png")
        screen.blit(bg_img, (0, 0))
        tfont = pygame.font.Font('font/IPix.ttf', width // 15)
        cfont = pygame.font.Font('font/IPix.ttf', width // 25)
        title = tfont.render(u'加载中...', True, (255, 0, 0))
        trect = title.get_rect()
        trect.midtop = (width / 2, height / 1.5)
        screen.blit(title,trect)
        # 创建加载界面的图片
        init_image_all = [None]*107
        for i in range(1,106):
            init_image_all[i] = pygame.image.load(r"images\init\init ("+str(i)+").png")

        # 显示加载界面（其中一张图片）
        screen.blit(init_image_all[1], (280,220))
        pygame.display.flip()
        now_i = 1

        # 创建选择关卡菜单的“主题”
        checkpoint_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        # 背景
        checkpoint_theme.background_color =pygame_menu.BaseImage(r"images/others/start.png")
        # 字体样式
        checkpoint_theme.widget_font=pygame.font.Font('font/IPix.ttf', width // 30)
        # 标题栏背景颜色
        checkpoint_theme.title_background_color = (0, 0, 0, 0)
        checkpoint_theme.widget_font_size = 35

        #创建说明界面菜单
        instruction_theme =  pygame_menu.themes.THEME_DEFAULT.copy()
        # 背景
        instruction_theme.background_color =pygame_menu.BaseImage(r"images/others/instruction.jpg")
        # 标题栏背景颜色
        instruction_theme.title_background_color = (0, 0, 0, 0)
        
        # 关卡模式“菜单”的创建
        level_mode_menu = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HIGHT, theme=checkpoint_theme)
        double_mode_menu = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HIGHT, theme=checkpoint_theme)
        instruction_menu = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HIGHT, theme=instruction_theme)

        # 此循环是将35关的图片加载到按钮里 并将按钮加入菜单中
        for i in range(1,17):
            # 事件检测 保证可以随时退出
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # 显示加载界面
            screen.blit(init_image_all[now_i], (280,220)) # 显示图片
            now_i += 1 # 将图片的索引换位下一张
            screen.blit(init_image_all[now_i], (280,220)) # 显示图片
            now_i += 1 # 将图片的索引换位下一张
            pygame.display.flip() # 刷新界面
            # 将图片初始化为默认背景图片
            background_image = pygame_menu.BaseImage(
                image_path=r"images\maps\Battle-City-"+str(i)+".png"
            )
            # 关卡模式菜单添加标签、间隔、按钮
            level_mode_menu.add.label(" 关卡"+str(i),margin = (10,10))
            level_mode_menu.add.vertical_margin(10)
            level_mode_menu.add.button('',Level_mode,i,background_color = background_image,
                                    padding = (90,180,80,80),margin = (10,10),border_inflate = (10,10),border_width = (10))
             # 关卡模式菜单添加标签、间隔、按钮
            double_mode_menu.add.label(" 关卡"+str(i),margin = (10,10))
            double_mode_menu.add.vertical_margin(10)
            double_mode_menu.add.button('',Level_mode,i,2,background_color = background_image,
                                    padding = (90,180,80,80),margin = (10,10),border_inflate = (10,10),border_width = (10))
            # 显示加载界面
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
            pygame.display.flip()
            # 显示加载界面
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
            pygame.display.flip()

        # 创建主菜单“主题”
        main_theme = pygame_menu.themes.THEME_BLUE.copy()
        # 背景颜色
        main_theme.background_color = pygame_menu.BaseImage(r"images/others/start.png")
        # 字体样式
        main_theme.widget_font=pygame.font.Font('font/IPix.ttf', width // 20)
        #main_theme.widget_font = pygame_menu.font.FONT_FRANCHISE
        # 标题栏背景颜色
        main_theme.title_background_color = (0, 0, 0, 0)
        main_theme.widget_font_size = 50
        # 创建主“菜单”
        main_menu = pygame_menu.Menu('',SCREEN_WIDTH, SCREEN_HIGHT, theme=main_theme)

        image_path = r"images\logo.png"
        main_menu.add.image(image_path,scale = (1,1))
        main_menu.add.button('单人模式', level_mode_menu)
        main_menu.add.button('双人模式', double_mode_menu)
        main_menu.add.button('游戏说明',instruction_menu)
        main_menu.add.button('退出', pygame_menu.events.EXIT)
        while now_i<=105:
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
        main_menu.mainloop(screen)
    # 关卡切换
    def show_switch_stage(self,screen, width, height, stage):
        bg_img = pygame.image.load("images/others/background.png")
        screen.blit(bg_img, (0, 0))
        font = pygame.font.Font('font/IPix.ttf', width // 10)
        content = font.render(u'第%d关' % stage, True, (0, 255, 0))
        rect = content.get_rect()
        rect.midtop = (width / 2, height / 3)
        screen.blit(content, rect)
        pygame.display.update()
        delay_event = pygame.constants.USEREVENT
        pygame.time.set_timer(delay_event, 1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == delay_event:
                    return


def Level_mode(i,num=1):
    Main=start.MainGame(i)
    Main.main(i,num)
    