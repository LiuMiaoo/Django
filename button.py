import pygame.font


class Button:
    def __init__(self,ai_game,msg):
        """初始化按钮的属性"""
        '''
        它Pygame能够将文本到屏幕上。方法__init__()接受参数 self、对象ai_game和msg，其中msg是要在按钮种显示的文本
        设置按钮尺寸，并背景颜色和文本颜色
        Pygame处理文本的方式是将要显示的字符串渲染为图像
        '''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width,self.height = 200,50
        self.button_color =(0,255,0)
        self.text_color =(255,255,255)
        self.font = pygame.font.SysFont(None,48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self._prep_msg(msg)


    def _prep_msg(self,msg):
        """将msg渲染为图像并在按钮上居中"""
        # 将文本转化为图像
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect =self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)


