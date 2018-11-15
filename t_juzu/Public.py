from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
import yaml
import time
import csv
import os
from selenium.common.exceptions import NoSuchElementException   # 异常处理


# 启动app
class StartApp:

    # 启动app
    def startUp_app(self, ip, v, pack, act):
        startUp_action = {
            'platformName': 'Android',                                  # android还是ios的环境
            'deviceName': ip,                                           # 手机设备名称，通过adb devices查看
            'platformVersion': v,                                       # android版本号
            'appPackage': pack,                                         # apk的包名
            'appActivity': act,                                         # apk的launcherActivity
            'noReset': True,                                            # 不需要每次都安装apk
            'unicodeKeyboard': True,                                    # 使用unicode编码方式发送字符串
            'resetKeyboard': True,                                      # 隐藏手机软键盘
            'automationName': 'Uiautomator2'                            # 定位toast元素,弹框消息提示定位
                        }
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', startUp_action)

        return driver

    # login 启动app,会重新安装app，启动到登录页面
    def login_app(self, ip, v, pack, act, path):    # (self, ip, v, pageElement, log_path, test):
        startUp_action = {
            'platformName': 'Android',
            'deviceName': ip,
            'platformVersion': v,
            'appPackage': pack,
            'appActivity': act,
            # 'noReset': True,                                        # 不需要每次都安装apk
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'automationName': 'Uiautomator2'
                        }
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', startUp_action)
        time.sleep(8)
        ms = Public()
        mx = Log()
        file_name = mx.logfile(path, '首次登陆权限')
        ms.permission(driver, file_name)

        return driver


class Log:

    # 创建log文件
    def logfile(self,path, test):
        test_time = (time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
        file_name = (path + test + test_time + ".txt")
        open(file_name, "a", encoding='utf-8')  # 创建log的txt文件

        return file_name

    # 写入日志
    def mylog(self, log, va, file_name):
        test_time = (time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))       # 系统当前时间
        with open(file_name, "a", encoding='utf-8') as f:

            if not va:
                f.write("\n%s :   %s" % (test_time, log))  # 写入txt
            else:
                f.write("\n%s :   %s" % (test_time, log + ',  ' + va))          # appium执行的语句


# 执行元素
class RunCase(Log):

    # 判断执行元素是否需要添加延时
    def wait_time(self, element):
        for i in element:                                     # 判断元素执行是否有加延时时间值
            if i == 'time':
                t = int(element['time'])
                time.sleep(t)

    # id 和id_send_keys
    def ids(self, driver, element, file_name):  # 未完成
        logs = element['name']
        value = element['value']
        value1 = element['value1']
        self.wait_time(element)
        if not value1:
            driver.find_element_by_id(value).click()
            va = 'driver.find_element_by_id(%s)' % (value)
        else:
            driver.find_element_by_id(value).send_keys(value1)
            va = 'driver.find_element_by_id(%s).send_keys(%s)' % (value, value1)
        self.mylog(logs, va, file_name)

    # xpath方法
    def xpath_type(self, driver, element, file_name):
        logs = element['name']
        value = element['value']
        value1 = element['value1']
        va = 'driver.find_element_by_xpath(%s).click(%s)' % (value, value1)
        self.mylog(logs, va, file_name)
        self.wait_time(element)                          # 判断执行元素是否需要添加延时
        driver.find_element_by_xpath(value).click()

    # tap方法
    def tap_type(self, driver, element, file_name):
        logs = element['name']
        value = element['value']
        va = 'driver.tap(%s)' % value
        self.mylog(logs, va, file_name)
        self.wait_time(element)                          # 判断执行元素是否需要添加延时
        driver.tap(value)

    # adb方法
    def adbs(self, driver, element, file_name, ip):
        logs = element['name']
        value = element['value']
        x= element['x']
        # y = element['y']
        self.wait_time(element)                          # 判断执行元素是否需要添加延时
        if not x:
            va = 'os.system(%s)' % value
            self.mylog(logs, va, file_name)
            os.system("adb -s %s shell input text '%s'" % (ip, value))
        else:
            print('sen_keys')
            ma = Public()
            xs, ys = ma.coordinate(driver, element)
            va = ('adb -s %s shell input tap' % ip + ' ' + str(xs) + ' ' + str(ys))
            self.mylog(logs, va, file_name)
            os.system(va)

    # tab键方法，光标进入下一个输入框
    def tab(self, element, file_name, ip):
        logs = element['name']
        value = element['value']
        va = 'adb -s %s shell input keyevent %s' % (ip, value)
        self.mylog(logs, va, file_name)
        self.wait_time(element)                          # 判断执行元素是否需要添加延时
        os.system(va)

    # 等待指定页面出现
    def wait_activity(self, driver, element, file_name):
        logs = element['name']
        value = element['value']
        va = "driver.wait_activity(%s, 30)" % value
        self.mylog(logs, va, file_name)
        self.wait_time(element)
        driver.wait_activity(value, 30)

    # 多个重复id的元素操作,,协拍邀请演员出演角色招募，同意演员申请
    def repeat(self, driver, element, file_name):
        ma = Public()
        logs = element['name']
        value = element['value']
        value1 = element['value1']
        x = element['x']
        for i in range(4):
            va = 'driver.find_elements_by_id(%s)[%s].click(), ' \
                 'driver.find_element_by_id(%s)[%s].click()' % (value, i, value1, i)
            self.mylog(logs, va, file_name)
            time.sleep(1)
            try:
                try:
                    driver.find_elements_by_id(value)[i].click()
                    time.sleep(1)
                    driver.find_element_by_xpath("//*[@text='%s']" % x).click()
                    break
                except:
                    ma.window_slip(driver, element, file_name)
                    time.sleep(1)
                    driver.find_element_by_id(value1).click()
                    break
            except:
                driver.back()


