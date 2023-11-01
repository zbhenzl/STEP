from PyQt5 import QtWidgets



class TimeAreaWindow(QtWidgets.QWidget):

    def __init__(self, **kvargs):
        super(TimeAreaWindow, self).__init__(**kvargs)

        self.setWindowTitle("Select date")
        calendar_layout = QtWidgets.QVBoxLayout()
        self.setLayout(calendar_layout)

        self.calendar_widget = QtWidgets.QCalendarWidget()
        calendar_layout.addWidget(self.calendar_widget)

        self.calendar_ok_button = QtWidgets.QPushButton("OK")
        calendar_layout.addWidget(self.calendar_ok_button)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.calendar_ok_button.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        if self.step_main_form.calendar_add_start:
            self.step_main_form.period_start_dateedit.setDate(self.calendar_widget.selectedDate())
        else:
            self.step_main_form.period_end_dateedit.setDate(self.calendar_widget.selectedDate())
        self.close()

    def closeEvent(self, event):
        self.step_main_form.setEnabled(True)
