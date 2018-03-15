
from unit import Unit
import skill

def attack(a: Unit, b: Unit):
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

def compute_damage(a: Unit, b: Unit):
    atk = a.atk
    adv = compute_adv(a, b)
    mit = 0.0
    if a.damage_type == 0:
        mit = b.defence
    elif a.damage_type == 1:
        mit = b.res
    dmg = atk + round(adv * atk) - mit
    return round(dmg)

def compute_adv(a: Unit, b: Unit):
    """
    Compute weapon-type advantage factor
    :param a: Unit, the unit initializes attack
    :param b: Unit, the unit being attacked
    :return: float, the adv factor
    """
    adv = skill.COLOR_ADVANTAGE[(a.color, b.color)]

    adv_2 = 0.0
    if a.passive_a == skill.PassiveA.TRIANGLE_ADEPT_1:
        adv_2 = 0.1
    elif a.passive_a == skill.PassiveA.TRIANGLE_ADEPT_2:
        adv_2 = 0.15
    elif a.passive_a == skill.PassiveA.TRIANGLE_ADEPT_3:
        adv_2 = 0.2

    adv_3 = 0.0
    if a.weapon == skill.Weapon.RUBY_SWORD_PLUS or a.weapon == skill.Weapon.SAPPHIRE_LANCE_PLUS or \
        a.weapon == skill.Weapon.EMERALD_AXE_PLUS:
        adv_3 = 0.2

    if a.passive_b == skill.PassiveB.CANCEL_AFFINITY_1:
        return adv

    if a.passive_b == skill.PassiveB.CANCEL_AFFINITY_2:
        return adv

    if a.passive_b == skill.PassiveB.CANCEL_AFFINITY_3:
        return adv

    if a.weapon in skill.RAVEN_TOMES:
        return

    adv_4 = max(adv_2, adv_3)
    if adv < 0.0:
        adv_4 = -adv_4
    elif adv == 0.0:
        adv_4 = 0.0

    return adv + adv_4


def compute_eff(a: Unit, b: Unit):


