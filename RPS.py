# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)

    guess = "R"
    if len(opponent_history) > 2:
        guess = opponent_history[-2]

    return guess


def playervsquincy(prev_play, counter=[0]):

    counter[0] += 1
    choices = ["P", "P", "S", "S", "R"]
    return choices[counter[0] % len(choices)]


def playervsmrugesh(prev_opponent_play, opponent_history=[]):
    opponent_history.append(prev_opponent_play)
    last_five = opponent_history[-5:]
    most_frequent = max(set(last_five), key=last_five.count)

    if most_frequent == '':
        most_frequent = "R"

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[most_frequent]


def playervskris(prev_opponent_play, counter= [0]):
    if prev_opponent_play == '':
        prev_opponent_play = "P"

    counter[0] += 2
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return list(ideal_response.keys())[counter[0] % 3]

