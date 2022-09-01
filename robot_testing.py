import asyncio
import logging
import csv
import mini.mini_sdk as MiniSdk
from mini.dns.dns_browser import WiFiDevice
from mini.apis.api_action import GetActionList, GetActionListResponse, RobotActionType
from mini.apis.api_sound import StartPlayTTS, AudioStorageType, PlayAudio, GetAudioListResponse, FetchAudioList, \
    AudioSearchType
from mini.apis.api_action import PlayAction, StopAllAction, PlayActionResponse  # action response control
from mini.apis.api_expression import PlayExpression, PlayExpressionResponse
from mini.apis.api_behavior import StartBehavior
from mini.apis.base_api import MiniApiResultType
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse

actionFilePath = r'data/actionlist.csv'
expressionFilePath = r'data/expressionlist.csv'


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# robot testing block

async def robot_test():
    await combination_responses('robot test now', 'wow', 'smile')
    # while True:
    # res = await play_local_customize_audio('M1_YRMU.mp3')
    # print('res:', res)
    await get_action_list()
    await move_robot('forward', 5)
    # await behaviour_response('songanddance')

    # end of the event loop
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)
    await asyncio.sleep(0)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------
# robot functions for testing below this line
# ------------------------------------------------------------------
# ------------------------------------------------------------------
async def play_local_customize_audio(file):
    """测试播放本地音效
    使机器人播放一段本地内置音效，音效名称为"file"，并等待结果
    """
    block: PlayAudio = PlayAudio(
        url=file,
        storage_type=AudioStorageType.CUSTOMIZE_LOCAL)
    # response是个PlayAudioResponse
    (resultType, response) = await block.execute()
    return response


async def move_robot(direct, step_count):
    """控制机器人移动demo
    控制机器人往左(LEFTWARD)移动10步，并等待执行结果
    #MoveRobotResponse.isSuccess : 是否成功　
    #MoveRobotResponse.code : 返回码
    """
    if direct == 'forward':
        move_direction = MoveRobotDirection.FORWARD
    elif direct == 'left':
        move_direction = MoveRobotDirection.LEFTWARD
    elif direct == 'right':
        move_direction = MoveRobotDirection.RIGHTWARD
    elif direct == 'backward':
        move_direction = MoveRobotDirection.BACKWARD
    else:
        move_direction = []
    # step: 移动几步
    # direction: 方向,枚举类型
    block: MoveRobot = MoveRobot(step=step_count, direction=move_direction)
    # response : MoveRobotResponse
    (resultType, response) = await block.execute()

    print(f'move_robot result:{response}')

    assert resultType == MiniApiResultType.Success, 'move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'


# 测试, 获取支持的动作文件列表
async def get_action_list():
    """获取动作列表demo
    获取机器人内置的动作列表，等待回复结果
    """
    # action_type: INNER 是指机器人内置的不可修改的动作文件, CUSTOM 是放置在sdcard/customize/action目录下可被开发者修改的动作
    block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
    # response:GetActionListResponse
    (resultType, response) = await block.execute()

    print(f'get_action_list result:{response}')

    assert resultType == MiniApiResultType.Success, 'get_action_list timetout'
    assert response is not None and isinstance(response,
                                               GetActionListResponse), 'get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'


# 测试获取机器人的音效资源
async def get_audio_list():
    """测试获取音效列表
    获取机器人内置的音效列表，并等待结果
    #GetAudioListResponse.audio ([Audio]) : 音效列表
        #Audio.name : 音效名
        #Audio.suffix : 音效后缀
    #GetAudioListResponse.isSuccess : 是否成功
    #GetAudioListResponse.resultCode : 返回码
    """
    # search_type: AudioSearchType.INNER 是指机器人内置的不可修改的音效, AudioSearchType.CUSTOM 是放置在sdcard/customize/music目录下可别开发者修改的音效
    block: FetchAudioList = FetchAudioList(search_type=AudioSearchType.INNER)
    # response是个GetAudioListResponse
    (resultType, response) = await block.execute()

    print(f'get_audio_list result: {response}')

    assert resultType == MiniApiResultType.Success, 'get_audio_list timetout'
    assert response is not None and isinstance(response, GetAudioListResponse), 'play_audio result unavailable'
    assert response.isSuccess, 'get_audio_list failed'


#  robot's chatting action code
async def robots_chat_response(response):
    block: StartPlayTTS = StartPlayTTS(text=response)
    await block.execute()
    # print(f 'say hello: {response}')


