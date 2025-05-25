#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComfyUI 桌面宠物监控器
结合 ComfyUI-TaskMonitor 和 DesktopPet 的桌面宠物挂件程序
"""

import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
if script_directory not in sys.path:
    sys.path.insert(1, script_directory) 
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from config import ConfigManager
from task_monitor_api import TaskMonitorAPI, TaskStatus
from pet_widget import PetWidget
from progress_window import ProgressWindow
from settings_dialog import SettingsDialog

class ComfyUIPetMonitor(QApplication):
    """ComfyUI 宠物监控主应用"""

    def __init__(self, argv):
        super().__init__(argv)

        # 设置应用属性
        self.setApplicationName("ComfyUI Pet Monitor")
        self.setApplicationVersion("1.0.0")
        self.setQuitOnLastWindowClosed(False)  # 关闭窗口时不退出应用

        # 初始化组件
        self.config_manager = ConfigManager()
        self.task_monitor = None
        self.pet_widget = None
        self.progress_window = None
        self.settings_dialog = None
        self.tray_icon = None

        # 状态变量
        self.is_progress_window_visible = False

        self.init_components()
        self.setup_tray_icon()
        self.apply_settings()

    def init_components(self):
        """初始化组件"""
        # 初始化任务监控API
        server_url = self.config_manager.get_comfyui_url()
        refresh_interval = self.config_manager.get("monitor_settings.refresh_interval", 1000)

        self.task_monitor = TaskMonitorAPI(server_url, refresh_interval)
        self.task_monitor.status_changed.connect(self.on_status_changed)
        self.task_monitor.progress_updated.connect(self.on_progress_updated)
        self.task_monitor.error_occurred.connect(self.on_error_occurred)
        self.task_monitor.connection_changed.connect(self.on_connection_changed)

        # 初始化宠物挂件
        selected_pet = self.config_manager.get("pet_settings.selected_pet", "meizi")
        self.pet_widget = PetWidget(selected_pet)
        self.pet_widget.double_clicked.connect(self.toggle_progress_window)
        self.pet_widget.settings_requested.connect(self.show_settings)
        self.pet_widget.quit_requested.connect(self.quit_application)
        self.pet_widget.position_changed.connect(self.on_pet_position_changed)  # 连接位置变化信号

        # 初始化进度窗口
        self.progress_window = ProgressWindow()
        self.progress_window.close_requested.connect(self.hide_progress_window)

        # 设置进度窗口透明度
        opacity = self.config_manager.get("monitor_settings.progress_window_opacity", 0.8)
        self.progress_window.set_opacity(opacity)

        # 设置进度窗口偏移量
        offset = self.config_manager.get("monitor_settings.progress_window_offset", {"x": 0, "y": 50})
        self.progress_window.set_offset(offset["x"], offset["y"])

    def setup_tray_icon(self):
        """设置系统托盘图标"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "系统托盘", "系统不支持托盘功能")
            return

        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon(self)

        # 设置图标
        icon_path = "images/favicon.png"
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # 使用默认图标
            self.tray_icon.setIcon(self.style().standardIcon(self.style().SP_ComputerIcon))

        # 创建托盘菜单
        tray_menu = QMenu()

        # 显示/隐藏宠物
        self.show_pet_action = QAction("显示宠物", self)
        self.show_pet_action.triggered.connect(self.toggle_pet_visibility)
        tray_menu.addAction(self.show_pet_action)

        # 显示进度窗口
        show_progress_action = QAction("显示进度", self)
        show_progress_action.triggered.connect(self.show_progress_window)
        tray_menu.addAction(show_progress_action)

        tray_menu.addSeparator()

        # 设置
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)

        # 关于
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        tray_menu.addAction(about_action)

        tray_menu.addSeparator()

        # 退出
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # 托盘图标点击事件
        self.tray_icon.activated.connect(self.on_tray_activated)

    def apply_settings(self):
        """应用设置"""
        # 应用宠物设置
        selected_pet = self.config_manager.get("pet_settings.selected_pet", "meizi")
        animation_speed = self.config_manager.get("pet_settings.animation_speed", 250)
        size_scale = self.config_manager.get("pet_settings.size_scale", 1.0)
        position = self.config_manager.get("pet_settings.position", {"x": 1400, "y": 800})

        self.pet_widget.set_pet(selected_pet)
        self.pet_widget.set_animation_speed(animation_speed)
        self.pet_widget.set_size_scale(size_scale)
        self.pet_widget.set_position(position["x"], position["y"])

        # 应用显示设置
        always_on_top = self.config_manager.get("display_settings.always_on_top", True)
        if always_on_top:
            self.pet_widget.setWindowFlags(
                self.pet_widget.windowFlags() | Qt.WindowStaysOnTopHint
            )
        else:
            self.pet_widget.setWindowFlags(
                self.pet_widget.windowFlags() & ~Qt.WindowStaysOnTopHint
            )

        # 应用监控设置
        refresh_interval = self.config_manager.get("monitor_settings.refresh_interval", 1000)
        self.task_monitor.set_refresh_interval(refresh_interval)

        server_url = self.config_manager.get_comfyui_url()
        self.task_monitor.set_base_url(server_url)

        # 应用进度窗口设置
        opacity = self.config_manager.get("monitor_settings.progress_window_opacity", 0.8)
        self.progress_window.set_opacity(opacity)

        offset = self.config_manager.get("monitor_settings.progress_window_offset", {"x": 0, "y": 50})
        self.progress_window.set_offset(offset["x"], offset["y"])

        # 显示宠物
        self.pet_widget.show()

        # 开始监控
        self.task_monitor.start_monitoring()

    def on_status_changed(self, status: str):
        """状态变化处理"""
        try:
            task_status = TaskStatus(status)
            self.pet_widget.set_task_status(task_status)

            # 更新托盘图标提示
            status_text = {
                "idle": "空闲",
                "running": "运行中",
                "completed": "已完成",
                "error": "错误",
                "queued": "排队中"
            }.get(status, status)

            self.tray_icon.setToolTip(f"ComfyUI Pet Monitor - {status_text}")

        except ValueError:
            print(f"未知状态: {status}")

    def on_progress_updated(self, progress_data):
        """进度更新处理"""
        if self.is_progress_window_visible:
            self.progress_window.update_progress(progress_data)

    def on_error_occurred(self, error_msg: str):
        """错误处理"""
        print(f"错误: {error_msg}")
        # 可以在这里添加错误通知

    def on_connection_changed(self, is_connected: bool):
        """连接状态变化处理"""
        if is_connected:
            print("已连接到 ComfyUI 服务器")
        else:
            print("与 ComfyUI 服务器连接断开")

    def on_pet_position_changed(self, x: int, y: int):
        """宠物位置变化处理"""
        # 如果进度窗口可见，更新其位置以跟随宠物
        if self.is_progress_window_visible:
            center_pos = self.pet_widget.get_center_position()
            self.progress_window.update_position_from_pet_center(center_pos["x"], center_pos["y"])

    def toggle_progress_window(self):
        """切换进度窗口显示"""
        if self.is_progress_window_visible:
            self.hide_progress_window()
        else:
            self.show_progress_window()

    def show_progress_window(self):
        """显示进度窗口"""
        if not self.is_progress_window_visible:
            center_pos = self.pet_widget.get_center_position()
            self.progress_window.show_at_center_position(center_pos["x"], center_pos["y"])
            self.is_progress_window_visible = True

            # 立即更新进度信息
            progress_data = self.task_monitor.get_progress_info()
            self.progress_window.update_progress(progress_data)

    def hide_progress_window(self):
        """隐藏进度窗口"""
        if self.is_progress_window_visible:
            self.progress_window.hide()
            self.is_progress_window_visible = False

    def toggle_pet_visibility(self):
        """切换宠物显示"""
        if self.pet_widget.isVisible():
            self.pet_widget.hide()
            self.show_pet_action.setText("显示宠物")
        else:
            self.pet_widget.show()
            self.show_pet_action.setText("隐藏宠物")

    def show_settings(self):
        """显示设置对话框"""
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog(self.config_manager)
            self.settings_dialog.settings_changed.connect(self.on_settings_changed)

        self.settings_dialog.exec_()

    def on_settings_changed(self, _):
        """设置变更处理"""
        # 重新应用设置
        self.apply_settings()

        # 保存宠物位置
        pet_pos = self.pet_widget.get_position()
        self.config_manager.set("pet_settings.position", pet_pos)
        self.config_manager.save_config()

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            None,
            "关于 ComfyUI Pet Monitor",
            "ComfyUI 桌面宠物监控器 v1.0.0\n\n"
            "一个结合 ComfyUI-TaskMonitor 和 DesktopPet 的\n"
            "桌面宠物挂件程序，用于监控 ComfyUI 工作流进度。\n\n"
            "功能特点：\n"
            "• 桌面透明背景宠物挂件\n"
            "• 实时监控 ComfyUI 工作流进度\n"
            "• 双击显示详细进度信息\n"
            "• 支持多种宠物形象\n"
            "• 可自定义设置"
        )

    def on_tray_activated(self, reason):
        """托盘图标激活处理"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_pet_visibility()

    def quit_application(self):
        """退出应用"""
        # 保存宠物位置
        if self.pet_widget:
            pet_pos = self.pet_widget.get_position()
            self.config_manager.set("pet_settings.position", pet_pos)
            self.config_manager.save_config()

        # 停止监控
        if self.task_monitor:
            self.task_monitor.stop_monitoring()

        # 退出应用
        self.quit()

def main():
    """主函数"""
    # 创建应用
    app = ComfyUIPetMonitor(sys.argv)

    # 检查是否支持系统托盘
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "系统托盘", "系统不支持托盘功能，程序无法运行")
        sys.exit(1)

    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
