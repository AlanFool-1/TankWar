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
        # ?????????????????????
        for each in map_stage.brickGroup:
            if pygame.sprite.collide_rect(tank_player.bullet, each):
                tank_player.bullet.being = False
                each.being = False
                map_stage.brickGroup.remove(each)
                break

        # ???????????????
        for each in map_stage.ironGroup:
            if pygame.sprite.collide_rect(tank_player.bullet, each):
                tank_player.bullet.being = False
                if  self.bullet_stronger:
                    each.being = False
                    map_stage.ironGroup.remove(each)
                break
    def display_object(self,screen,map_stage):
        # ?????????
        for each in map_stage.brickGroup:
            screen.blit(each.brick, each.rect)
        # ??????
        for each in map_stage.ironGroup:
            screen.blit(each.iron, each.rect)
        # ???
        for each in map_stage.iceGroup:
            screen.blit(each.ice, each.rect)
        # ??????
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
        # ???
       

    def show_start_interface(self, width, height):
        pygame.init()
        screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        pygame.display.set_caption("????????????")
        bg_img = pygame.image.load("images/others/start.png")
        screen.blit(bg_img, (0, 0))
        tfont = pygame.font.Font('font/IPix.ttf', width // 15)
        cfont = pygame.font.Font('font/IPix.ttf', width // 25)
        title = tfont.render(u'?????????...', True, (255, 0, 0))
        trect = title.get_rect()
        trect.midtop = (width / 2, height / 1.5)
        screen.blit(title,trect)
        # ???????????????????????????
        init_image_all = [None]*107
        for i in range(1,106):
            init_image_all[i] = pygame.image.load(r"images\init\init ("+str(i)+").png")

        # ??????????????????????????????????????????
        screen.blit(init_image_all[1], (280,220))
        pygame.display.flip()
        now_i = 1

        # ???????????????????????????????????????
        checkpoint_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        # ??????
        checkpoint_theme.background_color =pygame_menu.BaseImage(r"images/others/start.png")
        # ????????????
        checkpoint_theme.widget_font=pygame.font.Font('font/IPix.ttf', width // 30)
        # ?????????????????????
        checkpoint_theme.title_background_color = (0, 0, 0, 0)
        checkpoint_theme.widget_font_size = 35

        #????????????????????????
        instruction_theme =  pygame_menu.themes.THEME_DEFAULT.copy()
        # ??????
        instruction_theme.background_color =pygame_menu.BaseImage(r"images/others/instruction.jpg")
        # ?????????????????????
        instruction_theme.title_background_color = (0, 0, 0, 0)
        
        # ?????????????????????????????????
        level_mode_menu = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HIGHT, theme=checkpoint_theme)
        double_mode_menu = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HIGHT, theme=checkpoint_theme)
        instruction_menu = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HIGHT, theme=instruction_theme)

        # ???????????????35?????????????????????????????? ???????????????????????????
        for i in range(1,17):
            # ???????????? ????????????????????????
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # ??????????????????
            screen.blit(init_image_all[now_i], (280,220)) # ????????????
            now_i += 1 # ?????????????????????????????????
            screen.blit(init_image_all[now_i], (280,220)) # ????????????
            now_i += 1 # ?????????????????????????????????
            pygame.display.flip() # ????????????
            # ???????????????????????????????????????
            background_image = pygame_menu.BaseImage(
                image_path=r"images\maps\Battle-City-"+str(i)+".png"
            )
            # ????????????????????????????????????????????????
            level_mode_menu.add.label(" ??????"+str(i),margin = (10,10))
            level_mode_menu.add.vertical_margin(10)
            level_mode_menu.add.button('',Level_mode,i,background_color = background_image,
                                    padding = (90,180,80,80),margin = (10,10),border_inflate = (10,10),border_width = (10))
             # ????????????????????????????????????????????????
            double_mode_menu.add.label(" ??????"+str(i),margin = (10,10))
            double_mode_menu.add.vertical_margin(10)
            double_mode_menu.add.button('',Level_mode,i,2,background_color = background_image,
                                    padding = (90,180,80,80),margin = (10,10),border_inflate = (10,10),border_width = (10))
            # ??????????????????
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
            pygame.display.flip()
            # ??????????????????
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
            pygame.display.flip()

        # ???????????????????????????
        main_theme = pygame_menu.themes.THEME_BLUE.copy()
        # ????????????
        main_theme.background_color = pygame_menu.BaseImage(r"images/others/start.png")
        # ????????????
        main_theme.widget_font=pygame.font.Font('font/IPix.ttf', width // 20)
        #main_theme.widget_font = pygame_menu.font.FONT_FRANCHISE
        # ?????????????????????
        main_theme.title_background_color = (0, 0, 0, 0)
        main_theme.widget_font_size = 50
        # ?????????????????????
        main_menu = pygame_menu.Menu('',SCREEN_WIDTH, SCREEN_HIGHT, theme=main_theme)

        image_path = r"images\logo.png"
        main_menu.add.image(image_path,scale = (1,1))
        main_menu.add.button('????????????', level_mode_menu)
        main_menu.add.button('????????????', double_mode_menu)
        main_menu.add.button('????????????',instruction_menu)
        main_menu.add.button('??????', pygame_menu.events.EXIT)
        while now_i<=105:
            screen.blit(init_image_all[now_i], (280,220))
            now_i += 1
        main_menu.mainloop(screen)
    # ????????????
    def show_switch_stage(self,screen, width, height, stage):
        bg_img = pygame.image.load("images/others/background.png")
        screen.blit(bg_img, (0, 0))
        font = pygame.font.Font('font/IPix.ttf', width // 10)
        content = font.render(u'???%d???' % stage, True, (0, 255, 0))
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
    