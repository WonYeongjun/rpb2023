# rpb2023

## overview

This is project repo for team 13

# for qualifying round
# !/usr/bin/env python3
import rospy
import numpy as np
import cv2

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0

    def callback(self, data):
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            cv2.imshow('Image', image)
            cv2.waitKey(1)
            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP

            # determine background color
            # TODO
            # 이미지 읽어오기
            #img = cv2.imread('image.jpg')

	    # 이미지의 가로, 세로 길이 구하기
            height, width = image.shape[:2]

            # 이미지 전처리
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            canny = cv2.Canny(blur, 50, 150)

	    # 경계선 검출
            contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	    # 다각형 근사화
            max_area = 0
            max_contour = None
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    max_contour = contour

            approx = cv2.approxPolyDP(max_contour, 0.02 * cv2.arcLength(max_contour, True), True)

	    # 다각형 그리기
            cv2.drawContours(image, [approx], -1, (0, 0, 255), 3)

	    # 액자 내부 픽셀 분류
            mask = np.zeros((height, width), np.uint8)
            cv2.drawContours(mask, [approx], -1, (255, 255, 255), -1)
            red_mask = cv2.inRange(image, (0, 0, 50), (150, 150, 255))
            blue_mask = cv2.inRange(image, (50, 0, 0), (255, 150, 150))
            other_mask = cv2.bitwise_not(red_mask | blue_mask)
            red_pixels = cv2.countNonZero(cv2.bitwise_and(mask, red_mask))
            blue_pixels = cv2.countNonZero(cv2.bitwise_and(mask, blue_mask))
            other_pixels = cv2.countNonZero(cv2.bitwise_and(mask, other_mask))

	    # 분류 결과 출력
            print('Red Pixels: {}'.format(red_pixels))
            print('Blue Pixels: {}'.format(blue_pixels))
            print('Other Pixels: {}'.format(other_pixels))
            # determine the color and assing +1, 0, or, -1 for frame_id
            # msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)
           
           
            	
            	
            if red_pixels>blue_pixels:
            	if red_pixels>other_pixels:
            	    msg.frame_id='-1'
            	else:
            	    msg.frame_id='0'
            elif red_pixels<blue_pixels:
                if blue_pixels>other_pixels:
                    msg.frame_id='+1'
                else:
                    msg.frame_id='0'
           



            # publish color_state
            self.color_pub.publish(msg)

        except CvBridgeError as e:
            print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    detector = DetermineColor()
    rospy.init_node('CompressedImages1', anonymous=False)
    rospy.spin()
