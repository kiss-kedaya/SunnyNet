import json
import time

from SunnyNet import WebsocketTools, tools
from SunnyNet.CertManager import CertManager
from SunnyNet.Event import HTTPEvent, TCPEvent, UDPEvent, WebSocketEvent
from SunnyNet.HTTPClient import SunnyHTTPClient
from SunnyNet.Queue import Queue
from SunnyNet.SunnyNet import Version
from SunnyNet.SunnyNet import SunnyNet as Sunny

print("SunnyNet DLL版本：" + Version())

#
#  2025-04-13 (by:秦天)
#
# Sunny模块中 并没有完全封装，例如Sunny存取键值表,Redis。TCP客户端，wss客户端，因为这些功能在Python 中能够轻易实现
# Sunny模块中 并没有完全封装，例如Sunny存取键值表,Redis。TCP客户端，wss客户端，因为这些功能在Python 中能够轻易实现
# Sunny模块中 并没有完全封装，例如Sunny存取键值表,Redis。TCP客户端，wss客户端，因为这些功能在Python 中能够轻易实现
# Sunny模块中 并没有完全封装，例如Sunny存取键值表,Redis。TCP客户端，wss客户端，因为这些功能在Python 中能够轻易实现
""" 如果需要上述没有封装的功能 自己参考写法,自己封装呗 """
""" 以下是使用基本示例，我并没有将所有功能都测试一遍，如果某个功能有问题，QQ群(751406884)联系我 """


def __ScriptLogCallback__(LogInfo: str):
    print("脚本代码日志输出", LogInfo)


def __ScriptCodeCallback__(ScriptCode: str):
    print(ScriptCode, "在脚本代码处按下了保存代码按钮")


def __httpCallback__(Conn: HTTPEvent):
    if Conn.get_event_type() == Conn.EVENT_TYPE_REQUEST:
        Conn.get_request().remove_compression_mark()
        print(
            "请求客户端IP："
            + Conn.get_client_ip()
            + "|"
            + Conn.get_request().get_header("Meddyid")
        )
        return
    elif Conn.get_event_type() == Conn.EVENT_TYPE_RESPONSE:
        ss = (
            "请求完成："
            + Conn.get_url()
            + " 响应长度:"
            + str(Conn.get_response().body_length())
        )
        try:
            ss += " 响应内容：" + Conn.get_response().body_auto_str()
        except:
            ss += " -->> {响应内容:转字符串失败}请确认这是一个正常的字符串,你可以获取 使用 BodyAuto 函数 手动查看字节码,是否加密了？或者这是一张图片？"
        print(ss)
        return
    elif Conn.get_event_type() == Conn.EVENT_TYPE_ERROR:
        print(
            "请求客户端IP："
            + Conn.get_client_ip()
            + "|"
            + Conn.get_request().get_header("Meddyid")
        )
        return


def __TcpCallback__(Conn: TCPEvent):
    """你可以将 Conn.get_theology_id() 储存 起来 在回调函数之外的任意代码位置 调用 SunnyNet.TCPTools.SendMessage() 发送数据 或  SunnyNet.TCPTools.Close() 关闭会话"""

    if Conn.get_event_type() == Conn.EVENT_TYPE_ABOUT:
        print("TCP即将连接：" + Conn.get_local_addr() + "->" + Conn.get_remote_addr())
        return
    if Conn.get_event_type() == Conn.EVENT_TYPE_OK:
        print("TCP连接成功：" + Conn.get_local_addr() + "->" + Conn.get_remote_addr())
        return
    if Conn.get_event_type() == Conn.EVENT_TYPE_SEND:
        print(
            "TCP发送数据：" + Conn.get_local_addr() + "->" + Conn.get_remote_addr(),
            len(Conn.get_body()),
        )
        return
    elif Conn.get_event_type() == Conn.EVENT_TYPE_RECEIVE:
        print(
            "TCP接收数据：" + Conn.get_local_addr() + "->" + Conn.get_remote_addr(),
            len(Conn.get_body()),
        )
        return
    elif Conn.get_event_type() == Conn.EVENT_TYPE_CLOSE:
        print("TCP连接关闭：" + Conn.get_local_addr() + "->" + Conn.get_remote_addr())
        return


def __UDPCallback__(Conn: UDPEvent):
    """你可以将 Conn.get_theology_id() 储存 起来 在回调函数之外的任意代码位置 调用 SunnyNet.UDPTools.SendMessage() 发送数据"""
    if Conn.get_event_type() == Conn.EVENT_TYPE_SEND:
        print(
            "UDP发送数据：" + Conn.get_local_addr() + "->" + Conn.get_remote_addr(),
            len(Conn.get_body()),
        )
        return
    elif Conn.get_event_type() == Conn.EVENT_TYPE_RECEIVE:
        print(
            "UDP接收数据：" + Conn.get_local_addr() + "->" + Conn.get_remote_addr(),
            len(Conn.get_body()),
        )
        return
    elif Conn.get_event_type() == Conn.EVENT_TYPE_CLOSED:
        print("UDP连接关闭：" + Conn.get_local_addr() + "->" + Conn.get_remote_addr())
        return


