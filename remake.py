from selenium import webdriver
import random


def get_content(driver):
    content_set = set()
    lis = driver.find_elements_by_xpath("//ul[@id='lifeTrajectory']/*")
    for li in lis:
        texts = li.text.split("\n")
        content_set.add(texts[1])
    return content_set


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

    once_set = get_content(driver)
    summary_btn.click()
    driver.find_element_by_id("again").click()
    return once_set


def main():
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.get("https://liferestart.syaro.io/view/")

    res_set = set()
    for i in range(10):
        for res in one_more_time(driver):
            res_set.add(res)

    with open("./remake.txt", "w", encoding="utf-8") as f:
        for life in res_set:
            f.write(life)
            f.write("\n")

    driver.close()


if __name__ == "__main__":
    main()
