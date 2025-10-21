# SunnyNet 构建与跨平台说明

## 📦 关于构建 Warning

在构建 SunnyNet 包时，你会看到以下 warning 信息：

```
warning: no files found matching '*.dll'
warning: no files found matching '*.so'
warning: no files found matching '*.dylib'
```

**这些 warning 是正常的，不影响包的功能！**

### 为什么会出现这些 warning？

SunnyNet 采用了**动态下载**的设计，库文件（.dll/.so）不包含在 Python 包中，而是在用户安装后根据平台自动下载。

### 设计优势

1. **包体积小** - PyPI 上的包只有 15MB 左右，不包含大体积的二进制文件
2. **跨平台支持** - 同一个 Python 包可以在 Windows、Linux 上使用
3. **按需下载** - 用户只下载自己平台需要的库文件
4. **易于更新** - 库文件可以独立更新，无需重新发布 Python 包

---

## 🌍 跨平台支持

### SunnyNet 支持以下平台：

| 操作系统 | 架构 | 库文件 | 状态 |
|---------|------|--------|------|
| Windows | 64-bit | `SunnyNet64.dll` | ✅ 支持 |
| Windows | 32-bit | `SunnyNet.dll` | ✅ 支持 |
| Linux   | 64-bit (ARM) | `libSunnyNet-arm64.so` | ✅ 支持 |
| Linux   | 32-bit (x86) | `libSunnyNet-x86.so` | ✅ 支持 |
| macOS   | 64-bit | `SunnyNet64.dylib` | 🚧 计划中 |

### 如何使用

#### 1. 安装 Python 包（适用所有平台）

```bash
pip install SunnyNet
```

#### 2. 下载平台库文件

安装完成后，运行以下命令自动下载当前平台的库文件：

```bash
sunnynet install
```

该命令会：
- 自动检测你的操作系统和架构
- 测试多个镜像节点速度
- 选择最快的节点下载对应的库文件
- 下载并安装到正确位置

#### 3. 开始使用

```python
from SunnyNet import SunnyNet, HTTPEvent

def http_callback(event: HTTPEvent):
    if event.is_request():
        print(f"请求: {event.method()} {event.url()}")

sunny = SunnyNet()
sunny.set_callback(http_callback=http_callback)
sunny.set_port(8899)
sunny.start()
```

---

## 🔧 构建和发布

### 环境要求

```bash
pip install build twine
```

### 配置 PyPI 认证

```bash
python setup_pypi.py
```

按提示输入 PyPI API Token。

### 发布新版本

```bash
# 发布补丁版本 (1.5.3 -> 1.5.4)
python publish.py

# 发布次版本 (1.5.3 -> 1.6.0)
python publish.py minor

# 发布主版本 (1.5.3 -> 2.0.0)
python publish.py major

# 指定版本号
python publish.py 1.6.0

# 先测试到 TestPyPI
python publish.py --test
```

### 构建流程

1. **版本检查** - 自动更新 `setup.py` 和 `pyproject.toml` 中的版本号
2. **清理旧文件** - 删除 `build/`、`dist/`、`*.egg-info` 目录
3. **构建源码包** - 生成 `.tar.gz` 文件（约 14MB）
4. **构建二进制包** - 生成 `.whl` 文件（约 14MB）
5. **上传到 PyPI** - 使用 twine 上传

---

## 📝 关于 Warning 的详细说明

### setup.py 中的 package_data 配置

```python
package_data={
    "SunnyNet": ["*.dll", "*.so", "*.dylib"],
    "": ["*.dll", "*.so", "*.dylib"],
}
```

这些配置是为了：
1. 如果用户手动将库文件放入包目录，能够被正确包含
2. 为未来可能的预打包版本预留配置

### MANIFEST.in 配置

```
include *.dll
include *.so
include *.dylib
recursive-include SunnyNet *.dll *.so *.dylib
```

同样的原因，这些配置为可选的预打包模式预留。

### 实际工作流程

```
用户安装流程:
1. pip install SunnyNet  -> 下载 15MB Python 包
2. sunnynet install      -> 根据平台下载 5-15MB 库文件
3. import SunnyNet       -> 加载对应平台的库文件
```

这比将所有平台的库文件（总共 50+MB）都打包进 Python 包要高效得多！

---

## ❓ 常见问题

### Q: 为什么不把库文件一起打包？

**A**: 
1. 如果包含所有平台的库文件，包体积会超过 50MB
2. PyPI 对单个文件大小有限制
3. 用户只需要自己平台的库文件，下载其他平台的浪费带宽
4. 动态下载可以使用镜像加速，提高国内用户体验

### Q: 如果 sunnynet install 失败怎么办？

**A**: 可以手动下载：

1. 访问 Release 页面：https://github.com/kiss-kedaya/SunnyNet/releases/tag/v1.3.3
2. 下载对应平台的库文件
3. 放置到以下位置：
   - Windows: `%APPDATA%\SunnyNet\lib\`
   - Linux/Mac: `~/.sunnynet/lib/`

### Q: 构建时出现 Unicode 编码错误？

**A**: 最新版 `publish.py` 已修复此问题，所有输出都使用 ASCII 兼容字符。

### Q: 如何验证包的跨平台性？

**A**: 
```bash
# 构建包
python publish.py --test

# 在 Windows 上测试
pip install -i https://test.pypi.org/simple/ SunnyNet
sunnynet install

# 在 Linux 上测试（同样的命令）
pip install -i https://test.pypi.org/simple/ SunnyNet
sunnynet install
```

---

## 📊 包大小对比

| 方式 | PyPI 包大小 | 下载大小（Windows 64位） | 总计 |
|-----|------------|----------------------|------|
| **动态下载（当前）** | 15 MB | 5 MB | **20 MB** |
| 预打包所有平台 | 55+ MB | 0 MB | 55+ MB |

用户节省了 **35+ MB** 的下载量！🎉

---

## 🔗 相关资源

- **GitHub 仓库**: https://github.com/kiss-kedaya/SunnyNet
- **PyPI 页面**: https://pypi.org/project/SunnyNet/
- **官方网站**: https://esunny.vip
- **QQ 群**: 751406884, 545120699, 170902713, 616787804

---

## 更新日志

### v1.5.3 (2024-10-21)
- ✅ 修复构建时的 Unicode 编码问题
- ✅ 优化构建进度显示
- ✅ 改进错误提示信息
- ✅ 添加 PyPI 认证配置助手

### v1.4.0 (2024-10-21)
- ✅ 修复平台检测问题（使用 `sys.maxsize`）
- ✅ 添加镜像节点延迟检测
- ✅ 优化下载体验
- ✅ 固定 Release 版本为 v1.3.3


