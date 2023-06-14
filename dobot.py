import DobotDllType as dType
import time

def dobot_connect():
    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

    api = dType.load()
    state = dType.ConnectDobot(api, "COM3", 115200)[0]
    print("Connect status:", CON_STR[state])

    if (state == dType.DobotConnect.DobotConnect_NoError):
        set_dobot(api)

    return api


def set_dobot(api):
    # Clean Command Queued
    dType.SetQueuedCmdClear(api)

    # Async Motion Params Setting
    dType.SetHOMEParams(api, 240, 0, 20, 20, isQueued=1)  # Dobot Home(초기화) 설정
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued=1)  # Dobot 관절 단위로 초기 설정
    dType.SetPTPCommonParams(api, 50, 50, isQueued=1)  # Dobot 속도 설정

    dType.SetDeviceWithL(api, 1)  # use rali = 1(o), 0(x)
    print(dType.GetDeviceWithL(api))
    dType.SetIOMultiplexing(api, 16, 1, isQueued=1)
    dType.SetIOMultiplexing(api, 11, 1, isQueued=1)

    #dType.SetHOMECmd(api, temp=0, isQueued=1)[0]

def dobot_disconnection(api):
    dType.DisconnectDobot(api)

def remove_alram(api):
    dType.ClearAllAlarmsState(api)
    dType.SetQueuedCmdForceStopExec(api)
    dType.SetQueuedCmdClear(api)


def start(api, lastIndex):
    dType.SetQueuedCmdStartExec(api)
    print(str(lastIndex), str(dType.GetQueuedCmdCurrentIndex(api)[0]))
    # 마지막 횟수 만큼 동작
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        print(dType.GetQueuedCmdCurrentIndex(api))
        print(lastIndex)
        dType.dSleep(500)


def dobot_speed(api, x):
    dType.SetPTPCommonParams(api, x, x, isQueued=1)[0]




