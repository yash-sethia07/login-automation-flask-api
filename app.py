from flask import Flask

import time
import pickle
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import cv2
import pytesseract
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/icegate-login')
def icegatelogin():
    driver = webdriver.Chrome(ChromeDriverManager().install())  # Optional argument, if not specified will search path.

    driver.get('https://old.icegate.gov.in/iceLogin/loginAction');
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))



    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)


    username_input = driver.find_element("id", "login_icegate_id")
    username_input.clear()


    password_input = driver.find_element("id", "password")
    password_input.clear()

    username_input.send_keys("Yash")
    time.sleep(5)
    password_input.send_keys("Sethia")

    captcha_img = driver.find_element("id", "capimg")
    captcha_img.screenshot("captcha.png")

    time.sleep(5)
    driver.quit()

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    img = cv2.imread("captcha.png")

    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (h, w) = gry.shape[:2]
    gry = cv2.resize(gry, (w*2, h*2))

    cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
    thr = cv2.threshold(cls, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    txt = pytesseract.image_to_string(img)

    return txt


# OCR for captcha needs to be integrated
@app.route('/dgft-login')
def login():
    drv = webdriver.Chrome()

    drv.get("https://www.dgft.gov.in/CP/?opt=services#")
    pickle.dump(drv.get_cookies(), open("cookies1.pkl", "wb"))



    cookies = pickle.load(open("cookies1.pkl", "rb"))
    for cookie in cookies:
        drv.add_cookie(cookie)

        
    #object of ActionChains
    a = ActionChains(drv)


    #identify element 
    dashboard = drv.find_element("id", "mydashboard")

    #hover over element
    a.move_to_element(dashboard).perform()



    login_btn = drv.find_element("link text", "Log In")
    a.move_to_element(login_btn).click().perform()

    time.sleep(3)

    # username ; password ; captcha

    uname_input = drv.find_element("id", "username")
    uname_input.clear()

    pass_input = drv.find_element("id", "password")
    pass_input.clear()

    uname_input.send_keys("Yash")
    time.sleep(2)
    pass_input.send_keys("Sethia")

    captcha_img = drv.find_element("id", "captcha")
    captcha_img.screenshot("captcha1.png")


    time.sleep(5)
    drv.quit()






if __name__ == '__main__':
    app.run(debug=True)
