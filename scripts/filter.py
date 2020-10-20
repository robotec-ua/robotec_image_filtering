#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge
import numpy as np
import threading

class Node():
    def __init__(self):
        # Get ROS parameters
        self._publish_rate = rospy.get_param('~publish_rate', 100)
        lower_color_boundary = rospy.get_param('~lower_color_boundary')
        upper_color_boundary = rospy.get_param('~upper_color_boundary')
        self._box_color = rospy.get_param('~box_color')
        self._toVisualize = rospy.get_param('~visualization')
            
        # Create ROS topics
        self._result_pub = rospy.Publisher('~filtered_image', Image, queue_size=1)
        self._visual_pub = rospy.Publisher('~visualization', Image, queue_size=1)
        self._camera_input = rospy.Subscriber('~input', Image,
                                 self.imageCallback, queue_size=1)

        # Create multitreading locks
        self._last_msg = None
        self._msg_lock = threading.Lock()

        # Set range for the color
        self._lower = np.array(lower_color_boundary, np.uint8) 
        self._upper = np.array(upper_color_boundary, np.uint8) 

    def __createMask(hsvFrame) :
        # Obtain masks for colored objects
        mask = cv2.inRange(hsvFrame, self._lower, self._upper)
        kernal = np.ones((5, 5), "uint8")
        mask = cv2.dilate(mask, kernal)

        return mask

    def __drawBoxes(np_image, contours) : 
        for pic, contour in enumerate(contours): 
            area = cv2.contourArea(contour) 

            # Draw only big boxes
            if (area > 500): 
                # Get the coordinates of the box
                x, y, w, h = cv2.boundingRect(contour)

                # Draw the box
                np_image = cv2.rectangle(np_image, (x, y),  
                    (x + w, y + h),
                    self._box_color, 2)

        return np_image

    def __detect_colors(np_image) : 
        # If the message is not empty
        if msg is not None:
            hsvFrame = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)

            # Create the mask
            mask = __createMask(hsvFrame)

            # Create contours for the object
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            return contours 

    def imageCallback(self, msg):
        if self._msg_lock.acquire(False):
            self._last_msg = msg
            self._msg_lock.release()

    def run(self):
        rate = rospy.Rate(self._publish_rate)   # Rate of the main loop
        cv_bridge = CvBridge()                  #

        while not rospy.is_shutdown():
            # If there is no lock on the message (not being written to in the moment)
            if self._msg_lock.acquire(False):
                msg = self._last_msg
                self._last_msg = None
                self._msg_lock.release()
            else:
                rate.sleep()
                continue

            # Convert the message to an OpenCV object
            np_image = cv_bridge.imgmsg_to_cv2(msg, 'bgr8')

            # Get the contours of the objects
            contours = __detect_colors(np_image)

            # IF there are detected objects
            if (len(contours) != 0) :
                # Send the message
                self._result_pub.publish(msg)
                
                # If the option of visualization is enabled
                if (self._toVisualize) :
                    # Draw the boxes over the original image
                    np_image = __drawBoxes(np_image, mask)

                    # Send the redrawn image
                    redrawn_image = cv_bridge.cv2_to_imgmsg(np_image, 'bgr8')
                    self._visual_pub.publish(redrawn_image)
                    

def main():
    # Create a ROS node
    rospy.init_node('image_filtering')

    # Start the program
    node = Node()
    node.run()

if __name__ == '__main__':
    main()
