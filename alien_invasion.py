# 创建Pygame窗口以及响应用户的输入
import sys
from time import sleep

import pygame
from alien import Alien

from bullet import Bullet
from game_stats import GameStats
from scoreboard import Scoreboard
from setting import Settings
from ship import Ship
from button import Button


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏资源"""
        # 初始化背景设置
        pygame.init()
        self.settings = Settings()

        # 创建一个显示窗口，游戏的所有图形元素都将在其中绘制
        # 全屏模式
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # 无法预知屏幕的宽度和高度，要在创建之后进行更新
        self.settings.screen_width =self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        #创建计分牌
        self.sb = Scoreboard(self)


        #self指向当前AlienInvasion实例
        self.ship = Ship(self)
        #创建用于存储子弹的编组
        self.bullets = pygame.sprite.Group()
        # 创建alien存储外星人编组
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建play按钮
        self.play_button = Button(self,"play")








    def run_game(self):
        """开始游戏的主循环"""
        '''
        包含一个事件循环以及管理屏幕更新的代码
        事件是用户玩游戏时执行的操作，按键或移动鼠标
        '''

        while True:
            # 监视键盘和鼠标事件
            self._check_events()
            if self.stats.game_active:
                # 飞船按键移动
                self.ship.update()
                # 更新子弹的位置
                self.bullets.update()

                # 删除消失的子弹 遍历副本
                self._update_bullets()

                # 更新外星人的位置
                self._update_aliens()
            # 每次循环都重绘屏幕 用背景色填充屏幕
            self._update_screen()





    def _check_events(self):
        """响应按键和鼠标事件"""
        '''
        get()函数返回一个列表
        其中包含它在上一次被调用后发生的所有事情
        每当用户按键时，都在Pygame中注册一个事件
        每次按键都被注册成一个KEYDOWN事件
        可持续移动，直到松开为止
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 返回一个元组，包含玩家单机鼠标时的x和y坐标
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
                sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)




    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 绘制外星人
        '''
        对编组调用draw()时，Pygame将编组中的每个元素绘制到属性rect指定位置上
        接受一个参数，参数指定要将元素绘制到哪个surface上
        '''
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态就绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        '''
        在每次执行while循环时，都会绘制一个空屏幕并擦去旧屏幕，
        只有新屏幕可见，移动游戏元素时，将不断更新屏幕，显示元素的新的位置
        并在原来的位置印象元素，从而营造平滑移动的效果
        '''
        pygame.display.flip()

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查是否有子弹击中了外星人,删除相应的子弹和外星人、

        self._check_bullet_alien_collisions()



    def _create_fleet(self):
        """创建外星人群"""

        alien =Alien(self)
        alien_width,alien_height = alien.rect.size
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人宽度
        available_space_x = self.settings.screen_width-(2*alien_width)
        number_aliens_x = available_space_x //(2*alien_width)
        # 计算屏幕可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height)-ship_height)
        number_rows = available_space_y // (2*alien_height)



        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)


    def _create_alien(self,alien_number,row_number):
        # 创建一个外星人并将其加入当前行
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edgs()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        # 接受两个实参 一个精灵和一个编组，检查是都有成员精灵发生了碰撞
        # 并在找到与精灵发生碰撞的成员后停止遍历编组
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _check_fleet_edgs(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        '''
        将编组中每个元素的rect同另一个编组中每个元素的rect进行比较
        将每颗子弹的rect同每个外星人的rect进行比较 并会一个字典，其中包含了发生碰撞的子弹和外星人
        每个键都是一颗子弹，关联值时被该子弹集中的外星人
        '''
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # 更新得分
        if collisions:
            # 如果外星人在子弹射中的列表中
            for aliens in collisions.values():
              self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有子弹并新键一群外星人
            self.bullets.empty()
            self._create_fleet()
            # 增加速度
            self.settings.increase_speed()

            # 提高等级
            self.stats.level +=1
            self.sb.prep_level()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left >0:

            #将ships_left减一
            self.stats.ships_left -=1
            self.sb.prep_ship()

            # 清空剩下的子弹和外星人
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的外星人，并将飞船梵高屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #像飞船被撞到一样处理
                self._ship_hit()
                break

    def _check_play_button(self,mouse_pos):
        """在玩家单击play按钮时开始新游戏"""
        # 加检查鼠标单击位置是否在play按钮的rect内
        button_clicked =self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏统计信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)







if __name__ =='__main__':
    # 创建游戏实例并运行实例
    ai = AlienInvasion()
    ai.run_game()


