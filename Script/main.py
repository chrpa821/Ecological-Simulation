# Import libraries
import maya.cmds as cmds
import random
import math

# Remove old UI
if 'myWin' in globals():
    if cmds.window("myWin", exists=True):
        cmds.deleteUI("myWin", window=True)

##############
#   New UI   #
##############
myWin = cmds.window(title="Plant Distributions in Natural Scenes", menuBar=True)

### Create new World ###
cmds.frameLayout(collapsable=True, label="Create world")

# Create a new Scene
cmds.button(label="New Scene", command='new_scene()')

# user set width and length
cmds.intSliderGrp('input_width', label="Width", field=True, min=5, max=100, value=50)
cmds.intSliderGrp('input_length', label="Length", field=True, min=5, max=100, value=50)

# user set subdivisions
cmds.intSliderGrp('input_sub', label="Number of Subdivisions", field=True, min=5, max=100, value=50)

# Create new terrain
cmds.button(label="Create New Terrain", command='create_plane()')

# Delete selected object
cmds.button(label="Delete Selected Object", command='cmds.delete()')

cmds.setParent('..')
cmds.setParent('..')

### Set environment ###

cmds.frameLayout(collapsable=True, label="Set environment")

# user set environmental factors
cmds.intSliderGrp('input_age', label="Age", field=True, min=1, max=100, value=50)
cmds.intSliderGrp('input_temp', label="Temperature", field=True, min=-10, max=40, value=10)
cmds.floatSliderGrp('input_', label="light", field=True, min=0, max=1, value=0.5)
cmds.floatSliderGrp('input_soil', label="soil", field=True, min=0, max=1, value=0.5)

# create environment
cmds.button(label="Create Environment", command='create_environment')

cmds.showWindow(myWin)

##############
#   GLOBALS  #
##############

# initializing globals for access in all functions
mesh_name = ""
mesh_width = 0
mesh_length = 0
mesh_sub = 0

##################
#    Functions   #
##################


def new_scene():
    cmds.file(force=True, new=True)


def create_plane():
    global mesh_width
    mesh_width = cmds.intSliderGrp('input_width', query=True, value=True)
    global mesh_length
    mesh_length = cmds.intSliderGrp('input_length', query=True, value=True)
    global mesh_sub
    mesh_sub = cmds.intSliderGrp('input_sub', query=True, value=True)

    # Create a polygonal mesh
    global mesh_name
    mesh_name = "worldMesh"
    cmds.polyPlane(sx=mesh_sub, sy=mesh_sub,  w=mesh_width, h=mesh_length, n=mesh_name)


def create_environment():
    global my_environment
    age = cmds.intSliderGrp('input_age', query=True, value=True)
    temp = cmds.intSliderGrp('input_temp', query=True, value=True)
     = cmds.floatSliderGrp('input_', query=True, value=True)
    soil = cmds.floatSliderGrp('input_soil', query=True, value=True)

    my_environment = Environment(age, , temp, soil)
    print(my_environment.age)
    print(my_environment.)
    print(my_environment.temp)
    print(my_environment.soil)


