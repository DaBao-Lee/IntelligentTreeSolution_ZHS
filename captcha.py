from __init__ import *

class passCaptcha:

    def __init__(self, driver, wait, action, easy_model: str="", complex_model: str=""):

        self.driver = driver
        self.wait = wait
        self.action = action
        self.easyModel = ort.InferenceSession(easy_model)
        self.model_path = complex_model

    def passEasyCaptcha(self) -> bool:

        bytes = self.driver.find_element(By.CLASS_NAME, 'yidun_bgimg').screenshot_as_png
        img = cv2.imdecode(np.frombuffer(bytes, dtype=np.uint8), 1)
        h, w = img.shape[:-1]
        input_name = self.easyModel.get_inputs()[0].name  
        output_name = self.easyModel.get_outputs()[0].name 
        img_c = cv2.resize(img, (640, 640))
        img_c = img_c.astype(np.float32) / 255
        img_c = img_c.transpose([2, 0, 1])[None,]
        result = self.easyModel.run([output_name], {input_name: img_c})[0][0].transpose([1, 0])
        boxes, conf = [], []
        for layer in result:
            score = layer[-1]
            if score > 0.05:
                x_c, y_c, w1, h1 = (layer[:-1] / 640) * np.array([w, h, w, h])
                x = x_c - w1 // 2
                y = y_c - h1 // 2
                boxes.append((x, y, w1, h1))
                conf.append(score)
        index = cv2.dnn.NMSBoxes(boxes, conf, score_threshold=0.5, nms_threshold=0.4)
        try:
            index = index[0] if len(index) > 0 else 0
            x, y, w, h = np.int_(boxes[index])
        except: x = 10
        e = self.driver.find_element(By.XPATH, '/html/body/div[33]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[2]')
        self.action.click_and_hold(e).perform()
        self.action.move_by_offset(xoffset=x+8, yoffset=0).perform()
        self.action.release().perform()
        sleep(1)
        try:
            while self.passComplexCaptcha(condition=('By.XPATH', '/html/body/div[34]/div[2]/div/div/div[2]/div/div[1]/div/div[1]')):
                    pass
        except: pass
        if len(self.driver.find_elements(By.CLASS_NAME, 'yidun_modal__title')):
            return True
        else: 
            return False

    def passComplexCaptcha(self, condition: tuple=("By.CLASS_NAME", "yidun_bgimg")) -> bool:

        self.driver.switch_to.window(self.driver.window_handles[-1])
        color_dict = {0: "蓝", 1: "灰", 2: "绿", 3: "红", 4: "黄"}
        bytes = self.driver.find_element(eval(condition[0]), condition[1]).screenshot_as_png
        img = cv2.imdecode(np.frombuffer(bytes, dtype=np.int8), 1)
        if condition[0] != "By.CLASS_NAME":
            description = self.driver.find_elements(By.CLASS_NAME, 'yidun-fallback__tip')[-1].text
        else: description = self.driver.find_element(By.CLASS_NAME, 'yidun-fallback__tip').text
        complexModel = YOLO(self.model_path, task="detect", verbose=False)
        colorModel = YOLO("data/colorDetect.pt", task="classify", verbose=False)
        orcModel = ddddocr.DdddOcr(show_ad=False, use_gpu=True)
        result = complexModel.predict(img)[0].boxes
        segmentPosiveimg, segmentSideimg = [], []

        for index in range(len(result.xyxy)):
            x1, y1, x2, y2 = np.intp(result.xyxy[index].cpu())
            segmentImg = img[y1-5: y2+5, x1-5: x2+5]
            color = colorModel.predict(segmentImg, verbose=False)[0].probs.top1
            segmentImage = Image.fromarray(segmentImg)
            text = orcModel.classification(segmentImage)
            if text == "0": text = "o"
            if text == '' and "体" not in description: text = 'i'
            if "0" in description: description = description.replace("0", "o")
            
            if result.cls[index] == 0:
                segmentPosiveimg.append({text: [color_dict[color], (x1, y1, x2, y2)]})
            else: segmentSideimg.append({text: [color_dict[color], (x1, y1, x2, y2)]})

        alpha = [x for x in description if x.isascii()]
        answer = None
        # 仅考虑朝向
        if len(alpha) == 1 and "色" not in description:
            target = alpha[0].lower()
            if "侧" not in description:
                for item in segmentPosiveimg:
                    key = list(item.keys())[0].lower()
                    if key == target:
                        answer = item
            else:
                for item in segmentSideimg:
                    key = list(item.keys())[0].lower()
                    if key == target:
                        answer = item
        # 立方体乱入
        elif len(alpha) == 0 and "色" not in description and ("体" in description or "柱" in description or "锥" in description or "球" in description):
            segmentPosiveimg.extend(segmentSideimg)
            for item in segmentPosiveimg:
                key = list(item.keys())[0].lower()
                if key == '':
                    answer = item
        # 仅考虑颜色
        elif len(alpha) == 1 and "向" not in description:
            target = alpha[0].lower()
            target_color = description.split("色")[0][-1]
            segmentPosiveimg.extend(segmentSideimg)
            for item in segmentPosiveimg:
                key = list(item.keys())[0].lower()
                color = list(item.values())[0][0]
                if key == target and color == target_color:
                    answer = item
        # 立方体乱入
        elif len(alpha) == 0 and "向" not in description and ("体" in description or "柱" in description or "锥" in description or "球" in description):
            segmentPosiveimg.extend(segmentSideimg)
            for item in segmentPosiveimg:
                key = list(item.keys())[0].lower()
                if key == '':
                    answer = item
        # 考虑朝向和颜色 alpha: 2
        elif len(alpha) == 2 and "向" in description and "色" in description:
            target = alpha[0].lower()
            target1 = alpha[1].lower()
            target_color = description.split("色")[0][-1]
            for item in segmentPosiveimg:
                key = list(item.keys())[0].lower()
                color = list(item.values())[0][0]
                if key == target and color == target_color:
                    for item in segmentPosiveimg:
                        key = list(item.keys())[0].lower()
                        if key == target1:
                            answer = item
            for item in segmentSideimg:
                key = list(item.keys())[0].lower()
                color = list(item.values())[0][0]
                if key == target and color == target_color:
                    for item in segmentSideimg:
                        key = list(item.keys())[0].lower()
                        if key == target1:
                            answer = item
        # 考虑颜色不考虑朝向
        elif len(alpha) == 2 and "色" in description and "向" not in description:
            target = alpha[0].lower()
            target1 = alpha[1].lower()
            segmentPosiveimg.extend(segmentSideimg)
            for item in segmentPosiveimg:
                key = list(item.keys())[0].lower()
                if key == target:
                    target_color = list(item.values())[0][0]
                    for item in segmentPosiveimg:
                        key = list(item.keys())[0].lower()
                        color = list(item.values())[0][0]
                        if key == target1 and color == target_color:
                            answer = item
        # 考虑朝向不考虑颜色
        elif len(alpha) == 2 and "向" in description and "色" not in description:
            target = alpha[0].lower()
            target1 = alpha[1].lower()
            for item in segmentPosiveimg:
                key = list(item.keys())[0].lower()
                if key == target:
                    for item in segmentPosiveimg:
                        key = list(item.keys())[0].lower()
                        if key == target1:
                            answer = item
            for item in segmentSideimg:
                key = list(item.keys())[0].lower()
                if key == target:
                    for item in segmentSideimg:
                        key = list(item.keys())[0].lower()
                        if key == target1:
                            answer = item
        if answer is None: 
            answer = {"随心": ["彩", (0, 0, 0, 0)]}
        x1, y1, x2, y2 = np.intp(list(answer.values())[0][1])
        img = self.driver.find_element(eval(condition[0]), condition[1])
        self.action.move_to_element_with_offset(img, xoffset=-160+(x1+x2)//2,
                                                    yoffset=-78+(y1+y2)//2).click().perform()
        sleep(1.5)
        if len(self.driver.find_elements(eval(condition[0]), condition[1])) != 0:
            return True
        else: return False
            