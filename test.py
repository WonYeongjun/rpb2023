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
            src = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, src_bin = cv2.threshold(src, 66, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(src_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            h, w = src.shape[:2]
            mask = np.zeros_like(src)
            max_area=0
            second_area=0
            for i in range(len(contours)):
                points = contours[i]  # 외곽선을 그릴 객체의 포인트 행렬
                area = cv2.contourArea(points)
                if area>second_area:
                    if area>max_area:
                        second_area=max_area
                        max_area=area
                    else:
                        second_area=area
       
            for i in range(len(contours)):
                points = contours[i]  # 외곽선을 그릴 객체의 포인트 행렬
                area = cv2.contourArea(points)
                if area>second_area:
        #외곽선 그리기

       
        #외곽선으로 모멘트 계산
                    m = cv2.moments(points)
                #외곽선 둘레 * 0.01
                    p1 = 0.01 * cv2.arcLength(points, True)
        #외곽선 근사화(점의 수를 줄임)
                    ap = cv2.approxPolyDP(points, p1, True)
        #계산된 근사치 좌표로 외곽선 그림
                    cv2.drawContours(mask, [ap], 0, (255),1, cv2.LINE_AA)

	    # 액자 내부 픽셀 분류
            mask = np.zeros((height, width), np.uint8)
            cv2.drawContours(mask, [ap], -1, (255, 255, 255), -1)
            cv2.imshow('Image', image)
            cv2.waitKey(1)
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
