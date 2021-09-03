from selenium import webdriver
import random


def get_content(driver):
    content_set = set()
    lis = driver.find_elements_by_xpath("//ul[@id='lifeTrajectory']/*")
    for li in lis:
        texts = li.text.split("\n")
        content_set.add(texts[1])

    age_str = lis[len(lis) - 1].text.split("\n")[0]
    age = int(age_str[0:len(age_str) - 2])
    return age, content_set


def one_more_time(driver):
    driver.find_element_by_id("restart").click()
    driver.find_element_by_id("random").click()
    talent_set = set()
    while len(talent_set) < 3:
        talent_set.add(int(random.random() * 10) + 1)

    driver.find_element_by_xpath("//ul[@id='talents']/li[" + str(talent_set.pop()) + "]").click()
    driver.find_element_by_xpath("//ul[@id='talents']/li[" + str(talent_set.pop()) + "]").click()
    driver.find_element_by_xpath("//ul[@id='talents']/li[" + str(talent_set.pop()) + "]").click()

    driver.find_element_by_id("next").click()
    driver.find_element_by_id("random").click()
    driver.find_element_by_id("start").click()

    summary_btn = driver.find_element_by_id("summary")
    while not summary_btn.is_displayed():
        driver.find_element_by_id("lifeTrajectory").click()

    age, once_set = get_content(driver)
    summary_btn.click()
    driver.find_element_by_id("again").click()
    return age, once_set


def main():
    res_set = set()
    print("Please input remake times:")
    remake_times_str = input()
    remake_times = 0
    while remake_times == 0:
        try:
            remake_times = int(remake_times_str)
        except ValueError:
            print("Please input a number.")

    if remake_times > 100 or remake_times < 0:
        print("Wrong number, needs 1~ 99")
        return

    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.get("https://liferestart.syaro.io/view/")
    age_max = 0
    for i in range(remake_times):
        age, contents = one_more_time(driver)
        if age > age_max:
            age_max = age
        for res in contents:
            res_set.add(res)

    with open("./remake.txt", "w", encoding="utf-8") as f:
        f.write("You remake " + remake_times_str + " time(s).")
        f.write("\n")
        f.write("Your longest life is " + str(age_max) + " years old.")
        f.write("\n")
        for life in res_set:
            f.write(life)
            f.write("\n")

    driver.close()


if __name__ == "__main__":
    main()
