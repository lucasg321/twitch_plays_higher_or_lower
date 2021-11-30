import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

driver_path = 'C:/Users/sens_/Documents/twitch-plays-highrorlower/chromedriver'
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("load-extension=C:/Users/sens_/AppData/Local/Google/Chrome/User Data/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/4.34.0_0")
driver = webdriver.Chrome(options=options, executable_path=driver_path)
driver.get("http://www.higherlowergame.com/")
time.sleep(4) # TODO try catch here
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[0])
time.sleep(2)
driver.find_elements_by_xpath("//*[@id='root']/div/span/section/div[2]/div/button[1]")[0].click()
time.sleep(1)

f = open("highscore.txt","r")
high_score = f.readline()
f.close()


def parse_data(file_name):
    global high_score

    keywords = ['higher', 'lower']
    message_frequency = {}
    usernames = []

    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

        # Parse data in chat.log to only accept entries which follow a specific format, then turn those entries into an
        # easily interpretable format
        for line in lines:
            try:
                higher_button = driver.find_elements_by_xpath("//*[@id='root']/div/span/span/div/div[2]/div[2]/button[1]")
                lower_button = driver.find_elements_by_xpath("//*[@id='root']/div/span/span/div/div[2]/div[2]/button[2]")
                time_logged = line.split('—')[0].strip()
                time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')

                username_message = line.split('—')[1:]
                username_message = '—'.join(username_message).strip()

                username, channel, message = re.search(
                    ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message
                ).groups()

                # d = {
                #     'dt': time_logged,
                #     'channel': channel,
                #     'username': username,
                #     'message': message
                # }

                # Only allow users one vote per round - only counts their first vote
                #if username not in usernames:
                    #usernames.add(username)
                # Only tracks messages if they are an expected keyword
                if message in keywords:
                    # Increment the messages frequency in message_frequency or add it to message_frequency if it does not exist
                    if message not in message_frequency:
                        message_frequency[message] = 0
                    message_frequency[message] += 1

            except Exception:
                pass

        # Get the message with the highest frequency and click the appropriate button
        try:
            max_key = max(message_frequency, key=message_frequency.get)
        except:
            max_key = "error"

        if max_key == "higher":
            for btn in higher_button:
                try:
                    btn.click()
                except:
                    pass
            print("Higher")
        elif max_key == "lower":
            for btn in lower_button:
                try:
                    btn.click()
                except:
                    pass
            print("Lower")
        else:
            print("That's an error.")
            print("Recast your votes.")

    # Copy data from chat.log into chat-history.log and erase chat.log's data
    f1 = open('chat-history.log', 'a+')
    f2 = open(file_name, 'r')
    f1.write(f2.read())
    f1.close()
    f2.close()
    open(file_name, 'w').close()

    time.sleep(6)

    # Check if the game is lost, then reset it and update the high score if needed
    try:
        replay_btn = driver.find_element_by_xpath("//*[@id='game-over-btn']")
    except:
        replay_btn = None

    if replay_btn is not None:
        score = driver.find_element_by_xpath("//*[@id='root']/div/span/span/div/div/div[1]/p/span").text
        if score > high_score:
            high_score = score
            f = open("highscore.txt", "w")
            f.write(high_score)
            f.close()
            print("New high score of "+ high_score +"!")
        else:
            print("Chat's score is "+score)
            print("The high score is " + high_score)

        time.sleep(5)
        print("Playing again!")
        replay_btn.click()

    print("Cast your votes!")

    return


timer = datetime.utcnow()
prev_time = 0

while True:
    # Call the data parse function every minute
    seconds_since_timer = (datetime.utcnow() - timer).seconds

    # The 10 second count down, also only prints each number once
    if seconds_since_timer >= 20 and prev_time != seconds_since_timer:
        print(30 - seconds_since_timer)
        prev_time = seconds_since_timer

    if seconds_since_timer >= 30:
        print("Chat chooses...")
        time.sleep(3)
        parse_data('chat.log')
        timer = datetime.utcnow()

driver.close()