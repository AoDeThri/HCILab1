import time
import webbrowser

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from asrInterface import Ui_MainWindow
import speech_recognition as sr
import sys
import os
import requests


class RecognizerRunner(QThread):

    unrecognizedCommands = pyqtSignal(str)
    recognizedCommands = pyqtSignal(int, object)
    mainLabelReset = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.options = ["play music", "open notepad", "open browser", "check weather"]

    def run(self):
        self.interaction()

    def recognizeOrder(self):
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("'recognizer' must be 'Recognizer' instance")
        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("'microphone' must be 'Microphone' instance")

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        try:
            order = self.recognizer.recognize_sphinx(audio)
        except sr.RequestError:
            order = None
        except sr.UnknownValueError:
            order = None

        return order

    def execTask(self, index):
        r = None
        if index == 0:
            os.system("f1lcapae.wav")
        elif index == 1:
            os.system("notepad.exe")
        elif index == 2:
            webbrowser.open("www.baidu.com")
        elif index == 3:
            try:
                r = requests.get('http://www.weather.com.cn/data/cityinfo/101020100.html')
            except:
                r = None
            pass

        self.recognizedCommands.emit(index, r)
        time.sleep(10)
        self.mainLabelReset.emit()

    def interaction(self):
        while True:
            order = self.recognizeOrder()
            if order is None:
                continue
            else:
                order = order.lower()
            try:
                index = self.options.index(order)
                self.execTask(index)
            except ValueError:
                self.handleUnrecognizedCommands(order)
                continue

    def handleUnrecognizedCommands(self, order):
        # self.unrecognizedCommands.emit(order)
        self.execTask(3)
        time.sleep(5)
        self.mainLabelReset.emit()


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.recognizerRunner = RecognizerRunner()
        self.recognizerRunner.start()
        self.signalsBind()

    def signalsBind(self):
        self.recognizerRunner.unrecognizedCommands.connect(self.unrecognizedCommandsHandle)
        self.recognizerRunner.recognizedCommands.connect(self.recognizedCommandsHandle)
        self.recognizerRunner.mainLabelReset.connect(self.mainLabelResetHandle)

    def changeMainLabelText(self, tips):
        self.ui.label.setText(tips)

    def unrecognizedCommandsHandle(self, order):
        lengthLimit = 10
        if len(order) > lengthLimit:
            order = order[:lengthLimit] + "..."
        tips = f"Sorry, I can't understand '{order}' \n"\
               "Please try again in 5s."
        self.changeMainLabelText(tips)

    def mainLabelResetHandle(self):
        tips = "Hi! How can I help?"
        self.changeMainLabelText(tips)

    def recognizedCommandsHandle(self, order, r):
        tips = "Ok, I will "
        if order == 0:
            tips += "play a nice song!"
        elif order == 1:
            tips += "open the notepad!"
        elif order == 2:
            tips += "open the web browser!"
        elif order == 3:
            if r is not None and r.ok:
                wea = r.json()["weatherinfo"]
                tips = "The weather in Shanghai today:\n" \
                    f"{wea['weather'].encode('ISO-8859-1').decode('utf-8')}\n" \
                    f"{wea['temp1'].encode('ISO-8859-1').decode('utf-8')} ~ " \
                    f"{wea['temp2'].encode('ISO-8859-1').decode('utf-8')}"
            else:
                tips = "Network error, please check the network connection."
        self.changeMainLabelText(tips)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec())
