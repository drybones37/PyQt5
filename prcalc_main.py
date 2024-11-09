from prcalc import Ui_MainWindow
from styleInfo import stylesheet

import sys
import json

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog


Ui_MainWindow, baseClass = uic.loadUiType('prcalcU.ui')

class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        # Main Window Constructor
        super().__init__(*args, **kwargs)
        # Your code will go here
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #Calculate Button
        self.ui.pushButton.clicked.connect(self.calAc)
        

        # Menu commands
        self.ui.Save.triggered.connect(self.saveMn)
        self.ui.Load.triggered.connect(self.openMn)
        self.ui.Instructions.triggered.connect(self.instructionsMn)


        #Your code ends here
        self.show() 


    def calAc(self): 
        comboD = self.fetchComboBoxData()
        tableD = self.fetchTableData()
        print(comboD,tableD)


    # What's the math I want to do?
    # I want to add


    #Util Functions 
    def fetchComboBoxData(self):
        handiBasis = self.ui.comboBoxHandicapBasis.currentText()
        eliteBoys =  self.ui.comboBoxEliteBoys.currentText()
        eliteGirls =  self.ui.comboBoxEliteGirls.currentText()
        eliteAdvantage = self.ui.comboBoxEliteAdvantage.currentText()
        comboBoxInfoList = [handiBasis, eliteBoys, eliteGirls, eliteAdvantage]
        return comboBoxInfoList

    def fetchTableData(self):
        num_rows = self.ui.tableWidget.rowCount()
        num_columns = self.ui.tableWidget.columnCount()

        table_data = []
        for row in range(num_rows):
            row_data = []
            for column in range(num_columns):
                item = self.ui.tableWidget.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')  # Append an empty string if the cell is empty
            table_data.append(row_data)
        return table_data




    # Menubar commands
    def saveMn(self):
        data = {
            "handicap_basis": self.ui.comboBoxHandicapBasis.currentText(),
            "elite_guys": self.ui.comboBoxEliteBoys.currentText(),
            "elite_girls": self.ui.comboBoxEliteGirls.currentText(),
            "elite_advantage": self.ui.comboBoxEliteAdvantage.currentText(),
            "table_data": self.fetchTableData() 
        }
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)
            print("Data saved to", file_name)

    # Load function that restores table data
    def openMn(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as file:
                data = json.load(file)

            # Restore ComboBox selections
            index = self.ui.comboBoxHandicapBasis.findText(data.get("handicap_basis", ""))
            if index >= 0:
                self.ui.comboBoxHandicapBasis.setCurrentIndex(index)

            index = self.ui.comboBoxEliteBoys.findText(data.get("elite_guys", ""))
            if index >= 0:
                self.ui.comboBoxEliteBoys.setCurrentIndex(index)

            index = self.ui.comboBoxEliteGirls.findText(data.get("elite_girls", ""))
            if index >= 0:
                self.ui.comboBoxEliteGirls.setCurrentIndex(index)

            index = self.ui.comboBoxEliteAdvantage.findText(data.get("elite_advantage", ""))
            if index >= 0:
                self.ui.comboBoxEliteAdvantage.setCurrentIndex(index)

            # Restore table data
            self.loadTableData(data.get("table_data", []))
            print("Data loaded from", file_name) 

    # Method to populate the QTableWidget with saved data
    def loadTableData(self, table_data):
        self.ui.tableWidget.setRowCount(len(table_data))
        self.ui.tableWidget.setColumnCount(len(table_data[0]) if table_data else 0)
        
        for row, row_data in enumerate(table_data):
            for col, cell_data in enumerate(row_data):
                item = qtw.QTableWidgetItem(cell_data)
                self.ui.tableWidget.setItem(row, col, item)


    def instructionsMn(self): 
        print('Instructions Pressed')
    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    w = MainWindow()
    sys.exit(app.exec_())
