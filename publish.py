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
        print(f"\n[*] 当前版本: {self.current_version}")

        # 3. 计算新版本
        if version_arg:
            self.new_version = self.calculate_version(version_arg)
        else:
            # 默认增加补丁版本
            self.new_version = self.calculate_version("patch")

        print(f"[*] 新版本: {self.new_version}")

        # 4. 确认
        if not self.confirm_publish(test_pypi):
            print("\n[-] 取消发布")
            return False

        # 5. 更新版本号
        print("\n[*] 更新版本号...")
        if not self.update_version():
            return False

        # 6. 清理旧文件
        print("\n[*] 清理旧的构建文件...")
        self.clean_build()

        # 7. 构建包
        print("\n[*] 构建包...")
        if not self.build_package():
            return False

        # 8. 上传到 PyPI
        print("\n[*] 上传到 PyPI...")
        if not self.upload_package(test_pypi):
            return False

        # 9. 完成
        print("\n" + "=" * 70)
        print("[+] 发布成功!")
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
        print("\n[*] 检查环境...")

        required_tools = ["build", "twine"]
        missing_tools = []

        for tool in required_tools:
            try:
                __import__(tool)
                print(f"  [+] {tool}")
            except ImportError:
                print(f"  [-] {tool} (未安装)")
                missing_tools.append(tool)

        if missing_tools:
            print(f"\n[-] 缺少必要的工具: {', '.join(missing_tools)}")
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
        print(f"[!] 即将发布到 {pypi_name}:")
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
            print(f"  [+] 更新 setup.py")

            # 更新 pyproject.toml
            content = self.pyproject_toml.read_text(encoding="utf-8")
            content = re.sub(
                r'(version\s*=\s*["\'])([^"\']+)(["\'])',
                rf"\g<1>{self.new_version}\g<3>",
                content,
            )
            self.pyproject_toml.write_text(content, encoding="utf-8")
            print(f"  [+] 更新 pyproject.toml")

            return True
        except Exception as e:
            print(f"  [-] 更新版本号失败: {e}")
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
                        print(f"  [+] 删除 {path.name}")
            else:
                path = self.root / pattern
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                        print(f"  [+] 删除 {pattern}")
                    else:
                        path.unlink()

    def build_package(self):
        """构建包"""
        import time

        print("\n[1/2] 构建源码包 (sdist)...")
        print("-" * 60)

        try:
            # 显示构建进度
            start_time = time.time()

            # 设置环境变量以避免编码问题
            import os

            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"

            # 执行构建，实时显示输出
            process = subprocess.Popen(
                [sys.executable, "-m", "build"],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8",
                errors="replace",
                env=env,
            )

            # 实时输出构建信息
            build_output = []
            for line in process.stdout:
                try:
                    line = line.rstrip()
                    if line:
                        # 过滤掉一些冗余的警告信息
                        if (
                            "SetuptoolsDeprecationWarning" not in line
                            and "!!" not in line
                            and "****" not in line
                            and "Please use" not in line
                            and "See https://" not in line
                        ):
                            # 显示关键步骤
                            if "Building sdist" in line:
                                print("  [*] 正在构建源码包...")
                            elif "Building wheel" in line:
                                print("\n[2/2] 构建二进制包 (wheel)...")
                                print("-" * 60)
                                print("  [*] 正在构建 wheel 包...")
                            elif "Successfully built" in line:
                                # 避免直接输出可能包含 Unicode 的行
                                print(f"  [+] Successfully built packages")
                            # 不再基于输出内容判断错误，而是使用returncode

                        build_output.append(line)
                except UnicodeEncodeError:
                    # 忽略无法编码的字符
                    pass

            process.wait()

            if process.returncode != 0:
                print("\n构建详细信息:")
                print("\n".join(build_output))
                raise subprocess.CalledProcessError(process.returncode, process.args)

            elapsed = time.time() - start_time

            # 检查生成的文件
            dist_dir = self.root / "dist"
            if dist_dir.exists():
                files = list(dist_dir.glob("*"))
                print("\n" + "-" * 60)
                print("[+] 构建成功！")
                print(f"  耗时: {elapsed:.2f} 秒")
                print(f"\n生成的文件:")
                for f in files:
                    size = f.stat().st_size / 1024 / 1024
                    print(f"  - {f.name} ({size:.2f} MB)")

            return True

        except subprocess.CalledProcessError as e:
            print(f"\n[-] 构建失败")
            return False
        except Exception as e:
            print(f"\n[-] 构建过程出错: {e}")
            return False

    def check_pypi_credentials(self, test_pypi):
        """检查 PyPI 认证配置"""
        import os
        import configparser

        pypirc_path = Path.home() / ".pypirc"

        if not pypirc_path.exists():
            print("\n" + "=" * 70)
            print("[!] 未找到 PyPI 认证配置文件")
            print("=" * 70)
            print(f"\n配置文件路径: {pypirc_path}")
            print("\n请运行配置助手:")
            print("  python setup_pypi.py")
            print("\n或手动创建配置文件")
            print("\n" + "=" * 70)

            response = input("\n是否已配置完成？(y/N): ").strip().lower()
            if response != "y":
                print("\n取消上传")
                return False

        # 验证配置文件格式
        try:
            config = configparser.ConfigParser()
            config.read(pypirc_path)

            target_section = "testpypi" if test_pypi else "pypi"

            if target_section not in config:
                print(f"\n[!] 配置文件中缺少 [{target_section}] 部分")
                print(f"请运行: python setup_pypi.py")
                return False

            if "password" not in config[target_section]:
                print(f"\n[!] [{target_section}] 部分缺少 password 配置")
                print(f"请运行: python setup_pypi.py")
                return False

            password = config[target_section]["password"]
            if not password or "你的" in password or "Token" in password:
                print(f"\n[!] [{target_section}] 的 password 看起来不正确")
                print(f"请确保使用真实的 API Token")
                print(f"运行配置助手: python setup_pypi.py")
                return False

            print(f"\n[+] PyPI 配置验证通过")

        except Exception as e:
            print(f"\n[!] 读取配置文件时出错: {e}")
            print(f"请运行: python setup_pypi.py")
            return False

        return True

    def upload_package(self, test_pypi):
        """上传包到 PyPI"""
        import time

        # 检查认证配置
        if not self.check_pypi_credentials(test_pypi):
            return False

        dist_dir = self.root / "dist"
        files = list(dist_dir.glob("*"))

        if not files:
            print("  [-] 没有找到构建文件")
            return False

        pypi_name = "TestPyPI" if test_pypi else "PyPI"

        print(f"\n准备上传到 {pypi_name}...")
        print("-" * 60)
        for i, f in enumerate(files, 1):
            size = f.stat().st_size / 1024 / 1024
            print(f"  [{i}/{len(files)}] {f.name} ({size:.2f} MB)")

        # 构建 twine 命令
        cmd = [sys.executable, "-m", "twine", "upload"]

        if test_pypi:
            cmd.extend(["--repository", "testpypi"])

        cmd.extend([str(f) for f in files])

        try:
            print(f"\n正在上传到 {pypi_name}...")
            start_time = time.time()

            # 设置环境变量以避免编码问题
            import os

            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"

            # 执行上传，实时显示输出
            process = subprocess.Popen(
                cmd,
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8",
                errors="replace",
                env=env,
            )

            # 实时输出上传信息
            upload_output = []
            for line in process.stdout:
                try:
                    line = line.rstrip()
                    if line:
                        upload_output.append(line)
                        # 显示上传进度
                        if "Uploading" in line:
                            # 提取文件名
                            if ".tar.gz" in line or ".whl" in line:
                                print(f"  [*] {line}")
                        elif "100%" in line:
                            print(f"  [+] {line}")
                        elif "View at:" in line:
                            print(f"  [Link] {line}")
                        elif "ERROR" in line or "error" in line.lower():
                            print(f"  [!] {line}")
                        elif "WARNING" in line:
                            print(f"  [!] {line}")
                except UnicodeEncodeError:
                    # 忽略无法编码的字符
                    pass

            process.wait()

            if process.returncode != 0:
                # 显示详细的错误信息
                print("\n详细错误信息:")
                print("-" * 60)
                for line in upload_output[-20:]:  # 显示最后20行
                    print(line)
                print("\n" + "=" * 70)
                print("[-] 上传失败")
                print("=" * 70)
                print("\n可能的原因:")
                print("  1. API Token 未配置或配置错误")
                print("  2. API Token 权限不足")
                print("  3. 版本号已存在（PyPI 不允许覆盖）")
                print("  4. 网络连接问题")

                print(f"\n配置文件位置: {Path.home() / '.pypirc'}")
                print("\n解决方法:")
                print("  • 检查 API Token 是否正确配置")
                print("  • 访问 https://pypi.org/manage/account/token/ 重新生成 Token")
                print("  • 确保版本号是新的（当前版本: {})".format(self.new_version))
                print("  • 使用 --test 参数先上传到 TestPyPI 测试")
                print("\n" + "=" * 70)
                return False

            elapsed = time.time() - start_time
            print(f"\n[+] 上传成功！耗时: {elapsed:.2f} 秒")
            return True

        except subprocess.CalledProcessError as e:
            print(f"\n[-] 上传失败: {e}")
            print("\n请检查网络连接和 PyPI 认证配置")
            return False
        except Exception as e:
            print(f"\n[-] 上传过程出错: {e}")
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
