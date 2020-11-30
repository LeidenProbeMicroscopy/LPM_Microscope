# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 17:59:18 2020

@author: Leiden Probe Microscopy B.V.

This software is an example of how the data from a camera can be captured
and displayed using openCV.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Note that dependencies might be published under a license.
"""
from LPM_image_capture_library import opencv_camera as camera
#from LPM_image_capture_library import thorlabs as camera
cap = camera.open_camera()

from LPM_image_capture_library import show
show.open_img_window()

do_not_quit = True
while do_not_quit:
    do_not_quit, img = camera.get_frame(cap)
    do_not_quit &= show.frame(img)

show.close_windows()  
img_shape = camera.img_shape(cap)
camera.close_camera(cap)
