import time
import json
import re
import requests
from lxml import html
import lxml
from bs4 import BeautifulSoup

def get_captcha():
    # 发送GET请求到登录页面
    login_url = "https://cas.shmtu.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.shmtu.edu.cn%2Fshmtu%2Fhome.action"
    session = requests.Session()  # 使用session对象，这样Cookies会自动处理
    response = session.get(login_url)

    # 解析HTML
    tree = html.fromstring(response.text)
    # 提取名为'execution'的隐藏表单值
    execution_value = tree.xpath('//*[@id="login-form-controls"]/section[5]/input[1]/@value')[0]
    # print(execution_value)

    # 使用同一个session对象获取验证码图片，确保Cookies一致
    captcha_url = "https://cas.shmtu.edu.cn/cas/captcha"
    captcha_response = session.get(captcha_url)

    # 保存图片到本地
    with open('captcha.png', 'wb') as f:
        f.write(captcha_response.content)

    return session, execution_value

def login(session,username,password,validateCode,execution):
    login_url = "https://cas.shmtu.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.shmtu.edu.cn%2Fshmtu%2Fhome.action"
    data = {
        "username": username,
        "password": password,
        "validateCode": validateCode,
        "execution": execution,
        "_eventId": "submit",
        "geolocation": None
    }
    response = session.post(url=login_url, data=data)
    # print(response.text)
    # 解析HTML
    tree = html.fromstring(response.text)
    name_and_id_text = tree.xpath("//div[@class='welcome_bar']/form/span[@class='f5']/text()")

    # 检查是否成功找到目标文本
    if name_and_id_text:
        name_and_id = name_and_id_text[0]  # 提取列表中的第一个元素
        print("学生姓名（学号）" + name_and_id)
    else:
        name_and_id = None

    return name_and_id

def get_semester(session):
    url = "https://jwxt.shmtu.edu.cn/shmtu/dataQuery.action"
    data = {
        "dataType": "semesterCalendar",
        "empty": False,
    }
    response = session.post(url=url, data=data)
    # print(response.text)
    response_text = response.text
    # 使用正则表达式找到semesters部分的字符串
    match = re.search(r"semesters:\s*(\{.*?\}),yearIndex", response_text, re.DOTALL)

    if match:
        # 获取匹配到的semesters字符串
        semesters_str = match.group(1)

        # 由于原始字符串可能不是标准的JSON格式（特别是在键周围缺少引号的情况）
        # 所以这里我们使用正则表达式进一步处理这个字符串
        semesters_str = re.sub(r"(\w+):", r'"\1":', semesters_str)  # 给键加上引号
        semesters_str = semesters_str.replace("'", '"')  # 将单引号替换为双引号
        semesters_data = json.loads(semesters_str)
        # 准备一个列表来收集处理后的数据
        processed_data = []

        # 遍历解析后的数据
        for year, records in semesters_data.items():
            for record in records:
                # 提取和转换数据
                _id = record['id']
                school_year = record['schoolYear']
                name = "第一学期" if record['name'] == "1" else "第二学期"

                # 将处理后的数据添加到列表中
                processed_data.append({
                    "id": _id,
                    "schoolYear": school_year,
                    "name": name
                })
        # 将收集到的数据转换为JSON字符串
        json_output = json.dumps(processed_data, ensure_ascii=False, indent=4)
    else:
        json_output = None

    return json_output

def get_profileid(session):
    # 发送GET请求到登录页面
    url = "https://jwxt.shmtu.edu.cn/shmtu/stdElectCourse.action?_=1709844836012"
    response = session.get(url=url)
    # 定义一个正则表达式来匹配所需的模式
    pattern = r"/shmtu/stdElectCourse!defaultPage.action\?electionProfile.id=(\d+)"
    # 使用findall方法查找所有匹配的情况
    matches = re.findall(pattern, response.text)
    # print(matches[0])

    return str(matches[0])

