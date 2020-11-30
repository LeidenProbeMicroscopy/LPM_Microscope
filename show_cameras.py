# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 13:24:02 2020

@author: Leiden Probe Microscopy B.V.

This script searches for attached cameras and prints their ID

For detecting Thorlabs camera's: the folder 'Python Compact Scientific Camera Toolkit' must be in the same working directory as this .py file!
"""

# FOR DETECTING OTHER CAMERAS USING THE STANDARD DRIVERS
import cv2

def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    for i in range(10):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) # Last flag especcially for directshow driver, remove ', cv2.CAP_DSHOW' to check all builtin drivers for attached cameras
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
    return arr

camera_list = returnCameraIndexes()
print("OpenCV camera ID number(s) detected under standard driver:") 
print(camera_list) # In this list [0] will usually be the default (builtin) camera
print('')



# FOR DETECTING THORLABS CAMERAS
# first find Thorlabs .dll and add to path
import os
import sys

# Setting folder paths: The thorlabs software must know where the dll's are located, so add them to the environ['PATH']
relative_path_to_dlls = '.' + os.sep + 'Python Compact Scientific Camera Toolkit' + os.sep + 'dlls' + os.sep
if sys.maxsize > 2**32:     relative_path_to_dlls += '64_lib'
else:                       relative_path_to_dlls += '32_lib'
os.environ['PATH'] = os.path.abspath(os.path.split(__file__)[0] + os.sep + relative_path_to_dlls) + os.pathsep + os.environ['PATH']
del relative_path_to_dlls

# find available Thorlabs cameras
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK
with TLCameraSDK() as sdk:
    # Find cameras
    Thorlabs_cameras = sdk.discover_available_cameras()
    if len(Thorlabs_cameras) == 0:
        print("No Thorlabs cameras detected!") 
    else:
        print("Thorlabs Camera serial number(s):")
        print(Thorlabs_cameras)
    camera_list = camera_list + Thorlabs_cameras