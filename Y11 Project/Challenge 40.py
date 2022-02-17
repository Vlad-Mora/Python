import random

lives = 3
score = 0

questionsAndAnswers = {
    "Question 1\nA. First answer\nB. Second answer\nC. Third answer\nD. Fourth answer": "A",
    "Question 2\nA. First answer\nB. Second answer\nC. Third answer\nD. Fourth answer": "B",
    "Question 3\nA. First answer\nB. Second answer\nC. Third answer\nD. Fourth answer": "C",
    "Question 4\nA. First answer\nB. Second answer\nC. Third answer\nD. Fourth answer": "D",
    "UsedQuestions": []
    }

print("""
For each question, please enter either A, B, C or D.
""")
def getQuestion():
    global questionsAndAnswers
    global score
    global lives
    randomNumber = random.randint(1, len(questionsAndAnswers) - 1)
    questions = []
    for key in questionsAndAnswers.keys():
        if key != "UsedQuestions":
            questions.append(key)
    if not randomNumber in questionsAndAnswers["UsedQuestions"]:
        questionsAndAnswers["UsedQuestions"].append(randomNumber)
        answer = input(questions[randomNumber - 1])
        if answer.upper() == questionsAndAnswers[questions[randomNumber - 1]]:
            print("Correct!")
            score += 1
        else:
            print("Wrong!")
            lives -= 1


while lives != 0:
    getQuestion()

print(f"""
You have ran out of lives.
Your final score was of {score}.
Congratulations and thank you for playing.
      """)
