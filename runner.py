import os
import sys
import optparse
from sumolib import checkBinary
import traci
import api
import reinforcement as RL
import random
import randomTrips

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
    lane = [['gneE3_0', 'gneE3_1'], ['gneE13_0', 'gneE13_1'],
            ['gneE11_0', 'gneE11_1'], ['gneE7_0', 'gneE7_1']]
    initState = [15, 15, 15]
    MAX_EPOCHS = 1000
    EPOCHS = 0
    CYCLE = 132
    TIME = MAX_EPOCHS*CYCLE
    rl = RL.TrafficLight(initState, lane)

    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "4cross_TLS/1_1Cross.sumocfg"])
    rl.InitStateSpace()

    api.add_Route()
    # os.chdir("./4cross_TLS")
    # os.system('python randomTrips.py --net-file=1_1Cross.net.xml --route-file=1_1Cross.rou.xml --weights-prefix=1_1Cross --end='+str(TIME)+' --fringe-factor=10 --period=2.5 --trip-attributes="departLane=\'best\' departSpeed=\'max\' departPos=\'random\'"  -l --validate --fringe-factor 10  --max-distance 2000')

    # for i in range(MAX_EPOCHS):
    while True:
        print("----------------------------- EPOCHS: ",EPOCHS, "-----------------------------")
        rl.P_Greedy_Al()
        rl.updateFuction()
        rl.updateState()
        EPOCHS = EPOCHS+1
        print("----------------------------------------------------------------------")
sys.stdout.flush()
