import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QIntValidator

class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Тест Руфье")

        self.layout = QVBoxLayout(self)
        
        self.layout.addWidget(QLabel("Тест Руфье-Диксона позволяет быстро проверить Вашу общую физическую подготовку, состояние Вашего сердца, а также степень нервного и физического переутомления."))
        self.layout.addWidget(QLabel("Чтобы войти нажмите на кнопку ниже"))

        # кнопка перехода на следующую страницу
        self.button = QPushButton("start")
        self.button.clicked.connect(self.second_win)

        self.layout.addWidget(self.button)
    
    def second_win(self):
        # переход на след. страницу
        self.newwidget = MainMeasurer()
        self.newwidget.show()
        self.hide()

# страница с рассчётами
class MainMeasurer(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.t3 = False

        self.activeTimer = QTimer()
        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.frame)
        self.updateTimer.start(50)

        self.layout = QHBoxLayout(self)

        self.vlayout = QVBoxLayout(self)
        self.layout.addLayout(self.vlayout)
        self.vlayout.addWidget(QLabel("Ф.И.О.:"))
        self.vlayout.addWidget(QLineEdit())
        self.vlayout.addWidget(QLabel("ИНН:"))
        self.vlayout.addWidget(QLineEdit())
        self.vlayout.addWidget(QLabel("Номер паспорта:"))
        self.vlayout.addWidget(QLineEdit())
        self.vlayout.addWidget(QLabel("Номер карточки:"))
        self.vlayout.addWidget(QLineEdit())
        self.vlayout.addWidget(QLabel("CVV код карточки:"))
        self.vlayout.addWidget(QLineEdit())
        self.vlayout.addWidget(QLabel("Пароль от телефона:"))
        self.vlayout.addWidget(QLineEdit())
        self.vlayout.addWidget(QLabel("Пароль от онлайн банкинга:"))
        self.vlayout.addWidget(QLineEdit())
        self.vlayout.addWidget(QLabel("Местоположение сейфа:"))
        self.vlayout.addWidget(QLineEdit())
        self.vlayout.addWidget(QLabel("Пароль от сейфа:"))
        self.vlayout.addWidget(QLineEdit())

        self.vlayout.addWidget(QLabel("Полных лет:"))
        self.age_input = QLineEdit("0")
        self.age_input.setValidator(QIntValidator())
        self.vlayout.addWidget(self.age_input)

        self.vlayout.addWidget(QLabel("Лягте на спину и замерьте пульс за 15 секунд. Нажмите на кнопку для запуска таймера. Результат укажите ниже."))

        self.timerstart1 = QPushButton("Начать таймер для замера пульса")
        self.timerstart1.clicked.connect(self.timerstart1clicked)
        self.vlayout.addWidget(self.timerstart1)

        self.pulse1 = QLineEdit("0")
        self.pulse1.setValidator(QIntValidator())
        self.vlayout.addWidget(self.pulse1)

        self.vlayout.addWidget(QLabel("Выполните 30 приседаний за 45 секунд. Не смогли? Лох. Нажмите на кнопку для запуска таймера. Результат укажите ниже."))

        self.timerstart2 = QPushButton("Начать таймер для приседаний")
        self.timerstart2.clicked.connect(self.timerstart2clicked)
        self.vlayout.addWidget(self.timerstart2)

        self.vlayout.addWidget(QLabel("Лягте на спину и замерьте пульс за первые 15 секунд минуты, потом за последние 15 секунд. Нажмите на кнопку для запуска таймера. Таймер будет зелёным, когда нужно мерить пульс. Результаты укажите ниже."))

        self.timerstart3 = QPushButton("Начать таймер для замеров пульса")
        self.timerstart3.clicked.connect(self.timerstart3clicked)
        self.vlayout.addWidget(self.timerstart3)

        self.pulse2 = QLineEdit("0")
        self.pulse2.setValidator(QIntValidator())
        self.vlayout.addWidget(self.pulse2)

        self.pulse3 = QLineEdit("0")
        self.pulse3.setValidator(QIntValidator())
        self.vlayout.addWidget(self.pulse3)

        self.calculate = QPushButton("Показать результат")
        self.calculate.clicked.connect(self.calculateclicked)
        self.vlayout.addWidget(self.calculate)

        self.timerlayout = QVBoxLayout(self)
        self.layout.addLayout(self.timerlayout)
        self.timertext = QLabel("00:00:00")
        self.timerlayout.addWidget(self.timertext)

    def timerstart1clicked(self):
        self.activeTimer.stop()
        self.activeTimer = QTimer()
        self.activeTimer.timeout.connect(self.timerEnd)
        self.activeTimer.start(15 * 1000)
        self.t3 = False

    def timerstart2clicked(self):
        self.activeTimer.stop()
        self.activeTimer = QTimer()
        self.activeTimer.timeout.connect(self.timerEnd)
        self.activeTimer.start(45 * 1000)
        self.t3 = False

    def timerstart3clicked(self):
        self.activeTimer.stop()
        self.activeTimer = QTimer()
        self.activeTimer.timeout.connect(self.timerEnd)
        self.activeTimer.start(59 * 1000)
        self.t3 = True

    def timerEnd(self):
        self.activeTimer.stop()
        self.activeTimer = QTimer()
        self.timertext.setText("00:00:00")

    def calculateclicked(self):
        # переход на след. страницу
        self.newwidget = ResultsPage(int(self.age_input.text()), int(self.pulse1.text()), int(self.pulse2.text()), int(self.pulse3.text()))
        self.newwidget.show()
        self.hide()

    def frame(self):
        scs = round(self.activeTimer.remainingTime() / 1000)
        seconds = str(scs)
        if len(seconds) < 2:
            seconds = "0" + seconds
        self.timertext.setText(f"00:00:{seconds}")
        if self.t3:
            if scs == 0:
                self.timertext.setStyleSheet("")
            elif scs >= 45:
                self.timertext.setStyleSheet("color: green;")
            elif scs <= 15:
                self.timertext.setStyleSheet("color: green;")
            else:
                self.timertext.setStyleSheet("")
        else:
            self.timertext.setStyleSheet("")

