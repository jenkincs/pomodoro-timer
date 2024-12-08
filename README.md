# Pomodoro Timer 番茄工作法计时器

[English](#english) | [中文](#中文)

<a name="english"></a>
## English

A simple yet powerful Pomodoro Timer built with Python and Tkinter.

### Features

- Customizable work and break times (1-60 minutes)
- Clean and intuitive user interface
- System tray support
- Sound notifications
- Pause/Resume functionality
- Completion counter
- Windows 10/11 support

### Usage

#### Direct Use

1. Download `PomodoroTimer.exe` from the `dist` folder
2. Double-click to run the program
3. Set work time (1-60 minutes) and break time (1-30 minutes)
4. Click the start button to begin timing

#### Basic Operations

- **Start**: Click "Start" button or press Ctrl+S
- **Pause/Resume**: Click "Pause" button or press Ctrl+P
- **Stop**: Click "Stop" button or press Ctrl+X
- **Minimize**: Program minimizes to system tray
- **Exit**: Right-click system tray icon and select "Exit"

### Building from Source

#### Requirements

- Python 3.10 or higher
- pip (Python package manager)
- Windows 10/11 operating system

#### Installation Steps

1. Clone or download the source code
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate icon (optional):
   ```bash
   python create_icon.py
   ```
4. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
5. Package the program:
   ```bash
   pyinstaller pomodoro.spec
   ```

The packaged program will be in the `dist` folder.

#### Running from Source

If you don't need packaging, you can run the source directly:
```bash
python pomodoro.py
```

### Project Structure

- `pomodoro.py`: Main program source code
- `notification.mp3`: Alert sound file
- `requirements.txt`: Project dependencies
- `pomodoro.spec`: PyInstaller configuration
- `create_icon.py`: Icon generation script
- `tomato.ico`: Program icon

### Dependencies

- tkinter: GUI interface
- pygame: Audio playback
- pillow: Image processing
- pystray: System tray support

### Notes

1. First run may require firewall permission
2. Program plays alert sound at the end of work/break periods
3. Program continues running in background when minimized
4. Quick access through system tray icon

### Development Plans

- [ ] Add more customization options
- [ ] Support custom alert sounds
- [ ] Add statistics functionality
- [ ] Support theme switching
- [ ] Add task list feature

### Feedback

If you encounter any issues or have suggestions, please submit an Issue.

### License

MIT License

---

<a name="中文"></a>
## 中文

一个简单但功能强大的番茄工作法计时器，使用Python和Tkinter构建。

### 功能特点

- 可自定义的工作和休息时间（1-60分钟）
- 简洁的用户界面
- 系统托盘支持
- 声音提醒
- 暂停/继续功能
- 完成次数统计
- Windows 10/11 支持

### 使用方法

#### 直接使用

1. 下载 `dist` 文件夹中的 `PomodoroTimer.exe`
2. 双击运行程序
3. 设置工作时间（1-60分钟）和休息时间（1-30分钟）
4. 点击开始按钮开始计时

#### 基本操作

- **开始**: 点击"开始"按钮或按 Ctrl+S
- **暂停/继续**: 点击"暂停"按钮或按 Ctrl+P
- **停止**: 点击"停止"按钮或按 Ctrl+X
- **最小化**: 程序会最小化到系统托盘
- **退出**: 右键系统托盘图标选择"退出"

### 从源码构建

#### 环境要求

- Python 3.10 或更高版本
- pip（Python包管理器）
- Windows 10/11 操作系统

#### 安装步骤

1. 克隆或下载源代码
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 生成图标（可选）：
   ```bash
   python create_icon.py
   ```
4. 安装PyInstaller：
   ```bash
   pip install pyinstaller
   ```
5. 打包程序：
   ```bash
   pyinstaller pomodoro.spec
   ```

打包后的程序在 `dist` 文件夹中。

#### 直接运行源码

如果不需要打包，可以直接运行源码：
```bash
python pomodoro.py
```

### 项目结构

- `pomodoro.py`: 主程序源码
- `notification.mp3`: 提示音效文件
- `requirements.txt`: 项目依赖
- `pomodoro.spec`: PyInstaller打包配置
- `create_icon.py`: 图标生成脚本
- `tomato.ico`: 程序图标

### 依赖项

- tkinter: GUI界面
- pygame: 音频播放
- pillow: 图像处理
- pystray: 系统托盘支持

### 注意事项

1. 首次运行可能需要允许防火墙权限
2. 程序会在工作/休息时间结束时播放提示音
3. 最小化时程序会继续在后台运行
4. 可以通过系统托盘图标快速操作程序

### 开发计划

- [ ] 添加更多自定义选项
- [ ] 支持自定义提示音
- [ ] 添加统计功能
- [ ] 支持主题切换
- [ ] 添加任务列表功能

### 问题反馈

如果遇到问题或有建议，请提交Issue。

### 许可证

MIT License
