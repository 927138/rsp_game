import cv2
import mediapipe as mp
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
import pygame
import time

max_num_hands = 1


rps_gesture = {0:"바위", 5:"보", 9:"가위",10:'ok'}
prev_user = None
user = None
computer = None
t_user = "대기중"
t_computer = "대기중"
outcome = "대기중"
start = False
detect_start = True
count = 0
rsp_start = False
rsp_count = 0
w_result = []
st_result = []

# ㅇㄹㄹㄹㄹㄹ
last_result = False
last_win = ""
last_count = 0
win_image = False

ico = cv2.imread("images/main.png")
ico = cv2.resize(ico, (1920, 1080))

win = cv2.imread("images/win.jpg")
win = cv2.resize(win, (1080,1080))

draw1 = cv2.imread("images/draw.jpg")
draw1 = cv2.resize(draw1, (1080, 1080))

lose = cv2.imread("images/lose.jpg")
lose = cv2.resize(lose, (1080, 1080))

# api = dobot.dobot_connect()


# pygame sound 기초 설정, 오디오 객체 생성
# pygame.mixer.init()
# s_game = pygame.mixer.Sound("sound/rsp_start.wav")
# rsp = pygame.mixer.Sound("sound/rsp.wav")
# r_win = pygame.mixer.Sound("sound/win.wav")
# r_draw = pygame.mixer.Sound("sound/draw.wav")
# r_lose = pygame.mixer.Sound("sound/lose.wav")

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=max_num_hands,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# 입력값에 따른 승부결과 출력
def winner(move1, move2):
    if move1 == move2:
        return "무승부"
    if move1 == "바위":
        if move2 == "가위":
            return "사람"
        elif move2 == "보":
            return "컴퓨터"
    elif move1 == "가위":
        if move2 == "보":
            return "사람"
        elif move2 == "바위":
            return "컴퓨터"
    elif move1 == "보":
        if move2 == "바위":
            return "사람"
        elif move2 == "가위":
            return "컴퓨터"

# Gesture recognition model
file = np.genfromtxt('data/gesture_train.csv', delimiter=',')
angle = file[:,:-1].astype(np.float32)
label = file[:, -1].astype(np.float32)

