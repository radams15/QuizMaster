import re
import json

import requests

SAVE_FILE = "questions.json"

general_knowledge = ["http://freepubquiz.weebly.com/general-knowledge-{}.html".format(x) for x in range(1, 7)]
food_and_drink = ["http://freepubquiz.weebly.com/food--drink-{}.html".format(x) for x in range(3, 4)]
film_and_tv = ["http://freepubquiz.weebly.com/film--tv-{}.html".format(x) for x in range(1,2)]
question_regex = re.compile(r"(\d+\.(?:&nbsp;)? .*<br \/>)")

all_questions = {}

def get_questions(urls):
    i = 1
    qs = []
    for site in urls:
        data = requests.get(site).text
        matches = re.findall(question_regex, data)[0].replace("</div", "<span></span>").replace("<br />", "").replace("&nbsp;", "").split("<span></span>")

        questions = {}
        for match in matches:
            if (not match) or "BONUS QUESTION" in match or "ANSWERS" in match:
                continue
            match = match.split(".", 1)  # split, but only once

            num = int(match[0])
            q_or_a = match[1].strip()

            if num in questions.keys():
                questions[num][1] = q_or_a
            else:
                questions[num] = [q_or_a, None]

        questions = {i:q for i,q in questions.items() if q[1]}
        qs.append(questions)
        i += 1
    return qs

i=1

all_questions["general_knowledge"] = get_questions(general_knowledge)
all_questions["food_and_drink"] = get_questions(food_and_drink)
all_questions["film_and_tv"] = get_questions(film_and_tv)

out = []

for category, qs in all_questions.items():
    set_num = 1
    for set in qs: # question set
        for num, data in set.items():
            out.append([data[0], data[1], category, set_num, num])
        set_num += 1
with open(SAVE_FILE, "w") as f:
    json.dump(out, f)