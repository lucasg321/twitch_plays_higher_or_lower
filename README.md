# Twitch Plays Higher or Lower
An interactive game made for Twitch.

### Description: 
Twitch chat gets to play the infamous Higher or Lower game (http://www.higherlowergame.com/) as a hivemind. The viewer simply has to type higher or lower in the chat and the application will tally the votes every thirty seconds. Afterwards, it will select the answer that was voted the most. Current score and high score is also recoreded.

### Languages/Libraries/Frameworks: 
Python, Selenium

### Explanation: 
The application revolves around two python scripts. One creates a socket connection between itself and the Twitch chat and writes every message to a file. The other reads the data from the file every thirty seconds, parses it with Regex, and counts the amount of higher or lower votes. Once the tally is complete, the file is emptied and the higher or lower button on the website is clicked with Selenium. The program will recognize when a wrong answer is selected and will save the score into a file if it is a high score. 

### How it works:
Python is used for scripting and functionality. Selenium allows the application to interact with the higher or lower website. 

*See it work in real time! In chat_reader.py change _nickname = '' token = '' channel = ''_ to your channel information and the socket will read from your Twitch chat! 
