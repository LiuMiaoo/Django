import ship


class Settings:
    """存储游戏中所有的设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置

        # 激活游戏的动画循环后，每经过一次循环都将自动重绘这个surface
        self.screen_width=1200
        self.screen_height =800
        # 设置背景颜色 颜色使用RGB指定
        self.bg_color = (230,230,230)



        # 子弹设置

        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        self.ship_limit = 3

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1

        # 外星分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行变化的设置"""
        # 飞船设置
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1.0
        # 1表示向右移动，-1表示向左移动
        self.fleet_direction = 1

        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置和外星人的分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points*self.score_scale)

