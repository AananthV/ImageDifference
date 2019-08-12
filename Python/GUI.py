import numpy as np
import cv2
import tkinter as tk
import tkinter.filedialog as FileDialog
from PIL import Image, ImageTk
from imagedifference import imageDifference
from coordinatesender import coordinateSender

'''
    Function Name: SelectImage1
    Logic:
        - Selects and loads image1 using tkinter.filedialog and OpenCV
'''
def SelectImage1():
    global img1
    path = FileDialog.askopenfilename()
    if len(path) > 0:
        img1 = cv2.imread(path)
    UpdateImage(img1, img2)

'''
    Function Name: SelectImage2
    Logic:
        - Selects and loads image2 using tkinter.filedialog and OpenCV
'''
def SelectImage2():
    global img2
    path = FileDialog.askopenfilename()
    if len(path) > 0:
        img2 = cv2.imread(path)
    UpdateImage(img1, img2)

'''
    Function Name: findDifferences
    Logic:
        - Finds differences and obtains divisions using imageDifference class.
'''
def findDifferences():
    global img1, img2, divisions, message, imgDiff

    # Check if images exist.
    if img1 is None or img2 is None:
        message.configure(text="Select Images first!")
    else:
        # Find differences.
        _img1, _img2, divisions = imgDiff.findDifferences(img1, img2)

        # Error message if images are not of same dimension.
        if _img1 is None or _img2 is None:
            message.configure(text="Select Images of Equal dimensions!")
        else:
            UpdateImage(_img1, _img2)

'''
    Function Name: glowLed
    Logic:
        - Glows LED on the matrix using the coordinateSender class.
'''
def glowLed():
    global divisions, message, cs
    if len(divisions) == 0:
        message.configure(text="Find differences first!")
    else:
        cs.sendCoords(divisions)

'''
    Function Name: UpdateImage
    Inputs: img1, img2
    Logic:
        - Updates PanelA and PanelB to hold img1 and img2.
'''
def UpdateImage(img1, img2):
    global root, panelA, panelB

    # Check if both images exist.
    if img1 is None or img2 is None:
        return

    # OpenCV stores images in BGR format. Convert to RGB.
    image1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    image2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    # Use PIL to obtain Tkinter format images.
    image1 = Image.fromarray(image1)
    image2 = Image.fromarray(image2)
    image1 = ImageTk.PhotoImage(image1)
    image2 = ImageTk.PhotoImage(image2)

    # Check if panels are un initialised.
    if panelA is None or panelB is None:
        panelA = tk.Label(image=image1)
        panelA.image = image1
        panelA.pack(side="left", padx=10, pady=10)

        panelB = tk.Label(image=image2)
        panelB.image = image2
        panelB.pack(side="right", padx=10, pady=10)
    # If panels are initialised then simply update them.
    else:
        panelA.configure(image=image1)
        panelB.configure(image=image2)
        panelA.image = image1
        panelB.image = image2

# Declare Global Variables.
img1 = None
img2 = None
divisions = None
panelA = None
panelB = None

# initialise gui.
root = tk.Tk(screenName=None, baseName=None, className=' Image Difference', useTk=1)

# Create a imageDifference object.
imgDiff = imageDifference()

# Create a coordinateSender object.
cs = coordinateSender('COM6')

ledButton = tk.Button(root, text="Glow LED!", command=glowLed)
ledButton.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

diffButton = tk.Button(root, text="Find Differences!", command=findDifferences)
diffButton.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

selectFrame = tk.Frame(root)
sbtn1 = tk.Button(selectFrame, text="Select First Image", command=SelectImage1)
sbtn2 = tk.Button(selectFrame, text="Select Second Image", command=SelectImage2)
sbtn1.pack(side="left", fill="both", expand="yes", padx=10, pady=10)
sbtn2.pack(side="left", fill="both", expand="yes", padx=10, pady=10)
selectFrame.pack(side="bottom", fill="both", expand="yes", padx=10)

message = tk.Label(root, text="Select Images and find differences!")
message.pack(side="bottom", padx=10, pady=10)

# Start the GUI.
root.mainloop()
