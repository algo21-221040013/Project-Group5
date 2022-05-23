# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 15:21:12 2020

@author: admin
"""

#coding=utf-8
import traceback
import time
import os
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QFrame, QCheckBox, QLineEdit, QLabel, QPushButton, QTextBrowser, QTableWidget, \
	QAbstractItemView, QTableWidgetItem, QMenuBar, QStatusBar, QApplication, QMainWindow, QComboBox, QDateEdit
# mysql模块
import pymysql
from PyQt5.QtWidgets import QFileDialog  
from configparser import ConfigParser
import xlwt
import pandas as pd

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		self.sheet_type=""
		## 设置窗口的名称
		MainWindow.setObjectName("MainWindow")
		## 设置窗口大小
		MainWindow.resize(760, 700)
		self.df = pd.read_csv('data.csv',encoding='gb2312')

		# 根据窗口的大小固定大小 这里相当于设置全屏
		self.centralwidget =  QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.frame = QFrame(self.centralwidget)
		self.frame.setGeometry(QtCore.QRect(10, 10, 800, 121))
		self.frame.setFrameShape( QFrame.StyledPanel)
		self.frame.setFrameShadow( QFrame.Raised)
		self.frame.setObjectName("frame")

		################左侧按钮
		##产品名称选择
		self.label =  QLabel(self.frame)
		self.label.setGeometry(QtCore.QRect(20, 10, 64, 16))
		self.label.setObjectName("label")
		
		self.product_name =  QComboBox(self.frame)
		self.product_name.setGeometry(QtCore.QRect(90, 10, 113, 20))
		self.product_name.setObjectName("product_name")
		self.product_name.addItem("")
		self.product_name.addItem("")

		self.label1 =  QLabel(self.frame)
		self.label1.setGeometry(QtCore.QRect(230, 10, 64, 16))
		self.label1.setObjectName("label1")		
		self.select_product =  QComboBox(self.frame)
		self.select_product.setGeometry(QtCore.QRect(300, 10, 113, 20))
		self.select_product.setObjectName("select_product")
		self.select_product.addItem("")
		self.select_product.addItem("")
		self.select_product.addItem("")
		'''self.select_product.activated.connect(lambda:self.to_account(self.product_name.currentText(),self.select_product.currentText()))
		self.select_product.activated.connect(lambda:self.to_position(self.select_product.currentText()))
		self.select_product.activated.connect(lambda:self.to_exchange(self.select_product.currentText()))
		self.product_name.activated.connect(lambda:self.to_account(self.product_name.currentText(),self.select_product.currentText()))
		self.product_name.activated.connect(lambda:self.to_position(self.select_product.currentText()))		
		self.product_name.activated.connect(lambda:self.to_exchange(self.select_product.currentText()))'''

		self.label2 =  QLabel(self.frame)
		self.label2.setGeometry(QtCore.QRect(440, 10, 40, 16))
		self.label2.setObjectName("label2")
		
		self.select_account =  QComboBox(self.frame)
		self.select_account.setGeometry(QtCore.QRect(490, 10, 113, 20))
		self.select_account.setObjectName("select_account")
		self.select_account.addItem("")
		self.select_account.addItem("")
		self.select_account.addItem("")     
		###产品种类 期货？证券？期权？
		self.label3 =  QLabel(self.frame)
		self.label3.setGeometry(QtCore.QRect(20, 40, 64, 16))
		self.label3.setObjectName("label3")


		##交易所
		self.label5 =  QLabel(self.frame)
		self.label5.setGeometry(QtCore.QRect(20, 70, 64, 16))
		self.label5.setObjectName("label5")
		
		self.exchange =  QComboBox(self.frame)
		self.exchange.setGeometry(QtCore.QRect(90, 70, 113, 20))
		self.exchange.setObjectName("exchange")
		self.exchange.addItem("")
		self.exchange.addItem("")
		self.exchange.addItem("")  	
		self.exchange.addItem("")  	
		self.exchange.addItem("")  	

		self.label6 =  QLabel(self.frame)
		self.label6.setGeometry(QtCore.QRect(230, 70, 64, 16))
		self.label6.setObjectName("label6")
		
		self.select_position =  QComboBox(self.frame)
		self.select_position.setGeometry(QtCore.QRect(300, 70, 113, 20))
		self.select_position.setObjectName("select_position")
		self.select_position.addItem("")
		self.select_position.addItem("")
		self.select_position.addItem("")  		
		self.select_position.addItem("")  			     
		###日期check  
		self.check_date =  QCheckBox(self.frame)
		self.check_date.setGeometry(QtCore.QRect(20, 100, 71, 16))
		self.check_date.setObjectName("check_date")
		self.first_date =  QDateEdit(self.frame)
		self.first_date.setGeometry(QtCore.QRect(90, 100, 100, 20))
		self.first_date.setObjectName("first_date")		
		self.label7 =  QLabel(self.frame)
		self.label7.setGeometry(QtCore.QRect(199, 100, 16, 16))
		self.label7.setObjectName("label7")
		self.last_date =  QDateEdit(self.frame)
		self.last_date.setGeometry(QtCore.QRect(219, 100, 100, 20))
		self.last_date.setObjectName("last_date")		



		##查询按钮
		self.find =  QPushButton(self.frame)
		self.find.setGeometry(QtCore.QRect(660, 100, 75, 21))
		self.find.setObjectName("find")
		self.find.clicked.connect(self.find_btn)

		
		## sql语句展示框
		self.sql_out =  QTextBrowser(self.centralwidget)
		self.sql_out.setGeometry(QtCore.QRect(10, 140, 740, 61))
		self.sql_out.setObjectName("sql_out")
		
		##展示框
		self.result_out =  QTableWidget(self.centralwidget)
		self.result_out.setEditTriggers( QAbstractItemView.NoEditTriggers)  # 不可编辑表格
		self.result_out.setGeometry(QtCore.QRect(10, 210, 740, 350))
		self.result_out.setObjectName("result_out")

		self.PrevButton = QPushButton(self.centralwidget)
		self.PrevButton.setGeometry(QtCore.QRect(10, 580, 75, 21))
		self.PrevButton.setText("上一页")
		self.PrevButton.clicked.connect(self.prev_btn)

		'''
		self.label9 = QLabel(self.centralwidget)
		self.label9.setGeometry(QtCore.QRect(100, 580, 40, 16))

		self.switchpage = QLineEdit(self.centralwidget)
		self.switchpage.setGeometry(QtCore.QRect(145, 580, 16, 21))

		self.label10 = QLabel(self.centralwidget)
		self.label10.setGeometry(QtCore.QRect(165, 580, 16, 16))
		'''

		self.NextButton = QPushButton(self.centralwidget)
		self.NextButton.setGeometry(QtCore.QRect(100, 580, 75, 21))
		self.NextButton.setText("下一页")
		self.NextButton.clicked.connect(self.next_btn)

		self.label11 = QLabel(self.centralwidget)
		self.label11.setGeometry(QtCore.QRect(200, 580, 32, 16))

		self.switchpage = QLineEdit(self.centralwidget)
		self.switchpage.setGeometry(QtCore.QRect(230, 580, 22, 21))
		self.switchpage.editingFinished.connect(self.switch_page)
		self.label12 = QLabel(self.centralwidget)
		self.label12.setGeometry(QtCore.QRect(255, 580, 16, 16))

		#状态布局
		self.totalPageLabel = QLabel(self.centralwidget)
		self.totalPageLabel.setGeometry(QtCore.QRect(610, 575, 55, 16))

		self.currentPageLabel = QLabel(self.centralwidget)
		self.currentPageLabel.setGeometry(QtCore.QRect(680, 575, 50, 16))

		##保存按钮
		self.save_file= QPushButton(self.centralwidget)
		self.save_file.setGeometry(10, 630, 75, 21)
		self.save_file.setObjectName('save_file')
		self.save_file.setText('保存至')
		self.save_file.clicked.connect(self.p3_clicked)
		
		## 滚动按钮
		##退出按钮
		self.pushButton_2 =  QPushButton(self.centralwidget)
		self.pushButton_2.setGeometry(QtCore.QRect(675, 630, 75, 21))
		self.pushButton_2.setObjectName("pushButton_2")
		self.pushButton_2.clicked.connect(self.p2_clicked)

		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar =  QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 509, 23))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar =  QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		
	def p3_clicked(self):
		self.pyqt_clicked3.emit()
				
	def p2_clicked(self):
		self.pyqt_clicked1.emit()
	def prev_btn(self):
		self.pyqt_clicked5.emit()
	def next_btn(self):
		self.pyqt_clicked6.emit()		
	def find_btn(self):
		self.pyqt_clicked2.emit()
	def retranslateUi(self, MainWindow):
		### 输出特定的文字
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "历史交易数据查询", None))
		self.label.setText(_translate("MainWindow", "基金名称", None))
		self.label1.setText(_translate("MainWindow", "产品种类", None))
		self.label2.setText(_translate("MainWindow", "账户", None))
		self.label3.setText(_translate("MainWindow", "条件筛选", None))
		self.label5.setText(_translate("MainWindow", "交易所", None))
		self.label6.setText(_translate("MainWindow", "方向", None))
		self.label7.setText(_translate("MainWindow", "到", None))
		self.label11.setText(_translate("MainWindow", "到第", None))
		self.label12.setText(_translate("MainWindow", "页", None))
		self.check_date.setText(_translate("MainWindow", "日期自", None))

		self.product_name.setCurrentText(_translate("MainWindow", " "))
		self.product_name.setItemText(0, _translate("MainWindow", "串串一号-RSRS布林带则时策略"))
		self.product_name.setItemText(1, _translate("MainWindow", "串串二号-指数增强策略"))
		self.select_product.setCurrentText(_translate("MainWindow", " "))
		self.select_product.setItemText(0, _translate("MainWindow", "crypto currency"))
		self.select_product.setItemText(1, _translate("MainWindow", "security"))

		self.select_position.setCurrentText(_translate("MainWindow", " "))
		self.select_position.setItemText(0, _translate("MainWindow", "买"))
		self.select_position.setItemText(1, _translate("MainWindow", "卖"))
		self.select_account.setCurrentText(_translate("MainWindow", "521521521521"))
		self.select_account.setItemText(0, _translate("MainWindow", "521521521521"))

		self.exchange.setCurrentText(_translate("MainWindow", " "))
		self.exchange.setItemText(0, _translate("MainWindow", "上海证券交易所"))
		self.exchange.setItemText(1, _translate("MainWindow", "深圳证券交易所"))

		self.first_date.setDisplayFormat("yyyy-MM-dd")
		self.last_date.setDisplayFormat("yyyy-MM-dd")
		self.first_date.setDate(QtCore.QDate(2020,1,1))
		self.last_date.setDate(QDate.currentDate())

		self.find.setText(_translate("MainWindow", "查询", None))
		self.sql_out.setText('查询成功')
		self.pushButton_2.setText(_translate("MainWindow", "退出", None))

	def buttonTest2(self):
		_translate = QtCore.QCoreApplication.translate
		my_product = self.product_name.currentText()
		my_type = self.select_product.currentText()
		my_account = self.select_account.currentText()
		temp_sqlstring = ""
		self.result_out.setColumnCount(10)
		self.result_out.setRowCount(100)
		self.result_out.resizeColumnsToContents()
		self.result_out.resizeRowsToContents()
		for i in range(10):
			item =  QTableWidgetItem()
			self.result_out.setHorizontalHeaderItem(i, item)
			self.result_out.horizontalHeader().setDefaultSectionSize(100)
			self.result_out.horizontalHeader().setMinimumSectionSize(25)
			self.result_out.verticalHeader().setDefaultSectionSize(30)
		if self.check_date.isChecked():
			first = self.first_date.date().toString(Qt.ISODate)
			first = first.replace('-','')
			last = self.last_date.date().toString(Qt.ISODate)
			last = last.replace('-','')
		else:
			first=0
			last=0
		my_exchange=self.exchange.currentText()

		self.result_out.clearContents()  # 每一次查询时清除表格中信息
		#self.set_header()
		self.currentPage = 1
		self.to_table(self.df)
		self.sql_out.setText("find button pressed")

	def to_table(self,df):
		k=0
		for i in range(len(df)):
			w=0
			for j in range(len(df.columns)):
				if type(df.iloc[i,j])!=str:
					newItem = QTableWidgetItem(str(df.iloc[i,j]))
				else:
					newItem = QTableWidgetItem(df.iloc[i,j])
				self.result_out.setItem(k, w, newItem)
				w+=1
			k+=1

	def set_header(self):
		_translate = QtCore.QCoreApplication.translate
		fields = self.df.columns
		for i in range(len(fields)):
			item = self.result_out.horizontalHeaderItem(i+1)
			item.setText(_translate("MainWindow", fields[i], None))
	def switch_page(self):
		_translate = QtCore.QCoreApplication.translate
		page = int(self.switchpage.text())
		if page<=0 or page>self.page_count:
			print("page index out of range")
		else:
			self.currentPage = page
			self.currentPageLabel.setText(_translate("MainWindow","第%s页"%self.currentPage,None))
			sql_string = self.sql_order[:-1]+self.limit_sqlstring(self.currentPage)+';'
			self.cur.execute(sql_string)
			self.to_table(self.cur)
			self.set_header(self.cur)
			self.sql_out.setText("")
			self.sql_out.append(sql_string)

	def PressPrev(self):
		_translate = QtCore.QCoreApplication.translate
		if self.currentPage==1:
			pass
		else:
			self.currentPage-=1
			self.currentPageLabel.setText(_translate("MainWindow","第%s页"%self.currentPage,None))
			sql_string = self.sql_order[:-1]+self.limit_sqlstring(self.currentPage)+';'
			self.cur.execute(sql_string)
			self.to_table(self.cur)
			self.set_header(self.cur)
			self.sql_out.setText("")
			self.sql_out.append(sql_string)
	def PressNext(self):
		_translate = QtCore.QCoreApplication.translate
		if self.currentPage==self.page_count:
			pass
		else:
			self.currentPage+=1
			self.currentPageLabel.setText(_translate("MainWindow","第%s页"%self.currentPage,None))
			sql_string = self.sql_order[:-1]+self.limit_sqlstring(self.currentPage)+';'
			print(sql_string)
			self.cur.execute(sql_string)
			self.to_table(self.cur)
			self.set_header(self.cur)
			self.sql_out.setText("")
			self.sql_out.append(sql_string)
	#设置限制index得sql语句
	def limit_sqlstring(self,page):
		limitIndex = (page-1)*self.page_row
		return "limit %d,%d"%(limitIndex,self.page_row)
	#获取总页数
	def get_total_page(self,sql_string):
		self.page_row = 100
		rows = self.cur.execute(sql_string)
		if rows%self.page_row==0:
			return int(rows/self.page_row)
		else:
			return int(rows/self.page_row)+1
	def get_sql(self,text):
		self.sql_order = text
	def buttonExit(self):
		self.conn.commit()
		self.cur.close()
		self.conn.close()
		self.close()

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Escape:
			self.buttonExit()

			#if 'txt' in file:
#?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

class MyWindow( QMainWindow, Ui_MainWindow):
	pyqt_clicked1 = pyqtSignal()
	pyqt_clicked2 = pyqtSignal()
	pyqt_clicked3 = pyqtSignal()
	pyqt_clicked4 = pyqtSignal()
	pyqt_clicked5 = pyqtSignal()
	pyqt_clicked6 = pyqtSignal()	
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setupUi(self)
		self.pyqt_clicked1.connect(self.buttonExit)
		self.pyqt_clicked2.connect(self.buttonTest2)
		self.pyqt_clicked3.connect(self.set_header)
		self.pyqt_clicked5.connect(self.PressPrev)
		self.pyqt_clicked6.connect(self.PressNext)		



if __name__ == "__main__":
	work_path=os.path.split(os.path.realpath(sys.executable))[0]
	work_path=os.path.split(work_path)[0]
	#work_path = r"C:\Users\admin\实习\ui界面"
	now = time.strftime("%Y%m%d_%H_%M_%S")
	origin = sys.stdout
	if not os.path.exists(work_path+'\\log'):
		os.makedirs(work_path+'\\log')
	f = open(work_path+'\\log\\'+now+'.log', 'w')
	sys.stdout = f		
	app =  QApplication(sys.argv)
	app.aboutToQuit.connect(app.deleteLater)
	myshow = MyWindow()
	myshow.show()
	sys.exit(app.exec_())
	sys.stdout = origin
	f.close()
	f = open(work_path+'\\log\\'+now+'.log', 'r').read()
	print(f)		
	# app.exec_()
	# sys.exit(0)

	#except Exception as e:
		#s = traceback.format_exc()
		#print(e)
		#tra = traceback.print_exc()		