import os
import sys
import optparse
from sumolib import checkBinary
import traci
import api
import reinforcement as RL
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
    lane = [['gneE3_0', 'gneE3_1'], ['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
            ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
    init = [15, 15, 15]  
    rl = RL.TrafficLight(init,lane)
    rl.InitStateSpace()

    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')


    # temp = rl.P_Greedy_Al()
    # print(temp)

    traci.start([sumoBinary, "-c", "4cross_TLS/1_1Cross.sumocfg"])
    while traci.simulation.getMinExpectedNumber() > 0:
        rl.Find_Q_initState()
        traci.simulationStep()
    traci.close()
    
    # # temp = rl.Greedy_Al()
    # # print(temp)