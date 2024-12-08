import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import threading
from tkinter import messagebox
import json
import os
import pygame
import sys

class TopLevelNotification(tk.Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("提示")
        
        # 设置窗口始终置顶
        self.attributes('-topmost', True)
        
        # 获取屏幕尺寸
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # 设置窗口大小
        window_width = 300
        window_height = 150
        
        # 计算窗口位置，使其居中显示
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口大小和位置
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 添加消息标签
        label = ttk.Label(self, text=message, wraplength=250, justify="center")
        label.pack(pady=20)
        
        # 添加确定按钮
        button = ttk.Button(self, text="确定", command=self.destroy)
        button.pack(pady=10)
        
        # 设置焦点到确定按钮
        button.focus_set()
        
        # 绑定回车键到确定按钮
        self.bind("<Return>", lambda e: self.destroy())
        
        # 禁用最小化和最大化按钮
        self.resizable(False, False)

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("番茄钟")
        
        # 设置窗口大小
        window_width = 400
        window_height = 500
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算窗口位置，使其居中显示
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口大小和位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)  # 禁止调整窗口大小
        
        # 初始化pygame音频
        pygame.mixer.init()
        
        # 状态变量
        self.is_running = False
        self.is_break = False
        self.paused = False
        self.completed_count = 0
        self.remaining_time = 0
        self.timer_id = None  # 添加计时器ID变量
        
        # 默认时间设置（分钟）
        self.work_time = tk.IntVar(value=25)
        self.break_time = tk.IntVar(value=5)
        
        # 只跟踪工作时间的变化
        self.work_time.trace_add("write", self.update_display_time)
        
        self.setup_ui()
        self.setup_tray()
        self.setup_hotkeys()
        
        # 加载音效文件
        self.sound_file = os.path.join(os.path.dirname(__file__), "notification.mp3")
        
    def setup_ui(self):
        # 时间设置框架
        settings_frame = ttk.LabelFrame(self.root, text="时间设置（分钟）", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # 工作时间设置
        ttk.Label(settings_frame, text="工作时间:").grid(row=0, column=0, padx=5)
        vcmd = (self.root.register(self.validate_number), '%P')
        self.work_spinbox = ttk.Spinbox(
            settings_frame,
            from_=1,
            to=60,
            width=12,
            textvariable=self.work_time,
            validate='all',
            validatecommand=vcmd
        )
        self.work_spinbox.grid(row=0, column=1, padx=5)
        self.work_spinbox.bind('<FocusOut>', self.on_focus_out)
        self.work_spinbox.bind('<Return>', lambda e: self.on_focus_out(e))
        
        # 休息时间设置
        ttk.Label(settings_frame, text="休息时间:").grid(row=0, column=2, padx=5)
        self.break_spinbox = ttk.Spinbox(
            settings_frame,
            from_=1,
            to=30,
            width=12,
            textvariable=self.break_time,
            validate='all',
            validatecommand=vcmd
        )
        self.break_spinbox.grid(row=0, column=3, padx=5)
        self.break_spinbox.bind('<FocusOut>', self.on_focus_out)
        self.break_spinbox.bind('<Return>', lambda e: self.on_focus_out(e))
        
        # 设置spinbox的按钮样式
        style = ttk.Style()
        style.configure('TSpinbox', arrowsize=13)  # 设置上下箭头的大小
        
        # 计时器显示
        self.timer_label = ttk.Label(self.root, text="25:00", font=("Arial", 48))
        self.timer_label.pack(pady=20)
        
        # 状态显示
        self.status_label = ttk.Label(self.root, text="准备开始")
        self.status_label.pack()
        
        # 完成次数显示
        self.count_label = ttk.Label(self.root, text="完成次数: 0")
        self.count_label.pack(pady=10)
        
        # 控制按钮
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="开始", command=self.start_timer)
        self.start_button.pack(side="left", padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="暂停", command=self.pause_timer,
                                     state="disabled")
        self.pause_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="停止", command=self.stop_timer,
                                    state="disabled")
        self.stop_button.pack(side="left", padx=5)

    def setup_tray(self):
        # 创建系统托盘图标
        if 'win' in sys.platform:
            try:
                import pystray
                from PIL import Image, ImageDraw, ImagePath

                # 创建一个透明背景的图标
                icon_size = 64
                icon = Image.new('RGBA', (icon_size, icon_size), color=(0, 0, 0, 0))
                draw = ImageDraw.Draw(icon)
                
                # 定义叶子的颜色
                leaf_color = (76, 175, 80)  # 使用Material Design的绿色
                
                # 创建一个更自然的叶子形状
                leaf_shape = [
                    (32, 12),  # 顶部
                    (45, 25),  # 右上
                    (48, 32),  # 右中
                    (45, 39),  # 右下
                    (32, 52),  # 底部
                    (19, 39),  # 左下
                    (16, 32),  # 左中
                    (19, 25),  # 左上
                ]
                
                # 绘制主叶片
                draw.polygon(leaf_shape, fill=leaf_color)
                
                # 添加叶子中脉
                draw.line([(32, 12), (32, 52)], fill=(67, 160, 71), width=2)
                
                # 添加一些叶脉细节
                for i in range(20, 45, 5):
                    # 左侧叶脉
                    draw.line([(32, i), (22, i+5)], fill=(67, 160, 71), width=1)
                    # 右侧叶脉
                    draw.line([(32, i), (42, i+5)], fill=(67, 160, 71), width=1)
                
                def on_click(icon, item):
                    if str(item) == "显示":
                        self.root.deiconify()
                    elif str(item) == "退出":
                        self.quit_app()
                
                menu = (
                    pystray.MenuItem("显示", on_click),
                    pystray.MenuItem("退出", on_click)
                )
                
                self.tray_icon = pystray.Icon("番茄钟", icon, "番茄钟", menu)
                threading.Thread(target=self.tray_icon.run, daemon=True).start()
            except ImportError:
                print("无法创建系统托盘图标")

    def setup_hotkeys(self):
        # 绑定快捷键
        self.root.bind("<Control-s>", lambda e: self.start_timer())
        self.root.bind("<Control-p>", lambda e: self.pause_timer())
        self.root.bind("<Control-x>", lambda e: self.stop_timer())

    def start_timer(self):
        """开始计时"""
        if not self.is_running:
            # 如果是新的计时开始
            self.is_running = True
            self.paused = False
            if not self.is_break:
                self.remaining_time = self.work_time.get() * 60
            else:
                self.remaining_time = self.break_time.get() * 60
            # 更新按钮状态
            self.start_button.configure(state="disabled")
            self.pause_button.configure(state="normal")
            self.stop_button.configure(state="normal")
            self.update_timer()
        elif self.paused:
            # 如果是从暂停状态恢复
            self.paused = False
            # 更新按钮状态
            self.start_button.configure(state="disabled")
            self.pause_button.configure(state="normal")
            self.status_label.config(text="工作中..." if not self.is_break else "休息中...")
            # 继续计时
            self.update_timer()

    def pause_timer(self):
        """暂停计时"""
        if self.is_running and not self.paused:
            self.paused = True
            if self.timer_id:  # 取消当前的计时器
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            self.status_label.config(text="已暂停")
            # 更新按钮状态
            self.start_button.configure(state="normal")
            self.pause_button.configure(state="disabled")

    def stop_timer(self):
        """停止计时"""
        self.is_running = False
        self.paused = False
        self.is_break = False
        self.remaining_time = 0
        if self.timer_id:  # 取消当前的计时器
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_label.config(text=f"{self.work_time.get():02d}:00")
        self.status_label.config(text="准备开始")
        # 更新按钮状态
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
        self.stop_button.configure(state="disabled")

    def update_timer(self):
        """更新计时器"""
        if self.is_running and not self.paused:
            if self.remaining_time > 0:
                minutes = self.remaining_time // 60
                seconds = self.remaining_time % 60
                self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.status_label.config(text="工作中..." if not self.is_break else "休息中...")
                self.remaining_time -= 1
                # 设置下一次更新
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.timer_complete()

    def timer_complete(self):
        if not self.is_break:
            self.completed_count += 1
            self.count_label.config(text=f"完成次数: {self.completed_count}")
            self.play_notification()
            TopLevelNotification(self.root, "工作时间结束！该休息了！")
            self.is_break = True
            self.remaining_time = self.break_time.get() * 60
            self.status_label.config(text="休息时间")
            self.update_timer()
        else:
            self.play_notification()
            TopLevelNotification(self.root, "休息结束！开始新的工作吧！")
            self.is_break = False
            self.stop_timer()

    def play_notification(self):
        try:
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"播放提示音失败: {e}")

    def quit_app(self):
        pygame.mixer.quit()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.root.quit()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.root.mainloop()

    def minimize_to_tray(self):
        self.root.withdraw()

    def update_display_time(self, *args):
        """更新显示的时间"""
        if not self.is_running:  # 只在非运行状态下更新显示
            try:
                minutes = self.work_time.get()
                if minutes > 0:
                    self.timer_label.config(text=f"{minutes:02d}:00")
                else:
                    self.timer_label.config(text="00:00")
            except tk.TclError:
                self.timer_label.config(text="00:00")

    def validate_number(self, value):
        """验证输入是否为有效数字"""
        if value == "":
            return True
        try:
            val = int(value)
            return 0 <= val <= 60
        except ValueError:
            return False

    def on_focus_out(self, event):
        """失去焦点时确保值在有效范围内"""
        widget = event.widget
        try:
            val = int(widget.get())
            if val < 1:
                widget.set(1)
            elif val > 60:
                widget.set(60)
        except ValueError:
            # 设置默认值
            if widget == self.work_spinbox:
                widget.set(25)
            else:
                widget.set(5)
        
        # 如果是回车键，移动焦点到下一个部件
        if event.type == '2':  # KeyPress event
            widget.tk_focusNext().focus()

if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
