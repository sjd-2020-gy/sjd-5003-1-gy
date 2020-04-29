'''
Filename: agentframework.py 

Contains: 
- Classes: Agent and Wolf
- Methods (Agent): move, eat, share_with_neighbours, distance_between, 
                   Get<var name> (multiple) and Set<var name> (multiple).
- Methods (Wolf): move, hunt, Get<var name> (multiple) and 
                  Set<var name> (multiple).
'''
import random

#----------------------------------------------------------
# Agent Class
#----------------------------------------------------------
class Agent():
    '''
    Processing of an instance of an Agent.
    '''
    def __init__(self, environment, agents, start_y=None, start_x=None):
        '''
        Initialisation of the Agent instance with:
            - x and y boundary variables
            - plotting colour
            - Store variable
            - Agent number (sequential)
        
        Inputs:
            - environment: Raster data
            - agents: All agents created (ranges from 1 to n)
            - start_y: Default starting y coordinate (may not be supplied)
            - start_x: Default starting x coordinate (may not be supplied)
        '''
        #--------------------------------------------------
        # Initialise variables
        #--------------------------------------------------
        self.environment = environment
        self.agents = agents
        self.y_boundary = len(self.environment) - 1
        self.x_boundary = len(self.environment[0]) - 1
        self.colour = '#' + hex(random.randint(0x000000,0xffffff))[2:].zfill(6)
        self.store = 0
        self.moves = 0
        self.alive = 'Y'
        self.agent_num = len(agents) + 1

        #--------------------------------------------------
        # Boundaries are now known.
        # Randomise starting position of Agent.
        #--------------------------------------------------
        if start_y is None:
            self.y = random.randint(0, self.y_boundary)
        else:
            self.y = start_y
            
        if start_x is None:
            self.x = random.randint(0, self.x_boundary)
        else:
            self.x = start_x
            
           
    def __str__(self):
        '''
        Overriding print string with Agent processing data
        '''
        return 'Agent ' + str(self.agent_num).zfill(3) + \
               ': x=' + str(self.x).zfill(3) + \
               ', y=' + str(self.y).zfill(3) + \
               ', moves=' + str(self.moves) + \
               ', store=' + str(self.store) + \
               ', alive=' + self.alive + '.'


    def move(self):
        '''
        Move the Agent North-East, South-East, South-West or North-West 
        '''
        if random.random() < 0.5:
            self.y = (self.y + 1) % (self.y_boundary + 1)
        else:
            self.y = (self.y - 1) % (self.y_boundary + 1)

        if random.random() < 0.5:
            self.x = (self.x + 1) % (self.x_boundary + 1)
        else:
            self.x = (self.x - 1) % (self.x_boundary + 1)

        self.moves += 1
        
        
    def eat(self): 
        '''
        Nibble at the Environment raster
        '''
        # Allow Agernt to eat a maximum of 10 units or whatever is left
        if self.environment[self.y][self.x] >= 10:
            self.store += 10
            self.environment[self.y][self.x] -= 10

        elif self.environment[self.y][self.x] > 0:
            self.store += self.environment[self.y][self.x]
            self.environment[self.y][self.x] = 0

        # Put back to the environment if Agent has eaten too much
        if self.store > 100:
            self.environment[self.y][self.x] += self.store
            self.store = 0


    def distance_between(self, agent):
        '''
        Calculate the distance between two agents
        '''
        return (((self.y - agent.y)**2) + ((self.x - agent.x)**2))**0.5


    def share_with_neighbours(self, neighbourhood): 
        '''
        Average out the store between two neighbours
        '''
        for agent in self.agents:

            if agent == self or agent.alive == 'N':
                # Do not compare with itself or with a dead agent
                pass 
            else: 
                distance = self.distance_between(agent)
            
                if distance <= neighbourhood:
                    average = (self.store + agent.store) / 2
                    self.store = average
                    agent.store = average
                    self.store + agent.store
        

    #-------------------------------------
    # Get & Set methods
    #-------------------------------------
    @property
    def y(self):
        '''Get the y coordinate'''
        return self._y
            
    @y.setter
    def y(self,val):
        '''Set the y coordinate'''
        self._y = val
            
    @property
    def x(self):
        '''Get the x coordinate'''
        return self._x
            
    @x.setter
    def x(self,val):
        '''Set the x coordinate'''
        self._x = val
            
    @property
    def y_boundary(self):
        '''Get the y axis boundary'''
        return self._y_boundary
            
    @y_boundary.setter
    def y_boundary(self,val):
        '''Set the y axis boundary'''
        self._y_boundary = val
            
    @property
    def x_boundary(self):
        '''Get the x axis boundary'''
        return self._x_boundary
            
    @x_boundary.setter
    def x_boundary(self,val):
        '''Set the x axis boundary'''
        self._x_boundary = val
            
    @property
    def store(self):
        '''Get the Agent store value'''
        return self._store
            
    @store.setter
    def store(self,val):
        '''Set the Agent store value'''
        self._store = val
            
        
