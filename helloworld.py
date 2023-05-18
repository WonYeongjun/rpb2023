import rospy
import numpy as np
import cv2

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

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
        msg.frame_id = '0'        
   
# Step 1: 직사각형이 아닌 검은색 사각형 모니터 확인
def is_black_rectangle(image):
    # 이미지 크기를 가져옴
    height, width, _ = image.shape

    # 모니터의 꼭짓점 좌표
    top_left = (width // 4, height // 4)
    bottom_right = (width // 4 * 3, height // 4 * 3)

    # 모니터 영역의 색상 값을 추출
    monitor_color = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # 검은색 픽셀의 비율을 계산
    black_pixel_ratio = np.mean(monitor_color) < 10

    return black_pixel_ratio

# Step 2: 영상 배경색 확인
def classify_background_color(image):
    # 이미지 크기를 가져옴
    height, width, _ = image.shape
    # 배경색 추출을 위해 이미지의 중앙 영역 선택
    center_area = image[height // 4:height // 4 * 3, width // 4:width // 4 * 3]

    # 중앙 영역의 색상 값을 추출
    center_color = np.mean(center_area, axis=(0, 1))

    # 배경색 분류
    if center_color[2] > center_color[0] and center_color[2] > center_color[1]:
        background_color = 'Red'
    elif center_color[0] > center_color[1] and center_color[0] > center_color[2]:
        background_color = 'Blue'
    else:
        background_color = 'Other'

    return background_color

# Step 3: 배경색 분류
def main():
    # 이미지 파일 로드
    
    # Step 1: 직사각형이 아닌 검은색 사각형 모니터 확인
    if is_black_rectangle(image):
        # Step 2: 영상 배경색 확인
        background_color = classify_background_color(image)
        # Step 3: 배경색 분류
        print("배경색:", background_color)
    else:
        print("직사각형이 아닌 사각형 모니터가 아닙니다.")



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
