from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QProgressBar, QTextEdit, QFrame, QPushButton)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
from typing import Dict, Any

class ProgressWindow(QWidget):
    """进度显示窗体"""

    # 信号定义
    close_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.hide_window)
        self.auto_hide_delay = 3000  # 3秒后自动隐藏

        # 进度窗口相对于宠物的偏移量
        self.offset_x = 0  # 相对于宠物中心点的X偏移
        self.offset_y = 50  # 相对于宠物中心点的Y偏移

        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 设置窗口大小
        self.setFixedSize(400, 300)

        # 创建主框架
        self.main_frame = QFrame()
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 50);
            }
        """)

        # 创建布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_frame)

        # 内容布局
        content_layout = QVBoxLayout(self.main_frame)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(10)

        # 标题
        self.title_label = QLabel("ComfyUI 工作流监控")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.title_label)

        # 状态信息
        self.status_label = QLabel("状态: 空闲")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 12px;
                padding: 2px;
            }
        """)
        content_layout.addWidget(self.status_label)

        # 任务ID
        self.task_id_label = QLabel("任务ID: 无")
        self.task_id_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 10px;
                padding: 2px;
            }
        """)
        content_layout.addWidget(self.task_id_label)

        # 工作流进度
        workflow_layout = QVBoxLayout()

        self.workflow_label = QLabel("工作流进度:")
        self.workflow_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                padding: 2px;
            }
        """)
        workflow_layout.addWidget(self.workflow_label)

        self.workflow_progress = QProgressBar()
        self.workflow_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #333;
                text-align: center;
                color: white;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
        workflow_layout.addWidget(self.workflow_progress)

        content_layout.addLayout(workflow_layout)

        # 当前节点进度
        node_layout = QVBoxLayout()

        self.node_label = QLabel("当前节点:")
        self.node_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                padding: 2px;
            }
        """)
        node_layout.addWidget(self.node_label)

        self.node_progress = QProgressBar()
        self.node_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #333;
                text-align: center;
                color: white;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 4px;
            }
        """)
        node_layout.addWidget(self.node_progress)

        content_layout.addLayout(node_layout)

        # 执行时间
        self.time_label = QLabel("执行时间: 0秒")
        self.time_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 10px;
                padding: 2px;
            }
        """)
        content_layout.addWidget(self.time_label)

        # 队列信息
        self.queue_label = QLabel("队列: 运行中 0 | 等待中 0")
        self.queue_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 10px;
                padding: 2px;
            }
        """)
        content_layout.addWidget(self.queue_label)

        # 关闭按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.close_button = QPushButton("关闭")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.close_button.clicked.connect(self.hide_window)
        button_layout.addWidget(self.close_button)

        content_layout.addLayout(button_layout)

    def update_progress(self, progress_data: Dict[str, Any]):
        """更新进度信息"""
        # 重置自动隐藏定时器
        self.auto_hide_timer.stop()

        # 更新状态
        status = progress_data.get("status", "idle")
        status_text = {
            "idle": "空闲",
            "running": "运行中",
            "completed": "已完成",
            "error": "错误",
            "queued": "排队中"
        }.get(status, status)

        self.status_label.setText(f"状态: {status_text}")

        # 设置状态颜色
        status_colors = {
            "idle": "#888888",
            "running": "#00ff00",
            "completed": "#4CAF50",
            "error": "#f44336",
            "queued": "#ff9800"
        }
        color = status_colors.get(status, "#888888")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 12px;
                padding: 2px;
            }}
        """)

        # 更新任务ID
        task_id = progress_data.get("task_id")
        if task_id:
            self.task_id_label.setText(f"任务ID: {task_id}")
        else:
            self.task_id_label.setText("任务ID: 无")

        # 更新工作流进度
        workflow_progress = progress_data.get("workflow_progress", {})
        total_nodes = workflow_progress.get("total_nodes", 0)
        executed_nodes = workflow_progress.get("executed_nodes", 0)

        if total_nodes > 0:
            workflow_percentage = int((executed_nodes / total_nodes) * 100)
            self.workflow_progress.setValue(workflow_percentage)
            self.workflow_label.setText(f"工作流进度: {executed_nodes}/{total_nodes} 节点")
        else:
            self.workflow_progress.setValue(0)
            self.workflow_label.setText("工作流进度: 无数据")

        # 更新当前节点进度
        current_progress = progress_data.get("current_task_progress")
        if current_progress:
            node_type = current_progress.get("node_type", "未知")
            step = current_progress.get("step", 0)
            total_steps = current_progress.get("total_steps", 0)

            if total_steps > 0:
                node_percentage = int((step / total_steps) * 100)
                self.node_progress.setValue(node_percentage)
                self.node_label.setText(f"当前节点: {node_type} ({step}/{total_steps})")
            else:
                self.node_progress.setValue(0)
                self.node_label.setText(f"当前节点: {node_type}")
        else:
            self.node_progress.setValue(0)
            self.node_label.setText("当前节点: 无")

        # 更新执行时间
        execution_time = progress_data.get("execution_time", 0)
        if execution_time > 0:
            if execution_time < 60:
                time_text = f"{execution_time:.1f}秒"
            else:
                minutes = int(execution_time // 60)
                seconds = execution_time % 60
                time_text = f"{minutes}分{seconds:.1f}秒"
            self.time_label.setText(f"执行时间: {time_text}")
        else:
            self.time_label.setText("执行时间: 0秒")

        # 更新队列信息
        queue_info = progress_data.get("queue", {})
        running_count = queue_info.get("running_count", 0)
        pending_count = queue_info.get("pending_count", 0)
        self.queue_label.setText(f"队列: 运行中 {running_count} | 等待中 {pending_count}")

        # 如果任务完成，设置自动隐藏
        if status in ["completed", "error"]:
            self.auto_hide_timer.start(self.auto_hide_delay)

    def show_at_position(self, x: int, y: int):
        """在指定位置显示窗口"""
        # 使用偏移量计算最终位置
        final_x = x + self.offset_x
        final_y = y + self.offset_y
        self.move(final_x, final_y)
        self.show()
        self.raise_()
        self.activateWindow()

    def show_at_center_position(self, center_x: int, center_y: int):
        """基于宠物中心点显示窗口"""
        # 计算窗口应该显示的位置（考虑窗口大小，使其居中对齐）
        window_width = self.width()
        window_height = self.height()

        # 计算最终位置：中心点 + 偏移量 - 窗口大小的一半
        final_x = center_x + self.offset_x - window_width // 2
        final_y = center_y + self.offset_y - window_height // 2

        self.move(final_x, final_y)
        self.show()
        self.raise_()
        self.activateWindow()

    def update_position_from_pet_center(self, center_x: int, center_y: int):
        """根据宠物中心点更新窗口位置（用于跟随拖动）"""
        if self.isVisible():
            window_width = self.width()
            window_height = self.height()

            final_x = center_x + self.offset_x - window_width // 2
            final_y = center_y + self.offset_y - window_height // 2

            self.move(final_x, final_y)

    def set_offset(self, offset_x: int, offset_y: int):
        """设置相对于宠物中心点的偏移量"""
        self.offset_x = offset_x
        self.offset_y = offset_y

    def get_offset(self):
        """获取当前偏移量"""
        return {"x": self.offset_x, "y": self.offset_y}

    def hide_window(self):
        """隐藏窗口"""
        self.hide()
        self.close_requested.emit()

    def set_opacity(self, opacity: float):
        """设置透明度"""
        self.setWindowOpacity(opacity)

    def mousePressEvent(self, event):
        """鼠标点击事件 - 点击窗口外部时隐藏"""
        if event.button() == Qt.LeftButton:
            # 检查点击是否在窗口内
            if not self.main_frame.geometry().contains(event.pos()):
                self.hide_window()
        super().mousePressEvent(event)
