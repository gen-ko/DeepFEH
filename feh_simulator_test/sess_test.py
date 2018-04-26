
from feh_simulator.session import  Session



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
print(s.__len__())