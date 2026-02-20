"""
A simple robot simulator on a 2D grid.
"""

from enum import Enum
from typing import Tuple


class Facing(Enum):  # Facing 我们定义为一个枚举类，用于定义方向。如有疑问可以自行 Google / Ask AI
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Grid():
    def __init__(self, width: int, height: int, enemy_pos: tuple):  # DO NOT EDIT THIS METHOD
        self.width: int = width
        self.height: int = height
        self._current_pos: tuple = (0, 0)
        self.current_direction = Facing.UP
        self.enemy_pos: tuple = enemy_pos
        self.position_history: dict = {}  # 用于存储位置历史，键为步数，值为坐标

    @property
    def current_pos(self) -> Tuple[int, int]:
        """
        current_pos 属性的 getter，返回私有属性 _current_pos
        """
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: Tuple[int, int]) -> None:
        """
        current_pos 属性的 setter（作为第 1 题留空）

        要求：
          - 接受一个长度为 2 的 tuple (x, y)
          - 若传入非 tuple 或长度不为 2，应抛出 TypeError
          - 将 x, y 强制转换为 int ，检查是否超出了宽高范围，如果任何一个超出则将其限制在最大宽高范围即可
          - 处理后存入 self._current_pos
        """
        # TODO: Question 1
        # 检查传入的值是否为tuple且长度为2
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError("current_pos must be a tuple of length 2")

        # 强制转换为int类型
        x = int(value[0])
        y = int(value[1])

        # 限制坐标在网络范围内
        x = max(0, min(x, self.width))
        y = max(0, min(y, self.height))

        # 更新私有变量
        self._current_pos = (x, y)

    def move_forward(self) -> Tuple[int, int]:  # type: ignore
        '''
        让机器人向当前方向走一格
        返回新的坐标 (x,y) 同时更新成员变量
        利用好上面的 setter
        以右为X轴正方向，上为Y轴正方向
        '''
        # TODO: Question 2
        # 获取当前位置
        x, y = self.current_pos

        # 根据当前方向移动
        if self.current_direction == Facing.RIGHT:
            x += 1
        elif self.current_direction == Facing.UP:
            y += 1
        elif self.current_direction == Facing.LEFT:
            x -= 1
        elif self.current_direction == Facing.DOWN:
            y -= 1

        # 使用setter更新位置
        self.current_pos = (x, y)

        return self.current_pos

    def turn_left(self) -> Facing:  # type: ignore
        '''
        让机器人逆时针转向
        返回一个新方向 (Facing.UP/DOWN/LEFT/RIGHT)
        '''
        # TODO: Question 3a
        # 逆时针旋转：当前值为+1，然后对4取模
        new_value = (self.current_direction.value + 1) % 4
        self.current_direction = Facing(new_value)

        return self.current_direction

    def turn_right(self) -> Facing:  # type: ignore
        '''
        让机器人顺时针转向
        '''
        # TODO: Question 3b
        # 顺时针旋转：当前值为-1，然后对4取模
        new_value = (self.current_direction.value - 1) % 4
        self.current_direction = Facing(new_value)

        return self.current_direction

    def find_enemy(self) -> bool:  # type: ignore
        '''
        如果找到敌人（机器人和敌人坐标一致），就返回true
        '''
        # TODO: Question 4
        return self.current_pos == self.enemy_pos

    def record_position(self, step: int) -> None:
        '''
        将当前位置记录到 position_history 字典中
        键(key)为步数 step，值(value)为当前坐标 self.current_pos
        例如：step=1 时，记录 {1: (0, 0)}
        '''
        # TODO: Question 5a
        self.position_history[step] = self.current_pos

    def get_position_at_step(self, step: int) -> tuple:  # type: ignore
        '''
        从 position_history 字典中获取指定步数的坐标
        如果该步数不存在，返回 None
        '''
        # TODO: Question 5b
        # 使用get方法，如果键不存在则返回None
        return self.position_history.get(step)


