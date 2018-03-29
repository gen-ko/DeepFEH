from feh_simulator.unit import Unit

from feh_simulator.map import Map

m = Map('../feh_simulator/map_data/map_default.txt')
m.render()
u = Unit(team=0, x=0, y=0, unit_file='../feh_simulator/unit_data/unit_default.txt')
u.render()
m.register_unit(u, x=0, y=0)

m.render()