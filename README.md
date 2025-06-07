# 一个快速计算湖北理工学院的GPA工具

虽然学校的最终导出成绩单上面有GPA计算结果，但是还是不够明确，这个工具能够快速计算GPA，配合Excel改动分数和成绩属性能够为了快速选择刷分/达到毕业要求而重修课程使用。目前的计算方式使用的是2025届毕业生要求，GPA的计算方式使用的是平均GPA计算方法（学生手册和教务官网中有），有Python功底的可以按需修改。

## 成绩计算法则

根据2024年公布的《湖北理工学院学士学位授予暂行办法》中指出，GPA的计算法则如下所示：

<img src=".\Screenshot\image-20250607184717517.png" alt="image-20250607184717517" style="zoom:67%;" />





## 工具使用教程

<img src=".\Screenshot\image-20250607185015107.png" alt="image-20250607185015107" style="zoom:67%;" />

<img src=".\Screenshot\image-20250607185054332.png" alt="image-20250607185054332" style="zoom:67%;" />

![image-20250607185359107](E:\0 github\GPA_HBPU\Screenshot\image-20250607185149875.png)

<img src=".\Screenshot\image-20250607185229137.png" alt="image-20250607185229137" style="zoom:150%;" />

![image-20250607185326507](.\Screenshot\image-20250607185326507.png)

![image-20250607185454674](.\Screenshot\image-20250607185454674.png)



## 修改

根据不同学院的要求，工具提供了两种计算办法，一个是学位课计算（Degree.py），一般用于毕业要求的计算；一个是所有课程计算（AllCourses.py)。主要是去修改Degree，或者是计算法则，一般也就是这两处的修改，按照要求去变动就行。

![image-20250607185800698](.\Screenshot\image-20250607185800698.png)

计算法则如上图所示。

![image-20250607185846169](.\Screenshot\image-20250607185846169.png)

学位课筛选请修改此处。



## 使用方法

一般直接拉release下载就行，这里就只编译了Windows平台了，其他平台自己拉源代码跑requirements.txt就能运行了，用的pyQt5所以一定要有图形化界面（说的就是用Linux的人）。建议Python版本在3.9以上哈，也可以自己用Pyinstall打包一下。



## 后言

俺终于毕业了，估计以学校的习惯到时候又得改标准，希望这个工具你们有人能够慢慢完善一下，比较demo。或者提issue我有空改也行，诸君顺利。