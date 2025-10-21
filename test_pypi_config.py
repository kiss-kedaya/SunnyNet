#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 PyPI 配置是否正确
"""

from pathlib import Path
import configparser
import sys


def test_pypi_config():
    """测试 PyPI 配置"""

    print("=" * 70)
    print("PyPI 配置测试工具")
    print("=" * 70)

    pypirc_path = Path.home() / ".pypirc"

    print(f"\n[1/4] 检查配置文件是否存在...")
    print(f"路径: {pypirc_path}")

    if not pypirc_path.exists():
        print("[!] 配置文件不存在")
        print("\n请运行: python setup_pypi.py")
        return False

    print("[+] 配置文件存在")

    print(f"\n[2/4] 读取配置文件...")

    try:
        config = configparser.ConfigParser()
        config.read(pypirc_path, encoding="utf-8")
        print("[+] 配置文件格式正确")
    except Exception as e:
        print(f"[-] 配置文件格式错误: {e}")
        return False

    print(f"\n[3/4] 检查 PyPI 配置...")

    # 检查 PyPI
    has_pypi = False
    if "pypi" in config:
        print("\n[PyPI 正式环境]")
        print(f"  username: {config['pypi'].get('username', 'N/A')}")
        password = config["pypi"].get("password", "")
        if password:
            # 隐藏部分 token
            if len(password) > 20:
                masked = password[:10] + "..." + password[-10:]
            else:
                masked = password[:5] + "..."
            print(f"  password: {masked}")

            # 验证 token 格式
            if password.startswith("pypi-"):
                print("  [+] Token 格式正确")
                has_pypi = True
            else:
                print("  [!] Token 格式可能不正确（应以 'pypi-' 开头）")
        else:
            print("  [-] 缺少 password")
    else:
        print("\n[PyPI 正式环境]")
        print("  [-] 未配置")

    # 检查 TestPyPI
    has_testpypi = False
    if "testpypi" in config:
        print("\n[TestPyPI 测试环境]")
        print(f"  username: {config['testpypi'].get('username', 'N/A')}")
        print(f"  repository: {config['testpypi'].get('repository', 'N/A')}")
        password = config["testpypi"].get("password", "")
        if password:
            # 隐藏部分 token
            if len(password) > 20:
                masked = password[:10] + "..." + password[-10:]
            else:
                masked = password[:5] + "..."
            print(f"  password: {masked}")

            # 验证 token 格式
            if password.startswith("pypi-"):
                print("  [+] Token 格式正确")
                has_testpypi = True
            else:
                print("  [!] Token 格式可能不正确（应以 'pypi-' 开头）")
        else:
            print("  [-] 缺少 password")
    else:
        print("\n[TestPyPI 测试环境]")
        print("  [-] 未配置")

    print(f"\n[4/4] 配置总结...")
    print("-" * 70)

    if has_pypi:
        print("[+] PyPI 配置完整，可以发布到正式环境")
        print("    使用命令: python publish.py")
    else:
        print("[-] PyPI 未配置或配置不完整")

    if has_testpypi:
        print("[+] TestPyPI 配置完整，可以发布到测试环境")
        print("    使用命令: python publish.py --test")
    else:
        print("[-] TestPyPI 未配置或配置不完整")

    print("-" * 70)

    if not has_pypi and not has_testpypi:
        print("\n[!] 没有可用的配置")
        print("请运行: python setup_pypi.py")
        return False

    print("\n配置文件示例:")
    print("-" * 70)
    print("""[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw...""")
    print("-" * 70)

    print("\n" + "=" * 70)

    if has_pypi or has_testpypi:
        print("[+] 配置测试通过！")
        print("=" * 70)
        return True
    else:
        print("[-] 配置测试失败")
        print("=" * 70)
        return False


def main():
    """主函数"""
    try:
        success = test_pypi_config()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
