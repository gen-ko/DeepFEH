

from unit import Unit


def attack(a: Unit, b: Unit):
    if a.attack_type == 0:
        b.cur_hp -= max(0, (a.atk - b.defence))
    else:
        b.cur_hp -= max(0, (a.atk - b.res))
    if b.cur_hp <= 0:
        b.cur_hp = 0
        b.is_dead = 1
        return

    # counter-attack
    if b.attack_type == 0:
        a.cur_hp -= max(0, (b.atk - a.defence))
    else:
        a.cur_hp -= max(0, (b.atk - a.res))
    if a.cur_hp <= 0:
        a.cur_hp = 0
        a.is_dead = 1
        return

    # follow-attack
    if a.spd >= b.spd + 5:
        if a.attack_type == 0:
            b.cur_hp -= max(0, (a.atk - b.defence))
        else:
            b.cur_hp -= max(0, (a.atk - b.res))
    if b.cur_hp <= 0:
        b.cur_hp = 0
        b.is_dead = 1
        return

    # follow-counter-attack
    if b.spd >= a.spd + 5:
        if b.attack_type == 0:
            a.cur_hp -= max(0, (b.atk - a.defence))
        else:
            a.cur_hp -= max(0, (b.atk - a.res))
    if a.cur_hp <= 0:
        a.cur_hp = 0
        a.is_dead = 1
        return

    return
