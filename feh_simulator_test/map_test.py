from feh_simulator.unit import Unit

from feh_simulator.map import Map

m = Map('../feh_simulator/map_data/map_01.txt')
m.render()
u = Unit(team=0, unit_file='../feh_simulator/unit_data/unit_default.txt')
u.render()
m.register_unit(u, x=0, y=0)



m.render()

r = m.get_reachable_locations(u)
print(r)
u2 = Unit(team=0, unit_file='../feh_simulator/unit_data/unit_default.txt')

m.register_unit(u2, x=0, y=1)

m.render()
r = m.get_reachable_locations(u)
r2 = m.get_reachable_locations(u2)
print(r)
print(r2)

