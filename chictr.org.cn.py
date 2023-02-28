from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
import ddddocr
from pySelenium import PySelenium


class Run(PySelenium):
    # 验证码保存位置
    Code_Img_Path = './img/codeImg.png'

    # ------------------- 验证码处理 -------------------
    # ----<识别验证码并返回
    def discern_vfcode(self, Code_Img_Path=Code_Img_Path):
        ocr = ddddocr.DdddOcr()
        code_loc = self.driver.find_element(By.XPATH, './/input[@name="txtVerifyCode"]/following-sibling::img')
        code_loc.screenshot(Code_Img_Path)
        with open(Code_Img_Path, 'rb') as f:
            img_bytes = f.read()
        code = ocr.classification(img_bytes)
        return code

    # ----<碰到验证码后的处理方式
    def format_vfcode(self):

        # 验证码输入框
        code_input = (By.XPATH, './/div[@role="dialog"]//input[@name="txtVerifyCode"]')
        # 确认按钮
        code_submit = (By.XPATH, '//*[@id="btnSaveProRes"]')
        # 执行清空

        vfcode = self.discern_vfcode()  # 调用截取识别函数
        self.locator(code_input).clear()  # 输入验证码之前清空
        print(vfcode)
        # self.locator(code_input).send_keys(vfcode)  # 输入验证码
        # self.Enca_submit(code_submit)  # 点击确定

    # ----<验证码识别错误后的处理方式
    def error_vfcode(self):
        pass

    # ------------------- 解析 -------------------
    def get_data(self):
        pass

    # ------------------- 保存 -------------------
    def save_data(self):
        pass

    # ------------------- 翻页 -------------------
    def turn_pages(self):
        # 总页数
        page_count = int(
            self.locator((By.XPATH, '//*[@id="pgProj"]/span/label')).text.replace('第1页 共', '').replace('页', ''))
        # 每页的数量
        page_number = 10

        next_button = (By.XPATH, './/div[@class="pagearea"]/a[last()-1]')
        for page in range(0, page_count):
            print(f"---------------------第{page + 1}页")
            for data_index in range(2, page_number + 2):
                print(f"第{data_index - 1}条数据---------------------")
                this_data_link = (By.XPATH, f'.//table[@class="table_list"]//tr[{data_index}]/td[3]/p/a')
                try:
                    # 出现验证码时捕获异常并进行处理
                    self.locator(this_data_link).click()
                except ElementClickInterceptedException:
                    self.format_vfcode()
                # 进入数据详情
                self.forward()
                self.get_data()

                # info = (By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr[1]/td[2]')
                # info = self.locator(info).text
                # print(info)

                # 返回数据列表
                self.back_()
            # 点击下一页
            self.locator(next_button).click()


if __name__ == '__main__':
    url = 'http://d3d3LmNoaWN0ci5vcmcuY24=/searchproj.aspx'
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    start = Run(browser)
    start.max_win()
    start.visit_url(url)
    start.turn_pages()

    browser.quit()
