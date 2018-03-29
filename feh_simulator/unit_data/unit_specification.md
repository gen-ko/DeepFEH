Use blank space explicitly to tell the parser which is property name and
its corresponding values.

All property names are lower-cased,
values are either integer or upper-cased skill names,
if there are non-ASCII characters encountered in skill name, 
there might be problems in parsing, the authors are working a 
proper solution on this.

For now, the input order matters, so please follow the pattern below.

An example of an unit.txt file:

    max_hp = 40
    atk = 30
    spd = 36
    def = 25
    res = 26
    movement_type = INFANTRY
    weapon = NONE
    support = NONE
    special = NONE
    passive_a = CANCEL_AFFINITY_1
    passive_b = NONE
    passive_c = NONE
    passive_s = NONE