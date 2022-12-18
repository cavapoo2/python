import pathlib
import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QLineEdit,QFileDialog,QSplitter,QLayout,QFrame
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
from pathlib import Path
import subprocess

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)

class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'Sim Loader'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 200
        self.vipu_ps=None
        self.twsdb_ps=None
        self.spm_ps=None
        self.home = str(Path.home())
        self.config_path = Path.cwd() / "path_config.json"
        self.initUI()
        if not Path.exists(self.config_path):
            print("Cannot find config.json file")
            assert False
        self._populate_paths()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_layout_and_connections()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.verticalGroupBox)
        self.setLayout(windowLayout)
        self.show()

    def create_layout_and_connections(self):
        self.verticalGroupBox = QGroupBox()
        layout = QGridLayout()
        self.text = QLabel(self)
        self.text.setText("VIPU Sim")
        layout.addWidget(self.text, 0, 0)
        self.line_edit_vipu = QLineEdit(self)
        layout.addWidget(self.line_edit_vipu, 0, 1)
        self.push_button_vipu = QPushButton('Select ')
        layout.addWidget(self.push_button_vipu, 0, 2)
        self.push_button_vipu.clicked.connect(self.onClick)

        self.text2 = QLabel(self)
        self.text2.setText("TWSDB Sim")
        layout.addWidget(self.text2, 1, 0)
        self.line_edit_twsdb =QLineEdit(self)
        layout.addWidget(self.line_edit_twsdb, 1, 1)
        self.push_button_twsdb = QPushButton('Select ')
        layout.addWidget(self.push_button_twsdb, 1, 2)
        self.push_button_twsdb.clicked.connect(lambda: self.onClick(name="TWSDB"))

        self.text3 = QLabel(self)
        self.text3.setText("SPM Sim")
        layout.addWidget(self.text3, 2, 0)
        self.line_edit_spm = QLineEdit(self)
        layout.addWidget(self.line_edit_spm, 2, 1)
        self.push_button_spm = QPushButton('Select ')
        layout.addWidget(self.push_button_spm, 2, 2)
        self.push_button_spm.clicked.connect(lambda: self.onClick(name="SPM"))

        #layout.addWidget(QHLine(),3,0,1,4)
        #layout.addWidget(QVLine(),3,0,2,1)

        #load and close buttons

        self.text_load = QLabel(self)
        self.button_load = QPushButton("Start Sims")
        self.button_load.clicked.connect(self.on_start_sims)
        #note the last 2 number dont seem to do much. Attempt made to increase size of button
        layout.addWidget(self.button_load,4,1,1,1)

        self.button_close = QPushButton("Close Sims")
        self.button_close.clicked.connect(self.on_close_sims)
        layout.addWidget(self.button_close, 5, 1,1,1)

        #layout.addWidget(QHLine(),5,0,1,4)

        #status
        self.status = QLabel(self)
        self.status.setText("Status:")
        self.status_text = QLabel(self)
        self.status_text.setText("Nothing Running")
        layout.addWidget(self.status,6,0)
        layout.addWidget(self.status_text,6,1)

        #layout.addWidget(QHLine(), 7, 0, 1, 4)

        self.verticalGroupBox.setLayout(layout)

    @pyqtSlot()
    def on_start_sims(self):
        print("Start Sims clicked")
        if not self._check_all_paths_set():
            print("not all Sim paths are set!")
            return
        print("Strting VIPU Sim")
        pd = Path(self.line_edit_vipu.text()).cwd()
        self.vipu_ps = self._load_sim(self.line_edit_vipu.text(),cwd=str(pd))
        print("Starting SPM Sim")
        pd = Path(self.line_edit_spm.text()).cwd()
        self.spm_ps = self._load_sim(self.line_edit_spm.text(),cwd=str(pd))
        if self.line_edit_twsdb:
            print("Starting TWSDB Sim")
            pd = Path(self.line_edit_twsdb.text()).cwd()
            self.twsdb_ps = self._load_sim(self.line_edit_twsdb.text(),pd)
        self.status_text.setText("Sims Running")


    def on_close_sims(self):
        print("Closing sims")
        print("closing VIPU sim")
        self._close_sim(name="vipu")
        print("Closing SPM sim")
        self._close_sim(name="spm")
        print("Closing TWSDB Sim")
        self._close_sim(name="twsdb")
        self.status_text.setText("Nothing Running")


    def _populate_paths(self):
        p = Path(self.config_path)
        with p.open("r") as f:
            cm = json.load(f)
            if cm["vipu"]:
                self.line_edit_vipu.setText(cm["vipu"])
            if cm["twsdb"]:
                self.line_edit_twsdb.setText(cm["twsdb"])
            if cm["spm"]:
                self.line_edit_spm.setText(cm["spm"])

    def _update_config_file(self,name="vipu",value=""):
        p = Path(self.config_path)
        with p.open("r") as f:
            cm = json.load(f)
            if name.lower() not in cm:
                print(name.lower() + " is not in the config map")
                return
        with p.open("w") as f:
            cm[name.lower()] = value
            json.dump(cm,f)

    '''
    TWSDB not essential
    '''
    def _check_all_paths_set(self):
        if not self.line_edit_spm.text():
            print("SPM sim is not set")
            return False
        if not self.line_edit_vipu.text():
            print("VIPU sim is not set")
            return False
        if not self.line_edit_twsdb.text():
            print("TWSDB sim is not set")
        return True

    @pyqtSlot()
    def onClick(self,name="VIPU"):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.home)
        if fname[0]:
            print(fname[0])
            if name=="VIPU":
                self.line_edit_vipu.setText(fname[0])
            elif name=="TWSDB":
                self.line_edit_twsdb.setText(fname[0])
            elif "SPM":
                self.line_edit_spm.setText(fname[0])
            else:
                print("Name not recognised!!")
            self._update_config_file(name.lower(),fname[0])

    '''
    Ensure all sims are exe. if its a python script, then use 
    pyinstaller to convert the python to an exe.
    Reason, if its a python script, then would need to locate
    the path of the venv to guarantee the python script works ok
    with all its deps. Convert to exe avoids the hassle of that
    '''
    def _load_sim(self,name,*args,cwd=Path.cwd()):
        run_args=[name,*args]
        print("Run args:" + str(run_args))
        try:
            p = subprocess.Popen(run_args,cwd=cwd)
        except Exception as ex:
            print("Exception loading sim: " + name  + " : " + str(ex))
            raise Exception
        else:
            return p

    def _close_sim(self,name="vipu"):
        if name == "vipu" and self.vipu_ps:
            ps = self.vipu_ps
        elif name == "spm" and self.spm_ps:
            ps = self.spm_ps
        elif name == "twsdb" and self.twsdb_ps:
            ps = self.twsdb_ps
        else:
            print("Can't kill since process is not active")
            ps=None
        try:
            if ps:
                ps.kill()
                ps.communicate()
                print("Closed " + name)
        except Exception as ex:
            print("Problem kill process " + name + " : " + str(ex))

    def closeEvent(self, event):
        '''
        Handles closing sims if window is closed
        :param event:
        :return:
        '''
        print("Closing window")
        print("Closing sims")
        print("closing VIPU sim")
        self._close_sim(name="vipu")
        print("Closing SPM sim")
        self._close_sim(name="spm")
        print("Closing TWSDB Sim")
        self._close_sim(name="twsdb")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())