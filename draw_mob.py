import sys

import pygame
import math
import random

# 初始化 Pygame
pygame.init()
WHITE = (255, 255, 255)
DEEP_WHITE = (128, 128, 128)  # 深灰色

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("海绵绘制 - 多孔结构")

# 颜色定义
BACKGROUND = (30, 40, 50)
DARK_WHITE = (158, 158, 158)  # 深灰白色

LIGHT_GREY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 110, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BROWN = (160, 120, 80)
DARK_BROWN = (100, 70, 40)
ANTHOLE_BROWN = (89, 29, 10)
WING_COLOR = (200, 200, 255, 100)
MAP_GREEN = (100, 150, 50)
BUTTON_COLOR = (80, 80, 120)
BUTTON_HOVER_COLOR = (100, 100, 150)
MENU_BG = (30, 30, 60)
MENU_ACCENT = (70, 70, 120)
DARK_RED = (200, 5, 5)
MOB_DARK_GRAY = (90, 90, 90)
DEEP_RED = (139, 0, 0)
DARK_RED = (171, 31, 31)
CELL_COLOR = (200, 230, 255)  # 干细胞细胞质
MEMBRANE_COLOR = (100, 150, 200)
DARK_YELLOW = (153, 153, 0)
DEEP_YELLOW = (253, 210, 35)
HIVE_COLOUR = (112, 90, 0)

# 海绵专用颜色
SPONGE_LIGHT_BROWN = (217, 166, 89)  # (0.85, 0.65, 0.35)
SPONGE_LIGHT_YELLOW = (242, 217, 153)  # (0.95, 0.85, 0.60)
SPONGE_DARK_BROWN = (204, 153, 77)  # (0.80, 0.60, 0.30)
SPONGE_MEDIUM_BROWN = (230, 191, 115)  # (0.90, 0.75, 0.45)
SPONGE_HOLE_COLOR = (255, 255, 255)  # 白色孔洞
SPONGE_HOLE_EDGE = (190, 150, 80)  # 孔洞边缘颜色


def draw_quarter_circle_sector(surface, color, center, radius, start_angle, end_angle):
    """绘制1/4圆扇形（填充）"""
    points = [center]  # 从圆心开始

    steps = 30
    for i in range(steps + 1):
        angle = start_angle + (end_angle - start_angle) * i / steps
        x = center[0] + radius * math.cos(angle)
        y = center[1] - radius * math.sin(angle)  # Pygame的y轴向下，所以用减号
        points.append((int(x), int(y)))

    pygame.draw.polygon(surface, color, points)


def draw_quarter_circle_arc(surface, color, center, radius, start_angle, end_angle, width=1):
    """绘制1/4圆弧线"""
    points = []
    steps = 50

    for i in range(steps + 1):
        angle = start_angle + (end_angle - start_angle) * i / steps
        x = center[0] + radius * math.cos(angle)
        y = center[1] - radius * math.sin(angle)
        points.append((int(x), int(y)))

    pygame.draw.lines(surface, color, False, points, width)

def draw_sponge(x, y, scale=1.0, animation_timer=0):
    """
    规则波浪海绵 + 内部孔洞结构
    """

    base_radius = 50 * scale
    waves = 14
    wave_height = 8 * scale
    pulse = 2 * math.sin(animation_timer * 2)

    num_points = 180
    points = []

    # ===== 外轮廓 =====
    for i in range(num_points):
        angle = i * 2 * math.pi / num_points

        radius = (
            base_radius
            + math.sin(angle * waves) * wave_height
            + pulse
        )

        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)

        points.append((px, py))

    pygame.draw.polygon(screen, SPONGE_MEDIUM_BROWN, points)
    pygame.draw.polygon(screen, SPONGE_DARK_BROWN, points, int(3 * scale))

    # =========================
    # 内部孔洞结构（规则排列）
    # =========================

    hole_color = SPONGE_DARK_BROWN
    hole_inner = (60, 40, 30)  # 更深色

    # 中心孔
    pygame.draw.circle(screen, hole_color, (int(x), int(y)), int(10 * scale))


    # 第一圈孔
    ring1_count = 6
    ring1_radius = 20 * scale

    for i in range(ring1_count):
        angle = 2 * math.pi * i / ring1_count
        hx = x + math.cos(angle) * ring1_radius
        hy = y + math.sin(angle) * ring1_radius

        pygame.draw.circle(screen, hole_color, (int(hx), int(hy)), int(8 * scale))


    # 第二圈孔
    ring2_count = 6
    ring2_radius = 35 * scale

    for i in range(ring2_count):
        angle = 2 * math.pi * i / ring2_count
        hx = x + math.cos(angle) * ring2_radius
        hy = y + math.sin(angle) * ring2_radius

        pygame.draw.circle(screen, hole_color, (int(hx), int(hy)), int(7 * scale))
