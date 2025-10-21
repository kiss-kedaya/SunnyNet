#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SunnyNet 自动打包并上传到 PyPI 的脚本

使用方法:
    python publish.py           # 发布补丁版本 (1.3.3 -> 1.3.4)
    python publish.py minor     # 发布次版本 (1.3.3 -> 1.4.0)
    python publish.py major     # 发布主版本 (1.3.3 -> 2.0.0)
    python publish.py 1.5.0     # 指定版本号
    python publish.py --test    # 上传到 TestPyPI
"""

import os
import sys
import re
import shutil
import subprocess
from pathlib import Path


class Publisher:
    def __init__(self):
        self.root = Path(__file__).parent
        self.setup_py = self.root / "setup.py"
        self.pyproject_toml = self.root / "pyproject.toml"
        self.current_version = None
        self.new_version = None

    def run(self, version_arg=None, test_pypi=False):
        """执行发布流程"""
        print("=" * 70)
        print("SunnyNet PyPI 发布工具")
        print("=" * 70)

        # 1. 检查环境
        if not self.check_environment():
            return False

        # 2. 获取当前版本
        self.current_version = self.get_current_version()
        print(f"\n📌 当前版本: {self.current_version}")

        # 3. 计算新版本
        if version_arg:
            self.new_version = self.calculate_version(version_arg)
        else:
            # 默认增加补丁版本
            self.new_version = self.calculate_version("patch")

        print(f"📌 新版本: {self.new_version}")

        # 4. 确认
        if not self.confirm_publish(test_pypi):
            print("\n❌ 取消发布")
            return False

        # 5. 更新版本号
        print("\n📝 更新版本号...")
        if not self.update_version():
            return False

        # 6. 清理旧文件
        print("\n🧹 清理旧的构建文件...")
        self.clean_build()

        # 7. 构建包
        print("\n📦 构建包...")
        if not self.build_package():
            return False

        # 8. 上传到 PyPI
        print("\n🚀 上传到 PyPI...")
        if not self.upload_package(test_pypi):
            return False

        # 9. 完成
        print("\n" + "=" * 70)
        print("✅ 发布成功!")
        print("=" * 70)
        print(f"\n版本: {self.new_version}")

        if test_pypi:
            print(f"\n测试安装:")
            print(
                f"  pip install -i https://test.pypi.org/simple/ SunnyNet=={self.new_version}"
            )
        else:
            print(f"\n安装命令:")
            print(f"  pip install SunnyNet=={self.new_version}")
            print(f"\nPyPI 链接:")
            print(f"  https://pypi.org/project/SunnyNet/{self.new_version}/")

        return True

    def check_environment(self):
        """检查必要的工具是否安装"""
        print("\n🔍 检查环境...")

        required_tools = ["build", "twine"]
        missing_tools = []

        for tool in required_tools:
            try:
                __import__(tool)
                print(f"  ✓ {tool}")
            except ImportError:
                print(f"  ✗ {tool} (未安装)")
                missing_tools.append(tool)

        if missing_tools:
            print(f"\n❌ 缺少必要的工具: {', '.join(missing_tools)}")
            print(f"\n请安装: pip install {' '.join(missing_tools)}")
            return False

        return True

    def get_current_version(self):
        """从 setup.py 获取当前版本号"""
        content = self.setup_py.read_text(encoding="utf-8")
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
        raise ValueError("无法从 setup.py 中找到版本号")

    def calculate_version(self, version_arg):
        """计算新版本号"""
        if version_arg in ["patch", "minor", "major"]:
            parts = self.current_version.split(".")
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

            if version_arg == "patch":
                patch += 1
            elif version_arg == "minor":
                minor += 1
                patch = 0
            elif version_arg == "major":
                major += 1
                minor = 0
                patch = 0

            return f"{major}.{minor}.{patch}"
        else:
            # 直接使用指定的版本号
            return version_arg

    def confirm_publish(self, test_pypi):
        """确认发布"""
        pypi_name = "TestPyPI" if test_pypi else "PyPI"

        print(f"\n{'=' * 70}")
        print(f"⚠️  即将发布到 {pypi_name}:")
        print(f"  当前版本: {self.current_version}")
        print(f"  新版本: {self.new_version}")
        print(f"{'=' * 70}")

        response = input("\n是否继续? (yes/no): ").strip().lower()
        return response in ["yes", "y"]

    def update_version(self):
        """更新版本号"""
        try:
            # 更新 setup.py
            content = self.setup_py.read_text(encoding="utf-8")
            content = re.sub(
                r'(version\s*=\s*["\'])([^"\']+)(["\'])',
                rf"\g<1>{self.new_version}\g<3>",
                content,
            )
            self.setup_py.write_text(content, encoding="utf-8")
            print(f"  ✓ 更新 setup.py")

            # 更新 pyproject.toml
            content = self.pyproject_toml.read_text(encoding="utf-8")
            content = re.sub(
                r'(version\s*=\s*["\'])([^"\']+)(["\'])',
                rf"\g<1>{self.new_version}\g<3>",
                content,
            )
            self.pyproject_toml.write_text(content, encoding="utf-8")
            print(f"  ✓ 更新 pyproject.toml")

            return True
        except Exception as e:
            print(f"  ✗ 更新版本号失败: {e}")
            return False

    def clean_build(self):
        """清理构建文件"""
        dirs_to_clean = ["build", "dist", "*.egg-info"]

        for pattern in dirs_to_clean:
            if "*" in pattern:
                # 通配符匹配
                for path in self.root.glob(pattern):
                    if path.is_dir():
                        shutil.rmtree(path)
                        print(f"  ✓ 删除 {path.name}")
            else:
                path = self.root / pattern
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                        print(f"  ✓ 删除 {pattern}")
                    else:
                        path.unlink()

    def build_package(self):
        """构建包"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "build"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=True,
            )
            print(result.stdout)
            print("  ✓ 构建成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ 构建失败:")
            print(e.stderr)
            return False

    def upload_package(self, test_pypi):
        """上传包到 PyPI"""
        dist_dir = self.root / "dist"
        files = list(dist_dir.glob("*"))

        if not files:
            print("  ✗ 没有找到构建文件")
            return False

        print(f"\n将上传以下文件:")
        for f in files:
            print(f"  - {f.name}")

        # 构建 twine 命令
        cmd = [sys.executable, "-m", "twine", "upload"]

        if test_pypi:
            cmd.extend(["--repository", "testpypi"])

        cmd.extend([str(f) for f in files])

        try:
            subprocess.run(cmd, cwd=self.root, check=True)
            print("  ✓ 上传成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ 上传失败: {e}")
            return False


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="SunnyNet PyPI 发布工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python publish.py              # 发布补丁版本 (1.3.3 -> 1.3.4)
  python publish.py patch         # 发布补丁版本
  python publish.py minor         # 发布次版本 (1.3.3 -> 1.4.0)
  python publish.py major         # 发布主版本 (1.3.3 -> 2.0.0)
  python publish.py 1.5.0         # 指定版本号
  python publish.py --test        # 上传到 TestPyPI
  python publish.py 1.5.0 --test  # 指定版本并上传到 TestPyPI

注意:
  - 首次使用需要配置 PyPI API Token
  - 在 ~/.pypirc 中配置认证信息
  - TestPyPI 用于测试，不会影响正式版本
        """,
    )

    parser.add_argument(
        "version",
        nargs="?",
        default="patch",
        help="版本更新类型 (patch/minor/major) 或具体版本号 (如 1.5.0)",
    )

    parser.add_argument(
        "--test", action="store_true", help="上传到 TestPyPI 而不是正式 PyPI"
    )

    parser.add_argument(
        "--skip-confirm", action="store_true", help="跳过确认步骤（危险）"
    )

    args = parser.parse_args()

    publisher = Publisher()

    # 如果跳过确认，修改 confirm_publish 方法
    if args.skip_confirm:
        publisher.confirm_publish = lambda test_pypi: True

    success = publisher.run(args.version, args.test)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
