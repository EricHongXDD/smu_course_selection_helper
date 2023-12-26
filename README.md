# smu_course_election_helper
Request实现的SHMTU教务系统抢课辅助软件

# 声明 Statement
本软件不得用于商业用途，仅供学习交流，切勿用于非法用途，对此产生的一切后果作者本人概不负责。

This project can not be used for commercial purposes, it is intended solely for learning and communication. Do not use it for illegal purposes. The author is not responsible for any consequences that arise from its use.
# 用法 Usage
## Cookies：登录SHMTU教务系统或数字平台获取到的Cookies
https://jwxt.shmtu.edu.cn

https://portal.shmtu.edu.cn

## ProfileId：选课课次ID
 
如https://jwxt.shmtu.edu.cn/shmtu/stdElectCourse!defaultPage.action?electionProfile.id=1234

则ProfileId=1234

## Lessonid：课程ID
 
PC电脑端访问https://jwxt.shmtu.edu.cn/shmtu/teachTaskSearch!arrangeInfoList.action

搜索到课程后，点击对应课程前方的课序号

点击后得到当前页面链接

得到的链接类似如：https://jwxt.shmtu.edu.cn/shmtu/courseTable!taskTable.action?lesson.id=212345

则Lessonid=212345

## 间隔秒数：

相邻两次请求发送的间隔时间，单位为秒（s），可接受float类型小数
