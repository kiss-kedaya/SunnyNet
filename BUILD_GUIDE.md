# SunnyNet 打包发布指南

## 问题修复说明

已修复以下构建问题:

### 1. ✅ Unicode 编码问题
- **问题**: Windows GBK 编码无法处理 Unicode 字符（✓、✗、⚠️ 等）
- **修复**: 将所有 Unicode 字符替换为 ASCII 兼容字符
  - `✓` → `[+]` 或 `OK`
  - `✗` → `[-]` 或 `FAILED`
  - `⚠️` → `[!]`
  - `🔍` → `[*]`

### 2. ✅ pyproject.toml 配置问题
- **问题**: `setuptools_scm` 依赖缺失配置
- **修复**: 移除 `setuptools_scm[toml]>=6.2` 依赖
- **问题**: License 配置已弃用
- **修复**: 将 `license = {text = "MIT"}` 改为 `license = "MIT"`
- 移除了 License classifier (已弃用)

## 使用 publish.py 脚本

### 安装依赖

```bash
pip install build twine
```

### 配置 PyPI Token

1. 访问 https://pypi.org/manage/account/token/ 创建 API Token
2. 创建 `~/.pypirc` 文件:

**Windows**: `C:\Users\你的用户名\.pypirc`

**Linux/Mac**: `~/.pypirc`

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...你的PyPI_API_Token...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw...你的TestPyPI_API_Token...
```

### 发布新版本

```bash
# 发布补丁版本 (1.4.0 -> 1.4.1)
python publish.py

# 发布次版本 (1.4.0 -> 1.5.0)
python publish.py minor

# 发布主版本 (1.4.0 -> 2.0.0)
python publish.py major

# 指定版本号
python publish.py 1.5.0

# 先测试到 TestPyPI
python publish.py --test

# 指定版本并测试
python publish.py 1.5.0 --test
```

### 发布流程

脚本会自动执行以下步骤:

1. ✅ 检查环境（build、twine）
2. ✅ 获取当前版本号
3. ✅ 计算新版本号
4. ✅ 确认发布
5. ✅ 更新 setup.py 和 pyproject.toml 中的版本号
6. ✅ 清理旧的构建文件
7. ✅ 构建包（生成 .tar.gz 和 .whl）
8. ✅ 上传到 PyPI

## 手动构建（可选）

如果不使用 publish.py 脚本，可以手动构建:

```bash
# 1. 清理旧文件
rm -rf build dist *.egg-info

# 2. 构建包
python -m build

# 3. 检查包
twine check dist/*

# 4. 上传到 TestPyPI (测试)
twine upload --repository testpypi dist/*

# 5. 上传到 PyPI (正式)
twine upload dist/*
```

## 测试安装

### 从 TestPyPI 测试

```bash
pip install -i https://test.pypi.org/simple/ SunnyNet==1.4.0
```

### 从 PyPI 安装

```bash
pip install SunnyNet==1.4.0
```

## 注意事项

1. **版本号**: 每次发布必须使用新的版本号，PyPI 不允许覆盖已发布的版本
2. **测试**: 建议先发布到 TestPyPI 测试，确认无误后再发布到正式 PyPI
3. **Token 安全**: 不要将 `.pypirc` 文件提交到 Git 仓库
4. **构建文件**: `dist/` 和 `build/` 目录已在 `.gitignore` 中忽略

## 常见问题

### Q: 构建时提示 Unicode 错误
**A**: 已修复，所有输出信息都使用 ASCII 字符

### Q: 提示 setuptools_scm 错误
**A**: 已修复，移除了该依赖

### Q: 上传失败，提示认证错误
**A**: 检查 `~/.pypirc` 文件中的 Token 是否正确

### Q: 版本号冲突
**A**: PyPI 不允许覆盖已发布的版本，必须使用新版本号

## 版本历史

- **v1.4.0** (2024-10-21)
  - 修复 Unicode 编码问题
  - 修复平台检测问题（使用 sys.maxsize）
  - 添加镜像节点延迟检测
  - 固定 Release 版本为 v1.3.3
  - 优化 pyproject.toml 配置

- **v1.3.3** (之前)
  - 基础版本

