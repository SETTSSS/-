# encoding = utf-8
import time, os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def enter(url):
    # 登录
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    school_search = driver.find_element_by_id('quickSearch')
    school_search.send_keys('')  # 填入学校
    time.sleep(1)
    school_submit = driver.find_element_by_id('validataSchoolListDropCode')
    school_submit.click()
    time.sleep(1)
    user_id = driver.find_element_by_id('clCode')
    user_id.send_keys('')  # 添入学号
    time.sleep(1)
    user_password = driver.find_element_by_id('clPassword')
    user_password.send_keys('')  # 填入密码
    login = driver.find_element_by_class_name('wall-sub-btn')
    login.click()
    time.sleep(1)
    print('登录完成')

    # 选课
    def course_select():
        n = 0
        course_list = driver.find_elements_by_class_name('courseName')
        for i in course_list:
            n = n + 1
            print('课程名称为%s序号为%d' % (i.text, n))
        course_key = input('输入课程名称后的序号请确保为数字：')
        return course_key

    driver.find_elements_by_class_name('courseName')[int(course_select()) - 1].click()
    time.sleep(1)
    driver_lock = driver.window_handles[-1]
    driver.switch_to.window(driver_lock)
    time.sleep(2)
    print('已经进入观看')
    # 取消警告弹窗
    close_1 = driver.find_element_by_xpath('/html/body/div[1]/div/div[6]/div/div[3]/span/button')
    close_2 = driver.find_element_by_xpath('/html/body/div[1]/div/div[7]/div[2]/div[1]/i')
    close_3 = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/span/a')
    try:
        close_1.click()
        print('第一弹窗关闭')
        time.sleep(1)
        close_2.click()
        time.sleep(2)
        close_3.click()
        time.sleep(1)
    except Exception:
        print("捕捉弹题")
        answer = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]/span')
        answer.click()
        time.sleep(1)
        print('已答题')
        close_exam = driver.find_element_by_xpath('/html/body/div[1]/div/div[7]/div/div[3]/span/div')
        close_exam.click()
        print('已关闭')
        time.sleep(1)
        close_2.click()
        time.sleep(1)
        close_3.click()
        time.sleep(1)
        js = "var q= document.getElementsByClassName('controlsBar')[0];q.style.display ='block';"
        driver.execute_script(js)
        play_button = driver.find_element_by_id('playButton')
        play_button.click()
    judgement = driver.find_element_by_id('playButton').get_attribute('class')
    play_button = driver.find_element_by_id('playButton')
    js = "var q= document.getElementsByClassName('controlsBar')[0];q.style.display ='block';"
    speed_js = "var a=document.getElementsByClassName('speedBox')[0];a.span ='X 1.5' "
    print('按钮定位成功')
    play_button = driver.find_element_by_id('playButton')
    while judgement == 'playButton':
        print("")
        try:
            answer = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]/span')
            answer.click()
            time.sleep(1)
            print('已答题')
            close_exam = driver.find_element_by_xpath('/html/body/div[1]/div/div[7]/div/div[3]/span/div')
            close_exam.click()
            print('已关闭')
            time.sleep(1)
            driver.execute_script(js)
            play_button.click()
            break
        except Exception:
            print("错误已经处理")
            driver.execute_script(js)
            play_button.click()
            break
    time.sleep(1)
    print('所有初始弹窗关闭')
    # 调试清晰度音量
    driver.execute_script(js)
    play_volume = driver.find_element_by_class_name('volumeBox')
    play_volume.click()
    print('已经静音')
    time.sleep(3)
    try:
        driver.execute_script(js)
        play_speed = driver.find_element_by_xpath('//*[@id="vjs_container"]/div[10]/div[8]')
        play_speed.click()
        driver.find_element_by_xpath('//*[@id="vjs_container"]/div[10]/div[8]/div/div[1]').click()
        print('已经开启赛亚人模式')
        driver.execute_script(speed_js)
    except Exception:
        print("加速失败尝试重新加速")
        js_speed = "if (!/1\.5/.test($('.speedBox').attr('style'))) {console.log('提升到1.5倍速')$('.speedTab15').click()}"
        driver.execute_script(js_speed)
    # 播放和取消弹窗
    next_button = driver.find_element_by_class_name('nextButton')
    end_time = driver.find_element_by_xpath('//*[@id="vjs_container"]/div[10]/div[4]/span[2]').text
    print('结束时间为%s' % end_time)
    # interval = input('持续时间，单位为分钟：')
    for _ in range(3000):
        driver.execute_script(js)
        current_time = driver.find_element_by_xpath('//*[@id="vjs_container"]/div[10]/div[4]/span[1]').text
        print('现在时间为%s' % current_time)
        time.sleep(5)
        driver.execute_script(js)
        judgement = driver.find_element_by_id('playButton').get_attribute('class')
        time.sleep(5)
        current_time = driver.find_element_by_xpath('//*[@id="vjs_container"]/div[10]/div[4]/span[1]').text
        while current_time == end_time:
            print('准备进入下一章节')
            driver.execute_script(js)
            next_button.click()
            print('进入下一章节')
            try:
                driver.execute_script(js)
            except TypeError:
                time.sleep(5)
                js_2 = "var q= document.getElementsByClassName('controlsBar')[0];q.style.display ='block';"
                driver.execute_script(js_2)
            play_volume = driver.find_element_by_class_name('volumeBox')
            play_volume.click()
            time.sleep(2)
            print('已经静音')
            driver.execute_script(js)
            play_speed = driver.find_element_by_xpath('//*[@id="vjs_container"]/div[10]/div[8]')
            play_speed.click()
            driver.find_element_by_xpath('//*[@id="vjs_container"]/div[10]/div[8]/div/div[1]').click()
            print('已经开启赛亚人模式')
            break
        play_button = driver.find_element_by_id('playButton')
        while judgement == 'playButton' and current_time != end_time:
            answer = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[7]/div/div[2]/div/div[1]/div/div/div[2]/ul/li[1]/span')
            answer.click()
            time.sleep(1)
            close_exam = driver.find_element_by_xpath('/html/body/div[1]/div/div[7]/div/div[3]/span/div')
            close_exam.click()
            time.sleep(1)
            driver.execute_script(js)
            play_button.click()
            print('弹窗取消')
            break


def main():
    url = 'https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin#studentID'
    enter(url)


if __name__ == '__main__':
    main()
