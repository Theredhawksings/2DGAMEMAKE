

def check_collision(boy, obstacle_x, obstacle_y, angle_index):
    boy_left, boy_bottom, boy_right, boy_top = boy.get_bb()

    if angle_index == 0 or angle_index == 2:  # 위쪽 또는 아래쪽
        obstacle_left = obstacle_x + 15
        obstacle_right = obstacle_x + 17
        obstacle_bottom = obstacle_y
        obstacle_top = obstacle_y + 20

    else:  # 왼쪽 또는 오른쪽으로 90도 회전
        obstacle_left = obstacle_x
        obstacle_right = obstacle_x + 25
        obstacle_bottom = obstacle_y + 10
        obstacle_top = obstacle_y + 20

    if boy_right < obstacle_left: return False
    if boy_left > obstacle_right: return False
    if boy_top < obstacle_bottom: return False
    if boy_bottom > obstacle_top: return False

    collision_direction = ""

    if boy_right >= obstacle_left and boy_left < obstacle_left:
        collision_direction = "왼쪽"
    elif boy_left <= obstacle_right and boy_right > obstacle_right:
        collision_direction = "오른쪽"
    elif boy_top >= obstacle_bottom and boy_bottom < obstacle_bottom:
        collision_direction = "아래쪽"
    elif boy_bottom <= obstacle_top and boy_top > obstacle_top:
        collision_direction = "위쪽"

    print(
        f"충돌 감지: 소년({boy_left}, {boy_bottom}, {boy_right}, {boy_top}), "
        f"장애물({obstacle_left}, {obstacle_bottom}, {obstacle_right}, {obstacle_top}), "
        f"방향: {angle_index}, 충돌 방향: {collision_direction}"
    )

    return True

def handle_collision(boy):
    boy.x = boy.savepointX
    boy.y = boy.savepointY
    boy.is_jumping = False
    boy.jump_speed = 0
    boy.falling = False
    print(f'충돌 발생! 세이브포인트로 이동: x={boy.x}, y={boy.y}')