class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settigs = ai_game.settings
        self.reset_stats()


        # 游戏启动标志
        self.game_active = False

        # 任何情况下都不应该重置最高分
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settigs.ship_limit
        # 每次开始游戏都得重置得分
        self.score = 0
        # 显示等级
        self.level =1