def dobot_control(api):
    dType.SetQueuedCmdStartExec(api)
    dobot_speed(api, 40)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 245, 0, 10, 20, 0, isQueued=1)[0]

    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 245, 0, 10, 20, 0, isQueued=1)[0]

    # # Pin.16 = 에어펌프(0/off, 1/on)
    # # PIn.11 = 그립(0/open, 1/close)
    # # SetWAITCmd = ms 단위
    dType.SetIODO(api, 16, 1, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    dType.SetIODO(api, 11, 0, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    dType.SetIODO(api, 16, 0, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    print('df')
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 20, -60, 900, isQueued=1)[0]

    # 컵뺴기
    dobot_speed(api, 40)

    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 35, -60, 950, isQueued=1)[0]
    dType.SetIODO(api, 16, 1, 1)[0]
    dType.SetIODO(api, 11, 1, 1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 0, -60, 950, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 40, -60, 950, isQueued=1)[0]
    dType.SetIODO(api, 16, 0, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 40, -60, 930, isQueued=1)[0]
    dType.SetIODO(api, 16, 1, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetIODO(api, 11, 1, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetIODO(api, 16, 0, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 30, -60, 850, isQueued=1)[0]

    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 166, 0, 25, -60, 920, isQueued=1)[0]
    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 166, 0, 25, -60, 905, isQueued=1)[0]

    # ㅇㄹㄹㄹ
    # dType.SetIODO(api, 16, 1, 1)[0]
    # dType.SetWAITCmd(api, 500, isQueued=1)
    # dType.SetIODO(api, 11, 1, 1)[0]
    # dType.SetWAITCmd(api, 500, isQueued=1)
    # dType.SetIODO(api, 16, 0, 1)[0]
    # dType.SetWAITCmd(api, 500, isQueued=1)



    #컵뺴기
    # dobot_speed(api, 40)
    # # 31
    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 35, -60, 950, isQueued=1)[0]
    # dType.SetIODO(api, 16, 1, 1)[0]
    # dType.SetIODO(api, 11, 1, 1)[0]
    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 0, -60, 950, isQueued=1)[0]
    # # 22
    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 35, -60, 950, isQueued=1)[0]
    # # ㅇㄹㄹㄹ
    # dType.SetIODO(api, 16, 0, 1)[0]
    # dType.SetWAITCmd(api, 500, isQueued=1)
    #
    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 30, -60, 850, isQueued=1)[0]
    #
    # # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 166, 0, 25, -60, 920, isQueued=1)[0]
    # #dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 166, 0, 25, -60, 905, isQueued=1)[0]
    #
    # # ㅇㄹㄹㄹ
    # dType.SetWAITCmd(api, 500, isQueued=1)
    # dType.SetIODO(api, 16, 1, 1)[0]
    # dType.SetWAITCmd(api, 500, isQueued=1)
    # dType.SetIODO(api, 11, 1, 1)[0]
    # # dType.SetWAITCmd(api, 500, isQueued=1)
    # # dType.SetIODO(api, 16, 0, 1)[0]



    #컵뺀이후에 커피머신으로가는동작
    dobot_speed(api, 40)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 5, -60, 825, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 5, 20, 600, isQueued=1)[0]
    #dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 180, 0, 5, 20, 700, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 0, -180, 5, -70, 400, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 0, -260, 45, -70, 550, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 3, -260, 47, -70, 808, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 5, -260, 40, -70, 815, isQueued=1)[0]
    # 0 805
    dType.SetIODO(api, 16, 1, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    dType.SetIODO(api, 11, 0, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetIODO(api, 16, 0, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 5, -260, 40, -70, 815, isQueued=1)[0]
    # dType.SetWAITCmd(api, 500, isQueued=1)
    # dType.SetIODO(api, 16, 1, 1)[0]
    # dType.SetIODO(api, 11, 0, 1)[0]
    # dType.SetWAITCmd(api, 500, isQueued=1)
    # dType.SetIODO(api, 16, 0, 1)[0]
    # dType.SetWAITCmd(api, 1000, isQueued=1)

    # 컵 > 커피머신에 두기
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 35, -70, 700, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -200, 170, -160, 700, isQueued=1)[0]


    # 커피 버튼 클릭 / 그리포 오픈상태
    dobot_speed(api, 20)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 25, -194, 171, -160, 795, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 25, -194, 171, -160, 817, isQueued=1)[0]
    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 3, -194, 171, -160, 795, isQueued=1)[0]
    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 3, -194, 171, -160, 810, isQueued=1)[0]

    # 커피대기후 뺴오기 /그리퍼 OPEN > CLOSE
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 0, -240, 30, -70, 600, isQueued=1)[0]
    #dff
    dType.SetWAITCmd(api, 100, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 5, -240, 37, -70, 830, isQueued=1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 5, -240, 47, -70, 830, isQueued=1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    dType.SetIODO(api, 16, 1, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetIODO(api, 11, 1, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)

    dobot_speed(api, 10)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -200, 51, -70, 830, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -240, 51, -70, 500, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -240, 51, -70, 500, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 160, 0, 10, 20, 400, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 160, 0, 10, 20, 0, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 0, 300, -75, 107, 0, isQueued=1)[0]
    # OPEN, ALR OFF
    dType.SetIODO(api, 11, 0, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    dType.SetIODO(api, 16, 0, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)

    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 0, 300, -85, 107, 0, isQueued=1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 0, 200, -75, 107, 0, isQueued=1)[0]
    # DELAY
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 0, 200, 20, 107, 0, isQueued=1)[0]
    lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 245, 0, 10, 20, 0, isQueued=1)[0]
    # lastIndex = dType.SetHOMECmd(api, temp=0, isQueued=1)[0]
    start(api, lastIndex)

    return lastIndex