"""
在这里你需要实现 AdvancedGrid 类，继承自 Grid 类，并添加以下功能：
1. 追踪移动步数
2. 计算到敌人的曼哈顿距离

类名：AdvancedGrid
继承自：Grid
包含以下新属性：
- steps: int - 追踪移动步数，初始值为 0

包含以下方法：
1. move_forward(self) -> Tuple[int, int]
    调用父类的 move_forward 方法完成移动
    新增实现：移动步数 self.steps 加 1
    返回：移动后新坐标

2. distance_to_enemy(self) -> int
    计算当前位置到敌人位置的曼哈顿距离
    曼哈顿距离 = |x1 - x2| + |y1 - y2|
    返回：曼哈顿距离值

"""


# TODO: Question 6
class AdvancedGrid(Grid):
    def __init__(self, width: int, height: int, enemy_pos: tuple):
        # 调用父类的初始化方法
        super().__init__(width, height, enemy_pos)
        # 添加新属性：移动步数
        self.steps: int = 0

    def move_forward(self) -> Tuple[int, int]:
        '''
         重写move_forward方法，增加步数计数
        '''
        # 调用父类的move_forward方法
        new_pos = super().move_forward()

        # 步数加1
        self.steps += 1

        return new_pos

    def distance_to_enemy(self) -> int:
        '''
        计算当前位置到敌人的曼哈顿距离
        曼哈顿距离 = |x1 - x2| + |y1 - y2|
        '''
        # 获取当前坐标
        current_x, current_y = self.current_pos
        # 获取敌人坐标
        enemy_x, enemy_y = self.enemy_pos

        # 计算曼哈顿距离
        distance = abs(current_x - enemy_x) + abs(current_y - enemy_y)

        return distance


# 测试代码
if __name__ == "__main__":
    # 测试Grid类
    print("===测试Grid类===")
    grid = Grid(10, 10, (5, 5))

    # 测试setter
    print("1. 测试setter:")
    grid.current_pos = (3, 4)
    print(f"   设置位置为（3，4）：{grid.current_pos}")

    # 测试超出范围的情况
    grid.current_pos = (15, 15)
    print(f"   设置位置为（15，15）（超出范围）：{grid.current_pos}（应限制在9，9）")

    # 测试移动
    print("\n2.测试移动")
    grid.current_pos = (2, 2)
    grid.current_direction = Facing.RIGHT
    print(f"  当前位置：{grid.current_pos}，面向：{grid.current_direction}：")
    new_pos = grid.move_forward()
    print(f"  向前移动后：{new_pos}")

    # 测试转向
    print("\n3.测试转向：")
    grid.turn_left()
    print(f"  左转后：{grid.current_direction}")
    grid.turn_right()
    print(f"  右转后：{grid.current_direction}")

    # 4.测试寻找敌人
    print("\n4.测试寻找敌人：")
    grid.current_pos = (5, 5)
    print(f"  当前位置在敌人位置：{grid.find_enemy()}")
    grid.current_pos = (0, 0)
    print(f"  当前位置不在敌人位置：{grid.find_enemy()}")

    # 测试记录位置
    print("\n5.测试位置记录：")
    grid.record_position(1)
    grid.record_position(2)
    grid.move_forward()
    grid.record_position(3)
    print(f"  步数1的位置：{grid.get_position_at_step(1)}")
    print(f"  步数2的位置：{grid.get_position_at_step(2)}")
    print(f"  步数3的位置：{grid.get_position_at_step(3)}")
    print(f"  步数4的位置：{grid.get_position_at_step(4)}应为（None）")

    # 测试AdvancedGrid类
    print("\n===测试AdvancedGrid===")
    adv_grid = AdvancedGrid(10, 10, (5, 5))

    # 初始状态
    print(f"初始步数：{adv_grid.steps}")
    print(f"初始距离敌人：{adv_grid.distance_to_enemy()}")

    # 移动并测试
    adv_grid.current_pos = (0, 0)
    adv_grid.current_direction = Facing.RIGHT

    # 移动3次
    for i in range(3):
        adv_grid.move_forward()

    print(f"移动3次后步数：{adv_grid.steps}")
    print(f"移动3次后距离敌人：{adv_grid.distance_to_enemy()}")