def draw_shell():
    """绘制一个扇贝"""
    center_x, center_y = 600, 400  # 扇贝位置
    pygame.draw.rect(screen, (255, 220, 180), (600, 385, 10, 30))
    # === 扇贝壳主体 ===
    # 使用1/4圆作为扇贝的主体形状
    draw_quarter_circle_sector(screen, (255, 200, 150), (center_x, center_y), 50, -math.pi / 4, math.pi / 4)
    # 内部颜色（稍浅）
    draw_quarter_circle_sector(screen, (255, 220, 180), (center_x, center_y), 40, -math.pi / 4, math.pi / 4)

    # === 扇贝的放射状条纹 ===
    for i in range(7):
        angle = -math.pi / 4 + (math.pi / 2) * i / 6  # 从-45°到45°之间
        end_x = center_x + 35 * math.cos(angle)
        end_y = center_y - 35 * math.sin(angle)
        pygame.draw.line(screen, (200, 150, 100), (center_x, center_y), (end_x, end_y), 4)
def draw_bubble():
    BUBBLE_WHITE=(200,200,200,0.1)
    DEEP_BUBBLE_WHITE=(180,180,180,0.1)
    pygame.draw.circle(screen, BUBBLE_WHITE, (100, 100), 12)
    pygame.draw.circle(screen, DEEP_BUBBLE_WHITE, (100, 100), 10)
def draw_crab():#已经有了
    pass
def draw_starfish(x, y, scale=1.0, rotation_angle=0):
    """
    绘制五角海星（中等速度自转）

    rotation_angle: 当前旋转角度（每帧递增）
    """

    size = int(160 * scale)
    star_surface = pygame.Surface((size, size), pygame.SRCALPHA)

    center = size // 2
    base_radius = 60 * scale
    inner_radius = 28 * scale

    points = []
    num_points = 5

    # ===== 生成五角结构 =====
    for i in range(num_points * 2):
        angle = i * math.pi / num_points - math.pi / 2

        if i % 2 == 0:
            radius = base_radius
        else:
            radius = inner_radius

        px = center + radius * math.cos(angle)
        py = center + radius * math.sin(angle)
        points.append((px, py))

    STAR_LIGHT = (255, 150, 80)
    STAR_DARK = (200, 90, 40)

    pygame.draw.polygon(star_surface, STAR_LIGHT, points)
    pygame.draw.polygon(star_surface, STAR_DARK, points, int(4 * scale))

    # ===== 内部放射点阵 =====
    for i in range(5):

        angle = i * 2 * math.pi / 5 - math.pi / 2

        max_length = base_radius * 0.7
        steps = 5  # 点的数量

        for s in range(steps):
            t = s / steps

            px = center + math.cos(angle) * max_length * t
            py = center + math.sin(angle) * max_length * t

            dot_size = int(6 * scale * (1 - t * 0.5))  # 越往外越小

            pygame.draw.circle(
                star_surface,
                STAR_DARK,
                (int(px), int(py)),
                dot_size
            )

    pygame.draw.circle(star_surface, STAR_DARK, (center, center), int(8 * scale))

    # ===== 旋转 =====
    rotated = pygame.transform.rotate(star_surface, rotation_angle)
    rect = rotated.get_rect(center=(x, y))

    screen.blit(rotated, rect)
