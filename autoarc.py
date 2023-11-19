from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

#pip install selenium
#pip install webdriver-manager
# 크롬 드라이버 설치 하셈 

id = '아이디'
pw = '비번'
mul = 2 #배수
StartMoney = 100 #시작금액
stoplose = 15  #연패시 종료
bet = True #실제 베팅여부
mute = True #소리 끄기

options = webdriver.ChromeOptions()
# headless 옵션 설정
#options.add_argument('headless') #윈도우 숨기기 필요하면 주석해제
options.add_argument("no-sandbox")

# 브라우저 윈도우 사이즈
options.add_argument('window-size=1920x1080')

# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정


#options.headless = False

# 드라이버 위치 경로 입력
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=options)

driver.get('https://arca.live/u/login?goto=%2Fb%2Fthermometer')
driver.implicitly_wait(3)

driver.find_element(By.NAME, 'username').send_keys(id)
driver.find_element(By.ID, 'submitBtn').click()
time.sleep(1)
driver.find_element(By.NAME, 'password').send_keys(pw)
driver.find_element(By.ID, 'submitBtn').click()
time.sleep(1)


if mute == True:
    driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/article/div[1]/div[1]/div/div/span[1]').click()


countElement = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/article/div[1]/div[1]/div/div/div[2]/div[1]')


CurrentMoney = StartMoney
LastCount = countElement.text.split('회차')[0]
win = 0
lose = 0
wincount = 0
losecount = 0
maxlose = 0
maxlosecnt = 0
init = False

while True:
    countElement = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/article/div[1]/div[1]/div/div/div[2]/div[1]')
    CurrentCount = countElement.text.split('회차')[0]
    if (LastCount != CurrentCount):
        
        resultElement = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/article/div[1]/div[1]/div/div/div[2]/div[4]/div[1]')
        
        if (init == False):
            init = True
        elif ( '홀' not in resultElement.text or '폭발' in resultElement.text):
            lose += CurrentMoney
            CurrentMoney *= mul
            losecount += 1
            maxlosecnt +=1
            if maxlosecnt > maxlose:
                maxlose = losecount
            
        else:
            win += CurrentMoney * 0.99
            CurrentMoney = StartMoney
            wincount += 1
            maxlosecnt = 0
        
        if losecount >= stoplose:
            break
        
        LastCount = CurrentCount
        print('win : ' + str(wincount) + ' lose : ' + str(losecount))
        print('win money : ' + str(win) + ' lose money : ' + str(lose))
        print('total : ' + str(win - lose))
        print('결과 : ' + resultElement.text)
        print('베팅금액 : ' + str(CurrentMoney))
        print('최대 연패 : ' + str(maxlose) + ', 금액 : ' + str(StartMoney * pow(mul, maxlose) if maxlose else  0) + '\n')
        if bet == True:
            driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/article/div[1]/div[2]/form/div/div[2]/input').send_keys(str(CurrentMoney))
            driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/article/div[1]/div[2]/form/div/div[3]/div[2]/p[3]/span[1]').click()
    
    time.sleep(1)


