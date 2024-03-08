import json
import threading
import time
import tkinter as tk
from tkinter import ttk
import tools
from PIL import Image, ImageTk
import time
import json

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SMU抢课")
        self.create_widgets()
        self.session = None
        self.semester_id_map = {}  # 用于存储选项文本到ID的映射
        self.semester_id = None
        self.profileid = None
        self.lesson_id = None

    def create_widgets(self):
        # 设置组件之间的间隔
        padx_value = 10
        pady_value = 5

        # 用户名和密码输入框
        username_label = ttk.Label(self, text="学号")
        # 创建一个Tkinter变量
        vcmd = (self.register(self.only_numeric_input), '%P')
        self.username_entry = ttk.Entry(self, validate="key", validatecommand=vcmd)
        password_label = ttk.Label(self, text="密码")
        # self.password_entry = ttk.Entry(self, show="*")
        self.password_entry = ttk.Entry(self)

        # 验证码部分
        captcha_label = ttk.Label(self, text="验证码")
        self.captcha_entry = ttk.Entry(self, validate="key", validatecommand=vcmd)
        # 这里我们用一个标签替代验证码图片
        self.captcha_image_label = ttk.Label(self, text="登录前请获取验证码")

        # 登录和刷新按钮
        login_button = ttk.Button(self, text="登录", command=self.login)
        refresh_button = ttk.Button(self, text="刷新验证码\n或重新登陆", command=self.set_captcha_pic)

        # 课程名搜索输入框
        lesson_label = ttk.Label(self, text="课程名")
        self.lesson_entry = ttk.Entry(self)

        # 学期下拉框
        semester_label = ttk.Label(self, text="学期")
        # 初始化下拉框选项为空
        self.semester_combobox = ttk.Combobox(self, values=[])
        self.semester_combobox.grid(row=0, column=1, padx=10, pady=5)

        # 课程名搜索按钮
        self.lesson_button = ttk.Button(self, text="搜索课程名", command=self.search)

        # 选lessonId表单
        # 创建Treeview表格
        self.tree = ttk.Treeview(self)

        # 定义列
        self.tree['columns'] = ('Lessonid', '课序号', '课程号', '课程名', '教师', '实际人数', '上限')


        # 格式设置
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Lessonid", anchor=tk.CENTER, width=100)
        self.tree.column("课序号", anchor=tk.CENTER, width=100)
        self.tree.column("课程号", anchor=tk.CENTER, width=100)
        self.tree.column("课程名", anchor=tk.CENTER, width=100)
        self.tree.column("教师", anchor=tk.CENTER, width=80)
        self.tree.column("实际人数", anchor=tk.CENTER, width=80)
        self.tree.column("上限", anchor=tk.CENTER, width=80)

        # 创建表头
        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("Lessonid", text="Lessonid", anchor=tk.CENTER)
        self.tree.heading("课序号", text="课序号", anchor=tk.CENTER)
        self.tree.heading("课程号", text="课程号", anchor=tk.CENTER)
        self.tree.heading("课程名", text="课程名", anchor=tk.CENTER)
        self.tree.heading("教师", text="教师", anchor=tk.CENTER)
        self.tree.heading("实际人数", text="实际人数", anchor=tk.CENTER)
        self.tree.heading("上限", text="上限", anchor=tk.CENTER)

        # 添加数据
        data = [
        ]

        # 为Treeview添加滚动条
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        # 信息显示文本框
        self.info_text = ttk.Label(self, text="请先登录您的账号")
        # info_text.insert(tk.END, "登录内容显示区域，如验证码错误，登录成功等信息")

        # 控制台内容输出文本框
        self.console_text = tk.Text(self, height=15, width=47)
        self.console_text.insert(tk.END, "控制台内容输出文本框")

        # Lessonid、Profileid、访问间隔输入框
        lessonid_label = ttk.Label(self, text="Lessonid")
        self.lessonid_entry = ttk.Entry(self, validate="key", validatecommand=vcmd)
        profileid_label = ttk.Label(self, text="Profileid")
        self.profileid_entry = ttk.Entry(self, validate="key", validatecommand=vcmd)
        interval_label = ttk.Label(self, text="间隔秒数")
        self.interval_entry = ttk.Entry(self, validate="key", validatecommand=vcmd)
        self.interval_entry.insert(0, "1")  # 插入Lessonid

        # 开始按钮
        start_button = ttk.Button(self, text="开始", command=self.start)

        # 布局
        username_label.grid(row=0, column=0, padx=padx_value, pady=pady_value)
        self.username_entry.grid(row=0, column=1, padx=padx_value, pady=pady_value)
        password_label.grid(row=1, column=0, padx=padx_value, pady=pady_value)
        self.password_entry.grid(row=1, column=1, padx=padx_value, pady=pady_value)
        captcha_label.grid(row=2, column=0, padx=padx_value, pady=pady_value)
        self.captcha_entry.grid(row=2, column=1, padx=padx_value, pady=pady_value)
        self.captcha_image_label.grid(row=1, column=2, padx=padx_value, pady=pady_value, rowspan=2)
        login_button.grid(row=0, column=3, padx=padx_value, pady=pady_value)
        refresh_button.grid(row=1, column=3, padx=padx_value, pady=pady_value, rowspan=2)

        self.info_text.grid(row=3, column=0, columnspan=4, padx=padx_value, pady=pady_value)
        self.console_text.grid(row=8, column=2, columnspan=30, padx=padx_value, pady=pady_value)

        profileid_label.grid(row=4, column=0, padx=padx_value, pady=pady_value)
        self.profileid_entry.grid(row=4, column=1, padx=padx_value, pady=pady_value)
        lessonid_label.grid(row=5, column=0, padx=padx_value, pady=pady_value)
        self.lessonid_entry.grid(row=5, column=1, padx=padx_value, pady=pady_value)
        interval_label.grid(row=6, column=0, padx=padx_value, pady=pady_value)
        self.interval_entry.grid(row=6, column=1, padx=padx_value, pady=pady_value)
        start_button.grid(row=8, column=0, padx=padx_value, pady=pady_value, columnspan=2)

        # 课程搜索区
        self.semester_combobox.grid(row=4, column=3, padx=padx_value, pady=pady_value)
        self.semester_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)
        semester_label.grid(row=4, column=2, padx=padx_value, pady=pady_value)
        lesson_label.grid(row=5, column=2, padx=padx_value, pady=pady_value)
        self.lesson_entry.grid(row=5, column=3, padx=padx_value, pady=pady_value)
        self.lesson_button.grid(row=6, column=3, padx=padx_value, pady=pady_value)
        self.tree.grid(row=7, column=0, sticky='nsew', columnspan=30)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        scroll.grid(row=7, column=24, sticky='ns', columnspan=30)

    def only_numeric_input(self,P):
        # 如果输入为空或者为数字，则验证通过
        if P.isdigit() or P == "":
            return True
        else:
            return False

    def set_captcha_pic(self):
        # 获取图片
        self.session, self.execution = tools.get_captcha()
        # 打开图片
        captcha_image = Image.open("captcha.png")
        # 缩放图片到新尺寸，例如100x50
        new_size = (108, 50)
        resized_captcha = captcha_image.resize(new_size)
        # 将缩放后的图片转换为PhotoImage
        captcha_photo = ImageTk.PhotoImage(resized_captcha)
        # 保存对PhotoImage对象的引用，防止被垃圾回收
        self.captcha_image = captcha_photo
        # 更新标签的图片
        self.captcha_image_label.config(image=captcha_photo)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        validateCode = self.captcha_entry.get()

        if self.session and username and password and self.execution and validateCode is not None:
            name_and_id = tools.login(self.session, username, password, validateCode, self.execution)
            if name_and_id:
                self.info_text.config(text=f"登陆成功 {name_and_id}", foreground="green")

                self.semester = tools.get_semester(self.session)
                self.update_semester_options(self.semester)

                self.profileid = tools.get_profileid(self.session)
                if self.profileid:
                    self.profileid_entry.delete(0, tk.END)  # 删除profileid当前内容
                    self.profileid_entry.insert(0, self.profileid)  # 插入profileid
                    self.info_text.config(text=f"登陆成功 {name_and_id} 已获取到profileid={self.profileid}", foreground="green")
                else:
                    self.info_text.config(text=f"登陆成功 {name_and_id} 暂未获取到profileid",foreground="green")

            else:
                self.info_text.config(text="登陆失败 请刷新验证码后重试", foreground="red")
        else:
            self.info_text.config(text="登陆失败 您还未填写学号、密码、验证码", foreground="red")

    def update_semester_options(self, json_data):
        semester_options = []
        self.semester_id_map.clear()  # 清除旧的映射
        # 从json_data构建选项列表
        json_data = json.loads(json_data)
        for item in json_data:
            option_text = f"{item['schoolYear']} {item['name']}"
            semester_options.append(option_text)
            self.semester_id_map[option_text] = item['id']

        self.semester_combobox['values'] = semester_options
        if semester_options:
            self.semester_combobox.current(0)

    def on_combobox_select(self, event):
        selected_option = self.semester_combobox.get()
        self.semester_id = self.semester_id_map.get(selected_option)
        print(f"选中的学期ID: {self.semester_id}")

    def search(self):
        lesson_name = self.lesson_entry.get()
        if lesson_name and self.semester_id:
            lesson_data = tools.search_lesson(self.session, self.semester_id, lesson_name)
            self.clear_treeview()
            for item in lesson_data:
                self.tree.insert('', 'end', values=item)

    # 清除 Treeview 中的所有数据
    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def on_tree_select(self,event):
        # 获取选中的行ID
        selected_id = self.tree.selection()

        # 遍历所有选中的项（本例中假设只能选中一个）
        for sid in selected_id:
            item = self.tree.item(sid)
            self.lesson_id = item['values'][0]
            print(f"选中的Lessonid: {self.lesson_id}")
            self.lessonid_entry.delete(0, tk.END)  # 删除Lessonid当前内容
            self.lessonid_entry.insert(0, self.lesson_id)  # 插入Lessonid

    def start(self):
        self.wait_time = self.interval_entry.get()
        # 检查参数是否齐全
        if self.session and self.profileid and self.lesson_id and self.wait_time:
            self.wait_time = int(float(self.wait_time) * 1000)
            # 启动一个后台线程执行并发操作
            threading.Thread(target=self.perform_concurrent_operations, args=(self.session, self.profileid, self.lesson_id, self.wait_time),
                             daemon=True).start()

    def perform_concurrent_operations(self, session, profileId, lessonid, wait_time):
        self.sessiontime = tools.get_sessiontime(session, profileId)
        self.console_text.delete("1.0", tk.END)
        def task():
            result = tools.elect(session, profileId, self.sessiontime, lessonid)  # 执行elect函数
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if "同时打开多个选课页面，请至最新页面进行操作" in result:
                result = "选课页面失效，重新获取sessiontime"
                self.console_text.insert(tk.END, f"{current_time}: {result}\n")
                self.sessiontime = tools.get_sessiontime(session, profileId)
            else:
                # 将结果插入到console_text中
                self.console_text.insert(tk.END, f"{current_time}: {result}\n")
                self.console_text.see(tk.END)  # 滚动到底部
                self.after(wait_time, task)  # wait_time秒后再次执行task


        self.after(0, task)  # 立即执行task


# 运行程序
if __name__ == "__main__":
    app = Application()
    app.mainloop()