# 通用方法
class Public(RunCase):

    #  首次启动系统权限弹窗
    def permission(self , driver, file_name):
        va = ''
        for i in range(5):
            loc = ("xpath", "//*[@text='允许']")
            locs = ("xpath", "//*[@text='始终允许']")                    # 关闭权限弹窗的按钮字符
            try:
                try:
                    e = WebDriverWait(driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                    e.click()
                    logs = loc + '跳过权限窗口'
                    self.mylog(logs, va, file_name)
                except:
                    e = WebDriverWait(driver, 1, 0.5).until(EC.presence_of_element_located(locs))
                    e.click()
                    logs = locs + '跳过权限窗口'
                    self.mylog(logs, va, file_name)
            except:
                pass

    #  滑动屏幕页面
    def window_slip(self, driver, element, file_name, times=500):   # other=0.5,
        va = ''
        logs = element['name']
        self.mylog(logs, va, file_name)
        start = float(element['start'])
        end = float(element['end'])
        other = float(element['other'])               # 滑动的中心位置
        n = int(element['n'])                         # 滑动次数
        direction = element['direction']
        self.wait_time(element)
        t = times                                # 滑动时间
        size = driver.get_window_size()          # 获取屏幕大小，size = {u'width': 720, u'height': 1280}
        if direction == 'vertical':              # 上下滑动
            x1 = size['width'] * other
            y1 = size['height'] * start
            y2 = size['height'] * end
            for i in range(n):
                driver.swipe(x1, y1, x1, y2, t)
        elif direction == 'horizontal':          # 左右滑动
            x1 = size['width'] * start
            x2 = size['width'] * end
            y1 = size['height'] * other
            for i in range(n):
                driver.swipe(x1, y1, x2, y1, t)

    # 截图
    def cut_shot(self, driver, path):
        test_time = (time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
        screen_save_path = path + test_time + '.png'
        driver.get_screenshot_as_file(screen_save_path)

    # 计算坐标
    def coordinate(self, driver, element):
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        print('当前设备屏幕尺寸' + '：' + str(x) + ' ' + str(y))
        x1 = x * float(element['x'])
        y1 = y * float(element['y'])

        return x1, y1

    # 获取元素的text文本值
    def element_text(self, driver, element, file_name):
        va = ''
        logs = element['name']
        self.mylog(logs, va, file_name)
        self.wait_time(element)
        text = element['value1']
        el = driver.find_element_by_id(element['value'])
        if el.text == text:
            logss = '显示正确,显示为：' + el.text
            print(logss)
            self.mylog(logss, va, file_name)
        else:
            logsa = '显示不正确,显示为：' + el.text
            print(logsa)
            self.mylog(logsa, va, file_name)

    # toast消息判断
    def find_toast(self, driver, element, file_name, timeout=10, poll_frequency=0.3):
        va= ''
        try:
            logs = element['name']
            self.mylog(logs, va, file_name)
            text = element['value']
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % text)
            t = WebDriverWait(driver, timeout, poll_frequency).until(EC.presence_of_element_located(toast_loc))
            print(t.text)
        except:
            logs = '缺少toast消息'
            self.mylog(logs, va, file_name)
            print(logs)

    # 执行测试
    def judge_type(self, element, driver, file_name, ip):
        if element['type'] == 'id':
            self.ids(driver, element, file_name)
        elif element['type'] == 'xpath':
            self.xpath_type(driver, element, file_name)
        elif element['type'] == 'adb':
            self.adbs(driver, element, file_name, ip)
        elif element['type'] == 'tap':
            self.tap_type(driver, element, file_name)
        elif element['type'] == 'tab':
            self.tab(element, file_name, ip)
        elif element['type'] == 'wait':
            self.wait_activity(driver, element, file_name)
        elif element['type'] == 'text':
            self.element_text(driver, element, file_name)
        elif element['type'] == 'slip':
            self.window_slip(driver, element, file_name)
        elif element['type'] == 'toast':
            self.find_toast(driver, element, file_name)
        elif element['type'] == 'yao':
            self.repeat(driver, element, file_name)


# 读取yaml文件元素
class ReadFile(object):

    # 读取excel数据
    def read_excel(self, driver, j, page_element, log_path):

        pass

    # 遍历元素，创建log文件，记录报错报错信息
    def run_test(self, list, driver, test):
        element = list[0]
        path = list[1]
        ip = list[2]
        ma = Public()
        mx = Log()
        file_name = mx.logfile(path, test)
        k = element + '/' + test
        with open(k) as csvfile:
            reader = [each for each in csv.DictReader(csvfile)]  # 读取csv文件
            for i in reader:
                time.sleep(1.5)
                try:
                    ma.judge_type(i, driver, file_name, ip)
                except NoSuchElementException as msg:
                    print(msg)
                    for i in range(5):
                        ma.cut_shot(driver, path)  # 出错时调用截图
                        time.sleep(0.5)
                        i += 1
                    time.sleep(10)
                    ma.judge_type(i, driver, file_name, ip)
                except ValueError:
                    time.sleep(5)
                    ma.judge_type(i, driver, file_name, ip)

    '''
    nons = ['姓名', '年龄', '身高', '电话']                           # 创建csv文件
    csvFile2 = open('E:\Action用例/loginin.csv', 'w', newline='')
    writer2 = csv.writer(csvFile2)
    writer2.writerow(nons)
    '''

    # 读取文件里的元素
    def find_element(self, driver, file_name, na):
        ma = Public()
        Modulelog = na['newRepertoire']['dec']                       # 测试模块名称
        print(Modulelog)
        for i in na["newRepertoire"]['locators']:
            time.sleep(0.3)
            ma.judge_type(i, driver, file_name, Modulelog)

    # 读取yaml文件
    def parseyaml(self, file_name, pageElement):                       # 传入yaml文件的路径，yaml文件夹名称
        pageElements = {}
        for fpath, dirname, fnames in os.walk(pageElement):      # 遍历读取yaml文件
            for name in fnames:
                if name == file_name:                            # 找到指定文件
                    yaml_file_path = os.path.join(fpath, name)   # yaml文件绝对路径
                    if ".yaml" in str(yaml_file_path):           # 排除一些非.yaml的文件
                        with open(yaml_file_path, 'r', encoding='utf-8') as f:
                            page = yaml.load(f)
                            pageElements.update(page)
        return pageElements

