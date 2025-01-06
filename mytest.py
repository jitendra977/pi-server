from gpiozero import Button
from signal import pause

def say_hello():
    print("hello im pressed how are you ")

button = Button(21)

button.when_pressed = say_hello

pause()