#----------------------------------------------------------
# Wolf Class
#----------------------------------------------------------
class Wolf():
    '''
    Processing of an instance of an Wolf.
    '''
    def __init__(self, environment, wolf_pack, start_y=None, start_x=None):
        '''
        Initialisation of the Wolf instance with:
            - x and y boundary variables
            - plotting colour
            - Store variable
        
        Inputs:
            - environment: Raster data
            - wolf_pack: All wolves created (ranges from 1 to n)
            - start_y: Default starting y coordinate (may not be supplied)
            - start_x: Default starting x coordinate (may not be supplied)
        '''
        #--------------------------------------------------
        # Initialise variables
        #--------------------------------------------------
        self.environment = environment
        self.wolf_pack = wolf_pack
        self.y_boundary = len(self.environment) - 1
        self.x_boundary = len(self.environment[0]) - 1
        self.colour = '#' + hex(random.randint(0x000000,0xffffff))[2:].zfill(6)
        self.kills = 0
        self.wolf_num = len(wolf_pack) + 1

        #--------------------------------------------------
        # Boundaries are now known.
        # Randomise starting position of Wolf.
        #--------------------------------------------------
        if start_y is None:
            if self.wolf_num == 1:
                self.y = random.randint(0, self.y_boundary)
            else:
                self.y = wolf_pack[0].y
        else:
            self.y = start_y
            
        if start_x is None:
            if self.wolf_num == 1:
                self.x = random.randint(0, self.x_boundary)
            else:
                self.x = wolf_pack[0].x
        else:
            self.x = start_x
            
           
    def __str__(self):
        '''
        Overriding print string with Wolf processing data
        '''
        return 'Wolf ' + str(self.wolf_num).zfill(3) + \
               ': x=' + str(self.x).zfill(3) + \
               ', y=' + str(self.y).zfill(3) + \
               ', kills=' + str(self.kills) 


    def move(self):
        '''
        Move the Wolf North, East, South or West 
        '''
        where_to = random.random() 
        
        if where_to < 0.25:   # Go North
            self.y = (self.y + 3) % (self.y_boundary + 1)
        elif where_to < 0.5:  # Go East
            self.x = (self.x + 3) % (self.x_boundary + 1)
        elif where_to < 0.75: # Go South
            self.y = (self.y - 3) % (self.y_boundary + 1)
        else:                 # Go West
            self.x = (self.x - 3) % (self.x_boundary + 1)
            
        
    def hunt(self, agents): 
        '''
        Kill the Agent if there first and Agent still alive
        '''
        for agent in agents:
                
            if (agent.alive == 'Y') \
                and (self.y == agent.y) and (self.x == agent.x): 
                self.kills += 1
                
                agent.alive = 'N'
                
                print('Kill -', self) 
            
        
    #-------------------------------------
    # Get & Set methods
    #-------------------------------------
    @property
    def y(self):
        '''Get the y coordinate'''
        return self._y
            
    @y.setter
    def y(self,val):
        '''Set the y coordinate'''
        self._y = val
            
    @property
    def x(self):
        '''Get the x coordinate'''
        return self._x
            
    @x.setter
    def x(self,val):
        '''Set the x coordinate'''
        self._x = val
            
    @property
    def y_boundary(self):
        '''Get the y axis boundary'''
        return self._y_boundary
            
    @y_boundary.setter
    def y_boundary(self,val):
        '''Set the y axis boundary'''
        self._y_boundary = val
            
    @property
    def x_boundary(self):
        '''Get the x axis boundary'''
        return self._x_boundary
            
    @x_boundary.setter
    def x_boundary(self,val):
        '''Set the x axis boundary'''
        self._x_boundary = val
            
    @property
    def kills(self):
        '''Get the Wolf kill value'''
        return self._kill
            
    @kills.setter
    def kills(self,val):
        '''Set the Wolf kill value'''
        self._kill = val
