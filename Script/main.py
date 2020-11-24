# Import libraries
import maya.cmds as cmds
import random
import math
import maya.OpenMaya as OpenMaya

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
cmds.floatSliderGrp('input_sun', label="Sunlight", field=True, min=0, max=1, value=0.5)
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
    sun = cmds.floatSliderGrp('input_sun', query=True, value=True)
    soil = cmds.floatSliderGrp('input_soil', query=True, value=True)

    my_environment = Environment(age, sun, temp, soil)
    print(my_environment.age)
    print(my_environment.sun)
    print(my_environment.temp)
    print(my_environment.soil)


#Generic tree
class TreeInfo:
  def __init__(self):
    self.name = "tree"
    self.energy = 1.0
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


class Tree:
  def __init__(self, tree_info, tree_list, soil_value):
    self.plantInfo = plantInfo
    self.plantArray = plantArray
    self.soilValue = soilValue

##################
#    Classes     #
##################

class Environment:
    def __init__(self, age, sunlight, temperature, soil):
        self.age = age
        self.sunlight = sunlight
        self.temperature = temperature
        self.soil = soil # fix soil value based on map

    def update(self):
        print('Add TimeElement to update'.format(self.name))