def draw_jellyfish(animation_time=0):
    """绘制水母，触手均匀围绕圆形身体，轻微摆动"""
    center_x, center_y = 200, 200
    body_radius = 20

    # 创建半透明表面
    jellyfish_surface = pygame.Surface((100, 100), pygame.SRCALPHA)

    # 水母伞状体（半透明）
    pygame.draw.circle(jellyfish_surface, (200, 200, 200, 100), (50, 50), 20)
    pygame.draw.circle(jellyfish_surface, (255, 255, 255, 150), (50, 50), 16)

    # 将半透明表面绘制到主屏幕
    screen.blit(jellyfish_surface, (center_x - 50, center_y - 50))

    # 10根触手均匀围绕圆形身体
    num_tentacles = 8
    tentacle_length = 15
    num_segments = 8  # 每根触手的分段数

    for i in range(num_tentacles):
        # 均匀分布角度（360度/8 = 45度间隔）
        base_angle = (2 * math.pi * i) / num_tentacles - math.pi / 2  # 从上方开始

        # 触手起始位置（在圆形身体边缘）
        start_x = center_x + math.cos(base_angle) * body_radius
        start_y = center_y + math.sin(base_angle) * body_radius

        # 生成触手的弯曲路径点
        points = [(start_x, start_y)]

        for j in range(1, num_segments + 1):
            # 基础方向（从圆心向外辐射）
            segment_ratio = j / num_segments
            base_x = start_x + math.cos(base_angle) * tentacle_length * segment_ratio
            base_y = start_y + math.sin(base_angle) * tentacle_length * segment_ratio

            # 轻微摆动动画
            swing_amplitude = 1.5 + j * 0.3  # 轻微摆动
            swing_phase = animation_time * 2 + i * 0.6  # 每根触手有相位差
            swing_offset = math.sin(swing_phase + j * 0.4) * swing_amplitude

            # 垂直于触手方向的摆动
            perp_angle = base_angle + math.pi / 2
            x = base_x + math.cos(perp_angle) * swing_offset
            y = base_y + math.sin(perp_angle) * swing_offset

            points.append((x, y))

        # 绘制触手（使用线条连接所有点）
        if len(points) > 1:
            pygame.draw.lines(screen, (150, 150, 150), False, points, 4)
def draw_crabHole():
    CRABHOLE_BROWN=(64,49,4)
    DEEP_BROWN=(82,57,7)
    pygame.draw.circle(screen, DARK_BROWN, (200, 200), 40)
    pygame.draw.circle(screen, DEEP_BROWN, (200, 200), 30)
    pygame.draw.circle(screen, CRABHOLE_BROWN, (200, 200), 15)



def draw_white_blood_cell_original():
    """按照您原来代码中的绘制方法"""
    pygame.draw.circle(screen, DARK_WHITE, (200, 200), 20)
    pygame.draw.circle(screen, WHITE, (200, 200), 18)
    pygame.draw.circle(screen, DEEP_WHITE, (200, 200), 13)
    pygame.draw.circle(screen, DARK_WHITE, (200, 200), 12)


def draw_worker_fire_ant():
    pygame.draw.line(screen, BLACK, (200, 190), (235, 190), 5)
    pygame.draw.line(screen, BLACK, (200, 210), (235, 210), 5)
    pygame.draw.circle(screen, DEEP_RED, (170, 200), 18)
    pygame.draw.circle(screen, DARK_RED, (170, 200), 13)
    pygame.draw.circle(screen, DEEP_RED, (200, 200), 25)
    pygame.draw.circle(screen, DARK_RED, (200, 200), 20)


def draw_solider_fire_ant():
    pygame.draw.line(screen, BLACK, (200, 190), (235, 190), 5)
    pygame.draw.line(screen, BLACK, (200, 210), (235, 210), 5)
    pygame.draw.circle(screen, DEEP_RED, (170, 200), 18)
    pygame.draw.circle(screen, DARK_RED, (170, 200), 13)
    pygame.draw.ellipse(screen, LIGHT_GREY, (140, 180, 50, 15))
    pygame.draw.ellipse(screen, LIGHT_GREY, (140, 210, 50, 15))
    pygame.draw.circle(screen, DEEP_RED, (200, 200), 25)
    pygame.draw.circle(screen, DARK_RED, (200, 200), 20)


def draw_baby_fire_ant():
    pygame.draw.line(screen, BLACK, (200, 190), (235, 190), 5)
    pygame.draw.line(screen, BLACK, (200, 210), (235, 210), 5)
    pygame.draw.circle(screen, DEEP_RED, (200, 200), 30)
    pygame.draw.circle(screen, DARK_RED, (200, 200), 25)


def draw_fire_ant_overmind():
    pygame.draw.line(screen, BLACK, (200, 190), (260, 190), 5)
    pygame.draw.line(screen, BLACK, (200, 210), (260, 210), 5)
    pygame.draw.circle(screen, DEEP_RED, (200, 200), 50)
    pygame.draw.circle(screen, DARK_RED, (200, 200), 40)


