import json
import os
from typing import Dict, Any

class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = {
            "comfyui_server": {
                "host": "127.0.0.1",
                "port": 8188,
                "protocol": "http"
            },
            "pet_settings": {
                "selected_pet": "meizi",
                "animation_speed": 250,  # 毫秒
                "size_scale": 1.0,
                "position": {"x": 1400, "y": 800}
            },
            "monitor_settings": {
                "refresh_interval": 1000,  # 毫秒
                "auto_hide_progress": True,
                "progress_window_opacity": 0.8,
                "progress_window_offset": {"x": 0, "y": 50}  # 相对于宠物中心点的偏移
            },
            "display_settings": {
                "always_on_top": True,
                "show_in_taskbar": False,
                "enable_drag": True
            }
        }
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置，确保所有必要的键都存在
                return self._merge_config(self.default_config, config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"配置文件加载失败: {e}")
                return self.default_config.copy()
        else:
            return self.default_config.copy()

    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"配置文件保存失败: {e}")
            return False

    def get(self, key_path: str, default=None):
        """获取配置值，支持点分隔的路径"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, key_path: str, value):
        """设置配置值，支持点分隔的路径"""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value

    def get_comfyui_url(self) -> str:
        """获取 ComfyUI 服务器 URL"""
        protocol = self.get("comfyui_server.protocol", "http")
        host = self.get("comfyui_server.host", "127.0.0.1")
        port = self.get("comfyui_server.port", 8188)
        return f"{protocol}://{host}:{port}"

    def get_available_pets(self) -> list:
        """获取可用的宠物列表"""
        pets = []
        images_dir = "images"
        if os.path.exists(images_dir):
            for item in os.listdir(images_dir):
                item_path = os.path.join(images_dir, item)
                if os.path.isdir(item_path):
                    # 检查是否包含序列图片
                    files = os.listdir(item_path)
                    if any(f.endswith('.png') for f in files):
                        pets.append(item)
        return pets

    def _merge_config(self, default: dict, user: dict) -> dict:
        """递归合并配置，用户配置覆盖默认配置"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
