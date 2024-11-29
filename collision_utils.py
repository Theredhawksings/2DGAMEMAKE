collision_pairs = {}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]

    if isinstance(a, list):
        collision_pairs[group][0].extend(a)
    elif a:
        collision_pairs[group][0].append(a)

    if isinstance(b, list):
        collision_pairs[group][1].extend(b)
    elif b:
        collision_pairs[group][1].append(b)

    print(f"Collision pair added: {group}, {collision_pairs[group]}")


def collide(a, b):
    if hasattr(a, 'is_invincible') and a.is_invincible:
        return False

    if hasattr(b, 'get_bb') and isinstance(b.get_bb(), list):
        la, ba, ra, ta = a.get_bb()
        for bb in b.get_bb():
            lb, bb_b, rb, tb = bb
            if not (la > rb or ra < lb or ta < bb_b or ba > tb):
                print(f"Collision detected between {a} and {b}")
                print(f"Boy BB: {a.get_bb()}")
                print(f"Obstacle BB: {bb}")
                return True
        return False

    else:
        la, ba, ra, ta = a.get_bb()
        lb, bb, rb, tb = b.get_bb()

        if la > rb: return False
        if ra < lb: return False
        if ta < bb: return False
        if ba > tb: return False

        return True

def handle_collisions():
    any_collision = False
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    print(f"Handling collision for group {group} between {a} and {b}")
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
                    any_collision = True
    return any_collision

def remove_collision_pair(group, a):
    if group in collision_pairs:
        if a in collision_pairs[group][0]:
            collision_pairs[group][0].remove(a)
        if a in collision_pairs[group][1]:
            collision_pairs[group][1].remove(a)
        if not collision_pairs[group][0] and not collision_pairs[group][1]:
            del collision_pairs[group]

def clear_collision_pairs():
   collision_pairs.clear()