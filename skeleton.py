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
            # determine the color and assing +1, 0, or, -1 for frame_id
            # msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)
           
    # 이미지를 그레이스케일로 변환
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
    # 모니터 영상 검출을 위한 임계값 설정
            threshold = 10
   
    # 이진화하여 검은색 픽셀 검출
            _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
   
    # 검은색 모니터 영역 검출을 위한 외곽선 찾기
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
            for contour in contours:
        # 외곽선을 감싸는 최소한의 사각형 영역 구하기
                x, y, w, h = cv2.boundingRect(contour)
       

# Step 2: 모니터 내부 배경색 확인

    # 모니터 내부 영역 추출
            monitor_roi = image[y:y+h, x:x+w]
   
    # 모니터 내부 영상에서 가장 많은 픽셀을 차지하는 색상 계산
            pixels = monitor_roi.reshape(-1, 3)
            unique_colors, color_counts = np.unique(pixels, axis=0, return_counts=True)
   
    # 가장 많은 픽셀을 차지하는 색상 인덱스 추출
            max_color_index = np.argmax(color_counts)
   
    # 배경색을 나타내는 BGR 값 반환
            background_color = unique_colors[max_color_index]


# Step 3: 배경색 분류 (R/B/그 외)

    # 배경색 분류를 위한 임계값 설정
            red_threshold = 200
            blue_threshold = 200
            green_thresholdB = 248
            green_thresholdR = 200
           
   
    # 배경색 추출
            blue, green, red = background_color
   
    # 배경색 분류
            if blue > blue_threshold:
                if green < green_thresholdB:
                    background_color= "B"
                else:
                    background_color="Others.B"
            elif red > red_threshold:
                if green < green_thresholdR:
                    background_color= "R"
                else:
                    background_color="Others.R"
            else:
                background_color="Others"
            print(background_color)
            print(len(monitor_roi))

# Step 4: 배경색에 따라 다른 행동 수행
    # 배경색 분류
 
        # 그 외 배경색에 대한 행동 수행
        # 예: 다른 배경색이 감지되면 기본 동작을 수행하도록 설정
       
        # TODO: 다른 배경색에 대한 기본 동작 구현




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

