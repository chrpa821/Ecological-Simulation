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
myWin = cmds.window(
    title="Plant Distributions in Natural Scenes", menuBar=True)

cmds.frameLayout(collapsable=True, label="Create world")

# Create a new Scene
cmds.button(label="New Scene", command='new_scene()')

# user set width and length
cmds.intSliderGrp('input_width', label="Width",
                  field=True, min=5, max=100, value=50)
cmds.intSliderGrp('input_length', label="Length",
                  field=True, min=5, max=100, value=50)

# Create new terrain
cmds.button(label="Create New Terrain", command='create_plane()')

# Delete selected object
cmds.button(label="Delete Selected Object", command='cmds.delete()')

cmds.showWindow(myWin)

##############
#   GLOBALS  #
##############

# initializing globals for access in all functions
mesh_name = ""
mesh_width = 0
mesh_length = 0

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

    # Create a polygonal mesh
    global mesh_name
    mesh_name = "worldMesh"
    cmds.polyPlane(width=mesh_width, height=mesh_length, name=mesh_name)


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
  def __init__(self, TreeInfo, treeList[], soilValue):
    self.plantInfo = plantInfo
    self.plantArray = plantArray
    self.soilValue = soilValue




