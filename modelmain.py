'''
Agent model main processing

Filename: modelmain.py 

Called by:
    - modelhome.py (GUI front-end)
    - Command line
    - Developement IDE

Input:   
    - 9 optional arguments - able to be passed in in any order:
        - agents - Number of Agents
        - defaults - Use default Agent start locations
        - moves - Number of Agent & Wolf moves
        - distance - Distance considered to be a neighbour
        - wolves - Number of wolves in Wolf Pack
        - plotstart - Show starting location of Agents & Wolf Pack
        - dispagents - Display Agent summary data
        - dispwolves - Display Wolf summary data
        - dispparams - Display Parameter Data
      Note: All arguments have a hard coded default value if not supplied.

    - Environment raster file:
        - in.txt
        
Output:
    - Figure
        - Plotted Agent starting locations (dependant on argument passed in)
        - Plotted Wolf Pack starting location (dependant on argument passed in)
        - Plotted Agent finishing locations
        - Plotted Wolf finishing locations
    - Files
        - out1.txt - Modified input raster file
        - out2.txt - Agent finalised store data
        - out3.txt - Wolf finakised kill data
'''
import sys
import csv
import random
import argparse
import matplotlib.lines as lns
import matplotlib.pyplot as plt
import agentframework
import requests
import bs4


#----------------------------------------------------------
# Initialise variables
#----------------------------------------------------------
arg_name = ['--agents', '--defaults', '--moves', '--distance', '--wolves', 
            '--plotstart', '--dispagents', '--dispwolves', '--dispparams']
arg_dflt = ['10', 'N', '100', '20', '5', 'N', 'N', 'N', 'N']
arg_dest = ['num_of_agents', 
            'agent_defaults',
            'num_of_iterations', 
            'neighbourhood', 
            'num_in_wolf_pack',
            'plot_start',
            'display_agents',
            'display_wolves',
            'display_params']
arg_help = ['Number of Agents (numeric)', 
            'Use default Agent start locations (Y/N)',
            'Number of Agent & Wolf moves (numeric)', 
            'Distance considered to be a neighbour (numeric)',
            'Number of wolves in Wolf Pack (numeric)',
            'Show starting location of Agents & Wolf Pack (Y/N)',
            'Display Agent summary data (Y/N)',
            'Display Wolf summary data (Y/N)',
            'Display Parameter Data (Y/N)']
environment = []
agents = []
agents_move = []
agents_eat = []
agents_share = []
wolf_pack = []
wolf_pack_move = []
wolf_pack_hunt = []
num_of_agents_killed = 0


#----------------------------------------------------------
# Get and validate command line arguments
#----------------------------------------------------------
parser = argparse.ArgumentParser()

# Setup arguments
for i in range(len(arg_name)):
    parser.add_argument(arg_name[i], 
                        dest=arg_dest[i], 
                        default=arg_dflt[i], 
                        help=arg_help[i])

# Bring in arguments
args = parser.parse_args()

# Store in a list entered arguments and defaults for those not entered.
# Note: order is important for reasigning back
arg_value = [args.num_of_agents, 
             args.agent_defaults.upper(),
             args.num_of_iterations, 
             args.neighbourhood,
             args.num_in_wolf_pack,
             args.plot_start.upper(),
             args.display_agents.upper(),
             args.display_wolves.upper(),
             args.display_params.upper()]

# Test and finalise arguments
arg_err_count = 0

# Ensure arguments 0, 2, 3 and 4 are an integer and > 0.
# All others are strings and controlled by check and radio buttons (Y / N).
# Note: If a string argument contain anything other than Y or N, then the 
# logic will treat it as a N.
for i in list([0, 2, 3, 4]): 
    if arg_value[i].isnumeric() is True:
        arg_value[i] = int(arg_value[i])
            
        if arg_value[i] < 1:
            print(arg_name[i], arg_value[i], '- Must be an integer and > 0')
            arg_err_count += 1
        else:
            pass
    else:
        print(arg_name[i], arg_value[i], '- Must be an integer and > 0')
        arg_err_count += 1
  
# Abort if any command line errors
if arg_err_count > 0:
    parser.exit('Parameter error - aborting')

