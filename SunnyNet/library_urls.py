#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SunnyNet 库文件下载地址配置
请在这里配置各平台库文件的下载地址
"""

# 库文件下载地址
# 格式: "平台_架构": "下载地址"
LIBRARY_URLS = {
    # Windows 平台
    "windows_64": "https://example.com/downloads/SunnyNet64.dll",
    "windows_32": "https://example.com/downloads/SunnyNet.dll",
    # Linux 平台
    "linux_64": "https://example.com/downloads/SunnyNet64.so",
    "linux_32": "https://example.com/downloads/SunnyNet.so",
    # macOS 平台
    "darwin_64": "https://example.com/downloads/SunnyNet64.dylib",
    "darwin_32": "https://example.com/downloads/SunnyNet.dylib",
}


def get_library_url(system, arch):
    """
    获取指定平台的库文件下载地址

    Args:
        system: 操作系统名称 (windows/linux/darwin)
        arch: 架构 (32/64)

    Returns:
        str: 下载地址，如果未配置则返回 None
    """
    platform_key = f"{system.lower()}_{arch}"
    return LIBRARY_URLS.get(platform_key)


def set_library_url(system, arch, url):
    """
    设置指定平台的库文件下载地址

    Args:
        system: 操作系统名称 (windows/linux/darwin)
        arch: 架构 (32/64)
        url: 下载地址
    """
    platform_key = f"{system.lower()}_{arch}"
    LIBRARY_URLS[platform_key] = url