def draw_fire_ant_hole():
    pygame.draw.circle(screen, RED, (200, 200), 40)
    pygame.draw.circle(screen, DARK_RED, (200, 200), 30)
    pygame.draw.circle(screen, DEEP_RED, (200, 200), 15)


def draw_queen_ant():
    # 身体1
    pygame.draw.circle(screen, MOB_DARK_GRAY, (120, 90), 35)
    pygame.draw.circle(screen, GRAY, (120, 90), 30)
    # 身体2
    pygame.draw.circle(screen, MOB_DARK_GRAY, (50, 90), 50)
    pygame.draw.circle(screen, GRAY, (50, 90), 45)
    # 翅膀
    pygame.draw.ellipse(screen, LIGHT_GREY, (20, 60, 120, 30))
    pygame.draw.ellipse(screen, LIGHT_GREY, (20, 90, 120, 30))
    # 头（使用三角形）
    pygame.draw.polygon(screen, GRAY, ((130, 60), (130, 120), (190, 90)))
    pygame.draw.polygon(screen, MOB_DARK_GRAY, ((130, 60), (130, 120), (190, 90)), 5)


def draw_bacteria():
    """绘制细菌"""
    GREEN = (0, 200, 0)

    # 上弧线
    pygame.draw.arc(screen, DARK_GREEN, (150, 100, 60, 30),
                    math.radians(100), math.pi, 5)
    pygame.draw.arc(screen, DARK_GREEN, (170, 100, 60, 30),
                    math.radians(100), math.pi, 5)
    pygame.draw.arc(screen, DARK_GREEN, (190, 100, 60, 30),
                    math.radians(80), math.pi, 5)

    # 下弧线
    pygame.draw.arc(screen, DARK_GREEN, (150, 120, 60, 30),
                    math.radians(170), math.radians(260), 5)
    pygame.draw.arc(screen, DARK_GREEN, (170, 120, 60, 30),
                    math.radians(160), math.radians(260), 5)
    pygame.draw.arc(screen, DARK_GREEN, (190, 120, 60, 30),
                    math.radians(160), math.radians(280), 5)

    # 细菌主体（矩形）
    pygame.draw.polygon(screen, GREEN, [(150, 110), (150, 140), (210, 140), (210, 110)])
    pygame.draw.polygon(screen, DARK_GREEN, [(150, 110), (150, 140), (210, 140), (210, 110)], 5)

    # 中间线条
    pygame.draw.line(screen, DARK_GREEN, (160, 125), (200, 125), 5)


def draw_bee():
    """绘制蜜蜂"""
    # 尾刺
    pygame.draw.polygon(screen, BLACK, [(190, 110), (190, 140), (210, 125)])

    # 身体
    pygame.draw.ellipse(screen, YELLOW, (100, 100, 100, 50))
    pygame.draw.ellipse(screen, DARK_YELLOW, (100, 100, 100, 50), 5)

    # 条纹
    pygame.draw.line(screen, BLACK, (120, 110), (120, 140), 4)
    pygame.draw.line(screen, BLACK, (150, 105), (150, 145), 4)
    pygame.draw.line(screen, BLACK, (180, 110), (180, 140), 4)

    # 触角
    left_antenna_points = [(105, 120), (95, 115), (85, 110), (80, 108)]
    pygame.draw.lines(screen, BLACK, False, left_antenna_points, 2)
    pygame.draw.circle(screen, BLACK, (80, 108), 3)

    right_antenna_points = [(105, 130), (95, 135), (85, 140), (80, 142)]
    pygame.draw.lines(screen, BLACK, False, right_antenna_points, 2)
    pygame.draw.circle(screen, BLACK, (80, 142), 3)


def draw_hive():
    """绘制蜂巢"""
    center_x, center_y = 400, 300

    # 大六边形
    big_points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = center_x + 80 * math.cos(angle)
        y = center_y + 80 * math.sin(angle)
        big_points.append((x, y))

    # 中六边形
    medium_points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = center_x + 60 * math.cos(angle)
        y = center_y + 60 * math.sin(angle)
        medium_points.append((x, y))

    # 小六边形
    small_points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = center_x + 40 * math.cos(angle)
        y = center_y + 40 * math.sin(angle)
        small_points.append((x, y))

    tiny_points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = center_x + 20 * math.cos(angle)
        y = center_y + 20 * math.sin(angle)
        tiny_points.append((x, y))

    pygame.draw.polygon(screen, YELLOW, big_points)
    pygame.draw.polygon(screen, DEEP_YELLOW, medium_points)
    pygame.draw.polygon(screen, YELLOW, small_points)
    pygame.draw.polygon(screen, DEEP_YELLOW, tiny_points)