# Reasign back
args.num_of_agents, args.agent_defaults, args.num_of_iterations, \
    args.neighbourhood, args.num_in_wolf_pack, args.plot_start, \
    args.display_agents, args.display_wolves, args.display_params = arg_value

if args.display_params == 'Y':
    print('Processed with the following arguments:' + 
          ',\n - No. Agents: ' + str(args.num_of_agents) + 
          ',\n - Use default Agent start locations: ' + args.agent_defaults + 
          ',\n - No. Agent moves: ' + str(args.num_of_iterations) + 
          ',\n - Neighbourhood Distance: ' + str(args.neighbourhood) + 
          ',\n - No. Wolves: '+ str(args.num_in_wolf_pack) + 
          ',\n - Plot starting locations: ' + args.plot_start + '.')

#----------------------------------------------------------
# Read in raster dataset and create environment
#----------------------------------------------------------
f = open('in.txt', newline='')

reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)

try:
    for row_num, row in enumerate(reader): 

        if row_num > 0:
            # Test if the number of cell is the same as previous row
            if len(row) != len(environment[row_num-1]):
                f.close() 
                
                sys.exit('Inconsistent number of cells encountered in row #' +
                         str(row_num+1) + ' of input raster file.')
                
        # Convert each element from float to integer
        environment.append(list(map(lambda row_elem: int(row_elem), row)))
        
except ValueError:
    f.close() 

    sys.exit('Non numerical cell value encountered in row #' + 
             str(row_num+2) + ' of input raster file.')

f.close() 
#----------------------------------------------------------
# At this point, the contents of the raster have 
# been read in and have passed validation.
#----------------------------------------------------------


#----------------------------------------------------------
# Get starting locations for up to 100 agents
#----------------------------------------------------------
if args.agent_defaults == 'Y':
    r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/' + 
                     'practicals/python/agent-framework/part9/data.html')
    content = r.text
    soup = bs4.BeautifulSoup(content, 'html.parser')
    td_ys = soup.find_all(attrs={'class' : 'y'})
    td_xs = soup.find_all(attrs={'class' : 'x'})
else:
    td_ys = []
    td_xs = []


#----------------------------------------------------------
# Create agents
#----------------------------------------------------------
for i in range(args.num_of_agents):
    # create the next Agent instance
    if i+1 > len(td_ys):
        agents.append(agentframework.Agent(environment, agents))
    else:
        agents.append(agentframework.Agent(environment, agents, 
                      int(td_ys[i].text), int(td_xs[i].text))) 
        
    # Because the following functions are going to be called for a dynamic
    # number of times for each Agent, let's label each for effeciency sake. 
    agents_move.append(agents[i].move)
    agents_eat.append(agents[i].eat)
    agents_share.append(agents[i].share_with_neighbours)


#----------------------------------------------------------
# Create wolves
#----------------------------------------------------------

# All wolves will start as a pack at the same location
for i in range(args.num_in_wolf_pack):
    # create the next Wolf instance
    wolf_pack.append(agentframework.Wolf(environment, wolf_pack))

    # Because the following functions are going to be called for a dynamic 
    # number of times for each Wolf, let's label each for effeciency sake. 
    wolf_pack_move.append(wolf_pack[i].move)
    wolf_pack_hunt.append(wolf_pack[i].hunt)


#----------------------------------------------------------
# Now that we have the raster size, set the boundary 
# limits and other mapping attributes
#----------------------------------------------------------
plt.ylim(0, agents[0].y_boundary)
plt.xlim(0, agents[0].x_boundary)
plt.minorticks_on()
plt.copper()
plt.title('Agent Movements\nby Student 201388212')

cross = lns.Line2D([], [], color='Black', marker='x', markersize=5, 
                   linestyle='None')
circle = lns.Line2D([], [], color='Black', marker='o', markersize=5, 
                    linestyle='None')
delta = lns.Line2D([], [], color='Black', marker='v', markersize=5, 
                   linestyle='None')
diamond = lns.Line2D([], [], color='Black', marker='D', markersize=5, 
                     linestyle='None')