def __WebsocketCallback__(Conn: WebSocketEvent):
    """你可以将 Conn.get_theology_id() 储存 起来 在回调函数之外的任意代码位置 调用 SunnyNet.WebsocketTools.SendMessage() 发送数据   或  SunnyNet.WebsocketTools.Close() 关闭会话"""
    if Conn.get_event_type() == Conn.EVENT_TYPE_CONNECTION_SUCCESS:
        print("Websocket 连接成功：" + Conn.get_url())
        return
    if Conn.get_event_type() == Conn.EVENT_TYPE_SEND:
        print("Websocket 发送数据：" + Conn.get_url(), len(Conn.get_body()))
        return
    if Conn.get_event_type() == Conn.EVENT_TYPE_RECEIVE:
        print("Websocket 收到数据：" + Conn.get_url(), len(Conn.get_body()))
        return
    if Conn.get_event_type() == Conn.EVENT_TYPE_CLOSE:
        print("Websocket 连接关闭：" + Conn.get_url())
        return


def TestSunnyNet():
    """测试SunnyNet 网络中间件"""
    port = 2025
    app = Sunny()  # 创建一个 SunnyNet 应用实例
    app.set_port(port)  # 设置网络服务的端口为 2025
    app.install_cert_to_system()  # 将证书安装到系统中，以便进行安全通信
    # app.cancel_ie_proxy()  # 取消 IE代理
    # app.set_ie_proxy()  # 设置 IE代理

    app.set_callback(  # 设置回调函数，以处理不同的网络事件
        __httpCallback__,
        __TcpCallback__,
        __WebsocketCallback__,
        __UDPCallback__,
        __ScriptLogCallback__,
        __ScriptCodeCallback__,
    )

    if not app.start():  # 尝试启动应用
        print("启动失败")  # 如果启动失败，打印错误信息
        print(app.error())  # 打印具体的错误信息
        exit(0)  # 退出程序
    else:
        if app.is_script_code_supported():
            print(
                "当前脚本管理页面:http://127.0.0.1:"
                + str(port)
                + "/"
                + app.set_script_page("")
            )
        else:
            print("当前脚本是Mini版本不支持脚本代码")

        if not app.open_drive(
            False
        ):  # 尝试打开驱动，需要以管理员模式运行，参数 False 表示使用Proxifier驱动，设置True 表示使用NFAPI驱动
            raise Exception(
                "加载驱动失败，进程代理不可用(注意，需要管理员权限（请检查），NFAPI驱动win7请安装 KB3033929 补丁)"
            )  # 如果加载驱动失败，抛出异常并提供详细提示
        else:
            app.process_all(
                True, False
            )  # 开始处理所有网络请求，参数为 True 和 False 表示某些处理选项
            print(
                "正在运行 0.0.0.0:2025"
            )  # 打印当前运行状态，表明服务正在监听 0.0.0.0:2025

    while True:  # 进入无限循环，保持程序运行
        time.sleep(10)  # 每隔 10 秒钟休眠一次，避免 CPU 占用过高


def TestSunnyHTTPClient():
    """测试SunnyHTTPClient"""
    Client = SunnyHTTPClient()  # 创建一个 SunnyHTTPClient 实例
    Client.set_random_tls(True)  # 启用随机 TLS 配置，用于生成不同的 TLS 指纹
    Client.open(
        "GET", "https://tls.browserleaks.com/json"
    )  # 打开一个 GET 请求，目标 URL 为指定的 JSON 服务
    Client.set_http2_config(
        tools.HTTP2_fp_Config_Firefox
    )  # 设置 HTTP/2 的配置为 Firefox 浏览器的指纹配置 需在OPEN之后使用
    Client.send()  # 发送请求
    parsed_data = json.loads(Client.get_body_string())
    # 提取 ja3_hash 和 akamai_hash
    ja3_hash = parsed_data.get("ja3_hash")
    akamai_hash = parsed_data.get("akamai_hash")

    print(ja3_hash, akamai_hash)  # 打印响应体，输出请求返回的内容

    Client.reset()  # 重置客户端状态，以便进行新的请求

    time.sleep(
        7
    )  # 等待 6 秒，因为上一次的请求的底层连接要在无操作后的5秒后断开连接,所以等待7秒后再次重新连接,指纹才会更新
    Client.set_random_tls(True)  # 再次启用随机 TLS 配置
    Client.open(
        "GET", "https://tls.browserleaks.com/json"
    )  # 再次打开一个 GET 请求，目标 URL 相同
    Client.set_http2_config(
        tools.HTTP2_fp_Config_Opera
    )  # 设置 HTTP/2 的配置为 Opera 浏览器的指纹配置 需在OPEN之后使用
    Client.send()  # 发送请求
    parsed_data = json.loads(Client.get_body_string())
    # 提取 ja3_hash 和 akamai_hash
    ja3_hash = parsed_data.get("ja3_hash")
    akamai_hash = parsed_data.get("akamai_hash")
    print(ja3_hash, akamai_hash)  # 打印响应体，输出请求返回的内容


