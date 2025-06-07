import sys
import pandas as pd
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, \
    QTableWidgetItem, QTextEdit


# 定义成绩和绩点的映射关系
def grade_to_gpa(grade, nature):
    try:
        grade = float(grade)
    except ValueError:
        return 0.0  # 如果成绩不是数字，返回0.0

    if nature == "补考一":
        return 1.0 if grade >= 60 else 0.0
    elif nature == "重修":
        if 90 <= grade <= 100:
            return 4.0
        elif 80 <= grade < 90:
            return 3.0
        elif 70 <= grade < 80:
            return 2.0
        elif 60 <= grade < 70:
            return 1.0
        else:
            return 0.0
    elif nature == "正常考试":
        if 90 <= grade <= 100:
            return 4.5
        elif 80 <= grade < 90:
            return 3.5
        elif 70 <= grade < 80:
            return 2.5
        elif 60 <= grade < 70:
            return 1.5
        else:
            return 0.0


class GPAAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('请选择一个Excel文件:')
        layout.addWidget(self.label)

        self.button = QPushButton('选择文件')
        self.button.clicked.connect(self.showDialog)
        layout.addWidget(self.button)

        # 添加说明文本
        self.instruction_label = QTextEdit(self)
        self.instruction_label.setReadOnly(True)  # 设置为只读
        self.instruction_label.setTextInteractionFlags(Qt.TextBrowserInteraction)  # 允许文本交互，包括点击链接

        # 设置文本内容，使用 HTML 格式进行美观排版
        self.instruction_label.setHtml('''
            请在：<a href="https://jwglnew.hbpu.edu.cn/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default">https://jwglnew.hbpu.edu.cn/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default</a> 中<br>
            选择 - 学年：全部 学期：全部 课程标记：全部 ，然后点击”查询",然后点击"导出”，已选择导出列请全部导出，再点击下载为excel文件。<br>
            计科系学位课程为：<br>
            · 《计算机网络原理》&emsp;《操作系统原理》&emsp;《计算机数学》&emsp;《面向对象程序设计》<br>
            · 《数据结构》&emsp;《数据库系统》&emsp;《数字逻辑》&emsp;《计算机组成原理》<br>
            要求平均GPA为2.0及以上，已经适配了正常考试、补考、重修<br>
            有BUG请找：CBR
        ''')

        self.instruction_label.setFixedHeight(125)
        layout.addWidget(self.instruction_label)

        self.result_table = QTableWidget(self)
        layout.addWidget(self.result_table)

        self.gpa_label = QLabel(self)
        layout.addWidget(self.gpa_label)

        self.close_button = QPushButton('关闭')
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.setWindowTitle('GPA 分析器  Powered By： CBR')
        self.setGeometry(300, 300, 600, 550)

    def showDialog(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog  # 禁用本机文件对话框以提高兼容性
            fileName, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "",
                                                      "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)

            if fileName:
                self.analyzeFile(fileName)

            # 手动处理事件循环，防止阻塞
            QCoreApplication.processEvents()

        except Exception as e:
            print(f"Error occurred while selecting file: {e}")

    def analyzeFile(self, file_path):
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)

            required_courses = [
                "计算机网络原理", "操作系统原理", "计算机数学", "面向对象程序设计",
                "数据结构", "数据库系统", "数字逻辑", "计算机组成原理"
            ]

            # 过滤出必修课程
            filtered_df = df[df['课程名称'].isin(required_courses)].copy()  # 使用 .copy() 创建副本

            # 将成绩转换为数值类型，并处理补考情况
            filtered_df.loc[:, '成绩'] = pd.to_numeric(filtered_df['成绩'], errors='coerce').fillna(0)

            # 对名称相同的课程取最高分
            filtered_df = filtered_df.loc[filtered_df.groupby('课程名称')['成绩'].idxmax()]

            # 计算每门课程的绩点，根据成绩性质判断使用哪个绩点计算方法
            filtered_df['绩点'] = filtered_df.apply(lambda x: grade_to_gpa(x['成绩'], x['成绩性质']), axis=1)

            # 重新编号索引
            filtered_df.reset_index(drop=True, inplace=True)

            student_name = filtered_df['姓名'].iloc[0]

            # 确保清空表格
            self.result_table.clearContents()

            # 设置表格行列数（确保行数与实际数据行数相匹配）
            row_count = len(filtered_df)
            self.result_table.setRowCount(row_count)
            self.result_table.setColumnCount(5)
            self.result_table.setHorizontalHeaderLabels(['课程名称', '成绩性质', '成绩', '绩点', '学分'])

            column_width = (self.result_table.width() - 20) // 5
            for column in range(5):
                self.result_table.setColumnWidth(column, column_width)

            # 填充表格内容
            for i, row in filtered_df.iterrows():
                for j, key in enumerate(['课程名称', '成绩性质', '成绩', '绩点', '学分']):
                    item = QTableWidgetItem(str(row[key]))
                    item.setTextAlignment(Qt.AlignCenter)  # 居中对齐文本
                    self.result_table.setItem(i, j, item)

            # 自动调整列宽
            header = self.result_table.horizontalHeader()
            header.setStretchLastSection(True)

            # 计算总学分
            total_credits = filtered_df['学分'].sum()

            # 计算加权绩点总和
            weighted_gpa_sum = (filtered_df['绩点'] * filtered_df['学分']).sum()

            # 计算平均学分绩点
            average_gpa = weighted_gpa_sum / total_credits

            # 显示平均学分绩点
            self.gpa_label.setText(
                f"平均学分绩点: {average_gpa:.2f}\n{student_name} 达到标准" if average_gpa >= 2 else f"{student_name}  未达到标准"
            )

        except Exception as e:
            print(f"Error occurred during file analysis: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GPAAnalyzer()
    ex.show()
    sys.exit(app.exec_())
