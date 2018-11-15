from Public import StartApp, ReadFile
import time
import os

# 不同设备的IP及版本号
ip = 'emulator-5554'
v = '5.1.1'
ip_1 = '35c014d9'
v_1 = '7.1.1'
# ip_1 = 'emulator-5554'
# v_1 = '5.1.1'

# 包名和Activity
pack, act = 'cn.yygapp.action', 'cn.yygapp.action.ui.SplashActivity'
pack_1, act_1 = 'cn.yygapp.aikaishi', 'cn.yygapp.aikaishi.ui.SplashActivity'


def actions():
    login = StartApp()
    run = ReadFile()
    log_path = 'C:/Users/ac191/PycharmProjects/Action/Log'  # 日志文件夹路径
    element = 'E:/Action用例/全流程'  # 测试用例目录
    s_time = (time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))  # 系统当前时间
    path = log_path + '/' + s_time + '/'
    os.mkdir(path)  # 创建log的目录

    y = [element, path, ip]
    d = [element, path, ip_1]

    # 启动导演端app到登录页面
    driver = login.login_app(ip, v, pack_1, act_1, path)
    run.run_test(d, driver, "login.csv")

    # 新建剧目
    # run.run_test(d, driver, '新建剧目.csv')

    # 发布新招募信息
    # run.run_test(d, driver, '发布临演招募.csv')
    run.run_test(d, driver, '发布角色招募.csv')

    # 协拍接单
    driver1 = login.login_app(ip_1, v_1, pack, act, path)
    run.run_test(y, driver1, '协拍接角色招募.csv')
    # run.run_test(y, driver1, '协拍接临演招募.csv', ip_1)

    # 导演确认协拍申请
    driver = login.startUp_app(ip, v, pack_1, act_1)
    run.run_test(d, driver, '导演确认协拍申请.csv')

    # 协拍邀请演员出演角色
    driver1 = login.startUp_app(ip_1, v_1, pack, act)
    run.run_test(y, driver1, '协拍邀请出演角色.csv')

    # 演员接受协拍邀请
    driver1 = login.login_app(ip_1, v_1, pack, act, path)
    run.run_test(y, driver1, '临演接受邀请.csv')

    # 临时演员申请招募
    # driver1 = login.login_app(ip_1, v_1, pack, act)
    # run.run_test(y, driver1, '临演申请.csv')

    # 协拍同意临演申请
    # driver1 = login.login_app(ip_1, v_1, pack, act)
    # run.run_test(y, driver1, '协拍同意临演申请.csv')

    # 导演通过演员申请并给演员签到
    driver = login.startUp_app(ip, v, pack_1, act_1)
    run.run_test(d, driver, '导演同意演员申请与签到.csv')

    # 协拍申请收工
    driver1 = login.login_app(ip_1, v_1, pack, act, path)
    run.run_test(y, driver1, '协拍申请收工.csv')

    # 导演同意收工
    driver = login.startUp_app(ip, v, pack_1, act_1)
    run.run_test(d, driver, '导演同意收工.csv')

    # 协拍申请结算
    driver1 = login.startUp_app(ip_1, v_1, pack, act)
    run.run_test(y, driver1, '协拍申请结算.csv')

    # 导演同意结算
    driver = login.startUp_app(ip, v, pack_1, act_1)
    run.run_test(d, driver, '导演结算.csv')
    print('导演成功结算，走完全流程')


actions()