def search_lesson(session,semester_id,name):
    data = {
        "lesson.semester.id": semester_id,
        "lesson.project.id": 1,
        "lesson.no": None,
        "lesson.course.code": None,
        "lesson.course.name": name,
        "lesson.course.category.name": None,
        "lesson.course.courseType.id": None,
        "fake.adminclass.name": None,
        "lesson.teachClass.depart.id": None,
        "lesson.teachDepart.id": None,
        "fake.crossdepart": None,
        "teacher.name": None,
        "fake.teacher.null": None,
        "fake.teacher.department.id": None,
        "lesson.teachClass.grade": None,
        "fake.stdCount.start": None,
        "fake.stdCount.end": None,
        "lesson.courseSchedule.status": None,
        "fake.time.weekday": None,
        "fake.time.unit": None,
        "fake.week.start": None,
        "fake.week.end": None,
        "fake.limitCount.start": None,
        "fake.limitCount.end": None
    }

    url = "https://jwxt.shmtu.edu.cn/shmtu/teachTaskSearch!arrangeInfoList.action"
    response = session.post(url=url, data=data)
    soup = BeautifulSoup(response.text, 'lxml')
    data = []
    # 查找所有<tr>标签，这些标签包含课程信息
    for tr in soup.select('tbody[id$="_data"] tr'):
        try:
            lesson_id = tr.select_one('input[name="lesson.id"]')['value']
            course_seq = tr.select_one('td:nth-of-type(2) a').text.strip()
            course_code = tr.select_one('td:nth-of-type(3)').text.strip()
            course_name = tr.select_one('td:nth-of-type(4) a').text.strip()
            teacher = tr.select_one('td:nth-of-type(7)').text.strip()
            actual_count = tr.select_one('td:nth-of-type(8)').text.strip()
            limit = tr.select_one('td:nth-of-type(9)').text.strip()

            data.append((lesson_id, course_seq, course_code, course_name, teacher, actual_count, limit))
        except Exception as e:
            print(f"Error processing row: {e}")
            data = None

    return data


def get_sessiontime(session, profileId):
    while True:
        try:
            url = "https://jwxt.shmtu.edu.cn/shmtu/stdElectCourse!defaultPage.action?electionProfile.id=" + str(profileId)
            result = session.get(url)
            data = result.text
            # print(data)
            # 解析HTML
            tree = lxml.html.fromstring(data)
            # 使用XPath定位元素
            element = tree.xpath('/html/body/form[1]/input')[0]  # [0]用于获取第一个匹配的元素
            # 从元素中提取value属性
            value = element.get('value')
            print("sessiontime=" + value)  # 打印提取的value值
            return value
        except Exception as e:
            print("get_sessiontime出错")
            print("错误信息：", e)
            time.sleep(2)


def elect(session, profileId, elecSessionTime, lessonid):
    try:
        url = "https://jwxt.shmtu.edu.cn/shmtu/stdElectCourse!batchOperator.action?profileId=" + str(
            profileId) + "&elecSessionTime=" + str(elecSessionTime)

        data = {
            "operator0": str(lessonid) + ":true:0"
        }

        result = session.post(url, data=data)
        data = result.text
        # print(data)
        # 解析HTML
        tree = lxml.html.fromstring(data)
        # 使用XPath定位元素
        # 成功
        element = tree.xpath('//div[@style="width:85%;color:green;text-align:left;margin:auto;"]')
        # 检查是否找到了匹配的元素，并从中提取文本内容
        if element:
            result = element[0].text_content().strip()  # 使用text_content()获取文本并使用strip()删除前导和尾随的空白
        else:
            # 失败
            element = tree.xpath('//div[@style="width:85%;color:red;text-align:left;margin:auto;"]')
            if element:
                result = element[0].text_content().strip()  # 使用text_content()获取文本并使用strip()删除前导和尾随的空白
            else:
                result = "返回结果错误!"
        print(result)
        return result
    except Exception as e:
        print("elect出错")
        print("错误信息：", e)
        time.sleep(2)


