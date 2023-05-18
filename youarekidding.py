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
            # 이미지 토픽 수신
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            cv2.imshow('Image', image)
            cv2.waitKey(1)
            # rotate_cmd 메시지 준비
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # 기본값: 정지

            # 배경색 판별
            src = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, src_bin = cv2.threshold(src, 66, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(src_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            h, w = src.shape[:2]
            mask = np.zeros_like(src)
            max_area = 0
            second_area = 0
            for i in range(len(contours)):
                points = contours[i]
                area = cv2.contourArea(points)
                if area > second_area:
                    if area > max_area:
                        second_area = max_area
                        max_area = area
                    else:
                        second_area = area

            for i in range(len(contours)):
                points = contours[i]
                area = cv2.contourArea(points)
                if area > second_area:
                    m = cv2.moments(points)
                    p1 = 0.01 * cv2.arcLength(points, True)
                    ap = cv2.approxPolyDP(points, p1, True)
                    cv2.drawContours(mask, [ap], 0, (255), 1, cv2.LINE_AA)
                    cv2.fillPoly(mask, [ap], (255))
                    pixels = np.where(mask == 255)
            
            R = 0
            B = 0
            W = 0
            for pixel in zip(pixels[1], pixels[0]):
                x, y = pixel
                b, g, r = image[y, x]
                if 0 <= b <= 100 and 0 <= g <= 100 and 100 <= r <= 255:
                    R += 1
                elif 0 <= r <= 100 and 0 <= g <= 100 and 100 <= b <= 255:
                    B += 1
                else:
                    W += 1

            print("B =", B)
            print("R =", R)
            print("W =", W)
            cv2.imshow('src_bin', mask)

            # color_state 발행
            self.color_pub.publish(msg)

        except CvBridgeError as e:
            print(e)


if __name__ == '__main__':
    rospy.init_node('DetermineColor', anonymous=False)
    detector = DetermineColor()
    rospy.spin()


