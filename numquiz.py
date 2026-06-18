import random
import subprocess
from num2words import num2words
from blib.cosmetics import check, cross

import subprocess

def speak_uk(text, rate=140):
    # Speak the text using the Lesya voice in the background
    subprocess.Popen(
        ["say", "-v", "Lesya", "-r", str(rate), text]
    )

def run_quiz():
    while True:

        number = random.randint(10, 10000)

        text = num2words(number, lang='uk')

        speak_uk(text)

        while True:
            answer = input("> ").strip()

            if answer == "r" or len(answer) == 0:
                speak_uk(text)
                continue
            elif answer.lower() == 'q':
                break

            break

        if answer.lower() == 'q':
            break

        print(text)

        if answer == str(number):
            print(f"{check} Correct")
        else:
            print(f"{cross} Incorrect ({number})")


if __name__ == "__main__":
    run_quiz()
