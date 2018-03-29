from unit import Unit

from feh_simulator.map import Map

units = [Unit(i, int(i / 4)) for i in range(8)]
m = Map(8, 6, units)
m.render()

# # test get_distance
# print(m.get_distance(units[0], units[1]))
# print(m.get_distance(units[0], units[4]))
# print(m.get_distance(units[0], units[7]))

# test get_enemies
# print([i for i in range(8) if units[i] in m.get_enemies(units[1])])
# print([i for i in range(8) if units[i] in m.get_enemies(units[7])])

# test action
# print(m.action(Action(units[3], [2, 3], None)))
# m.render()
# print(m.action(Action(units[3], [2, 3], units[7])))
m.render()
ass = m.get_action_space(units[3])
print(ass[2])
m.action(ass[2])
m.render()

ass = m.get_action_space(units[3])
print(ass[2])
m.action(ass[2])
m.render()

# # get action
# for act in m.get_action_space(units[3]):
#     print(act)

# test location
# x, y = m.get_locations()
# print(x)
# print(y)