def TestSunnyQueue():
    nm = Queue("5556666")
    nm.create()
    nm.push("123456")
    nm.push("1234560")
    nm.push("9999999999999999")
    nm.push("888888888888888888")
    print(nm.pull_string())
    print(nm.pull())
    nv = Queue("5556666")

    print(nv.pull_string())
    print(nv.pull())


def TestSunnyCertManager():
    cert = CertManager()
    cert.create("www.baidu.com")
    print(cert.export_pub_key())
    print(cert.export_private_key())
    print(cert.export_ca_cert())
    pass


def TestMultiPortWithFixedCert():
    """
    测试多端口代理 + 固定证书
    演示如何：
    1. 使用固定的证书（每次启动都使用同一个证书，避免重复安装）
    2. 同时开启多个端口进行代理
    """
    import os

    # ============ 步骤1: 准备固定证书 ============
    # 定义证书文件保存路径（使用绝对路径，确保每次都保存在同一位置）
    # 使用 P12 格式，这是标准的证书打包格式

    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cert_p12_file = os.path.join(script_dir, "sunny_cert.p12")  # P12 证书文件
    cert_password = "sunny2025"  # P12 证书密码

    print(f"\n[证书配置]")
    print(f"  证书文件路径: {cert_p12_file}")
    print(f"  证书密码: {cert_password}")
    print(f"  当前工作目录: {os.getcwd()}")

    # 创建证书管理器
    cert_manager = CertManager()

    # 检查 P12 证书文件是否已存在
    if os.path.exists(cert_p12_file):
        # 如果证书文件已存在，则从文件加载（使用固定证书）
        print("\n" + "=" * 60)
        print("检测到已有证书文件，正在加载固定证书...")
        print("=" * 60)

        try:
            # 从 P12 文件加载证书
            cert_manager.load_p12(cert_p12_file, cert_password)

            # 验证证书是否成功加载
            common_name = cert_manager.get_common_name()
            print(f"✓ 成功从 {os.path.basename(cert_p12_file)} 加载固定证书")
            print(f"  证书通用名称: {common_name}")
            print(f"  文件大小: {os.path.getsize(cert_p12_file)} 字节")
        except Exception as e:
            print(f"✗ 加载证书失败: {e}")
            print("  将重新创建证书...")
            # 如果加载失败，删除旧证书并重新创建
            try:
                os.remove(cert_p12_file)
            except:
                pass
            # 继续执行创建证书的逻辑
            os.path.exists(cert_p12_file)  # 重新检查（这里会是 False）

    if not os.path.exists(cert_p12_file):
        # 如果证书文件不存在，则创建新证书并保存到文件
        print("\n" + "=" * 60)
        print("未检测到证书文件，正在创建新证书...")
        print("=" * 60)

        # 创建新证书（域名可以自定义，这里使用 SunnyProxy）
        # 参数说明：
        # - common_name: 证书的通用名称
        # - country: 国家代码（默认 CN）
        # - organization: 组织名称（默认 Sunny）
        # - not_after: 有效期天数（默认 3650 天，即 10 年）
        print("  正在生成证书...")
        if not cert_manager.create("SunnyProxy"):
            print("✗ 证书创建失败")
            return

        print("  证书创建成功，正在保存...")

        # 将证书导出为 P12 格式并保存到文件
        export_result = cert_manager.export_p12(cert_p12_file, cert_password)

        print(f"  导出函数返回: {export_result}")

        # 再次验证文件是否真的被保存
        if os.path.exists(cert_p12_file):
            file_size = os.path.getsize(cert_p12_file)
            print(f"✓ 证书已成功创建并保存为 P12 格式")
            print(f"  - 文件路径: {cert_p12_file}")
            print(f"  - 文件大小: {file_size} 字节")
            print(f"  - 证书密码: {cert_password}")

            if file_size == 0:
                print("✗ 警告：文件大小为 0，可能保存失败")
                return
        else:
            print(f"✗ 证书保存失败：文件不存在")
            print(f"  - 预期路径: {cert_p12_file}")
            print(f"  - 导出结果: {export_result}")
            return

    print()

    # ============ 步骤2: 创建多个代理实例（不同端口）============
    # 定义要使用的端口列表
    ports = [8888, 8889, 8890]  # 可以根据需要添加更多端口

    # 存储所有代理实例
    proxy_apps = []

    print("=" * 60)
    print("正在创建多端口代理实例...")
    print("=" * 60)

    for port in ports:
        print(f"\n>>> 配置端口 {port} 的代理...")

        # 创建 SunnyNet 代理实例
        app = Sunny()

        # 设置端口
        app.set_port(port)
        print(f"  ✓ 设置端口: {port}")

        # 导入固定证书（所有端口使用同一个证书）
        if app.set_cert(cert_manager):
            print(f"  ✓ 已应用固定证书")
        else:
            print(f"  ✗ 证书设置失败")
            continue

        # 安装证书到系统（只需要安装一次即可，多个端口共用同一个证书）
        # 注意：如果证书已经安装过，这个操作不会重复安装
        if app.install_cert_to_system():
            print(f"  ✓ 证书已安装到系统")
        else:
            print(f"  ! 证书可能已经安装过了")

        # 设置回调函数（处理网络事件）
        app.set_callback(
            __httpCallback__,  # HTTP 请求回调
            __TcpCallback__,  # TCP 连接回调
            __WebsocketCallback__,  # WebSocket 回调
            __UDPCallback__,  # UDP 回调
            __ScriptLogCallback__,  # 脚本日志回调
            __ScriptCodeCallback__,  # 脚本代码保存回调
        )
        print(f"  ✓ 已设置回调函数")

        # 启动代理服务
        if app.start():
            print(f"  ✓ 端口 {port} 代理启动成功")

            # 显示脚本管理页面地址（如果支持）
            if app.is_script_code_supported():
                script_page = app.set_script_page("")
                print(f"  ✓ 脚本管理页面: http://127.0.0.1:{port}/{script_page}")

            # 将成功启动的代理实例添加到列表
            proxy_apps.append({"port": port, "app": app})
        else:
            print(f"  ✗ 端口 {port} 启动失败: {app.error()}")
            continue

    # ============ 步骤3: 显示运行状态 ============
    print("\n" + "=" * 60)
    print("多端口代理启动完成！")
    print("=" * 60)
    print(f"成功启动 {len(proxy_apps)} 个代理端口：")
    for proxy_info in proxy_apps:
        print(f"  - 0.0.0.0:{proxy_info['port']}")

    print("\n使用方法：")
    print("  1. 在浏览器或应用中配置 HTTP/HTTPS 代理")
    print("  2. 代理地址: 127.0.0.1")
    print("  3. 代理端口: 选择上述任意端口（如 8888、8889、8890）")
    print("  4. 所有端口使用同一个证书，无需重复配置")
    print("\n注意：")
    print("  - 证书文件已保存，下次启动会自动使用相同的证书")
    print("  - 如需重新生成证书，请删除 *.pem 文件后重启")
    print("=" * 60)

    # ============ 步骤4: 可选 - 启用进程代理（需要管理员权限）============
    # 如果需要拦截所有进程的网络请求，可以启用驱动
    # 注意：这需要管理员权限，且只能有一个实例加载驱动
    enable_driver = False  # 设置为 True 启用进程代理

    if enable_driver and len(proxy_apps) > 0:
        print("\n正在尝试启用进程代理（需要管理员权限）...")
        first_app = proxy_apps[0]["app"]

        # 参数说明：
        # False = 使用 Proxifier 驱动（不支持 UDP，不支持 32 位系统）
        # True = 使用 NFAPI 驱动（Win7 需要安装 KB3033929 补丁）
        if first_app.open_drive(False):
            # 捕获所有进程的网络请求
            first_app.process_all(True, False)
            print("✓ 进程代理已启用，所有程序的网络请求都会经过代理")
        else:
            print("✗ 进程代理启动失败（可能需要管理员权限）")

    # ============ 步骤5: 保持程序运行 ============
    print("\n程序正在运行中，按 Ctrl+C 停止...")
    try:
        while True:
            time.sleep(10)  # 每 10 秒检查一次
    except KeyboardInterrupt:
        print("\n\n正在关闭所有代理...")
        for proxy_info in proxy_apps:
            proxy_info["app"].stop()
        print("所有代理已关闭，程序退出。")


if __name__ == "__main__":
    # TestSunnyNet()  # 基础示例
    # TestSunnyHTTPClient()  # HTTP客户端示例
    # TestSunnyQueue()  # 队列示例
    # TestSunnyCertManager()  # 证书管理示例
    TestMultiPortWithFixedCert()  # 多端口 + 固定证书示例