results = {
    15: [15, 11, 6, 0.5],
    13: [16.5, 12.5, 7.5, 2],
    11: [18, 14, 9, 3.5],
    9: [19.5, 15.5, 10.5, 5],
    7: [21, 17, 12, 6.5],
}

# страница с результатом
class ResultsPage(QWidget):
    def __init__(self, age: int, pulse1: int, pulse2: int, pulse3: int):
        QWidget.__init__(self)

        self.layout = QVBoxLayout(self)
        if age < 7:
            self.layout.addWidget(QLabel("Вы слишком мелкий чтобы проходить тест"))
        elif age > 128:
            self.layout.addWidget(QLabel("Вы слишком дед чтобы проходить тест"))
        else:
            index = (4 * (pulse1 + pulse2 + pulse3) - 200) / 10
            lvl = 4
            for k in results:
                if age >= k:
                    for i in range(4):
                        if index >= results[k][i]:
                            print(k, results[k], index, results[k][i])
                            lvl = i
                            break
                    break
            self.layout.addWidget(QLabel(f"Индекс Руфье: {index}"))
            if lvl == 4:
                self.layout.addWidget(QLabel("Результат:Высокий"))
            elif lvl == 3:
                self.layout.addWidget(QLabel("Результат:Выше среднего"))
            elif lvl == 2:
                self.layout.addWidget(QLabel("Результат:Средний желательно обратиться к врачу"))
            elif lvl == 1:
                self.layout.addWidget(QLabel("Результат:Удовлетворительный обратитесь к врачу"))
            else:
                self.layout.addWidget(QLabel("Результат: Низкий Срочно обратитесь к врачу!"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = Main()
    widget.show()

    sys.exit(app.exec())