agent_legend = plt.legend([cross, circle, delta, diamond],
                          ['Agent Start', 'Agent End', 
                           'Wolf Start', 'Wolf End'], 
                          loc = 'center left', 
                          bbox_to_anchor = (-0.5, 0.5))
    
plt.fig = plt.figure(1)
plt.fig.set_size_inches(10, 6)
plt.fig.subplots_adjust(top=0.9)
plt.fig.savefig('legend_test.png', bbox_extra_artists=(agent_legend))


#----------------------------------------------------------
# If plotting the start locations of each Agent & Wolf is
# required, then plot each 
# - Agent location with an 'x' and its allocated colour
# - Wolf location with a white triangle (All wolves start
#   at the same location then split up).
#----------------------------------------------------------
if args.plot_start == 'Y':
    for agent in agents:
        plt.scatter(agent.x, agent.y, marker='x', color=agent.colour)
        
        if args.display_agents == 'Y':
            print('Start -', agent) 

    for wolf in wolf_pack:
        # Only need to plot once as the wolves start as a pack
        if wolf.wolf_num == 1:
            plt.scatter(wolf.x, wolf.y, marker='v', color='white')
        
        if args.display_wolves == 'Y':
            print('Start -',  wolf) 


#----------------------------------------------------------
# Move the agents and wolves (j times each)
#----------------------------------------------------------
for j in range(args.num_of_iterations):
    if args.num_of_agents > num_of_agents_killed:
        # Randomly shuffle the Agents before next iteration of moves
        random.shuffle(agents)
        random.shuffle(wolf_pack)
    
        for agent in agents: 
            if agent.alive == 'Y':
                # Use agent.agent_num as index as the agents_move, agents_eat
                # and agents_share lists were not randomly shuffled.
            
                # Move 1 raster cell
                agents_move[agent.agent_num-1]()   
        
                # Eat at new location
                agents_eat[agent.agent_num-1]()
        
                # Interact with neighbours if there is more than 1 Agent
                if args.num_of_agents > 1:
                    agents_share[agent.agent_num-1](args.neighbourhood)
            
        num_of_agents_killed = 0

        for wolf in wolf_pack:
            # Use wolf.wolf_num as index as the wolf_pack_move and
            # wolf_pack_hunt lists were not randomly shuffled.

            # Move 3 raster cells
            wolf_pack_move[wolf.wolf_num-1]()
        
            # let the wolf kill the Agent if at the same location
            wolf_pack_hunt[wolf.wolf_num-1](agents)
        
            # accumulate wolf pack kills
            num_of_agents_killed += wolf.kills
    else:
        # That is it!  All the Agent are dead.  No use carrying on!
        break

            
#----------------------------------------------------------
# Plot each Agent finishing location with a cirle using 
# the same colour that was used to plot the Agent starting 
# location
#----------------------------------------------------------
for agent in agents:
    plt.scatter(agent.x, agent.y, marker='o', color=agent.colour)
        
    if args.display_agents == 'Y':
        print('Finish -', agent) 
    

#----------------------------------------------------------
# Plot each Wolf finishing location with a white diamond
#----------------------------------------------------------
for wolf in wolf_pack:
    plt.scatter(wolf.x, wolf.y, marker='D', color='white')
        
    if args.display_wolves == 'Y':
        print('Finish -', wolf) 
    

#----------------------------------------------------------
# Display finalised environment and plotting
#----------------------------------------------------------
plt.imshow(environment)
plt.colorbar()
plt.show()


#----------------------------------------------------------
# Output datasets
# - out1.txt - environment raster data
# - out2.txt - Agent store data
# - out3.txt - Wolf data
#----------------------------------------------------------
f1 = open('out1.txt', 'w', newline='')
f2 = open('out2.txt', 'a', newline='')
f3 = open('out3.txt', 'a', newline='')

output1 = csv.writer(f1, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
output2 = csv.writer(f2, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
output3 = csv.writer(f3, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

for row in environment: 
    # Round as integer (to match input) finalised cells and output
    output1.writerow(list(map(lambda row_elem: round(row_elem), row)))

# Round to 2 decimal places finalised stores
output2.writerow([round(agent.store,2) for agent in agents])
output3.writerow([wolf.kills for wolf in wolf_pack])

f1.close() 
f2.close() 
f3.close() 

