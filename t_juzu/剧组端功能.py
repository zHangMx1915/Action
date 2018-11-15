from Public import StartApp, ReadFile
import time
import os

# 不同设备的IP及版本号
ip = '127.0.0.1:5555'
v = '5.1.1'

'''''
# 新建剧目
def textAction(self):
    # global driver
    log_path = 'C:/Users/ac191/PycharmProjects/Action/Log/'  # 日志文件夹路径
    basepath = 'C:/Users/ac191/PycharmProjects/Action/element'  # 当前脚本路径
    pageElement = os.path.join(basepath, "JuZu_Element")  # yaml文件夹
    na = Public.read_file.parseyaml('新建剧目.yaml', pageElement)  # 调用读元素方法
    driver = Public.startUp_app.startUp_app_yaml(self, deviceName, platformVersion)  # 启动app
    Public.Public.log_file(driver, log_path, na)  # 创建log目录，并传送用例目录开始执行用例
'''


class DaoYan(StartApp, ReadFile):

    def login_actions(self):
        # 导演端app包名和Activity
        pack_1, act_1 = 'cn.yygapp.aikaishi', 'cn.yygapp.aikaishi.ui.SplashActivity'
        log_path = 'C:/Users/ac191/PycharmProjects/Action/Log'  # 日志文件夹路径
        element = 'E:/Action用例'  # 测试用例目录
        s_time = (time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))  # 系统当前时间
        path = log_path + '/' + s_time + '/'
        os.mkdir(path)  # 创建log的目录

        # 启动app到登录页面
        # driver = StartApp.login_app(self, ip, v, )
        driver = self.login_app(ip, v, pack_1, act_1)
        # 启动并登录app
        self.run_test(driver, element, path, 'login.csv', ip)
        # 新建剧目
        self.run_test(driver, element, path, '新建剧目.csv', ip)
        # 发布新招募信息
        self.run_test(driver, element, path, '发布招募.csv', ip)
        # 授信人员
        # ReadFile.run_test(driver, pageElement, path, '授信人员.csv')
        # 个人信息页面
        # ReadFile.run_test(driver, pageElement, path, '个人信息.csv')


if __name__ == '__main__':
    star = DaoYan()
    star.login_actions()
