import os
import glob
from PyQt5.QtWidgets import QLabel, QMenu, QAction, QApplication
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from task_monitor_api import TaskStatus

class PetWidget(QLabel):
    """桌面宠物挂件组件"""

    # 信号定义
    double_clicked = pyqtSignal()  # 双击信号
    settings_requested = pyqtSignal()  # 设置请求信号
    quit_requested = pyqtSignal()  # 退出请求信号
    position_changed = pyqtSignal(int, int)  # 位置变化信号 (x, y)

    def __init__(self, pet_name: str = "meizi", parent=None):
        super().__init__(parent)

        self.pet_name = pet_name
        self.images = []
        self.current_frame = 0
        self.animation_timer = QTimer()
        self.animation_speed = 250  # 毫秒
        self.is_dragging = False
        self.drag_start_position = QPoint()
        self.size_scale = 1.0

        # 动画状态
        self.animation_state = "idle"  # idle, running, completed
        self.is_animating = False

        self.init_ui()
        self.load_pet_images()
        self.setup_animation()
        self.setup_context_menu()

    def init_ui(self):
        """初始化UI"""
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # 设置鼠标追踪
        self.setMouseTracking(True)

    def load_pet_images(self):
        """加载宠物图片"""
        images_dir = os.path.join("images", self.pet_name)
        if not os.path.exists(images_dir):
            print(f"宠物图片目录不存在: {images_dir}")
            return

        # 获取所有PNG图片并排序
        pattern = os.path.join(images_dir, f"{self.pet_name}_*.png")
        image_files = glob.glob(pattern)

        # 按数字排序
        def extract_number(filename):
            try:
                base = os.path.basename(filename)
                number_str = base.split('_')[-1].split('.')[0]
                return int(number_str)
            except:
                return 0

        image_files.sort(key=extract_number)

        # 加载图片
        self.images = []
        for image_file in image_files:
            pixmap = QPixmap(image_file)
            if not pixmap.isNull():
                # 应用缩放
                if self.size_scale != 1.0:
                    size = pixmap.size()
                    new_size = size * self.size_scale
                    pixmap = pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.images.append(pixmap)

        if self.images:
            self.setPixmap(self.images[0])
            self.adjustSize()
        else:
            print(f"未找到宠物图片: {self.pet_name}")

    def setup_animation(self):
        """设置动画"""
        self.animation_timer.timeout.connect(self.next_frame)

    def setup_context_menu(self):
        """设置右键菜单"""
        pass  # 在show_context_menu中实现

    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)

        # 设置菜单项
        settings_action = QAction("设置", self)
        # 添加设置图标
        eye_icon_path = os.path.join("images", "eye.png")
        if os.path.exists(eye_icon_path):
            settings_action.setIcon(QIcon(eye_icon_path))
        settings_action.triggered.connect(self.settings_requested.emit)
        menu.addAction(settings_action)

        menu.addSeparator()

        # 退出菜单项
        quit_action = QAction("退出", self)
        # 添加退出图标
        exit_icon_path = os.path.join("images", "exit.png")
        if os.path.exists(exit_icon_path):
            quit_action.setIcon(QIcon(exit_icon_path))
        quit_action.triggered.connect(self.quit_requested.emit)
        menu.addAction(quit_action)

        # 显示菜单
        menu.exec_(self.mapToGlobal(position))

    def set_pet(self, pet_name: str):
        """设置宠物"""
        if pet_name != self.pet_name:
            self.pet_name = pet_name
            self.load_pet_images()
            self.current_frame = 0
            if self.images:
                self.setPixmap(self.images[0])

    def set_animation_speed(self, speed: int):
        """设置动画速度"""
        self.animation_speed = speed
        if self.animation_timer.isActive():
            self.animation_timer.stop()
            self.animation_timer.start(speed)

    def set_size_scale(self, scale: float):
        """设置大小缩放"""
        if scale != self.size_scale:
            self.size_scale = scale
            self.load_pet_images()  # 重新加载并缩放图片

    def set_task_status(self, status: TaskStatus):
        """根据任务状态设置动画"""
        if status == TaskStatus.IDLE:
            self.set_animation_state("idle")
        elif status in [TaskStatus.RUNNING, TaskStatus.QUEUED]:
            self.set_animation_state("running")
        elif status == TaskStatus.COMPLETED:
            self.set_animation_state("completed")
        elif status == TaskStatus.ERROR:
            self.set_animation_state("idle")  # 错误时显示静止状态

    def set_animation_state(self, state: str):
        """设置动画状态"""
        if state == self.animation_state:
            return

        self.animation_state = state

        if state == "idle":
            # 显示第一帧静态图片
            self.stop_animation()
            if self.images:
                self.current_frame = 0
                self.setPixmap(self.images[0])

        elif state == "running":
            # 播放完整动画
            self.start_animation()

        elif state == "completed":
            # 显示最后一帧静态图片
            self.stop_animation()
            if self.images:
                self.current_frame = len(self.images) - 1
                self.setPixmap(self.images[-1])

    def start_animation(self):
        """开始动画"""
        if self.images and not self.animation_timer.isActive():
            self.animation_timer.start(self.animation_speed)
            self.is_animating = True

    def stop_animation(self):
        """停止动画"""
        if self.animation_timer.isActive():
            self.animation_timer.stop()
            self.is_animating = False

    def next_frame(self):
        """下一帧动画"""
        if not self.images:
            return

        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.setPixmap(self.images[self.current_frame])

    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.is_dragging and event.buttons() == Qt.LeftButton:
            new_position = event.globalPos() - self.drag_start_position
            self.move(new_position)
            # 发送位置变化信号
            self.position_changed.emit(new_position.x(), new_position.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.setCursor(QCursor(Qt.ArrowCursor))
        super().mouseReleaseEvent(event)

    def get_position(self):
        """获取当前位置"""
        pos = self.pos()
        return {"x": pos.x(), "y": pos.y()}

    def get_center_position(self):
        """获取宠物中心点位置"""
        pos = self.pos()
        size = self.size()
        center_x = pos.x() + size.width() // 2
        center_y = pos.y() + size.height() // 2
        return {"x": center_x, "y": center_y}

    def set_position(self, x: int, y: int):
        """设置位置"""
        self.move(x, y)
