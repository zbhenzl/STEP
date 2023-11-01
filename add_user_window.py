from PyQt5 import QtWidgets, QtGui
from step_main_form import Popup
from database import check_input


class AddUserWindow(QtWidgets.QWidget):

    def __init__(self, **kvargs):
        super(AddUserWindow, self).__init__(**kvargs)

        self.setWindowTitle("Add user")
        self.setWindowIcon(QtGui.QIcon("user--plus.png"))
        add_user_window_layout = QtWidgets.QFormLayout()
        self.setLayout(add_user_window_layout)
        self.setFocus()
        self.add_user_lineedit = QtWidgets.QLineEdit()
        self.add_authorization_combobox = QtWidgets.QComboBox()
        self.add_authorization_combobox.addItem("User")
        self.add_authorization_combobox.addItem("Administrator")
        self.add_ok_button = QtWidgets.QPushButton("OK")

        add_user_window_layout.addRow(QtWidgets.QLabel("User: "), self.add_user_lineedit)
        add_user_window_layout.addRow(QtWidgets.QLabel("permissions"), self.add_authorization_combobox)
        add_user_window_layout.addRow(None, self.add_ok_button)


    def setup(self):
        from step_application import root
        self.users = root.database.users
        self.step_main_form = root.step_main_form
        self.add_ok_button.clicked.connect(self.save_new_user)

    def save_new_user(self):
        if check_input(self.add_user_lineedit.text().strip()):
            for user in self.users.users():
                if user[1] == self.add_user_lineedit.text().strip():
                    a = Popup("Name exist", "This user name already exist. I can´t save it again",
                              buttons="Exit w/o save, Try again".split(","))
                    if a.do() == 0:
                        self.close()
                        self.add_user_lineedit.clear()
                        return
                    else:
                        self.add_user_lineedit.clear()
                        return
            if self.add_user_lineedit.text() != "":
                self.step_main_form.users.add_user(self.add_user_lineedit.text(),
                                                   self.add_authorization_combobox.currentText())
                self.step_main_form.user_combobox.addItem(self.add_user_lineedit.text())
                self.step_main_form.user_combobox.setCurrentText(self.add_user_lineedit.text())
            self.close()
            self.add_user_lineedit.clear()
        else:
            a = Popup("Name error", "The name contains forbidden characters and will not be saved")
            a.do()
            self.add_user_lineedit.clear()
            self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.step_main_form.setEnabled(True)



class RenameUserWindow(QtWidgets.QWidget):

    def __init__(self, **kvargs):
        super(RenameUserWindow, self).__init__(**kvargs)

        self.setWindowTitle("Rename user")
        self.setWindowIcon(QtGui.QIcon("user-share.png"))
        add_user_window_layout = QtWidgets.QFormLayout()
        self.setLayout(add_user_window_layout)
        self.setFocus()
        self.add_user_lineedit = QtWidgets.QLineEdit()
        self.add_ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        add_user_window_layout.addRow(QtWidgets.QLabel("New user name: "), self.add_user_lineedit)
        add_user_window_layout.addRow(self.add_ok_button, self.cancel_button)


    def setup(self):
        from step_application import root
        self.users = root.database.users
        self.step_main_form = root.step_main_form
        self.add_ok_button.clicked.connect(self.rename_user)
        self.cancel_button.clicked.connect(self.close)

    def rename_user(self):
        new_name = self.add_user_lineedit.text().strip()
        if check_input(new_name):
            for user in self.users.users():
                if user[1] == new_name:
                    a = Popup("Name exist", "This user name already exist. I can´t save it again",
                              buttons="Exit w/o save, Try again".split(","))
                    if a.do() == 0:
                        self.close()
                        self.add_user_lineedit.clear()
                        return
                    else:
                        self.add_user_lineedit.clear()
                        return
            if new_name != "":
                self.step_main_form.users.rename_user(new_name, self.step_main_form.user.name())
                self.step_main_form.places.change_user(new_name, self.step_main_form.user.name())
                self.step_main_form.database.observation_logs.change_user(new_name, self.step_main_form.user.name())
                self.step_main_form.stars.change_user_in_user_list(new_name, self.step_main_form.user.name())
                self.step_main_form.user_combobox.clear()
                self.step_main_form.user_combobox.addItems(self.step_main_form.users.return_user_list())
                self.step_main_form.user_combobox.setCurrentText(new_name)
            self.close()
            self.add_user_lineedit.clear()
        else:
            a = Popup("Name error", "The name contains forbidden characters and will not be saved")
            a.do()
            self.add_user_lineedit.clear()
            self.close()

    def closeEvent(self, event):
        self.step_main_form.setEnabled(True)
