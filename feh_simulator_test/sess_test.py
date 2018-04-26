from feh_simulator.unit import Unit

from feh_simulator.map import Map

from feh_simulator.session import  Session

m = Map('../feh_simulator/map_data/map_01.txt')
m.render()
u = Unit(team=0, unit_file='../feh_simulator/unit_data/unit_default.txt')
u.render()
m.register_unit(u, x=0, y=0)


sess = Session(map_file='../feh_simulator/map_data/map_01.txt', 
               unit_files=['../feh_simulator/unit_data/unit_default.txt',
                           '../feh_simulator/unit_data/unit_default.txt',
                           '../feh_simulator/unit_data/unit_default.txt',
                           '../feh_simulator/unit_data/unit_default.txt',
                           '../feh_simulator/unit_data/unit_default.txt',
                           '../feh_simulator/unit_data/unit_default.txt',
                           '../feh_simulator/unit_data/unit_default.txt',
                           '../feh_simulator/unit_data/unit_default.txt'],
               unit_teams=[1, 1, 1, 1, 2, 2, 2, 2])


s = sess.current_state()

print(s)