#  robot's responses action code
async def combination_responses(C, A, E):
    # print("responseChat:", C, "responseAction:", A, " responseExpression:", E)
    cha = asyncio.create_task(robots_chat_response(C))
    exp = asyncio.create_task(playexpression(E))
    act = asyncio.create_task(playaction(A))
    await exp
    await act
    await cha
    await asyncio.sleep(0)


async def behaviour_response(name):
    await playbehaviour(name)
    await asyncio.sleep(0)


async def stopallaction():
    print("stopaction")
    StopAllAction(is_serial=True)


async def playbehaviour(name3):
    behaviourcode = find_code('action', name3)
    # print("behaviourcode code:", behaviourcode)
    block: StartBehavior = StartBehavior(name=behaviourcode)
    (resultType, response) = await block.execute()


async def playaction(name1):
    actioncode = find_code('action', name1)
    # print("action code:", actioncode)
    block: PlayAction = PlayAction(action_name=actioncode)
    # response: PlayActionResponse
    (resultType, response) = await block.execute()
    # print(f'play_action result:{response}')


async def playexpression(name2):
    expressioncode = find_code('expression', name2)
    # print("expression code:", expressioncode)
    block: PlayExpression = PlayExpression(express_name=expressioncode)
    # response: PlayExpressionResponse
    (resultType, response) = await block.execute()
    # print(f'test_play_expression result: {response}')


def find_code(path, tag):
    # print("tag:", tag)
    # create a dictionary
    data = {}
    if path == 'action':
        csvFilePath = actionFilePath
        # print("jump in actionFilePath!!")

    elif path == 'expression':
        csvFilePath = expressionFilePath
        # print("jump in expressionFilePath!!")

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        data = []

        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            data.append(rows)
    # print(intents)

    for find in data:
        if tag == find["name"]:
            code = find['code']
            # print(code)
    return code


# 搜索指定序列号(在机器人屁股后面)的机器人, 可以只输入序列号尾部字符即可,长度任意, 建议5个字符以上可以准确匹配, 10秒超时
# 搜索的结果WiFiDevice, 包含机器人名称,ip,port等信息
async def get_device_by_name():
    """根据机器人序列号后缀搜索设备

    搜索指定序列号(在机器人屁股后面)的机器人, 可以只输入序列号尾部字符即可,长度任意, 建议5个字符以上可以准确匹配, 10秒超时


    Returns:
        WiFiDevice: 包含机器人名称,ip,port等信息

    """
    result: WiFiDevice = await MiniSdk.get_device_by_name("00048", 10)
    print(f"get_device_by_name result:{result}")
    return result


# 搜索指定序列号(在机器人屁股后面)的机器人,
async def get_device_list():
    """搜索所有设备

    搜索所有设备，10s后返回结果

    Returns:
        [WiFiDevice]: 所有搜索到的设备，WiFiDevice数组

    """
    results = await MiniSdk.get_device_list(10)
    print(f"get_device_list results = {results}")
    return results


# MiniSdk.connect 返回值为bool, 这里忽略返回值
async def connect(dev: WiFiDevice) -> bool:
    """连接设备

    连接指定的设备

    Args:
        dev (WiFiDevice): 指定的设备对象 WiFiDevice

    Returns:
        bool: 是否连接成功

    """
    return await MiniSdk.connect(dev)


# 进入编程模式,机器人有个tts播报,这里通过asyncio.sleep 让当前协程等6秒返回,让机器人播完
async def start_run_program():
    """进入编程模式demo

    使机器人进入编程模式，等待回复结果，并延时6秒，让机器人播完"进入编程模式"

    Returns:
        None:

    """
    await MiniSdk.enter_program()


# 断开连接并释放资源
async def shutdown():
    """断开连接并释放资源

    断开当前连接的设备，并释放资源

    """
    await MiniSdk.quit_program()
    await MiniSdk.release()


# 默认的日志级别是Warning, 设置为INFO
MiniSdk.set_log_level(logging.DEBUG)
# 设置机器人类型
MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)

if __name__ == '__main__':
    W_device: WiFiDevice = asyncio.get_event_loop().run_until_complete(get_device_by_name())
    if W_device:
        asyncio.get_event_loop().run_until_complete(connect(W_device))
        asyncio.get_event_loop().run_until_complete(start_run_program())
        asyncio.get_event_loop().run_until_complete(robot_test())

        # 定义了事件监听对象,必须让event_loop.run_forever()
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