def draw_HiveEgg():
    """绘制蜂卵"""
    pygame.draw.ellipse(screen, DARK_YELLOW, (100, 50, 70, 100))
    pygame.draw.ellipse(screen, HIVE_COLOUR, (100, 50, 70, 100), 6)


def draw_fly(angle=0):  # angle 是旋转角度
    # 身体
    pygame.draw.circle(screen, DARK_GRAY, (400, 400), 35)
    pygame.draw.circle(screen, GRAY, (400, 400), 30)

    # 创建翅膀 Surface
    wing_surface = pygame.Surface((50, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(wing_surface, WHITE, (0, 0, 50, 30))

    # 翅膀1（右边）- 保持原样
    wing1 = wing_surface
    screen.blit(wing1, (410, 390))

    # 翅膀2（左边）- 水平翻转
    wing2 = pygame.transform.flip(wing_surface, True, False)
    screen.blit(wing2, (390 - 50, 390))  # 减去宽度因为翻转后位置会变


def get_hexagon_points(center_x, center_y, radius):
    """计算正六边形的 6 个顶点坐标"""
    points = []
    for i in range(6):
        # 角度：0, 60, 120... (弧度制)
        # -30 度偏移是为了让六边形平顶朝上
        angle = math.radians(60 * i - 30)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    return points


def get_pupil_position(eye_center_x, eye_center_y, mouse_pos, max_offset):
    """
    计算眼珠位置：跟随鼠标，但不超出眼眶范围
    """
    mx, my = mouse_pos

    # 计算鼠标相对于眼睛中心的向量
    dx = mx - eye_center_x
    dy = my - eye_center_y

    # 计算距离
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # 如果距离为 0，返回眼睛中心
    if distance == 0:
        return eye_center_x, eye_center_y

    # 如果距离超过最大偏移量，则限制在边缘
    if distance > max_offset:
        ratio = max_offset / distance
        dx *= ratio
        dy *= ratio

    return eye_center_x + dx, eye_center_y + dy


def draw_Digger(screen, mouse_pos, is_angry=False):
    """
    绘制 Digger 生物
    :param screen: pygame surface
    :param mouse_pos: 鼠标位置元组 (x, y)，用于控制眼珠
    :param is_angry: 布尔值，True 为愤怒/攻击状态，False 为微笑状态
    """
    CENTER_X, CENTER_Y = 400, 400

    # --- 1. 绘制外圈 (正六边形) ---
    hex_radius = 70
    hex_points = get_hexagon_points(CENTER_X, CENTER_Y, hex_radius)

    # 填充灰色
    pygame.draw.polygon(screen, GRAY, hex_points)
    # 绘制黑色边框 (宽度 5)
    pygame.draw.polygon(screen, BLACK, hex_points, 5)

    # --- 2. 绘制身体 (双层圆) ---
    # 外层深色
    pygame.draw.circle(screen, DARK_GRAY, (CENTER_X, CENTER_Y), 50)
    # 内层浅色
    pygame.draw.circle(screen, GRAY, (CENTER_X, CENTER_Y), 45)

    # --- 3. 绘制眼睛 (眼眶 + 随动眼珠) ---
    # 眼睛参数
    eye_left_center = (385, 390)
    eye_right_center = (415, 390)
    eye_width = 10
    eye_height = 16
    pupil_max_offset = 4  # 眼珠最大移动半径

    # 计算眼珠实时位置
    lp_x, lp_y = get_pupil_position(eye_left_center[0], eye_left_center[1], mouse_pos, pupil_max_offset)
    rp_x, rp_y = get_pupil_position(eye_right_center[0], eye_right_center[1], mouse_pos, pupil_max_offset)

    # 绘制左眼眼眶 (椭圆更像生物)
    left_eye_rect = pygame.Rect(eye_left_center[0] - 5, eye_left_center[1] - 8, eye_width, eye_height)
    pygame.draw.ellipse(screen, BLACK, left_eye_rect)

    # 绘制右眼眼眶
    right_eye_rect = pygame.Rect(eye_right_center[0] - 5, eye_right_center[1] - 8, eye_width, eye_height)
    pygame.draw.ellipse(screen, BLACK, right_eye_rect)

    # 绘制左眼珠 (白色，跟随鼠标)
    pygame.draw.circle(screen, WHITE, (int(lp_x), int(lp_y)), 3)

    # 绘制右眼珠
    pygame.draw.circle(screen, WHITE, (int(rp_x), int(rp_y)), 3)

    # --- 4. 绘制嘴巴 (根据状态切换) ---
    mouth_rect = (380, 415, 40, 20)  # (x, y, w, h)

    if is_angry:
        # 愤怒嘴巴：向下的弧线 (红色)
        # start_angle=0 (右边), end_angle=180 (左边) -> 画上半圆看起来像皱眉，或者反过来
        # 这里画一个倒 U 型表示愤怒
        pygame.draw.arc(screen, (255, 0, 0), mouth_rect,
                        math.radians(0), math.radians(180), 5)

        # 可选：添加愤怒的眉毛
        pygame.draw.line(screen, BLACK, (380, 385), (395, 392), 3)
        pygame.draw.line(screen, BLACK, (420, 385), (405, 392), 3)

    else:
        # 微笑嘴巴：向上的弧线 (黑色)
        # start_angle=180 (左边), end_angle=360 (右边) -> 画下半圆
        pygame.draw.arc(screen, BLACK, mouth_rect,
                        math.radians(180), math.radians(360), 5)


def draw_TrashDigger():
    #外圈，会缩放
    DARK_BROWN=(50,25,0)
    BROWN=(56,31,7)
    pygame.draw.circle(screen, BLACK, (400, 400), 65,5)
    #身体
    pygame.draw.circle(screen, DARK_BROWN, (400, 400), 50)
    pygame.draw.circle(screen, BROWN, (400, 400), 45)
    #眼框
    pygame.draw.ellipse(screen, BLACK, (380, 370, 15,25 ))
    pygame.draw.ellipse(screen, BLACK, (410, 370, 15,25 ))
    #眼珠（随方向运动，但是不超出眼框）
    pygame.draw.circle(screen, WHITE, (385, 380), 3)
    pygame.draw.circle(screen, WHITE, (415, 380), 3)
    #眼睛（愤怒）
    pygame.draw.polygon(screen, BLACK, ((385, 355), (385, 380), (400, 380), (400, 370),(390, 355)))
    pygame.draw.polygon(screen, BLACK, ((405, 370), (405, 380), (420, 380), (420, 355),(415, 355)))
    #2个嘴巴看情况使用，只使用一个
    #嘴巴（微笑---在没有锁定生物的时候）
    pygame.draw.arc(screen, DARK_BROWN, (380, 410, 40, 20),
                    math.radians(200), math.radians(360), 5)
    #嘴巴2（愤怒---在锁定生物和攻击时候）
    pygame.draw.arc(screen, DARK_BROWN, (380, 410, 40, 20),
                    math.radians(360), math.radians(200), 5)
def draw_manhole():
    DEEP_BROWN=(81,55,20)
    #边缘
    DARK_GRAY=(100,100,100)
    GRAY=(160,160,160)
    DARK_BROWN=(105,71,26)
    BROWN=(135,81,21)
    pygame.draw.circle(screen, DARK_GRAY, (400, 400), 50)
    pygame.draw.circle(screen, GRAY, (400, 400), 45)
    #内部
    pygame.draw.circle(screen, DARK_BROWN, (400, 400), 35)
    pygame.draw.circle(screen, BROWN, (400, 400), 30)
    pygame.draw.circle(screen, DARK_BROWN, (400, 400), 15)
    pygame.draw.circle(screen, DEEP_BROWN, (400, 400), 10)


def main():
    clock = pygame.time.Clock()
    running = True
    animation_timer = 0
    rotation = 0

    # ⭐ 修改这里：不要叫 screen，改叫 display_surface
    display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # ⭐ 修改这里：使用新的变量名清屏
        display_surface.fill(BACKGROUND)

        animation_timer += 0.05
        rotation += 1.4
        if rotation >= 360:
            rotation -= 360

        # ⭐ 修改这里：把 display_surface 传给 draw_Digger
        # 注意：你的 draw_Digger 定义需要接收 surface 参数
        draw_TrashDigger()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()