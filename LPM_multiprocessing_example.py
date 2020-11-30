# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 16:00:41 2020

@author: Leiden Probe Microscopy B.V.

This software is an example of how the data from a camera can be captured,
filtered/processed, and displayed using openCV, while the work is done on
multiple processes. For this we use the mproc library from LPM, which uses
numpy and the standard multiprocessing module.

mproc provides a function template: general_procedure that is designed to
work smoothly in a flow of video data. The wanted function that needs to be
applied to the datastream must have the form:
    output_frame = some_filter_function(input_frame(optional), other_arguments)
Most filters from the opencv library have this form, so they can be used without 
modification, which makes this example a powerful realtime image manipulation engine.

specify the some_filter_function and its arguments in the procs dictionary below:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Note that dependencies might be published under a license.
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from LPM_image_capture_library import mproc
from LPM_image_capture_library import show

#UNCOMMENT THIS BLOCK FOR A CAMERA WORKING VIA WINDOWS DRIVERS (DIRECTSHOW)
from LPM_image_capture_library import opencv_camera as camera
img_shape = (480,640) #due to initialization of the workers, we need to know the frame size in advance
scale_percentage = 100

#UNCOMMENT THIS BLOCK FOR A THORLABS CAMERA (VIA THORLABS SDK)
# =============================================================================
# from LPM_image_capture_library import thorlabs as camera
# img_shape = (2160,4096) #due to initialization of the workers, we need to know the frame size in advance
# scale_percentage = 20   # scale the image down, just before showing onscreen because it is too big for my monitor
# =============================================================================

data_type = np.uint8 # np.uint8 works with most opencv filters. Some do work in an other format, but some don't. Errors may occur in other format.

# here you can define or redefine image processing functions
def do_nothing(a): return a # can be useful for debuggin the program
def otsu_threshold(frm):
    _, frm = cv2.threshold(frm, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return frm
def normalize_manual(img, lower_boundary, upper_boundary):
    coefficient = 255/(upper_boundary-lower_boundary)
    frame = (img.astype(np.float32)-lower_boundary)*coefficient
    return frame.astype(img.dtype)

# Define process dictionary which specifies the processes for the workers
# 'specify some name': [(0)init_function     , (1)core_function        , (2)close_function     , (3)core_function arguments without input image, (4)name of input image given by the process name where it should retrieve the image from ]
procs = {
         'capture': [camera.open_camera, camera.get_frame_bare, camera.close_camera, ()            , None      ] ,
         'blur': [None              , cv2.GaussianBlur        , None               , ((5,5),0)     , 'capture' ] ,
         'otsu': [None              , otsu_threshold          , None               , ()            , 'blur'    ] ,
         'edge': [None              , cv2.Canny               , None               , (50,150)      , 'blur'    ] ,
        #'norm_man': [None          , normalize_manual        , None               , (100,200)     , 'capture' ] 
        }

def img_hist(frame): # %run '%matplotlib Qt5' in the python console to set that the figures are shown in an external window instead of the Plots window
    fig = plt.figure('LPM Histogram')
    #fig.clf()
    fig.suptitle('Image intensity histogram')
    plt.xlabel('intensity')
    plt.ylabel('# of pixels')
    histr = cv2.calcHist([frame], [0], None, [256], [0, 256], accumulate=False)
    plt.plot(histr)
    #plt.hist(frame.flat,range(max(frame.flat)))
    fig.canvas.draw()

if __name__ == '__main__':
    # The go function in mproc takes the procs dictionary as input and extends the lists in this dictonary so that len(procs['capture or any other proc_name']) = 11. This dictionary basically defines all interconnections between all processes. After that it starts all processes.
    (procs, stop_event) = mproc.go(procs, data_type, img_shape)
    
    # create window
    window_title = show.open_img_window(init_scale_percentage = scale_percentage)
    cv2.createTrackbar('hist', window_title, 0, 1, lambda x: img_hist(next(right_image)))
    
    # create image generators that will give the latest image from the buffer eacht time you run next(left_image). You can change the feed of the buffer with left_image.send(new_proc_name). We run generators after instantiating once to initialize.
    left_image  = mproc.image_from_buf_generator(procs)
    cv2.createTrackbar('left', window_title, 0, len(procs)-1, lambda x: left_image.send( list(procs)[x] ))
    next(left_image)
    right_image = mproc.image_from_buf_generator(procs, list(procs)[-1])
    cv2.createTrackbar('right', window_title, len(procs)-1, len(procs)-1, lambda x: right_image.send( list(procs)[x] ))
    next(right_image)
   
    while not stop_event.is_set():
        continue_show = show.frame([next(left_image), next(right_image)])
        if not continue_show:
            stop_event.set()  
    show.close_windows()