#Generic tree
class TreeInfo:

    def __init__(self):
        self.name = "tree"
        self.energy = 1.0
        self.fitness = 1.0
        self.currentAge = 1
        self.maxAge = 30
        self.reproductionAge = 3
        self.seedCount = 5
        self.temperaturePreferred = 38
        self.temperatureLower = 0
        self.temperatureUpper = 40
        self.sunlightPreferred = 0.9
        self.sunlightLower = 0.3
        self.sunlightUpper = 1.0
        self.soilPreferred = 0.4
        self.soilLower = 0.0
        self.soilUpper = 0.6
        self.spacePreferred = 0.2
        self.spaceLower = 0.0
        self.spaceUpper = 0.3



    def update_fitness(self):
        self.fitness = self.compute_soil_adaptability() * self.compute_sun_adaptability() * self.compute_temperature_adaptability()


    def compute_soil_adaptability(self):

        if self.soilPreferred - 0.5*(
        abs(self.soilPreferred - self.soilLower)) <= my_environment.soil <= self.soilPreferred + 0.5 * (
        abs(self.soilPreferred - self.soilUpper)):
            return 1.0

        elif self.soilPreferred + 0.5*(abs(self.soilPreferred - self.soilUpper)) < my_environment.soil <= self.soilUpper:
            temp = -((1/(
                abs(self.soilUpper - self.soilPreferred + 0.5*abs(self.soilPreferred-self.soilUpper))))*abs(
                my_environment.soil - self.soilPreferred + 0.5*abs(self.soilPreferred - self.soilUpper))) + 1.0
            return temp

        elif self.soilLower <= my_environment.soil < self.soilPreferred - 0.5*abs(self.soilPreferred - self.soilLower):
            temp = -((1/(
                abs(self.soilLower - self.soilPreferred - 0.5*abs(self.soilPreferred-self.soilLower))))*abs(
                my_environment.soil - self.soilPreferred - 0.5*abs(self.soilPreferred - self.soilUpper))) + 1.0
            return temp

        else:
            return 0


    def compute_sun_adaptability(self):
        if self.sunlightPreferred - 0.5 * (
        abs(self.sunlightPreferred - self.sunlightLower)) <= my_environment.sun <= self.sunlightPreferred + 0.5 * (
        abs(self.sunlightPreferred - self.sunlightUpper)):
            return 1.0

        elif self.sunlightPreferred + 0.5 * (
        abs(self.sunlightPreferred - self.sunlightUpper)) < my_environment.sun <= self.sunlightUpper:
            temp = -((1 / (
                abs(self.sunlightUpper - self.sunlightPreferred + 0.5 * abs(self.sunlightPreferred - self.sunlightUpper)))) * abs(
                my_environment.sun - self.sunlightPreferred + 0.5 * abs(self.sunlightPreferred - self.sunlightUpper))) + 1.0
            return temp

        elif self.sunlightLower <= my_environment.sun < self.sunlightPreferred - 0.5 * abs(
                self.sunlightPreferred - self.sunlightLower):
            temp = -((1 / (
                abs(self.sunlightLower - self.sunlightPreferred - 0.5 * abs(self.sunlightPreferred - self.sunlightLower)))) * abs(
                my_environment.sun - self.sunlightPreferred - 0.5 * abs(self.sunlightPreferred - self.sunlightUpper))) + 1.0
            return temp

        else:
            return 0


    def compute_temperature_adaptability(self):
        if self.temperaturePreferred - 0.5 * (
        abs(self.temperaturePreferred - self.temperatureLower)) <= my_environment.sun <= self.temperaturePreferred + 0.5 * (
        abs(self.temperaturePreferred - self.temperatureUpper)):
            return 1.0

        elif self.temperaturePreferred + 0.5 * (
        abs(self.temperaturePreferred - self.temperatureUpper)) < my_environment.sun <= self.temperatureUpper:
            temp = -((1 / (
                abs(self.temperatureUpper - self.temperaturePreferred + 0.5 * abs(self.temperaturePreferred - self.temperatureUpper)))) * abs(
                my_environment.sun - self.temperaturePreferred + 0.5 * abs(self.temperaturePreferred - self.temperatureUpper))) + 1.0
            return temp

        elif self.temperatureLower <= my_environment.sun < self.temperaturePreferred - 0.5 * abs(
                self.temperaturePreferred - self.temperatureLower):
            temp = -((1 / (
                abs(self.temperatureLower - self.temperaturePreferred - 0.5 * abs(self.temperaturePreferred - self.temperatureLower)))) * abs(
                my_environment.sun - self.temperaturePreferred - 0.5 * abs(self.temperaturePreferred - self.temperatureUpper))) + 1.0
            return temp

        else:
            return 0

class Tree:
  def __init__(self, tree_info, tree_list, soil_value):
    self.tree_info = tree_info
    self.tree_list = tree_list
    self.soil_value = soil_value

##################
#    Classes     #
##################

class Environment:
    def __init__(self, age, light, temperature, soil):
        self.age = age
        self.sunlight = light
        self.temperature = temperature
        self.soil = soil # fix soil value based on map

    def update(self):
        print('Add TimeElement to update'.format(self.name))


def increment_age(tree_list):

    for plants in tree_list:
        # Fitness (f = 1.0)
        # Energy (e = 1.0)
        # Increment age (a) every t seconds
        # Check fitness (f) in each cycle
        # If f = 0, reduce energy (e) by energy loss (l)
        # If e = 0, plant dies
        # If probability (p < 0.5), reproduce offspring
        # Reproduction based on fitness:
        # Scatter number of seeds (s * f)
        # at distance (d) around the parent
        plants.age += 1
        if plants.fitness == 0:
            plants.energy -= 0.1 #energy loss = 0.1
        if plants.energy == 0
            #plant dies
        if (random.uniform(0,1) < 0.5)
            #reprodce offspring
            #scatter seeds plants.seeds*plants.fitness at distance d around plant