knn = cv2.ml.KNearest_create()
knn.train(angle, cv2.ml.ROW_SAMPLE, label)

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
flag = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # user and computer 가위바위보 결과들 보기
    # 첫번째 (x1, y1) >> 좌상단 꼭지점 값 , 두번째 (x2, y2) >> 우하단 꼭지점 값
    # x = 1280 / 2 >> 640 / 2 = 0 320 640 960 1280
    # y = 720 / 2 >> 360 / 2  = 0 180 360 540 720

    roi = frame[300:900, 240:840]
    ior = cv2.imread("images/default.jpg")
    ior = cv2.resize(ior, (600, 600))

    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    result = hands.process(img)

    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)
    frame = np.array(pil_image)
    # cam에서 자른 부분들 삽입
    frame[0:1080, 0:1920] = ico
    frame[300:900, 240:840] = roi

    # computer 랜덤으로 낸 동작을 frame에 추가하여 보여준다
    # else일 때 ior부분 삽입
    if computer != None:
        path = "./images/{}.jpg".format(computer)
        e_img = np.fromfile(path, np.uint8)
        icon = cv2.imdecode(e_img, cv2.IMREAD_UNCHANGED)
        icon = icon[:, :, :3]
        icon = cv2.resize(icon, (600, 600))
        # print(icon.shape)
        frame[300:900, 1080:1680] = icon
    else:
        frame[300:900, 1080:1680] = ior

    if last_result:
        print("Dffffffffffffff", last_win)
        last_count += 1
        if last_win == "사람":
            frame[0:1080, 420:1500] = win
        elif last_win == "무승부":
            frame[0:1080, 420:1500] = draw1
        elif last_win == "컴퓨터":
            frame[0:1080, 420:1500] = lose

    if last_count > 30:
        last_win = ""
        last_result = False
        last_count = 0

    if win_image:
        frame[0:1080, 420:1500] = win
        win_image = False

    # 손가락 인식 여부
    if result.multi_hand_landmarks is not None:
        # print(user)
        rps_result = []
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # Compute angles between joints
            v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]  # Parent joint
            v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]  # Child joint
            v = v2 - v1  # [20,3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            # Get angle using arcos of dot product
            angle = np.arccos(np.einsum('nt,nt->n',
                                        v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                        v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

            angle = np.degrees(angle)  # Convert radian to degree

            # Inference gesture
            data = np.array([angle], dtype=np.float32)
            ret, results, neighbours, dist = knn.findNearest(data, 3)
            idx = int(results[0][0])

            # Draw gesture result
            # rps_gesture값이 있으면 user 에 저장
            if idx in rps_gesture.keys():
                org = (int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0]))
                rps_result.append({
                    'rps': rps_gesture[idx],
                    'org': org
                })
                user = rps_gesture[idx]

            # 게임 result 배열과 같이 돌아서 boolean 값을 지정하여 조건에 만족하면 추가
            # st_result = 주먹이 일정 배열안에 들어와 있으면 시작
            if detect_start:
                st_result.append(user)

            # 인식된 손가락 그리기
            # 보고싶으면 주석 삭제
            # mp_drawing.draw_landmarks(frame[300:900, 240:840], res, mp_hands.HAND_CONNECTIONS)


        # start 인식 될때 게임시작
        if start:
            rsp_count += 1
            # 음성대기시간 반복문 속도로 카운트하여 만듬
            # 하드코딩(반목문이 돌아가는 시간을 계산하여 프레임이 끊기지않도록 보여짐)
            # 컴퓨터 사양마다 값이 다름
            if rsp_count > 25:
                rsp_start = True

            # rsp_start 오디오 재생 대기
            # user = 인식된 제스처 > ok일때만 동작
            # if rsp_stat //주먹으로 인식할 때 if문
            if rsp_start and user != "ok":
                if prev_user != user:
                    computer = random.choice(["가위", "바위", "보"])
                    outcome = winner(user, computer)
                    t_user = user
                    t_computer = computer
                prev_user = user
                w_result.append(outcome)
                # print(user)

                # 가위바위보 음성 재생 후 바로인식
                if len(w_result) > 5:
                    w_result = Counter(w_result).most_common(n=1)
                    last_win = w_result[0][0]
                    last_result = True
                    print(w_result)
                    if w_result[0][0] != "대기중":

                        # print(w_result[0][0])
                        # print(start)
                        if w_result[0][0] == '사람':
                            print("user")
                            # r_win.play()

                            # time.sleep(10)
                            time.sleep(0.5)
                            win_image = True

                            # 승리시 dobot 동작
                            # lastIndex = dobot.dobot_control(api)
                            # dobot.remove_alram(api)
                            # count += 1

                        elif w_result[0][0] == '무승부':
                            # r_draw.play()
                            time.sleep(0.5)
                            print("draw1")
                        elif w_result[0][0] == '컴퓨터':
                            # r_lose.play()
                            time.sleep(0.5)
                            print("computer1")
                        else:
                            outcome = "대기중"
                        detect_start = True ##
                        start = False ##
                        user = None
                        prev_user = None
                        computer = None
                        outcome = "대기중"
                        t_user = "대기중"
                        t_computer = "대기중"
                        w_result = []
                        rsp_count = 0
                    rsp_start = False


        # 시작 배열
        if len(st_result) > 22:
            st_result = Counter(st_result).most_common(n=1)
            # ok 손동작이 일정값이 입력되면 게임시작
            if st_result[0][0] == "ok" and st_result[0][1] > 22:
                time.sleep(3.5)
                detect_start = False
                start = True
                # rsp.play()
                print(start)
            st_result = []

    # dobot 초기화
    # if count > 3:
    #     dobot.set_home(api)
    #     dobot.remove_alram(api)
    #     count = 0

    cv2.imshow('Game', frame)

    # space 클릭시 인식 o, 재 클릭시 인식 x
    key = cv2.waitKey(10)
    if key == 32:
        start = not start
    if key == ord('q'):
        break

# dobot.dobot_disconnection(api)
cap.release()
cv2.destroyAllWindows()
