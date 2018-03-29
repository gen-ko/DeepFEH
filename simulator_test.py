from feh_simulator.simulator import Simulator
s = Simulator()
ass = s.reset()
s.map.render()
ass = s.step(ass[2][3][17])
s.map.render()
ass = s.step(ass[2][3][35])
s.map.render()
