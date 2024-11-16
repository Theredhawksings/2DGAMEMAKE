collision_pairs = {}

def add_collision_pair(group, a, b):
   if group not in collision_pairs:
       collision_pairs[group] = [[], []]
   if a:
       collision_pairs[group][0].append(a)
   if b:
       collision_pairs[group][1].append(b)


def collide(a, b):
    if a.is_invincible:
        return False

    if isinstance(b.get_bb(), list):
        la, ba, ra, ta = a.get_bb()
        for bb in b.get_bb():
            lb, bb_b, rb, tb = bb
            if not (la > rb or ra < lb or ta < bb_b or ba > tb):
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
   for group, pairs in collision_pairs.items():
       for a in pairs[0]:
           for b in pairs[1]:
               if collide(a, b):
                   a.handle_collision(group, b)
                   b.handle_collision(group, a)
                   return True


def clear_collision_pairs():
   collision_pairs.clear()