def test(api):
    dType.SetQueuedCmdStartExec(api)
    dType.SetIODO(api, 16, 1, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    dType.SetIODO(api, 11, 0, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    dType.SetIODO(api, 16, 0, 1)[0]
    dType.SetWAITCmd(api, 1000, isQueued=1)
    print('df')
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 10, -60, 880, isQueued=1)[0]

    # 컵뺴기
    dobot_speed(api, 40)
    # 31
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 35, -60, 950, isQueued=1)[0]
    dType.SetIODO(api, 16, 1, 1)[0]
    dType.SetIODO(api, 11, 1, 1)[0]
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 0, -60, 950, isQueued=1)[0]
    # 22
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 40, -60, 950, isQueued=1)[0]
    # ㅇㄹㄹㄹ
    dType.SetIODO(api, 16, 0, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)

    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 164, 0, 30, -60, 850, isQueued=1)[0]

    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 166, 0, 25, -60, 920, isQueued=1)[0]
    # dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 166, 0, 25, -60, 905, isQueued=1)[0]

    # ㅇㄹㄹㄹ
    dType.SetIODO(api, 16, 1, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetIODO(api, 11, 1, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    dType.SetIODO(api, 16, 0, 1)[0]
    dType.SetWAITCmd(api, 500, isQueued=1)
    lastIndex = dType.SetWAITCmd(api, 500, isQueued=1)[0]
    start(api, lastIndex)
    # dType.SetWAITCmd(api, 500, isQueued=1)
    # dType.SetIODO(api, 16, 0, 1)[0]


def set_home(api):
    lastIndex = dType.SetHOMECmd(api, temp=0, isQueued=1)[0]

    start(api, lastIndex)
    return lastIndex

def set_dff(api):
    lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 245, 0, 10, 20, 700, isQueued=1)[0]
    start(api, lastIndex)
    return lastIndex

if __name__ == "__main__":
    api = dobot_connect()


    lastIndex = dobot_control(api)
    # lastIndex = set_home(api)
    # lastIndex = test(api)
    remove_alram(api)
    dobot_disconnection(api)





















# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 245, 0, 10, -60, 900, isQueued=1)[0]
#
#
# dobot_speed(60)
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 240, 0, 36, -60, 977, isQueued=1)[0]
# lastIndex = dType.SetIODO(api, 16, 1, 1)[0]
# lastIndex = dType.SetIODO(api, 11, 1, 1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 240, 0, 0, -60, 977, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 240, 0, 55, -60, 977, isQueued=1)[0]
# lastIndex = dType.SetIODO(api, 16, 0, 1)[0]
#
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 240, 0, 25, -60, 905, isQueued=1)[0]
#
# dType.SetWAITCmd(api, 500, isQueued=1)
# lastIndex = dType.SetIODO(api, 16, 1, 1)[0]
# dType.SetWAITCmd(api, 500, isQueued=1)
# lastIndex = dType.SetIODO(api, 11, 1, 1)[0]
#
# dobot_speed(80)
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 240, 0, 5, -60, 820, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 240, 0, 5, 20, 700, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 180, 0, 5, 20, 700, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -180, 5, -70, 600, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 52, -70, 700, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 52, -70, 805, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 40, -70, 805, isQueued=1)[0]
#
# dType.SetWAITCmd(api, 500, isQueued=1)
# lastIndex = dType.SetIODO(api, 11, 0, 1)[0]
# dType.SetWAITCmd(api, 500, isQueued=1)
# lastIndex = dType.SetIODO(api, 16, 0, 1)[0]
#
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 40, -70, 700, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 6, -200, 170, -160, 700, isQueued=1)[0]
#
# #lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 6, -200, 170, -160, 700, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 52, -70, 700, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 52, -70, 805, isQueued=1)[0]
#
# dType.SetWAITCmd(api, 500, isQueued=1)
# lastIndex = dType.SetIODO(api, 16, 1, 1)[0]
# dType.SetWAITCmd(api, 500, isQueued=1)
# lastIndex = dType.SetIODO(api, 11, 1, 1)[0]
# dType.SetWAITCmd(api, 1000, isQueued=1)
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 60, -70, 805, isQueued=1)[0]
# dobot_speed(30)
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -260, 40, -70, 0, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 0, -180, 40, -70, 0, isQueued=1)[0]
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 220, 0, -90, 20  ,0, isQueued=1)[0]
# dType.SetWAITCmd(api, 500, isQueued=1)
# lastIndex = dType.SetIODO(api, 11, 0, 1)[0]
#
#
# lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 245, 0, 10, 20, 0, isQueued=1)[0]





