import sys
import pandas as pd
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, \
    QTableWidgetItem, QTextEdit


# 定义成绩和绩点的映射关系（湖北理工学院的规则）
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
        elif grade == '合格':
            return 69
        elif grade == '良好':
            return 79
        elif grade == '优秀':
            return 90
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
            成绩单绩点计算规则请参考以下说明：<br>
            - 100-90分：4.5绩点 (优秀)<br>
            - 89-80分：3.5绩点 (良好)<br>
            - 79-70分：2.5绩点 (中等)<br>
            - 69-60分：1.5绩点 (及格)<br>
            - 60分以下：0绩点 (不及格)<br>
            - 补考合格：1.0绩点<br>
            - 重修成绩：按实际成绩计算绩点<br>
            需要根据上述规则修改你的成绩文件中的绩点计算。
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

            # 将成绩转换为数值类型，并处理补考情况
            df.loc[:, '成绩'] = pd.to_numeric(df['成绩'], errors='coerce').fillna(0)

            # 对名称相同的课程取最高分
            df = df.loc[df.groupby('课程名称')['成绩'].idxmax()]

            # 计算每门课程的绩点，根据成绩性质判断使用哪个绩点计算方法
            df['绩点'] = df.apply(lambda x: grade_to_gpa(x['成绩'], x['成绩性质']), axis=1)

            # 重新编号索引
            df.reset_index(drop=True, inplace=True)

            student_name = df['姓名'].iloc[0]

            # 确保清空表格
            self.result_table.clearContents()

            # 设置表格行列数（确保行数与实际数据行数相匹配）
            row_count = len(df)
            self.result_table.setRowCount(row_count)
            self.result_table.setColumnCount(5)
            self.result_table.setHorizontalHeaderLabels(['课程名称', '成绩性质', '成绩', '绩点', '学分'])

            column_width = (self.result_table.width() - 20) // 5
            for column in range(5):
                self.result_table.setColumnWidth(column, column_width)

            # 填充表格内容
            for i, row in df.iterrows():
                for j, key in enumerate(['课程名称', '成绩性质', '成绩', '绩点', '学分']):
                    item = QTableWidgetItem(str(row[key]))
                    item.setTextAlignment(Qt.AlignCenter)  # 居中对齐文本
                    self.result_table.setItem(i, j, item)

            # 自动调整列宽
            header = self.result_table.horizontalHeader()
            header.setStretchLastSection(True)

            # 计算总学分
            total_credits = df['学分'].sum()

            # 计算加权绩点总和
            weighted_gpa_sum = (df['绩点'] * df['学分']).sum()

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