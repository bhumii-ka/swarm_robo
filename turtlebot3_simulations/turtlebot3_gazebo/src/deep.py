#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def depth_callback(msg):
    bridge = CvBridge()
    try:
        # Convert to depth image
        depth_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # Normalize and display the depth image for visualization
        if depth_image.dtype == 'float32':
            depth_image = (depth_image * 255 / depth_image.max()).astype('uint8')
        elif depth_image.dtype == 'uint16':
            depth_image = (depth_image / 256).astype('uint8')

        cv2.imshow("Depth Map", depth_image)
        cv2.waitKey(1)
    except CvBridgeError as e:
        rospy.logerr(f"Failed to convert depth image: {e}")

if __name__ == "__main__":
    rospy.init_node("depth_map_viewer")
    rospy.Subscriber("/depth_camera/depth/image_raw", Image, depth_callback)
    rospy.spin()
    cv2.destroyAllWindows()
