import cv2
import numpy as np
import math

'''
    Class Name: imageDifference
    - Helper Class for GUI.py which finds the differences between two given images.
'''
class imageDifference:
    '''
        Function Name: equivalence_classes
        Inputs: self, iterable, relation
        Output: class
        Logic:
            - Splits the 'iterable' into equivalance classes on the 'relation'
            - More on Equivalence Classes: https://en.wikipedia.org/wiki/Equivalence_class
        Example Call:
            In this example the Set S = {0, 1, 2, 3, 4} is split into equivalence classes
            on the Relation R = {aRb: (a - b) MOD 2 = 0}
                S = [i for i in range(5)]
                R = lambda i, j: (i - j) % 2 == 0
                EC = self.equivalence_classes(S, R)
            The Equivalence Classes EC so formed are {0, 2, 4} and {1, 3}
    '''
    def equivalence_classes(self, iterable, relation):
        classes = []
        for o in iterable:  # for each object
            # find the class it is in
            found = False
            for c in classes:
                if relation(next(iter(c)), o):  # is it equivalent to this class?
                    c.append(o)
                    found = True
                    break
            if not found:  # it is in a new class
                classes.append([o])
        return classes

    '''
        Function Name: ptDistance
        Inputs: self, pt1, pt2, n
        Output: distance
        Logic:
            - Computes the distace between two 'n' dimensional vectors 'pt1' and 'pt2'
        Example Call:
            To find the distace between the points (3,0) and (0,4) on the 2D Plane
                pt1 = [3, 0]
                pt2 = [0, 4]
                distance = self.ptDistance(pt1, pt2, 2)
            The computed distance = 5.
    '''
    def ptDistance(self, pt1, pt2, n):
        dist = 0
        for i in range(n):
            dist += (pt1[i] - pt2[i])**2
        return dist**0.5

    '''
        Function Name: contourDistance
        Inputs: self, cntCircle1, cntCircle2
                - Here cntCircle is a list containing the (center, radius) of the minEnclosingCircle of the Contour.
        Output: distance
                - Here distance is the absolute distance between the boundaries of the minEnclosingCircles of the respective contours.
        Logic:
                - Distance between two circles is calculated by subtracting both their radii from the distance between their centers.
        Example Call:
            To find the distance between two contours c1 and c2
                distance = self.contourDistance(list(cv2.minEnclosingCircle(c1)), list(cv2.minEnclosingCircle(c2)))
    '''
    def contourDistance(self, cntCircle1, cntCircle2):
        return abs(self.ptDistance(cntCircle1[0], cntCircle2[0], 2) - (cntCircle1[1] - cntCircle2[1]))

    '''
        Function Name: maxContourDistRelation
        Inputs: self, maxDist
        Output: function
                - The Output is a lambda function which accepts two cntCircles (refer contourDistance) returns
                    True if distance between the two contours is less than 'maxDist'
                    False if distance between the two contous is greater than or equal to 'maxDist'
        Example Call:
            To obtain a relation R between two cntCircles a and b such that
                R = {aRb: distance between a and b < maxDist}
            Call as follows;
                R = self.maxContourDistRelation(maxDist)
    '''
    def maxContourDistRelation(self, maxDist):
        return lambda cntCircle1, cntCircle2: self.contourDistance(cntCircle1, cntCircle2) < maxDist

    '''
        Function Name: returnCntCirles
        Inputs: self, contours
                - contours is a list of contours
        Output: cntCircles
                - cntCircles is a list of (center, radius) of circles
        Logic:
                - Retruns a list containing the minEnclosingCircles of a given list of contours.
        Example Call:
            To obtain the minEnclosingCircles of a list of contours C
                cntCircles = self.returnCntCirles(C)
    '''
    def returnCntCirles(self, contours):
        cntCircles = []
        for cnt in contours:
            center, radius = cv2.minEnclosingCircle(cnt)
            cntCircles.append([center, radius])
        return cntCircles

    '''
        Function Name: findRegion
        Inputs: self, contour, height, width, divisionsX, divisionsY
                - height, width: height, width of the image
                - divisionsX, divisionsY: number of divisions to split the image into along the X and Y axes
        Outputs: (divisionX, divisionY)
                - Co-ordinates on the X,Y Plane
        Logic:
                - Given the number of divisions an image is split into along each axis,
                  it finds the division in which the given contour lies.
                - Finds the center of the minEnclosingCircle of the contour and
                  finds the division approximately by finding the division the center lies in
        Example Call:
            To find the region where a contour C lies in a image of dimensions (300, 300)
            split into 3 regions along both axes (total 9 regions).
                (divisionX, divisionY) = self.findRegion(C, 300, 300, 3, 3)
    '''
    def findRegion(self, contour, height, width, divisionsX, divisionsY):
        center, radius = cv2.minEnclosingCircle(contour)
        divisionX = (center[0]*divisionsX)//width
        divisionY = (center[1]*divisionsY)//height
        return math.floor(divisionX), math.floor(divisionY)

    '''
        ### MAIN FUNCTION OF THIS CLASS ###
        Function Name: findDifferences
        Inputs: self, image1, image2
        Outputs: img1, img2, divisions
        Logic:
            - Inputs two images image1 and image2 and finds the differences between them
            - Returns images with rectangles drawn over the differences and the divisions in which the differences lie in
            - Explained in detail along the code.
        Example Call:
            To find the difference between two images.
            img1, img2, divisions = self.findDifferences(img1, img2)
    '''
    def findDifferences(self, image1, image2):
        # Copy images so that the originals aren't modified.
        img1 = image1.copy()
        img2 = image2.copy()

        # Define the number of regions to split the image into.
        divisionsX = 8
        divisionsY = 8

        # Store the Height and Width of the image and calculate the number of divisions
        imageH = img1.shape[0]
        imageW = img1.shape[1]
        divisionXL = imageW//divisionsX
        divisionYL = imageH//divisionsY


        # Return an error message is the dimensions dont match.
        if img2.shape[0] != imageH or img2.shape[1] != imageW:
            return None, None, None

        '''
        -------------
        Preprocessing
        -------------
        '''
        # Find the absolute difference between the two images.
        diff = cv2.absdiff(img1, img2)

        # Convert to Grayscale
        diffBW = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Define a kernel and perform opening.
        kernel = np.ones((4,4))
        opening = cv2.morphologyEx(diffBW, cv2.MORPH_OPEN, kernel)

        # Apply a threshold to finally obtain the mask
        _, mask = cv2.threshold(opening, 10, 255, cv2.THRESH_BINARY)

        # Find the contours on the mask
        contours, heirarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        '''
        ------------
        Cutoff Area
        ------------
        - Remove Very Small Contours as they may be caused by small fluctuations.
        - Differences must atleast have an area of 50 px^2. (Arbitrary).
        ------------
        '''
        cutoffArea = 50
        filteredContours = []
        for cnt in contours:
            if cv2.contourArea(cnt) > cutoffArea:
                filteredContours.append(cnt)
        contours = filteredContours

        '''
        ------------------------------
        Combination of Nearby Contours
        ------------------------------
        '''
        # Obtain the list of minEnclosingCircles of the contours.
        cntCircles = self.returnCntCirles(contours)

        # Combine nearby contours using by finding the equivalence classes of
        # cntCircles on the relation obtained by maxContourDistRelation
        finalContours = self.equivalence_classes(cntCircles, self.maxContourDistRelation(20))
        # finalContours is a list of equivalence classes (lists) containing (center, radius) lists.
        #   Eg: [[[center1, radius1]], [[center2, radius2], [center3, radius3]]]

        # We need to obtain the contours present in each class in finalContours.
        # This is done by finding the index of the circles present in each class in cntCircles.
        # The index of the circle in cntCircles corresponds to the index of the contour in contours.
        # The indices are stored in cnts.
        # Eg: [[1, 2], [0], [3]]
        cnts = []
        for classes in finalContours:
            indices = []
            for cnt in classes:
                indices.append(cntCircles.index(cnt))
            cnts.append(indices)

        '''
        ---------------------------------------------------------
        Draw Rectangles around the differences and find divisions
        ---------------------------------------------------------
        '''
        divisions = []

        # Looping through each equivalence class (their indices).
        for set in cnts:
            # Obtaining the contours corresponding to the indices.
            cntSet = []
            for circle in set:
                    # Convert contours to a list to make addition (concatenation) possible.
                    # Here we want to combine the contours of a class to obtain a single contour.
                    cntSet += list(contours[circle])

            # Convert cntSet into an numpy array to use with OpenCV.
            cntSet = np.array(cntSet)

            # Obtain the rectangle with the minimum area enclosing the contour set.
            rect = cv2.minAreaRect(cntSet)
            box = np.int0(cv2.boxPoints(rect))

            # Draw the recatangles on both images.
            img1 = cv2.drawContours(img1,[box],0,(255, 0, 0),2)
            img2 = cv2.drawContours(img2,[box],0,(255, 0, 0),2)

            # Find the divisions and append to an array.
            divisionX, divisionY = self.findRegion(box, imageH, imageW, divisionsX, divisionsY)
            divisions.append([divisionY, divisionX])

        # Concatenate and combine the two images to obtain side to side differences.
        #finalImage = np.concatenate((img1, img2), axis = 1)

        # Return the images and the divisions.
        return img1, img2, divisions
