import sys
import random
import subprocess
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import Qt, QAbstractTableModel, QAbstractItemModel, QModelIndex
from PySide2.QtGui import QColor

# class SearchResultsTableModel(QAbstractTableModel):
# 	def __init__(self, data=None):
# 		QAbstractTableModel.__init__(self)
# 		self.load_data(data)

# 	def load_data(self, data):
# 		self.results = data
# 		self.column_count = 4
# 		self.row_count = len(self.results) if self.results else 0
# 		return

# 	def rowCount(self, parent=QModelIndex()):
# 		return self.row_count

# 	def columnCount(self, parent=QModelIndex()):
# 		return self.column_count

# 	def headerData(self, section, orientation, role):
# 		if role != Qt.DisplayRole:
# 			return None
# 		if orientation == Qt.Horizontal:
# 			return ("ID", "Title", "Description", "Downloads")[section]
# 		else:
# 			return "{}".format(section)

# 	def emitDataChanged(self):
# 		self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(len(self.results), 3) , [Qt.DisplayRole])
# 		return

# 	def data(self, index, role=Qt.DisplayRole):
# 		column = index.column()
# 		row = index.row()
# 		print(self.results[row][column])
# 		if role == Qt.DisplayRole:
# 			return self.results[row][column]
# 		elif role == Qt.BackgroundRole:
# 			return QColor(Qt.white)
# 		elif role == Qt.TextAlignmentRole:
# 			return Qt.AlignRight

# 		return None

# 	def flags(self, index):
# 		return QtCore.Qt.ItemIsEnabled

# 	def insertRows(row, count):
# 		if count < 1 or row < 0 or row > len(self.results)
# 			return False
# 		self.beginInsertRows(self.createIndex(0, 0), row, row + count - 1)
# 		self.endInsertRows()
# 		return True

# class SearchResultsWidget(QtWidgets.QWidget):
# 	def __init__(self, data=None):
# 		QtWidgets.QWidget.__init__(self)

# 		# Getting the Model
# 		self.model = SearchResultsTableModel(data)

# 		# Creating a QTableView
# 		self.table_view = QtWidgets.QTableView()
# 		self.table_view.setModel(self.model)

# 		# QTableView Headers
# 		self.horizontal_header = self.table_view.horizontalHeader()
# 		self.vertical_header = self.table_view.verticalHeader()
# 		self.horizontal_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
# 		self.vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
# 		self.horizontal_header.setStretchLastSection(True)

# 		# QWidget Layout
# 		self.main_layout = QtWidgets.QHBoxLayout()
# 		size = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

# 		## Left layout
# 		size.setHorizontalStretch(1)
# 		self.table_view.setSizePolicy(size)
# 		self.main_layout.addWidget(self.table_view)

# 		# Set the layout to the QWidget
# 		self.setLayout(self.main_layout)

class SearchTools(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.text = QtWidgets.QLabel("Search tool")
		self.text.setAlignment(QtCore.Qt.AlignCenter)

		self.searchLineEdit = QtWidgets.QLineEdit()
		self.searchLineEdit.setPlaceholderText("Search a tool in Boutiques...")
		self.button = QtWidgets.QPushButton("Search")

		# Search input
		self.searchGroupBox = QtWidgets.QGroupBox()
		self.searchLayout = QtWidgets.QHBoxLayout()
		self.searchLayout.addWidget(self.searchLineEdit)
		self.searchLayout.addWidget(self.button)
		self.searchGroupBox.setLayout(self.searchLayout)
		
		# self.searchResultsWidget = SearchResultsWidget([['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']])
		self.createTable()
		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.searchGroupBox)
		self.layout.addWidget(self.table)
		self.setLayout(self.layout)

		self.button.clicked.connect(self.searchBoutiquesTools)
		self.searchLineEdit.returnPressed.connect(self.searchBoutiquesTools)

	def createTable(self):
		self.table = QtWidgets.QTableWidget()
		self.table.setRowCount(0)
		self.table.setColumnCount(4)
		self.table.move(0,0)
		self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.table.setHorizontalHeaderLabels(["ID", "Title", "Description", "Downloads"])
		return

	def searchBoutiquesTools(self):
		searchQuery = self.searchLineEdit.text()
		result = subprocess.run(["bosh", "search", "-m 50", searchQuery], capture_output=True)
		lines = result.stdout.decode("utf-8").splitlines()
		print(lines)
		
		if len(lines) < 2:
			return

		line = lines[1]
		idIndex = line.find("ID")
		titleIndex = line.find("TITLE")
		descriptionIndex = line.find("DESCRIPTION")
		downloadsIndex = line.find("DOWNLOADS")
		self.table.setRowCount(len(lines)-2)

		n = 0
		for line in lines[2:]:
			id = line[idIndex:titleIndex].strip()
			title = line[titleIndex:descriptionIndex].strip()
			description = line[descriptionIndex:downloadsIndex].strip()
			downloads = line[downloadsIndex:].strip()

			self.table.setItem(n, 0, QtWidgets.QTableWidgetItem(id))
			self.table.setItem(n, 1, QtWidgets.QTableWidgetItem(title))
			self.table.setItem(n, 2, QtWidgets.QTableWidgetItem(description))
			self.table.setItem(n, 3, QtWidgets.QTableWidgetItem(downloads))

			n += 1

		# self.searchResultsWidget.model.load_data(data)
		# self.searchResultsWidget.model.emitDataChanged()

class InvocationWidget(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.layout = QtWidgets.QVBoxLayout()

		self.generateSimpleInvocationButton = QtWidgets.QPushButton("Generate simple invocation")
		self.generateFullInvocationButton = QtWidgets.QPushButton("Generate full invocation")
		self.openInvocationButton = QtWidgets.QPushButton("Open invocation file")
		# self.invocationEditor = QtGui.QTextEdit()
		self.saveInvocationButton = QtWidgets.QPushButton("Save invocation file")

		self.layout.addWidget(self.generateSimpleInvocationButton)
		self.layout.addWidget(self.generateFullInvocationButton)
		self.layout.addWidget(self.openInvocationButton)
		# self.layout.addWidget(self.invocationEditor)
		self.layout.addWidget(self.saveInvocationButton)

		self.setLayout(self.layout)
		return

	def file_open(self):
		name = QtGui.QFileDialog.getOpenFileName(self, 'Open Invocation File')
		file = open(name,'r')

		with file:
			text = file.read()
			self.invocationEditor.setText(text)


class MyWidget(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.searchTools = SearchTools()
		self.invocationWidget = InvocationWidget()

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.searchTools)
		self.layout.addWidget(self.invocationWidget)

		self.executeButton = QtWidgets.QPushButton("Execute")
		self.layout.addWidget(self.executeButton)

		self.setLayout(self.layout)


if __name__ == "__main__":
	app = QtWidgets.QApplication([])

	widget = MyWidget()
	widget.resize(800, 600)
	widget.show()

	sys.exit(app.exec_())
