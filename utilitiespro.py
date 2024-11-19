from textblob import TextBlob
import pandas as pd
import re
from cognitives import determine_sentiment, determine_category
import threading
import datetime


categories = ["Other", "ACCESS PRODUCTS", "CLOSURE PRODUCTS", "GUIDEWIRE PRODUCTS",
              "CATHETERS PRODUCTS", "EMBOLICS PRODUCTS", "PERIPHERAL INTERVENTION DEVICES",
              "CORONARY INTERVENTION DEVICES"]

# A thread-safe list to store the processed data
data_lock = threading.Lock()
processed_data = []


def process_text(text, source):
    """Process each text to determine sentiment and category."""
    # Determine sentiment
    sentiment = determine_sentiment(text)
    # Determine category
    category = determine_category(text, categories)
    
    # Add the results to the shared data list in a thread-safe manner
    with data_lock:
        processed_data.append([source, text, sentiment, category, "emotion"])


def process_data(source, texts):
    """Process a list of texts using multithreading."""
    start = datetime.datetime.now()
    print("start:", start)

    threads = []

    # Create threads for each text
    for text in texts:
        thread = threading.Thread(target=process_text, args=(text, source))
        print(thread)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end = datetime.datetime.now()
    print("end:", end)
    print("Processed data:", processed_data)
    print("duration:", end - start)
    
    return processed_data


def create_excel_report(data):
    """Create an Excel report from the processed data."""
    df = pd.DataFrame(data, columns=["Platform", "Text", "Sentiment", "Category", "Emotion"])
    df.to_excel("results.xlsx", index=False)
    print("File saved")
    
    # Open the saved Excel file in binary mode
    with open("results.xlsx", "rb") as f:
        file_data = f.read()
    
    return file_data


# Test Usage

test_text = ['Biden welcoming the 1st Indigenous Congresswomen in U.S. history; Deb Haaland NM & Sharice Davids KS', 'Wolfsburg fan reaction after Haaland does the pointing celebration towards him', 'Biden picks Rep. Deb Haaland (D-N.M.) to be first Native American interior secretary', "Dortmund [1]-0 Schalke 04 : Haaland 29'", 'Haaland sworn in wearing traditional Native American skirt, moccasins', "Dortmund [2]-1 PSG : Haaland 77'", 'Congresswoman Deb Haaland of New Mexico photographed with traditional wet plate process (2019)', 'Haaland misses his teammates', 'Erling Haaland mocking Ben Godfrey', "Slow-mo replay of Erling Haaland's flying backheel wonder goal against Sparta Prague", 'Haaland throws the ball at Gabriel after they score', "Deb Haaland says 'of course' she would serve as Interior secretary under Biden; she would be the first Native American in the Cabinet, and overseeing public lands.", '[Official] Erling Haaland joins Manchester City', "Schalke 0 - [2] Dortmund - Erling Haaland 45' (Great Goal)", '[OC] I watched and graded all of Messi’s 800 goals to determine their average quality (and distract myself from my breakup)', '[PSA] Kamala Harris vows to double federal minimum wage to $15', 'Haaland on not touching the ball enough times: "My dream is to touch the ball 5 times and score 5 goals."', '[Daily Mail] Jack Grealish on Erling Haaland: "He\'s the best professional I\'ve seen. Recovers. In the gym. 10 hours of treatment a day. Ice baths. Diet. I swear I couldn\'t be like that. After a game, he say: \'Hey. Don\'t go out tonight partying\'. I just tell him to shut up & go sit in his ice bath."', 'Haaland joins Dortmund', '[Official] Erling Haaland scores the most goals ever scored in a Premier League Season', 'Erling Haaland: "Just raw dogged a 7 hour flight. No phone, no sleep, no water, no food. Only map. easy."', '[Official] Erling Haaland breaks Man City club record for most goals scored in a single season.', 'Haaland gets double tackled in the air and proceeds as if nothing happened', 'Deb Haaland: ‘Of Course’ I’d Be Interested In Being Biden’s Interior Secretary - Tribal leaders are urging the president-elect to make history by picking the Native American congresswoman to oversee public lands', 'Fallon d’floor nominee: Haaland vs Barcelona | club friendly', 'The ref drops his spray foam and haaland picks it up in the middle of the attack and quickly hands it back.', 'Sen. Ted Cruz funneled campaign money into his own pocket - and other Republican misconduct piles up', 'Lucas Hernandez & Haaland square up to each other and then shake hands', '[Bild Sport via Sport Witness] - Chelsea have ‘little chance of signing’ Erling Haaland. The player does not want to take an intermediate step and instead wants to join ‘an absolute top club’ - Chelsea do not fit into this category.', 'Erling Haaland: "Tomorrow, I will wake up & think about to get 3 points against Leeds. I can\'t keep thinking about these records or else I would become crazy. I will go home, play some video games, eat something and then sleep... I cannot tell people what video games I play. It is too embarrassing."', 'Not One Republican Asked Deb Haaland About Her Vision For Indian Country | They quizzed the Cabinet nominee extensively about fossil fuels, showing what one Native American advocate called their “allegiance” to that industry.', 'Erling Haaland: "I have five hat-trick balls in my bed and I sleep well with them. They are my girlfriends"', '[Matt Law] Paris Saint-Germain are attempting to make an incredible last-minute swoop to replace Kylian Mbappe with Erling Haaland in what could complete one of the most remarkable ends to a transfer window in history.', 'Erling Haaland on was he upset with PSG players imitating his meditation pose:‘No, not really,’ ‘I think they helped me a lot to get meditation out in the world and to show the whole world that meditation is an important thing so I’m thankful that they helped me with that.’', "A boy invades the pitch to get Erling Haaland's autograph during friendly.", 'Cole Palmer tried listening into Manchester City’s huddle but Haaland pushed him away.', 'Erling Haaland finds a new fan', '[Premier League] Erling Haaland now holds the record for the most goals of any player in a 38-match PL season!', 'Graphic of most hat-tricks in the Premier League', 'Senate Confirms Progressive Climate and Native Champion Deb Haaland to Interior', '[Manchester City] Erling Haaland is the first player to score three consecutive home hat-tricks in the Premier League', '[Translation in comments] Former roommate on Haaland: "He watched Hannah Montana without feeling embarrassed at all and laughed heartily at it. Erling is a delightful person, and it was incredibly fun to live with him."', '[Official] Manchester City are delighted to confirm the signing of Erling Haaland from Borussia Dortmund.', "[Erling Haaland] I don't understand why there is still room for racism and discrimination. We will never tire of fighting against any form of discrimination. Instead of being applauded for having the courage to take the penalties, these young men are attacked with racist insults. I am speechless.", "'I'll be fierce for all of us': Deb Haaland on climate, Native rights and Biden", 'Reason for referees Haaland-autograph revealed: «Sovre has for years helped a center in the Bihor region for children and adults with severe forms of autism. The center is funded by donations and gifts, which are sold at an annual auction.»', 'Onana vs Haaland in the penalty shootout ', 'Emi Martinez double save against Haaland', 'Erling Haaland accidentally swearing in post match interview', 'Salzburgs Max Wober after Erling Haalands hat trick: "Erling is crazy. Last night our captain was walking with his daughter. Then a car stopped. Erling was inside. He rolled down the window. And there he was, listening to the Champions League anthem."']
data = process_data("Twitter", test_text)
create_excel_report(data)
