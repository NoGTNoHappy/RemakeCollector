import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


def get_content(driver):
    content = dict()
    lis = driver.find_elements_by_xpath("//ul[@id='lifeTrajectory']/*")
    for li in lis:
        texts = li.text.split("\n")
        age_str = texts[0]
        age = int(age_str[0:len(age_str) - 2])
        content[age] = texts[1]

    age = max(content.keys())
    return age, content


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
    res = dict()
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
    try:
        driver.get("https://liferestart.syaro.io/view/")
        try:
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "restart"))
            )
        except Exception:
            print("Can't load Remake Simulator for 10 seconds.")
            return

        age_dict = dict()
        for i in range(remake_times):
            age, contents = one_more_time(driver)
            age_count = age_dict.get(age, 0)
            age_count += 1
            age_dict[age] = age_count
            for age in contents.keys():
                content_set = res.get(age, set())
                content_set.add(contents[age])
                res[age] = content_set

        ages = list(age_dict.keys())
        ages.sort()
        with open("./remake.txt", "w", encoding="utf-8") as f:
            f.write("You remake %s time(s)." % remake_times_str)
            f.write("\n")

            f.write("Your shortest life is %d year(s) old." % ages[0])
            f.write("\n")
            f.write("Your longest life is %d year(s) old." % ages[len(ages) - 1])
            f.write("\n")

            for age in ages:
                f.write("%3d year(s) old: %d time(s)." % (age, age_dict[age]))
                f.write("\n")
            f.write("\n")

            age_list = list(res.keys())
            age_list.sort()
            for age in age_list:
                f.write("Age %d:" % age)
                f.write("\n")
                for life in res[age]:
                    f.write(life)
                    f.write("\n")

                f.write("\n")
    except Exception as e:
        print("Exception caught.")
        print(e)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
