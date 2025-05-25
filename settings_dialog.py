import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
                             QCheckBox, QPushButton, QGroupBox, QFormLayout,
                             QTabWidget, QWidget, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from config import ConfigManager

class SettingsDialog(QDialog):
    """设置对话框"""

    # 信号定义
    settings_changed = pyqtSignal(dict)  # 设置变更信号

    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)

        self.config_manager = config_manager
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("ComfyUI 宠物监控 - 设置")
        self.setFixedSize(500, 600)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        # 设置窗口图标
        net_icon_path = os.path.join("images", "net.png")
        if os.path.exists(net_icon_path):
            self.setWindowIcon(QIcon(net_icon_path))

        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建选项卡
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 服务器设置选项卡
        self.create_server_tab()

        # 宠物设置选项卡
        self.create_pet_tab()

        # 监控设置选项卡
        self.create_monitor_tab()

        # 显示设置选项卡
        self.create_display_tab()

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.test_button = QPushButton("测试连接")
        self.test_button.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_button)

        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_button)

        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept_settings)
        button_layout.addWidget(self.ok_button)

        main_layout.addLayout(button_layout)

    def create_server_tab(self):
        """创建服务器设置选项卡"""
        server_widget = QWidget()
        layout = QVBoxLayout(server_widget)

        # 服务器连接组
        server_group = QGroupBox("ComfyUI 服务器连接")
        server_form = QFormLayout(server_group)

        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["http", "https"])
        server_form.addRow("协议:", self.protocol_combo)

        self.host_edit = QLineEdit()
        self.host_edit.setPlaceholderText("127.0.0.1")
        server_form.addRow("主机地址:", self.host_edit)

        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(8188)
        server_form.addRow("端口:", self.port_spin)

        layout.addWidget(server_group)
        layout.addStretch()

        self.tab_widget.addTab(server_widget, "服务器")

    def create_pet_tab(self):
        """创建宠物设置选项卡"""
        pet_widget = QWidget()
        layout = QVBoxLayout(pet_widget)

        # 宠物外观组
        appearance_group = QGroupBox("宠物外观")
        appearance_form = QFormLayout(appearance_group)

        self.pet_combo = QComboBox()
        # 加载可用宠物
        available_pets = self.config_manager.get_available_pets()
        self.pet_combo.addItems(available_pets)
        appearance_form.addRow("宠物类型:", self.pet_combo)

        self.size_scale_spin = QDoubleSpinBox()
        self.size_scale_spin.setRange(0.1, 3.0)
        self.size_scale_spin.setSingleStep(0.1)
        self.size_scale_spin.setValue(1.0)
        self.size_scale_spin.setSuffix("x")
        appearance_form.addRow("大小缩放:", self.size_scale_spin)

        self.animation_speed_spin = QSpinBox()
        self.animation_speed_spin.setRange(50, 2000)
        self.animation_speed_spin.setSingleStep(50)
        self.animation_speed_spin.setValue(250)
        self.animation_speed_spin.setSuffix(" ms")
        appearance_form.addRow("动画速度:", self.animation_speed_spin)

        layout.addWidget(appearance_group)
        layout.addStretch()

        self.tab_widget.addTab(pet_widget, "宠物")

    def create_monitor_tab(self):
        """创建监控设置选项卡"""
        monitor_widget = QWidget()
        layout = QVBoxLayout(monitor_widget)

        # 监控设置组
        monitor_group = QGroupBox("监控设置")
        monitor_form = QFormLayout(monitor_group)

        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(100, 10000)
        self.refresh_interval_spin.setSingleStep(100)
        self.refresh_interval_spin.setValue(1000)
        self.refresh_interval_spin.setSuffix(" ms")
        monitor_form.addRow("刷新间隔:", self.refresh_interval_spin)

        self.auto_hide_check = QCheckBox("任务完成后自动隐藏进度窗口")
        self.auto_hide_check.setChecked(True)
        monitor_form.addRow(self.auto_hide_check)

        self.progress_opacity_spin = QDoubleSpinBox()
        self.progress_opacity_spin.setRange(0.1, 1.0)
        self.progress_opacity_spin.setSingleStep(0.1)
        self.progress_opacity_spin.setValue(0.8)
        monitor_form.addRow("进度窗口透明度:", self.progress_opacity_spin)

        # 进度窗口偏移设置
        offset_layout = QHBoxLayout()

        self.offset_x_spin = QSpinBox()
        self.offset_x_spin.setRange(-500, 500)
        self.offset_x_spin.setValue(0)
        self.offset_x_spin.setSuffix(" px")
        offset_layout.addWidget(QLabel("X:"))
        offset_layout.addWidget(self.offset_x_spin)

        self.offset_y_spin = QSpinBox()
        self.offset_y_spin.setRange(-500, 500)
        self.offset_y_spin.setValue(50)
        self.offset_y_spin.setSuffix(" px")
        offset_layout.addWidget(QLabel("Y:"))
        offset_layout.addWidget(self.offset_y_spin)

        offset_widget = QWidget()
        offset_widget.setLayout(offset_layout)
        monitor_form.addRow("进度窗口偏移:", offset_widget)

        layout.addWidget(monitor_group)
        layout.addStretch()

        self.tab_widget.addTab(monitor_widget, "监控")

    def create_display_tab(self):
        """创建显示设置选项卡"""
        display_widget = QWidget()
        layout = QVBoxLayout(display_widget)

        # 显示设置组
        display_group = QGroupBox("显示设置")
        display_form = QFormLayout(display_group)

        self.always_on_top_check = QCheckBox("始终置顶显示")
        self.always_on_top_check.setChecked(True)
        display_form.addRow(self.always_on_top_check)

        self.show_in_taskbar_check = QCheckBox("在任务栏显示")
        self.show_in_taskbar_check.setChecked(False)
        display_form.addRow(self.show_in_taskbar_check)

        self.enable_drag_check = QCheckBox("允许拖拽移动")
        self.enable_drag_check.setChecked(True)
        display_form.addRow(self.enable_drag_check)

        layout.addWidget(display_group)
        layout.addStretch()

        self.tab_widget.addTab(display_widget, "显示")

    def load_settings(self):
        """加载设置"""
        # 服务器设置
        self.protocol_combo.setCurrentText(self.config_manager.get("comfyui_server.protocol", "http"))
        self.host_edit.setText(self.config_manager.get("comfyui_server.host", "127.0.0.1"))
        self.port_spin.setValue(self.config_manager.get("comfyui_server.port", 8188))

        # 宠物设置
        selected_pet = self.config_manager.get("pet_settings.selected_pet", "meizi")
        index = self.pet_combo.findText(selected_pet)
        if index >= 0:
            self.pet_combo.setCurrentIndex(index)

        self.size_scale_spin.setValue(self.config_manager.get("pet_settings.size_scale", 1.0))
        self.animation_speed_spin.setValue(self.config_manager.get("pet_settings.animation_speed", 250))

        # 监控设置
        self.refresh_interval_spin.setValue(self.config_manager.get("monitor_settings.refresh_interval", 1000))
        self.auto_hide_check.setChecked(self.config_manager.get("monitor_settings.auto_hide_progress", True))
        self.progress_opacity_spin.setValue(self.config_manager.get("monitor_settings.progress_window_opacity", 0.8))

        # 进度窗口偏移设置
        offset = self.config_manager.get("monitor_settings.progress_window_offset", {"x": 0, "y": 50})
        self.offset_x_spin.setValue(offset.get("x", 0))
        self.offset_y_spin.setValue(offset.get("y", 50))

        # 显示设置
        self.always_on_top_check.setChecked(self.config_manager.get("display_settings.always_on_top", True))
        self.show_in_taskbar_check.setChecked(self.config_manager.get("display_settings.show_in_taskbar", False))
        self.enable_drag_check.setChecked(self.config_manager.get("display_settings.enable_drag", True))

    def save_settings(self):
        """保存设置"""
        # 服务器设置
        self.config_manager.set("comfyui_server.protocol", self.protocol_combo.currentText())
        self.config_manager.set("comfyui_server.host", self.host_edit.text())
        self.config_manager.set("comfyui_server.port", self.port_spin.value())

        # 宠物设置
        self.config_manager.set("pet_settings.selected_pet", self.pet_combo.currentText())
        self.config_manager.set("pet_settings.size_scale", self.size_scale_spin.value())
        self.config_manager.set("pet_settings.animation_speed", self.animation_speed_spin.value())

        # 监控设置
        self.config_manager.set("monitor_settings.refresh_interval", self.refresh_interval_spin.value())
        self.config_manager.set("monitor_settings.auto_hide_progress", self.auto_hide_check.isChecked())
        self.config_manager.set("monitor_settings.progress_window_opacity", self.progress_opacity_spin.value())

        # 进度窗口偏移设置
        offset = {"x": self.offset_x_spin.value(), "y": self.offset_y_spin.value()}
        self.config_manager.set("monitor_settings.progress_window_offset", offset)

        # 显示设置
        self.config_manager.set("display_settings.always_on_top", self.always_on_top_check.isChecked())
        self.config_manager.set("display_settings.show_in_taskbar", self.show_in_taskbar_check.isChecked())
        self.config_manager.set("display_settings.enable_drag", self.enable_drag_check.isChecked())

        # 保存到文件
        self.config_manager.save_config()

    def test_connection(self):
        """测试连接"""
        protocol = self.protocol_combo.currentText()
        host = self.host_edit.text()
        port = self.port_spin.value()

        url = f"{protocol}://{host}:{port}"

        try:
            import requests
            response = requests.get(f"{url}/task_monitor/status", timeout=5)
            if response.status_code == 200:
                QMessageBox.information(self, "连接测试", "连接成功！")
            else:
                QMessageBox.warning(self, "连接测试", f"连接失败: HTTP {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "连接测试", f"连接失败: {str(e)}")

    def reset_settings(self):
        """重置设置"""
        reply = QMessageBox.question(self, "重置设置", "确定要重置所有设置为默认值吗？",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 重置为默认配置
            self.config_manager.config = self.config_manager.default_config.copy()
            self.load_settings()

    def accept_settings(self):
        """接受设置"""
        self.save_settings()

        # 发送设置变更信号
        self.settings_changed.emit(self.config_manager.config)

        self.accept()
