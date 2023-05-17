#!/usr/bin/python3
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from controller import *
import platform


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi()
        self._controller = Controller()
    def setupUi(self):
        self.setWindowTitle("PE-infector GUI V1.0")
        self.setFixedSize(450, 160)

        #labels
        self._label_executor = QLabel("Path to PE-infector:", self)
        self._label_source = QLabel("Path to target binary:", self)
        self._label_destination = QLabel("Path to patched binary:", self)
        self._label_payload = QLabel("Path to payload:", self)
        self._label_method = QLabel("Inject method:", self)

        self._label_executor.move(0, 0)
        self._label_source.move(0, 32)
        self._label_destination.move(0, 64)
        self._label_payload.move(0, 96)
        self._label_method.move(0, 128)

        self._label_executor.resize(132, 30)
        self._label_source.resize(140, 30)
        self._label_destination.resize(152, 30)
        self._label_payload.resize(106, 30)
        self._label_method.resize(100, 30)

        #line edits
        self._line_path_executor = QLineEdit("", self)
        self._line_path_source = QLineEdit("", self)
        self._line_path_destination = QLineEdit("", self)
        self._line_path_payload = QLineEdit("", self)

        self._line_path_executor.move(157, 0)
        self._line_path_source.move(157, 32)
        self._line_path_destination.move(157, 64)
        self._line_path_payload.move(157, 96)

        self._line_path_executor.resize(265, 30)
        self._line_path_source.resize(265, 30)
        self._line_path_destination.resize(265, 30)
        self._line_path_payload.resize(265, 30)

        self._line_path_executor.setReadOnly(True)
        self._line_path_source.setReadOnly(True)
        self._line_path_destination.setReadOnly(True)
        self._line_path_payload.setReadOnly(True)

        #buttons
        self._btn_executor = QPushButton("...", self)
        self._btn_source = QPushButton("...", self)
        self._btn_destination = QPushButton("...", self)
        self._btn_payload = QPushButton("...", self)
        self._btn_generate = QPushButton("Generate", self)

        self._btn_executor.resize(25, 30)
        self._btn_source.resize(25, 30)
        self._btn_destination.resize(25, 30)
        self._btn_payload.resize(25, 30)
        self._btn_generate.resize(90, 30)

        self._btn_executor.move(425, 0)
        self._btn_source.move(425, 32)
        self._btn_destination.move(425, 64)
        self._btn_payload.move(425, 96)
        self._btn_generate.move(360, 128)

        self._btn_executor.clicked.connect(self.onClickSetExecutor)
        self._btn_source.clicked.connect(self.onClickSetSourceBinary)
        self._btn_destination.clicked.connect(self.onClickSetDestinationBinary)
        self._btn_payload.clicked.connect(self.onClickSetPayload)
        self._btn_generate.clicked.connect(self.onClickGenerate)

        #checkbox for thread impl
        self._checkbox_thr = QCheckBox("Run in thread", self)
        self._checkbox_thr.move(210, 128)
        self._checkbox_thr.resize(110, 30)

        #combobox
        self._combo_method = QComboBox(self)
        self._combo_method.addItems(["code", "sect", "resz"])
        self._combo_method.move(100, 128)
    
    def onClickSetExecutor(self):
        params = self._controller.getParams()
        path = params['infector_executable']
        file_filter = "Executable (*.exe)" if platform.system() == "Windows" else "Executable (*)"

        file_name = QFileDialog.getOpenFileName(self, 'Open file', path, file_filter)[0]

        if file_name:
            self._line_path_executor.setText(file_name)
            params['infector_executable'] = file_name
            self._controller.setParams(params)


    def onClickSetSourceBinary(self):
        params = self._controller.getParams()
        path = params['source_file']
        file_filter = "Windows PE (*.exe *.dll)"

        file_name = QFileDialog.getOpenFileName(self, 'Open file', path, file_filter)[0]

        if file_name:
            self._line_path_source.setText(file_name)
            params['source_file'] = file_name
            self._controller.setParams(params)

    def onClickSetPayload(self):
        params = self._controller.getParams()
        path = params['payload_file']

        file_name = QFileDialog.getOpenFileName(self, 'Open file', path)[0]

        if file_name:
            self._line_path_payload.setText(file_name)
            params['payload_file'] = file_name
            self._controller.setParams(params)

    def onClickSetDestinationBinary(self):
        params = self._controller.getParams()
        path = params['destination_file']
        file_filter = "Windows PE (*.exe *.dll)"

        file_name = QFileDialog.getSaveFileName(self, 'Save file', path, file_filter)[0]

        if file_name:
            self._line_path_destination.setText(file_name)
            params['destination_file'] = file_name
            self._controller.setParams(params)

    def onClickGenerate(self):
        params = self._controller.getParams()

        #checking current params
        if not params['infector_executable']:
            msg = QMessageBox()
            msg.setWindowTitle("Generation failed")
            msg.setText("PE-infector executable is not defined!")
            msg.setIcon(QMessageBox.Critical)

            msg.exec_()
            return

        if not params['source_file']:
            msg = QMessageBox()
            msg.setWindowTitle("Generation failed")
            msg.setText("Target binary is not defined!")
            msg.setIcon(QMessageBox.Critical)

            msg.exec_()
            return

        if not params['destination_file']:
            msg = QMessageBox()
            msg.setWindowTitle("Generation failed")
            msg.setText("Patched binary is not defined!")
            msg.setIcon(QMessageBox.Critical)

            msg.exec_()
            return

        if not params['payload_file']:
            msg = QMessageBox()
            msg.setWindowTitle("Generation failed")
            msg.setText("Payload is not defined!")
            msg.setIcon(QMessageBox.Critical)

            msg.exec_()
            return

        #gather information from widgets and call self._controller.setParams(args)
        params['method'] = self._combo_method.currentText()
        params['thread'] = self._checkbox_thr.isChecked()

        ret = self._controller.generate()

        if ret != 0:
            if ret == -1:
                msg = QMessageBox()
                msg.setWindowTitle("Generation failed")
                msg.setText("Can't open file " + params['source_file'])
                msg.setIcon(QMessageBox.Critical)

                msg.exec_()
                return

            if ret == -2:
                msg = QMessageBox()
                msg.setWindowTitle("Generation failed")
                msg.setText("Bad target PE file")
                msg.setIcon(QMessageBox.Critical)

                msg.exec_()
                return

            if ret == -3:
                msg = QMessageBox()
                msg.setWindowTitle("Generation failed")
                msg.setText("Internal error: can't allocate memory for DOS gap")
                msg.setIcon(QMessageBox.Critical)

                msg.exec_()
                return

            if ret == -4:
                msg = QMessageBox()
                msg.setWindowTitle("Generation failed")
                msg.setText("Internal error: can't allocate memory for section gap")
                msg.setIcon(QMessageBox.Critical)

                msg.exec_()
                return

            if ret == -5:
                msg = QMessageBox()
                msg.setWindowTitle("Generation failed")
                msg.setText("Can't write file" + params['destination_file'])
                msg.setIcon(QMessageBox.Critical)

                msg.exec_()
                return

            if ret == -6:
                msg = QMessageBox()
                msg.setWindowTitle("Generation failed")
                msg.setText("Can't open file" + params['payload_file'])
                msg.setIcon(QMessageBox.Critical)

                msg.exec_()
                return

            if ret == -7:
                msg = QMessageBox()
                msg.setWindowTitle("Generation failed")
                msg.setText("Internal error: can't allocate memory for shellcode")
                msg.setIcon(QMessageBox.Critical)

                msg.exec_()
                return

            msg = QMessageBox()
            msg.setWindowTitle("Generation failed")
            msg.setText("Unknown error with code " + str(ret))
            msg.setIcon(QMessageBox.Critical)

            msg.exec_()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Generation completed!")

            msg.exec_()
