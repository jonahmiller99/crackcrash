from selenium import webdriver
import requests
import time
from time import sleep
import csv

global stack
stack = []
global counter
counter = 0


# organize all of our multipliers using a "stack"
def addToStack(number):
    if(len(stack) != 0 and stack[len(stack) - 1][0] == number[0]):
        return
    else:
        stack.append(number)


# parse html with selenium
driver = webdriver.Chrome('/Users/jonahmiller/Downloads/chromedriver')
driver.get("https://roobet.com/crash")

# wait for page to load
time.sleep(5)
# sleep(3)
# using css selector to find the location of the "x" button... there is no id
# I can find that css code with inspect but it changes all the time? i dont know why.... and it is very random
css_loc = driver.find_element_by_css_selector('.MuiButtonBase-root-656')
css_loc.click()


# while timer < x mins check top multiplier value and addToStack
runtime = time.time() + 86400

while True:
    # find tick
    # This is is location of the most recent multiplier
    # To scrape I will need to pull this value every 6 seconds
    # checking most recent two elements to make sure I record duplicates correctly
    tick_elem = driver.find_element_by_css_selector('div.jss386:nth-child(1) > button:nth-child(1) > span:nth-child(1)')
    tick_elem2 = driver.find_element_by_css_selector('div.jss386:nth-child(2) > button:nth-child(1) > span:nth-child(1)')

    tick_value = tick_elem.get_attribute('innerHTML')
    tick_value2 = tick_elem2.get_attribute('innerHTML')
    # convert tick
    # get rid of x and save actual float value
    tick_value_float = float(tick_value[0:len(tick_value) - 1])
    tick_value2_float = float(tick_value2[0:len(tick_value2) - 1])
    print(tick_value_float)

    # check to see if there is an actual duplicate (if yes append it)
    if tick_value2_float == tick_value_float:
        duplicate_pair = (tick_value2_float, time.time())

        counter += 1
        stack.append(duplicate_pair)

    # wait for new number to appear... there is always at least 8 secs between games
    # also need to make sure cpu is not overloaded
    sleep(7)

    # add to stack value and time
    stack_tupe = (tick_value_float, time.time())
    addToStack(stack_tupe)

    if time.time() > runtime:
        break


driver.close()


# create a list of only multiplier values
multiplier_no_times = []

for i in range(len(stack)):
    val = stack[i]
    multiplier_no_times.append(val)


# write our data to a csv so we can analyze later
with open('crash_data.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(map(lambda x: [x], multiplier_no_times))

print(stack)

