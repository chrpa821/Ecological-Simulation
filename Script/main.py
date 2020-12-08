# Import libraries
import maya.cmds as cmds
import random
import maya.OpenMaya as OpenMaya
import pymel.core as pm
import math
import re

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

# Edit terrain
cmds.button(label="Edit Mesh With Tool", command='select_mesh_tool()')

# Delete selected object
cmds.button(label="Delete Selected Object", command='cmds.delete()')

cmds.setParent('..')
cmds.setParent('..')

### Set environment ###

cmds.frameLayout(collapsable=True, label="Create Environment")

# user set environmental factors
cmds.text( label='Plant Mesh name (full name):' )
plant_name = cmds.textField()
cmds.intSliderGrp('input_seeds', label="Amount of Seeds", field=True, min=1, max=50, value=20)
cmds.intSliderGrp('input_age', label="Age", field=True, min=1, max=100, value=50)
cmds.intSliderGrp('input_temp', label="Temperature", field=True, min=-10, max=40, value=38)
cmds.floatSliderGrp('input_sun', label="Sunlight", field=True, min=0, max=1, value=0.9)
cmds.floatSliderGrp('input_soil', label="Soil", field=True, min=0, max=1, value=0.4)

# create environment
cmds.button(label="Create Environment", command='create_environment()')


### Placement of plants  ###

cmds.setParent('..')

cmds.frameLayout(collapsable=True, label="Placement of Plants")

# Increment environment age
cmds.button(label="Increment Environment Age", command='place_objects()')

cmds.showWindow(myWin)

##############
#   GLOBALS  #
##############

# initializing globals for access in all functions
mesh_name = ""
mesh_width = 0
mesh_length = 0
mesh_sub = 0
seeds = 20
tree_list = []

##################
#    Functions   #
##################

def new_scene():
    cmds.file(force=True, new=True)


def select_mesh_tool():
    cmds.SetMeshSculptTool()
    cmds.select(mesh_name, replace=True)


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

    age = cmds.intSliderGrp('input_age', query=True, value=True)
    temp = cmds.intSliderGrp('input_temp', query=True, value=True)
    sun = cmds.floatSliderGrp('input_sun', query=True, value=True)
    soil = cmds.floatSliderGrp('input_soil', query=True, value=True)

    global my_environment # Fix
    my_environment = Environment(age, sun, temp, soil)

    global seeds
    seeds = cmds.intSliderGrp('input_seeds', query=True, value=True)


def increment_age(trees):

    global seeds
    seeds = 0
    for plant in trees[:]:

        plant.update_fitness()
        print(plant.fitness)
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
        plant.age += 1

        if plant.fitness <= 0:
            plant.energy -= 0.6  # energy loss = 0.1

        if plant.energy <= 0:

            cmds.select(plant.instance)
            cmds.delete()
            trees.remove(plant)

        if plant.age >= 38:

            cmds.select(plant.instance)
            cmds.delete()
            trees.remove(plant)

        print(plant.fitness)

        if random.uniform(0, 1) < 0.5:
            seeds += int(plant.seedCount * plant.fitness)


def place_objects():

    cmds.select(mesh_name)
    number_of_faces = cmds.polyEvaluate(f=True)

    # we're comparing with up
    comparisonVector = OpenMaya.MVector(0, 1, 0)

    if len(tree_list) != 0:
        increment_age(tree_list)

    global seeds
    #print(seeds)
    for x in range(seeds):
        place = random.randint(0, number_of_faces)
        face = pm.MeshFace("{}.f[{}]".format(mesh_name, place))

        # check normal of face
        pm.select(face)
        polyInfo = pm.polyInfo(fn=True)
        polyInfoArray = re.findall(r"[\w.-]+", polyInfo[0])  # convert the string to array with regular expression
        polyInfoX = float(polyInfoArray[2])
        polyInfoY = float(polyInfoArray[3])
        polyInfoZ = float(polyInfoArray[4])
        face_normal = OpenMaya.MVector(polyInfoX, polyInfoY, polyInfoZ)

        deltaAngle = math.degrees(face_normal.angle(comparisonVector))

        # the angle is in degrees so the result is
        # "if the difference between this normal and 'up' is more then 20 degrees, turn the point off"
        if abs(deltaAngle) > 10:
            continue

        # Get center of face
        pt = face.__apimfn__().center(OpenMaya.MSpace.kWorld)
        centerPoint = pm.datatypes.Point(pt)


        plant = cmds.textField(plant_name, query=True, text=True)
        cmds.select(plant)
        tree_list.append(TreeInfo(cmds.instance(plant)))
        cmds.move(centerPoint[0], centerPoint[1], centerPoint[2])

        tree_list[-1].update_fitness


##################
#    Classes     #
##################


#Generic tree
class TreeInfo():

    def __init__(self, instance):
        self.energy = 1.0
        self.fitness = 1.0
        self.age = 1
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
        self.instance = instance

    def update_fitness(self):
        global my_environment
        self.fitness = self.compute_adaptability(self.soilPreferred, self.soilLower, self.soilUpper,
                                                 my_environment.soil)\
                       * self.compute_adaptability(self.sunlightPreferred, self.sunlightLower, self.sunlightUpper,
                                                   my_environment.sun) \
                       * self.compute_adaptability(self.temperaturePreferred, self.temperatureLower,
                                                   self.temperatureUpper, my_environment.temperature)

    def compute_adaptability(self, preferred, lower, upper, environment):

        if preferred - 0.5*(abs(preferred - lower)) <= environment <= preferred + 0.5 * (abs(preferred - upper)):
            return 1.0

        elif preferred + 0.5*(abs(preferred - upper)) < environment <= upper:
            temp = -((1/(
                abs(upper - preferred + 0.5*abs(preferred - upper))))*abs(
                environment - preferred + 0.5*abs(preferred - upper))) + 1.0
            return temp

        elif lower <= environment < preferred - 0.5*abs(preferred - lower):
            temp = -((1/(
                abs(lower - preferred - 0.5*abs(preferred - lower))))*abs(
                environment - preferred - 0.5*abs(preferred - upper))) + 1.0
            return temp

        else:
            return 0


class Trees:
    
    def __init__(self, tree_info, tree_list, soil_value):
        self.tree_info = tree_info
        self.tree_list = tree_list
        self.soil_value = soil_value


class Environment:
    def __init__(self, age, light, temperature, soil):
        self.age = age
        self.sun = light
        self.temperature = temperature
        self.soil = soil # fix soil value based on map

    def update(self):
        print('Add TimeElement to update'.format(self.name))

