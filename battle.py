

import unit
import skill

def attack(a: unit.Unit, b: unit.Unit):
    if a.damage_type == 0:
        b.cur_hp -= max(0, (a.atk - b.defence))
    else:
        b.cur_hp -= max(0, (a.atk - b.res))
    if b.cur_hp <= 0:
        b.cur_hp = 0
        b.is_dead = 1
        return

    # counter-attack
    if b.damage_type == 0:
        a.cur_hp -= max(0, (b.atk - a.defence))
    else:
        a.cur_hp -= max(0, (b.atk - a.res))
    if a.cur_hp <= 0:
        a.cur_hp = 0
        a.is_dead = 1
        return

    # follow-attack
    if a.spd >= b.spd + 5:
        if a.damage_type == 0:
            b.cur_hp -= max(0, (a.atk - b.defence))
        else:
            b.cur_hp -= max(0, (a.atk - b.res))
    if b.cur_hp <= 0:
        b.cur_hp = 0
        b.is_dead = 1
        return

    # follow-counter-attack
    if b.spd >= a.spd + 5:
        if b.damage_type == 0:
            a.cur_hp -= max(0, (b.atk - a.defence))
        else:
            a.cur_hp -= max(0, (b.atk - a.res))
    if a.cur_hp <= 0:
        a.cur_hp = 0
        a.is_dead = 1
        return

    return

def compute_damage(a: unit.Unit, b: unit.Unit):
    atk = a.atk
    if a.damage_type == 0:
        mit = b.defence
    elif a.damage_type == 1:
        mit = b.res


def compute_adv(a: unit.Unit, b: unit.Unit):
    """
    Compute weapon-type advantage factor
    :param a: Unit, the unit initializes attack
    :param b: Unit, the unit being attacked
    :return: float, the adv factor
    """
    adv = 0.0
    if a.color == unit.Color.RED:
        if b.color == unit.Color.GREEN:
            adv += 0.2
            if a.skill_a == skill.PassiveA.TRIANGLE_ADEPT_1:
                adv += 0.1
            elif a.skill_a == skill.PassiveA.TRIANGLE_ADEPT_2:
                adv += 0.15
            elif a.skill_a == skill.PassiveA.TRIANGLE_ADEPT_3:
                adv += 0.2
            elif a.skill_weapon == skill.Weapon.RUBY_SWORD:
                adv += 0.2
        elif b.color == unit.Color.BLUE:
            adv -= 0.2
            if a.skill_a == skill.PassiveA.TRIANGLE_ADEPT_1:
                adv -= 0.1
            elif a.skill_a == skill.PassiveA.TRIANGLE_ADEPT_2:
                adv -= 0.15
            elif a.skill_a == skill.PassiveA.TRIANGLE_ADEPT_3:
                adv -= 0.2
            elif a.skill_weapon == skill.Weapon.RUBY_SWORD:
                adv -= 0.2
    return adv


