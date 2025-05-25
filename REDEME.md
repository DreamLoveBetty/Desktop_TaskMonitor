# ComfyUI Pet Monitor

ComfyUI 桌面宠物监控器 - 一个结合 ComfyUI-TaskMonitor 和 DesktopPet 的桌面宠物挂件程序，用于监控 ComfyUI 工作流进度。


### 🎨 资源文件
```
images/                       # 图标和宠物图片目录
├── eye.png                   # 设置菜单图标
├── exit.png                  # 退出菜单图标
├── net.png                   # 设置窗口图标
├── favicon.png               # 托盘图标
├── music.ico                 # 音乐图标
├── meizi/                    # 美女宠物动画帧
│   ├── meizi_0.png
│   ├── meizi_1.png
│   └── ... (62 帧动画)
├── ConeheadZombie/           # 路障僵尸宠物动画帧
│   ├── ConeheadZombie_0.png
│   └── ... (21 帧动画)
├── WallNut/                  # 坚果宠物动画帧
│   ├── WallNut_0.png
│   └── ... (16 帧动画)
├── Zombie/                   # 普通僵尸宠物动画帧
│   ├── Zombie_0.png
│   └── ... (22 帧动画)
└── Girl/                     # 女孩宠物动画帧
    ├── Girl_00001_.png
    └── ... (100 帧动画)
```

### 🚀 启动脚本
```
启动程序.bat                   # Windows 快速启动脚本
comfyui_pet_monitor.pyw        # Python 启动脚本，全局依赖完成双击后可直接运行
```

## 项目概述

ComfyUI 桌面宠物监控器是一个可爱的桌面挂件程序，它能够实时监控 ComfyUI 工作流的执行状态，并通过不同的宠物动画来直观地展示当前的工作状态。

## 🌟 主要功能

### 🐱 桌面宠物挂件
- **透明背景显示**: 宠物挂件支持透明背景，完美融入桌面
- **多种宠物选择**: 支持美女、僵尸、坚果、女孩等多种宠物形象
- **自由创作导入**: 自定义连续帧动画存入images目录即可

### 📊 实时监控功能
- **工作流状态监控**: 实时监控 ComfyUI 工作流执行状态
- **进度显示**: 显示当前节点进度和整体工作流进度
- **执行时间统计**: 精确计算并显示工作流执行时间
- **队列信息**: 显示当前运行和等待中的任务数量

### ⚙️ 高级设置
- **服务器配置**: 可配置 ComfyUI 服务器地址和端口
- **宠物设置**: 自定义宠物类型、大小、动画速度
- **显示设置**: 配置透明度、置顶、任务栏显示等
- **进度窗口设置**: 自定义进度窗口位置偏移量
- **监控设置**: 配置刷新间隔、自动隐藏等

### 🔧 安装步骤
需先拉取以下节点到comfyui的节点目录下：
1. **拉取监听节点**：
   ```bash
  git clone https://github.com/hmwl/ComfyUI-TaskMonitor.git 
  
   ```

2. **重启 ComfyUI**：
   ```bash
   # 重启 ComfyUI 服务器以加载插件
   ```

3. **验证安装**：
   - 访问 `http://localhost:8188/task_monitor/status`
   - 应该返回 JSON 格式的状态信息


#### 方法一：自动安装（推荐）
```bash
git clone 本仓库至X:\便携包路径\ComfyUI_windows_portable（或任意目录，但bat批处理指令需更改）

# 双击运行启动脚本（会自动检查并安装依赖）
start.pyw     # Python 启动脚本，全局依赖完成双击后可直接运行
```

#### 方法二：手动安装
```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 启动程序
comfyui_pet_monitor.pyw        # Python 启动脚本，全局依赖完成双击后可直接运行

#### 方法三：同comfyui一同启动
```
将start.bat放入ComfyUI_windows_portable目录下（自部署comfyui需修改bat内解释器路径）


### 📦 依赖包
```
PyQt5>=5.15.0          # GUI 框架
requests>=2.25.0       # HTTP 客户端
```


## 📄 许可证

本项目基于 MIT 许可证开源。

## 🙏 致谢
[借鉴依赖的项目]
(https://github.com/daylight2022/DesktopPet.git)
https://github.com/hmwl/ComfyUI-TaskMonitor.git




