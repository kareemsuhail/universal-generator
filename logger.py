from termcolor import colored
from colorama import init


class Logger():
    def __init__(self, message="", type="info", ):
        self.message_types = {
            "error": {
                "term": "Error:",
                "term-color": "white",
                "term-background": "on_red",
                "message-color": "red",
                "message": message
            },
            "hint": {
                "term": "Hint:",
                "term-color": "white",
                "term-background": "on_blue",
                "message-color": "blue",
                "message": message
            },
            "info": {
                "term": "Info:",
                "term-color": "white",
                "term-background": "on_blue",
                "message-color": "blue",
                "message": message
            },
            "progress": {
                "term": "Progress:",
                "term-color": "white",
                "term-background": "on_green",
                "message-color": "green",
                "message": message
            },
            "warning": {
                "term": "Warning:",
                "term-color": "white",
                "term-background": "on_yellow",
                "message-color": "yellow",
                "message": message
            }

        }
        self.type = type

    def show(self):
        init()
        message = self.message_types[self.type]
        print(colored(message['term'], message['term-color'], message['term-background']), end=' ')
        print(colored(message['message'], message['message-color']))
