#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyPI 认证配置助手

帮助配置 PyPI API Token
"""

from pathlib import Path
import sys


def setup_pypi_config():
    """设置 PyPI 配置"""

    print("=" * 70)
    print("PyPI 认证配置助手")
    print("=" * 70)

    pypirc_path = Path.home() / ".pypirc"

    print(f"\n配置文件位置: {pypirc_path}")

    if pypirc_path.exists():
        print("\n⚠️  配置文件已存在")
        response = input("是否覆盖现有配置? (y/N): ").strip().lower()
        if response != "y":
            print("取消配置")
            return

        # 备份现有配置
        backup_path = pypirc_path.with_suffix(".pypirc.backup")
        import shutil

        shutil.copy(pypirc_path, backup_path)
        print(f"已备份到: {backup_path}")

    print("\n" + "=" * 70)
    print("获取 API Token")
    print("=" * 70)
    print("\n1. 访问以下网址获取 API Token:")
    print("   PyPI (正式): https://pypi.org/manage/account/token/")
    print("   TestPyPI (测试): https://test.pypi.org/manage/account/token/")
    print("\n2. 创建新的 API Token:")
    print("   - Token name: 随意命名，例如 'SunnyNet Upload'")
    print("   - Scope: 选择 'Entire account' 或指定项目")
    print("   - 点击 'Add token'")
    print("\n3. 复制生成的 Token (pypi-AgE...)")
    print("   ⚠️  Token 只显示一次，请务必保存")

    input("\n按回车键继续...")

    print("\n" + "=" * 70)
    print("配置 Token")
    print("=" * 70)

    # 询问是否配置 PyPI
    print("\n配置 PyPI (正式环境):")
    pypi_token = input("请输入 PyPI Token (留空跳过): ").strip()

    # 询问是否配置 TestPyPI
    print("\n配置 TestPyPI (测试环境):")
    testpypi_token = input("请输入 TestPyPI Token (留空跳过): ").strip()

    if not pypi_token and not testpypi_token:
        print("\n未配置任何 Token，退出")
        return

    # 生成配置文件
    config_lines = [
        "[distutils]",
        "index-servers =",
    ]

    if pypi_token:
        config_lines.append("    pypi")
    if testpypi_token:
        config_lines.append("    testpypi")

    config_lines.append("")

    if pypi_token:
        config_lines.extend(
            ["[pypi]", "username = __token__", f"password = {pypi_token}", ""]
        )

    if testpypi_token:
        config_lines.extend(
            [
                "[testpypi]",
                "repository = https://test.pypi.org/legacy/",
                "username = __token__",
                f"password = {testpypi_token}",
                "",
            ]
        )

    # 写入配置文件
    try:
        with open(pypirc_path, "w", encoding="utf-8") as f:
            f.write("\n".join(config_lines))

        # 在 Unix 系统上设置文件权限为 600 (仅所有者可读写)
        if sys.platform != "win32":
            import os

            os.chmod(pypirc_path, 0o600)

        print("\n" + "=" * 70)
        print("✓ 配置完成!")
        print("=" * 70)
        print(f"\n配置文件已保存到: {pypirc_path}")

        if pypi_token:
            print("\n✓ PyPI 已配置")
        if testpypi_token:
            print("✓ TestPyPI 已配置")

        print("\n现在可以使用以下命令发布包:")
        if testpypi_token:
            print("  python publish.py --test    # 上传到 TestPyPI 测试")
        if pypi_token:
            print("  python publish.py           # 上传到 PyPI 正式环境")

        print("\n⚠️  安全提示:")
        print("  - 不要将 .pypirc 文件提交到 Git 仓库")
        print("  - 如果 Token 泄露，请立即在 PyPI 网站上撤销")
        print("\n" + "=" * 70)

    except Exception as e:
        print(f"\n✗ 配置失败: {e}")
        return


def main():
    """主函数"""
    try:
        setup_pypi_config()
    except KeyboardInterrupt:
        print("\n\n用户取消")
    except Exception as e:
        print(f"\n错误: {e}")


if __name__ == "__main__":
    main()
