import requests
import json
import time
from typing import Dict, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from enum import Enum

class TaskStatus(Enum):
    """任务状态枚举"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    QUEUED = "queued"

class TaskMonitorAPI(QObject):
    """ComfyUI 任务监控 API 客户端"""

    # 信号定义
    status_changed = pyqtSignal(str)  # 状态变化信号
    progress_updated = pyqtSignal(dict)  # 进度更新信号
    error_occurred = pyqtSignal(str)  # 错误信号
    connection_changed = pyqtSignal(bool)  # 连接状态变化信号

    def __init__(self, base_url: str, refresh_interval: int = 1000):
        super().__init__()
        self.base_url = base_url.rstrip('/')
        self.refresh_interval = refresh_interval
        self.is_connected = False
        self.last_status = TaskStatus.IDLE
        self.last_task_data = {}

        # 执行时间跟踪
        self.execution_start_time = None
        self.current_execution_time = 0
        self.last_task_id = None

        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_status)

    def start_monitoring(self):
        """开始监控"""
        self.timer.start(self.refresh_interval)

    def stop_monitoring(self):
        """停止监控"""
        self.timer.stop()

    def set_refresh_interval(self, interval: int):
        """设置刷新间隔"""
        self.refresh_interval = interval
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(interval)

    def set_base_url(self, url: str):
        """设置服务器 URL"""
        self.base_url = url.rstrip('/')

    def fetch_status(self):
        """获取任务状态"""
        try:
            url = f"{self.base_url}/task_monitor/status"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                self._handle_status_response(data)

                # 更新连接状态
                if not self.is_connected:
                    self.is_connected = True
                    self.connection_changed.emit(True)

            else:
                self._handle_connection_error(f"HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            self._handle_connection_error(str(e))
        except json.JSONDecodeError as e:
            self._handle_connection_error(f"JSON 解析错误: {e}")
        except Exception as e:
            self._handle_connection_error(f"未知错误: {e}")

    def _handle_status_response(self, data: Dict[str, Any]):
        """处理状态响应"""
        try:
            status_str = data.get("status", "idle")
            current_status = TaskStatus(status_str)
            current_task_id = data.get("task_id")

            # 检查任务是否变化
            if current_task_id != self.last_task_id:
                self.last_task_id = current_task_id
                if current_status == TaskStatus.RUNNING:
                    # 新任务开始
                    self.execution_start_time = time.time()
                    self.current_execution_time = 0
                else:
                    # 任务结束或空闲
                    self.execution_start_time = None
                    self.current_execution_time = 0

            # 计算当前执行时间
            if self.execution_start_time and current_status == TaskStatus.RUNNING:
                self.current_execution_time = time.time() - self.execution_start_time
            elif current_status in [TaskStatus.COMPLETED, TaskStatus.ERROR]:
                # 任务完成，保持最后的执行时间
                if self.execution_start_time:
                    self.current_execution_time = time.time() - self.execution_start_time
                    self.execution_start_time = None
            elif current_status == TaskStatus.IDLE:
                # 空闲状态，重置时间
                self.execution_start_time = None
                self.current_execution_time = 0

            # 检查状态是否变化
            if current_status != self.last_status:
                self.last_status = current_status
                self.status_changed.emit(status_str)

            # 更新数据，添加我们计算的执行时间
            updated_data = data.copy()
            updated_data["execution_time"] = self.current_execution_time

            # 发送进度更新信号
            self.last_task_data = updated_data
            self.progress_updated.emit(updated_data)

        except ValueError:
            # 未知状态值
            self.error_occurred.emit(f"未知状态: {data.get('status')}")

    def _handle_connection_error(self, error_msg: str):
        """处理连接错误"""
        if self.is_connected:
            self.is_connected = False
            self.connection_changed.emit(False)
            self.error_occurred.emit(f"连接错误: {error_msg}")

    def get_last_status(self) -> TaskStatus:
        """获取最后的状态"""
        return self.last_status

    def get_last_task_data(self) -> Dict[str, Any]:
        """获取最后的任务数据"""
        return self.last_task_data.copy()

    def is_task_running(self) -> bool:
        """检查是否有任务正在运行"""
        return self.last_status in [TaskStatus.RUNNING, TaskStatus.QUEUED]

    def get_progress_info(self) -> Dict[str, Any]:
        """获取进度信息"""
        if not self.last_task_data:
            return {}

        progress_info = {
            "status": self.last_status.value,
            "task_id": self.last_task_data.get("task_id"),
            "execution_time": self.last_task_data.get("execution_time", 0),
            "workflow_progress": self.last_task_data.get("workflow_progress", {}),
            "current_task_progress": self.last_task_data.get("current_task_progress"),
            "queue": self.last_task_data.get("queue", {}),
            "error_info": self.last_task_data.get("error_info")
        }

        return progress_info

    def get_workflow_progress_percentage(self) -> float:
        """获取工作流进度百分比"""
        workflow_progress = self.last_task_data.get("workflow_progress", {})
        total_nodes = workflow_progress.get("total_nodes", 0)
        executed_nodes = workflow_progress.get("executed_nodes", 0)

        if total_nodes > 0:
            return (executed_nodes / total_nodes) * 100
        return 0.0

    def get_current_node_progress_percentage(self) -> float:
        """获取当前节点进度百分比"""
        current_progress = self.last_task_data.get("current_task_progress")
        if current_progress:
            step = current_progress.get("step", 0)
            total_steps = current_progress.get("total_steps", 0)
            if total_steps > 0:
                return (step / total_steps) * 100
        return 0.0
