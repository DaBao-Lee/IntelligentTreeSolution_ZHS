import sys
from os import path
from time import sleep
from colorama import Fore
from threading import Thread
import selenium.webdriver as wb
addition_path = path.abspath("zhs.py")
sys.path.append("\\".join(addition_path.split("\\")[: -1]))
from captcha import passCaptcha
from question import questMoudle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class treeSolution:
    def __init__(self, username:str=None, mm:str=None, arg=None) -> None:
        
        options = wb.EdgeOptions()
        if arg == "--headless": 
            options.add_argument('--headless')
            options.add_argument('log-level=3')
        else: options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        self.driver = wb.Edge(options=options)
        self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)
        try:
            self.flag = True 
            self.quest = questMoudle(self.driver, self.wait, self.action)
        except: self.flag = False 
        self.driver.set_window_size(1200, 800)
        self.driver.get('https://onlineweb.zhihuishu.com/onlinestuh5')
        self.net = passCaptcha(self.driver, self.wait, self.action,
                                easy_model="data/passEasy.onnx",
                                complex_model="data/passComplex.pt")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="lUsername"]'))).send_keys(str(username))
        self.driver.find_element(By.XPATH, '//*[@id="lPassword"]').send_keys(str(mm))
        self.driver.find_element(By.XPATH, '//*[@id="f_sign_up"]/div[1]/span').click()
        sleep(0.8)
        while self.net.passEasyCaptcha(): pass
        print(Fore.LIGHTYELLOW_EX + "登入成功".center(60, '-'))
        self.task = Thread(target=self.errorCheck, daemon=True); self.task.start()
        self.controlCenter()

    def mainWindow(self):

        self.driver.switch_to.window(self.driver.window_handles[-1])
        if self.driver.current_url != "https://onlineweb.zhihuishu.com/onlinestuh5":
            self.driver.get("https://onlineweb.zhihuishu.com/onlinestuh5")
            try:
                self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-left-course')))
            except:
                self.driver.get("https://onlineweb.zhihuishu.com")
                sleep(0.5)
                self.driver.get("https://onlineweb.zhihuishu.com/onlinestuh5")
                sleep(0.8)

    def controlCenter(self):

        self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-left-course')))
        needToPlay = len(self.driver.find_elements(By.CLASS_NAME, 'interestingHoverList'))
        for index in range(needToPlay):
            self.mainWindow()
            toPlay = self.driver.find_elements(By.CLASS_NAME, 'interestingHoverList')[index]
            self.classLearn(toPlay)
            try:
                self.mainWindow()
                toPlay = self.driver.find_elements(By.CLASS_NAME, 'interestingHoverList')[index]
                self.faceToFaceClass(toPlay)
                self.mainWindow()
                toPlay = self.driver.find_elements(By.CLASS_NAME, 'interestingHoverList')[index]
                if self.flag: self.quest.startAnswer(toPlay)
            except: pass
        print("学习结束".center(60, '-'))
        self.driver.quit()
        sys.exit()

    def classLearn(self, toPlay):
        
        print("-" * 60)
        className = toPlay.find_element(By.CLASS_NAME, 'courseName')
        try: toPlay.find_element(By.CLASS_NAME, 'right-item-course')
        except: 
            print(f"【{className.text}】 该课程尚未开始 跳过")
        else:
            print(f"开始学习课程: 【{className.text}】")
            className.click()
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tabTitle')))
            sleep(1.5)
            self.complexCaptchaCheck()
            toFinish = self.driver.find_elements(By.CLASS_NAME, 'time_ico_half')
            hasFinish = self.driver.find_elements(By.CLASS_NAME, 'time_icofinish')
            progressNum = self.driver.find_elements(By.CLASS_NAME, 'progress-num')
            progressNum = [x for x in progressNum if int(x.text.strip("%")) > 82]
            if len(toFinish) == len(hasFinish) or len(toFinish) == len(progressNum): pass
            else:
                uls = self.driver.find_elements(By.TAG_NAME, 'ul')
                true_uls = [x for x in uls if x.get_attribute('class') == "list"]
                for ul in true_uls:
                    print('-' * 64)
                    classes = ul.find_elements(By.TAG_NAME, 'li')[: -1]
                    for per_class in classes:
                        self.complexCaptchaCheck()
                        print(" ".join(per_class.text.split()), end=" ")
                        try:
                            if int(per_class.find_element(By.CLASS_NAME, 'progress-num').text.strip("%")) >= 82:
                                print("完成")
                                continue
                        except: 
                            try:
                                per_class.find_element(By.CLASS_NAME, 'time_ico_half')
                            except: 
                                print("完成")
                                continue
                        if len(per_class.find_elements(By.CLASS_NAME, "time_icofinish")) == 1:
                            print("完成")
                            continue
                        sleep(0.5)
                        per_class.click()
                        sleep(1.5)
                        self.speedChange()
                        while True:
                            self.complexCaptchaCheck()
                            try:
                                if len(per_class.find_elements(By.CLASS_NAME, 'time_icofinish')) == 1:
                                    break
                            except: pass
                            try:
                                class_progress = per_class.find_element(By.CLASS_NAME, 'progress-num').text
                                if int(class_progress.strip("%")) >= 82:
                                    break
                            except: pass
                            print(f"\r{' '.join(per_class.text.split())}", end=" ")
                        print("完成")
                sleep(0.5)
            print('-' * 60)
            print("【1】章节视频学习完成")

    def faceToFaceClass(self, toPlay):

        toPlay.find_elements(By.CLASS_NAME, "course-menu-w")[-1].click()
        sleep(2.5)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        try: 
            face_classes = [x for x in self.driver.find_elements(By.CLASS_NAME, 'melightgreen_color') if x.text == "回放"]
            tmp_url = self.driver.current_url
            for index in range(len(face_classes)):
                if self.driver.current_url != tmp_url: 
                    self.driver.get(tmp_url)
                    sleep(1.5)
                face_classes = [x for x in self.driver.find_elements(By.CLASS_NAME, 'melightgreen_color') if x.text == "回放"]
                face_classes[index].click()
                sleep(1.5)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                video_list = self.wait.until(EC.presence_of_element_located((By.ID, 'videoList')))
                videos = video_list.find_elements(By.CLASS_NAME, 'videomenu')
                progress_temp = [video for video in videos if int(video.find_element(By.TAG_NAME, 'span').text.strip("%")) >= 82]
                if len(progress_temp) == len(videos): continue
                for video in videos:
                    video.click()
                    sleep(1)
                    self.speedChange(areaClick=True)
                    while True:
                        progress = video.find_element(By.TAG_NAME, 'span').text
                        print(f"\r【2】见面课进度: {progress}", end=" ")
                        if int(progress.strip("%")) > 82:
                            break
                    print("\r【2】见面课进度已达80% 学习完成")
        except: print("【2】暂无见面课可观看.")
        else: print('【2】见面课播放完毕')
        
    def speedChange(self, areaClick=False):
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'videoArea'))).click()
            sleep(0.5)
            self.driver.find_element(By.CLASS_NAME, 'speedBox').click()
            self.driver.find_element(By.CLASS_NAME, 'speedTab15').click()
            self.driver.find_element(By.CLASS_NAME, 'volumeIcon').click()
            if areaClick: 
                sleep(0.5)
                self.driver.find_element(By.CLASS_NAME, 'videoArea').click()
        except: pass      

    def complexCaptchaCheck(self):

        try:
            while self.net.passComplexCaptcha():
                pass 
        except: pass

    def errorCheck(self):

        while True:
            try: self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[6]/div[2]/div[1]/i').click()
            except: pass
            try:
                self.driver.find_elements(By.CLASS_NAME, 'item-topic')[0].click()
                self.driver.find_element(By.CLASS_NAME, 'btn-content').click()
            except: pass
            try:
                numbers = self.driver.find_element(By.CLASS_NAME, 'el-pager').find_elements(By.CLASS_NAME, "number")
                for number in numbers:
                    number.click()
                    self.driver.find_elements(By.CLASS_NAME, 'item-topic')[0].click()
                self.driver.find_element(By.XPATH, '//*[@id="playTopic-dialog"]/div/div[3]/span/div').click()
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'videoArea'))).click()
            except: pass
            try: self.driver.find_element(By.CLASS_NAME, 'popbtn_yes').click()
            except: pass
            try: self.driver.find_element(By.CLASS_NAME, 'popboxes_close').click()
            except: pass
            try: 
                true_i = [x for x in self.driver.find_elements(By.TAG_NAME, 'i') if x.get_attribute("class") == 'el-icon-error']
                true_i[-1].click()
            except: pass
            if len(self.driver.window_handles) > 2:
                for window in self.driver.window_handles[: -2]:
                    self.driver.switch_to.window(window)
                    self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])

            sleep(0.1)  

def login():
    username = input("输入手机号:")
    mm = input("输入密码:")
    y_n = input("是否保存用户:[y/n]")
    if y_n.lower() == 'y':
        log = open("../user.txt", '+w')
        log.write(username + '\n')
        log.write(mm)
        log.close()
    treeSolution(username, mm)

if __name__ == "__main__":
    if path.exists('../user.txt'):
        if len(sys.argv) > 1:
            if sys.argv[1] == "-y": y_n = 'y'
        else: y_n = input("发现已有用户, 是否选择登入:[y/n]")
        arg = sys.argv[-1] if sys.argv[-1] == "--headless" else None
        if y_n.lower() == 'y':
            log = open("../user.txt", 'r')
            username = log.readline().strip()
            mm = log.readline().strip()
            treeSolution(username, mm, arg)
        else: login()
    else: login()
        