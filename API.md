# SunnyNet Python API 完整文档

## 目录

- [安装](#安装)
- [快速开始](#快速开始)
- [核心类](#核心类)
  - [SunnyNet - 网络中间件](#sunnynet---网络中间件)
  - [SunnyHTTPClient - HTTP 客户端](#sunnyhttpclient---http-客户端)
  - [CertManager - 证书管理](#certmanager---证书管理)
  - [Queue - 队列](#queue---队列)
- [事件类](#事件类)
  - [HTTPEvent - HTTP 事件](#httpevent---http-事件)
  - [TCPEvent - TCP 事件](#tcpevent---tcp-事件)
  - [UDPEvent - UDP 事件](#udpevent---udp-事件)
  - [WebSocketEvent - WebSocket 事件](#websocketevent---websocket-事件)
- [工具类](#工具类)
  - [TCPTools - TCP 工具](#tcptools---tcp-工具)
  - [UDPTools - UDP 工具](#udptools---udp-工具)
  - [WebsocketTools - WebSocket 工具](#websockettools---websocket-工具)
- [完整示例](#完整示例)

---

## 安装

### 方式一：使用 pip 安装（推荐）

```bash
pip install SunnyNet
```

安装后运行以下命令下载平台对应的库文件：

```bash
sunnynet install
```

### 方式二：从源码安装

```bash
git clone https://github.com/yourusername/SunnyNet.git
cd SunnyNet
pip install -e .
```

### 验证安装

```python
import SunnyNet
print(SunnyNet.Version())  # 打印 DLL 版本
```

---

## 快速开始

### 基础 HTTP 代理示例

```python
from SunnyNet import SunnyNet, HTTPEvent

def http_callback(event: HTTPEvent):
    """HTTP 请求/响应回调"""
    if event.is_request():
        print(f"请求: {event.method()} {event.url()}")
    elif event.is_response():
        print(f"响应: {event.response().status_code()}")

# 创建 SunnyNet 实例
sunny = SunnyNet()

# 设置回调函数
sunny.set_callback(http_callback=http_callback)

# 启动代理
sunny.set_port(8899)
sunny.start()

# 设置系统代理
sunny.set_ie_proxy(True)

print("代理已启动在端口 8899，按 Ctrl+C 退出...")

try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sunny.stop()
    sunny.cancel_ie_proxy()
    print("代理已停止")
```

---

## 核心类

### SunnyNet - 网络中间件

`SunnyNet` 是核心代理中间件类，支持 HTTP/HTTPS、TCP、UDP、WebSocket 协议。

#### 初始化

```python
from SunnyNet import SunnyNet

sunny = SunnyNet()
```

#### 主要方法

##### 启动与停止

```python
# 启动中间件
sunny.start() -> bool

# 停止中间件
sunny.stop() -> None

# 关闭中间件（完全释放资源）
sunny.close() -> bool
```

##### 端口与代理设置

```python
# 设置代理端口（启动前调用）
sunny.set_port(port: int) -> None

# 获取当前端口
sunny.get_port() -> int

# 设置系统 IE 代理
sunny.set_ie_proxy(enable: bool) -> bool

# 取消系统 IE 代理
sunny.cancel_ie_proxy() -> None
```

##### 回调函数设置

```python
sunny.set_callback(
    http_callback=None,          # HTTP 回调
    tcp_callback=None,           # TCP 回调
    ws_callback=None,            # WebSocket 回调
    udp_callback=None,           # UDP 回调
    ScriptLogCallback=None,      # 脚本日志回调
    ScriptCodeCallback=None      # 脚本代码保存回调
)
```

##### 证书管理

```python
# 安装证书到系统
sunny.install_cert_to_system() -> bool

# 导出证书
sunny.export_cert() -> str

# 设置自定义证书
sunny.set_cert(cert: str, pkey: str) -> bool

# 重置证书为默认证书
sunny.reset_cert() -> bool

# 设置单个域名证书
sunny.set_domain_cert(domain: str, cert: str, pkey: str) -> bool
```

##### TCP 直连模式

```python
# 开启/关闭 TCP 直连（HTTPS 无法解码）
sunny.must_tcp(enable: bool) -> None

# 添加 TCP 直连规则（正则表达式）
sunny.must_tcp_add_regexp(regexp: str, within: bool) -> bool

# 移除 TCP 直连规则
sunny.must_tcp_remove_regexp(regexp: str) -> bool

# 清空所有 TCP 直连规则
sunny.must_tcp_clear_regexp() -> None
```

##### JA3 指纹

```python
# 开启/关闭随机 JA3 指纹
sunny.random_ja3(enable: bool) -> bool
```

##### DNS 设置

```python
# 设置 DNS 服务器（支持 TLS DNS，853 端口）
sunny.set_dns_server(server_name: str) -> None
```

##### 出口 IP 设置

```python
# 设置全局出口 IP（网卡内网 IP）
sunny.set_OutRouterIP(ip: str) -> bool
```

##### S5 代理验证

```python
# 开启/关闭 S5 代理身份验证
sunny.open_verify_user(enable: bool) -> None

# 添加 S5 验证用户
sunny.add_verify_user(username: str, password: str) -> bool

# 移除 S5 验证用户
sunny.remove_verify_user(username: str) -> bool

# 清空所有 S5 验证用户
sunny.clear_verify_user() -> None
```

##### WebAssembly 脚本

```python
# 加载并执行 Wasm 脚本
sunny.wasm_run(wasm_file: str) -> bool

# 停止 Wasm 脚本
sunny.wasm_stop() -> None
```

##### 获取上下文

```python
# 获取 SunnyNet 上下文（用于底层调用）
sunny.context() -> int
```

---

### SunnyHTTPClient - HTTP 客户端

独立的 HTTP/HTTPS 客户端，支持各种 HTTP 操作。

#### 初始化

```python
from SunnyNet import SunnyHTTPClient

client = SunnyHTTPClient()
```

#### 主要方法

##### 请求操作

```python
# 打开 HTTP 请求
client.open(method: str, url: str)

# 发送请求
client.send(data: bytes = None) -> bool

# 发送字符串数据
client.send_str(data: str = None) -> bool

# 发送文件数据
client.send_file(file_path: str) -> bool
```

##### 请求头设置

```python
# 设置单个请求头
client.set_header(name: str, value: str)

# 批量设置请求头（字典）
client.set_headers(headers: dict)

# 设置 User-Agent
client.set_user_agent(user_agent: str)

# 设置 Content-Type
client.set_content_type(content_type: str)

# 设置 Cookie
client.set_cookie(cookie: str)
```

##### 代理设置

```python
# 设置上游代理（S5 或 HTTP）
client.set_proxy(proxy_url: str) -> bool
# 示例：
#   HTTP 代理: http://admin:123456@127.0.0.1:8888
#   S5 代理: socket5://admin:123456@127.0.0.1:8888
```

##### 超时与重定向

```python
# 设置超时时间（毫秒）
client.set_timeout(timeout: int)

# 设置是否允许重定向
client.set_redirect(enable: bool)

# 设置最大重定向次数
client.set_max_redirects(max_redirects: int)
```

##### TLS/JA3 设置

```python
# 设置 TLS 版本
client.set_tls_version(version: str)

# 随机化 JA3 指纹
client.random_ja3() -> bool

# 设置 HTTP/2 配置
client.set_h2_config(config: str)
```

##### 响应获取

```python
# 获取响应状态码
client.get_status_code() -> int

# 获取响应头
client.get_response_header(name: str) -> str

# 获取所有响应头
client.get_response_headers() -> str

# 获取响应体（字节）
client.get_response_body() -> bytes

# 获取响应体（字符串）
client.get_response_text() -> str

# 将响应体保存到文件
client.save_response_to_file(file_path: str) -> bool
```

##### 其他方法

```python
# 获取最后的错误信息
client.get_error() -> str

# 重置客户端（清除所有设置）
client.reset()

# 设置出口 IP
client.set_OutRouterIP(ip: str) -> bool
```

#### 完整示例

```python
from SunnyNet import SunnyHTTPClient

client = SunnyHTTPClient()

# 设置请求
client.open("GET", "https://api.github.com/users/github")
client.set_user_agent("Mozilla/5.0")
client.set_timeout(30000)  # 30 秒

# 发送请求
if client.send():
    print(f"状态码: {client.get_status_code()}")
    print(f"响应: {client.get_response_text()}")
else:
    print(f"错误: {client.get_error()}")
```

---

### CertManager - 证书管理

证书管理器，用于生成和管理 TLS 证书。

#### 初始化

```python
from SunnyNet import CertManager

cert_mgr = CertManager()
```

#### 主要方法

```python
# 生成 CA 证书
cert_mgr.generate_ca_cert(
    subject: str = "CN=SunnyNet CA",
    valid_days: int = 365
) -> tuple[str, str]  # 返回 (cert_pem, key_pem)

# 生成域名证书
cert_mgr.generate_domain_cert(
    domain: str,
    ca_cert: str,
    ca_key: str,
    valid_days: int = 365
) -> tuple[str, str]  # 返回 (cert_pem, key_pem)

# 从文件加载证书
cert_mgr.load_cert_from_file(cert_file: str) -> str

# 保存证书到文件
cert_mgr.save_cert_to_file(cert_pem: str, file_path: str) -> bool
```

---

### Queue - 队列

线程安全的队列类，用于多线程通信。

#### 初始化

```python
from SunnyNet import Queue

queue = Queue()
```

#### 主要方法

```python
# 入队
queue.put(item: any)

# 出队（阻塞）
queue.get() -> any

# 出队（非阻塞）
queue.get_nowait() -> any

# 队列大小
queue.size() -> int

# 是否为空
queue.empty() -> bool

# 清空队列
queue.clear()
```

---

## 事件类

### HTTPEvent - HTTP 事件

HTTP 请求/响应事件对象，在 HTTP 回调函数中接收。

#### 事件类型判断

```python
# 是否为请求事件
event.is_request() -> bool

# 是否为响应事件
event.is_response() -> bool

# 是否为错误事件
event.is_error() -> bool

# 是否为 WebSocket 升级
event.is_websocket() -> bool
```

#### 基本信息

```python
# 获取 HTTP 方法
event.method() -> str

# 获取完整 URL
event.url() -> str

# 获取域名
event.host() -> str

# 获取路径
event.path() -> str

# 获取进程 ID
event.pid() -> int

# 获取消息 ID
event.message_id() -> int
```

#### 请求操作（Request）

```python
# 获取请求对象
req = event.request()

# 获取/设置请求体
req.body() -> bytes
req.body_to_str() -> str
req.set_body(data: bytes) -> bool
req.set_str(data: str) -> bool

# 获取/设置请求头
req.get_header(name: str) -> str
req.set_header(name: str, value: str) -> bool
req.del_header(name: str) -> bool
req.headers() -> str  # 获取所有请求头
req.set_headers(headers: str)  # 设置所有请求头

# Cookie 操作
req.get_cookie(name: str) -> str
req.set_cookie(cookie: str) -> bool
req.cookies() -> str

# URL 操作
req.get_url() -> str
req.set_url(url: str) -> bool

# 获取/设置 User-Agent
req.get_user_agent() -> str
req.set_user_agent(ua: str) -> bool

# 设置代理
req.set_proxy(proxy_url: str, timeout: int) -> bool

# 设置超时
req.set_request_timeout(timeout: int)

# JA3 随机化
req.random_ja3() -> bool

# HTTP/2 配置
req.set_h2_config(config: str)

# 设置出口 IP
req.set_OutRouterIP(ip: str) -> bool

# 检查是否为原始 body
req.is_request_raw_body() -> bool

# 保存原始请求数据到文件
req.raw_request_data_to_file(save_file: str) -> bool
```

#### 响应操作（Response）

```python
# 获取响应对象
resp = event.response()

# 获取/设置响应体
resp.body() -> bytes
resp.body_to_str() -> str
resp.set_body(data: bytes) -> bool
resp.set_str(data: str) -> bool

# 获取/设置响应头
resp.get_header(name: str) -> str
resp.set_header(name: str, value: str) -> bool
resp.del_header(name: str) -> bool
resp.headers() -> str
resp.set_headers(headers: str)

# 状态码操作
resp.status_code() -> int
resp.set_status_code(code: int) -> bool

# Cookie 操作
resp.get_cookie(name: str) -> str
resp.set_cookie(cookie: str) -> bool
```

#### 连接操作

```python
# 丢弃当前请求/响应
event.drop()

# 重新请求
event.repeat()
```

---

### TCPEvent - TCP 事件

TCP 连接事件对象。

#### 事件类型

```python
# 连接建立
event.is_connected() -> bool

# 接收数据
event.is_received() -> bool

# 发送数据
event.is_send() -> bool

# 连接关闭
event.is_closed() -> bool
```

#### 基本信息

```python
# 本地地址
event.local_addr() -> str

# 远程地址
event.remote_addr() -> str

# 获取数据
event.data() -> bytes

# 进程 ID
event.pid() -> int

# 消息 ID
event.message_id() -> int
```

#### 操作方法

```python
# 发送数据
event.send(data: bytes) -> bool

# 关闭连接
event.close() -> bool

# 设置出口 IP
event.set_OutRouterIP(ip: str) -> bool
```

---

### UDPEvent - UDP 事件

UDP 数据包事件对象。

#### 事件类型

```python
# 接收数据包
event.is_received() -> bool

# 发送数据包
event.is_send() -> bool
```

#### 基本信息

```python
# 本地地址
event.local_addr() -> str

# 远程地址
event.remote_addr() -> str

# 进程 ID
event.pid() -> int

# 消息 ID
event.message_id() -> int
```

#### 操作方法

```python
# 读取数据
event.read() -> bytes

# 写入数据
event.write(data: bytes) -> bool

# 关闭
event.close() -> bool

# 设置出口 IP
event.set_OutRouterIP(ip: str) -> bool
```

---

### WebSocketEvent - WebSocket 事件

WebSocket 连接事件对象。

#### 事件类型

```python
# 连接打开
event.is_open() -> bool

# 接收消息
event.is_message() -> bool

# 连接关闭
event.is_close() -> bool

# 错误
event.is_error() -> bool
```

#### 消息类型

```python
# 文本消息
event.is_text() -> bool

# 二进制消息
event.is_binary() -> bool
```

#### 基本信息

```python
# URL
event.url() -> str

# 进程 ID
event.pid() -> int

# 消息 ID
event.message_id() -> int
```

#### 操作方法

```python
# 获取消息内容
event.get_message() -> bytes
event.get_message_str() -> str

# 发送消息
event.send_text(text: str) -> bool
event.send_binary(data: bytes) -> bool

# 关闭连接
event.close() -> bool

# 设置出口 IP
event.set_OutRouterIP(ip: str) -> bool
```

---

## 工具类

### TCPTools - TCP 工具

提供 TCP 连接操作的工具函数。

```python
from SunnyNet import TCPTools

# 创建 TCP 连接
conn_id = TCPTools.connect(host: str, port: int) -> int

# 发送数据
TCPTools.send(conn_id: int, data: bytes) -> bool

# 接收数据
TCPTools.recv(conn_id: int, size: int) -> bytes

# 关闭连接
TCPTools.close(conn_id: int) -> bool
```

### UDPTools - UDP 工具

提供 UDP 数据包操作的工具函数。

```python
from SunnyNet import UDPTools

# 创建 UDP socket
sock_id = UDPTools.create() -> int

# 发送数据包
UDPTools.sendto(sock_id: int, data: bytes, host: str, port: int) -> bool

# 接收数据包
UDPTools.recvfrom(sock_id: int, size: int) -> tuple[bytes, str, int]

# 关闭 socket
UDPTools.close(sock_id: int) -> bool
```

### WebsocketTools - WebSocket 工具

提供 WebSocket 连接操作的工具函数。

```python
from SunnyNet import WebsocketTools

# 创建 WebSocket 连接
ws_id = WebsocketTools.connect(url: str) -> int

# 发送文本消息
WebsocketTools.send_text(ws_id: int, text: str) -> bool

# 发送二进制消息
WebsocketTools.send_binary(ws_id: int, data: bytes) -> bool

# 接收消息
WebsocketTools.recv(ws_id: int) -> bytes

# 关闭连接
WebsocketTools.close(ws_id: int) -> bool
```

---

## 完整示例

### 示例 1：HTTP 请求/响应修改

```python
from SunnyNet import SunnyNet, HTTPEvent

def http_callback(event: HTTPEvent):
    """修改 HTTP 请求和响应"""
    
    # 请求阶段
    if event.is_request():
        req = event.request()
        
        # 修改 User-Agent
        req.set_user_agent("CustomBot/1.0")
        
        # 添加自定义请求头
        req.set_header("X-Custom-Header", "MyValue")
        
        # 打印请求信息
        print(f"[请求] {req.get_method()} {event.url()}")
    
    # 响应阶段
    elif event.is_response():
        resp = event.response()
        
        # 修改响应头
        resp.set_header("X-Modified", "true")
        
        # 修改响应体
        body = resp.body_to_str()
        if "example" in body:
            body = body.replace("example", "modified")
            resp.set_str(body)
        
        print(f"[响应] {resp.status_code()} - {len(resp.body())} bytes")

# 启动代理
sunny = SunnyNet()
sunny.set_callback(http_callback=http_callback)
sunny.set_port(8899)
sunny.start()
sunny.set_ie_proxy(True)

print("代理运行中...")
input("按回车键停止\n")

sunny.stop()
sunny.cancel_ie_proxy()
```

### 示例 2：TCP 流量监控

```python
from SunnyNet import SunnyNet, TCPEvent

def tcp_callback(event: TCPEvent):
    """监控 TCP 流量"""
    
    if event.is_connected():
        print(f"[TCP 连接] {event.local_addr()} -> {event.remote_addr()}")
    
    elif event.is_received():
        data = event.data()
        print(f"[TCP 接收] {len(data)} bytes from {event.remote_addr()}")
        # 可以修改接收的数据
        # event.send(modified_data)
    
    elif event.is_send():
        data = event.data()
        print(f"[TCP 发送] {len(data)} bytes to {event.remote_addr()}")
    
    elif event.is_closed():
        print(f"[TCP 关闭] {event.remote_addr()}")

sunny = SunnyNet()
sunny.set_callback(tcp_callback=tcp_callback)
sunny.must_tcp(True)  # 开启 TCP 直连模式
sunny.set_port(8899)
sunny.start()

print("TCP 监控运行中...")
input("按回车键停止\n")

sunny.stop()
```

### 示例 3：WebSocket 消息拦截

```python
from SunnyNet import SunnyNet, WebSocketEvent

def ws_callback(event: WebSocketEvent):
    """拦截 WebSocket 消息"""
    
    if event.is_open():
        print(f"[WS 连接] {event.url()}")
    
    elif event.is_message():
        if event.is_text():
            msg = event.get_message_str()
            print(f"[WS 消息] {msg}")
            
            # 修改消息内容
            if "hello" in msg:
                modified_msg = msg.replace("hello", "hi")
                event.send_text(modified_msg)
        
        elif event.is_binary():
            data = event.get_message()
            print(f"[WS 二进制] {len(data)} bytes")
    
    elif event.is_close():
        print(f"[WS 关闭] {event.url()}")

sunny = SunnyNet()
sunny.set_callback(ws_callback=ws_callback)
sunny.set_port(8899)
sunny.start()

print("WebSocket 拦截运行中...")
input("按回车键停止\n")

sunny.stop()
```

### 示例 4：使用 HTTP 客户端

```python
from SunnyNet import SunnyHTTPClient

def send_request():
    client = SunnyHTTPClient()
    
    # GET 请求
    client.open("GET", "https://api.github.com/users/github")
    client.set_user_agent("Mozilla/5.0")
    client.set_timeout(30000)
    
    if client.send():
        print(f"状态码: {client.get_status_code()}")
        print(f"响应头: {client.get_response_headers()}")
        print(f"响应体: {client.get_response_text()[:200]}...")
    else:
        print(f"请求失败: {client.get_error()}")
    
    # POST 请求
    client.reset()
    client.open("POST", "https://httpbin.org/post")
    client.set_content_type("application/json")
    
    json_data = '{"name": "test", "value": 123}'
    if client.send_str(json_data):
        print(f"\nPOST 响应: {client.get_response_text()}")

send_request()
```

### 示例 5：证书管理

```python
from SunnyNet import SunnyNet, CertManager

# 生成自定义 CA 证书
cert_mgr = CertManager()
ca_cert, ca_key = cert_mgr.generate_ca_cert(
    subject="CN=My Custom CA",
    valid_days=365
)

# 使用自定义证书
sunny = SunnyNet()
sunny.set_cert(ca_cert, ca_key)

# 为特定域名设置证书
domain_cert, domain_key = cert_mgr.generate_domain_cert(
    domain="example.com",
    ca_cert=ca_cert,
    ca_key=ca_key,
    valid_days=365
)
sunny.set_domain_cert("example.com", domain_cert, domain_key)

sunny.set_port(8899)
sunny.start()
```

### 示例 6：多线程队列通信

```python
from SunnyNet import SunnyNet, HTTPEvent, Queue
import threading

# 创建队列
request_queue = Queue()

def http_callback(event: HTTPEvent):
    """将请求放入队列"""
    if event.is_request():
        request_queue.put({
            'method': event.method(),
            'url': event.url(),
            'headers': event.request().headers()
        })

def process_requests():
    """处理队列中的请求"""
    while True:
        try:
            req = request_queue.get()
            print(f"处理请求: {req['method']} {req['url']}")
        except:
            break

# 启动处理线程
thread = threading.Thread(target=process_requests, daemon=True)
thread.start()

# 启动代理
sunny = SunnyNet()
sunny.set_callback(http_callback=http_callback)
sunny.set_port(8899)
sunny.start()

print("多线程代理运行中...")
input("按回车键停止\n")

sunny.stop()
```

---

## 版本信息

```python
from SunnyNet import __version__, Version

print(f"Python 包版本: {__version__}")
print(f"DLL 版本: {Version()}")
```

---

## 常见问题

### Q: 如何处理 HTTPS 流量？

**A**: SunnyNet 默认支持 HTTPS 解密。首次使用需要安装证书：

```python
sunny = SunnyNet()
if sunny.install_cert_to_system():
    print("证书安装成功")
```

### Q: 如何避免解密特定域名的 HTTPS？

**A**: 使用 TCP 直连模式的正则规则：

```python
# 规则内的域名走 TCP 直连（不解密）
sunny.must_tcp_add_regexp(r".*\.example\.com", within=True)
```

### Q: 如何设置上游代理？

**A**: 在请求回调中设置：

```python
def http_callback(event: HTTPEvent):
    if event.is_request():
        req = event.request()
        req.set_proxy("http://127.0.0.1:7890", 30000)
```

### Q: 如何获取请求的进程信息？

**A**: 使用 `pid()` 方法：

```python
def http_callback(event: HTTPEvent):
    print(f"进程 ID: {event.pid()}")
```

### Q: 库文件下载失败怎么办？

**A**: 可以手动下载并放置到正确位置：

```bash
# 查看安装信息
sunnynet info

# 强制重新下载
sunnynet install --force
```

---

## 技术支持

- **GitHub**: https://github.com/kiss-kedaya/SunnyNet
- **官网**: https://esunny.vip
- **QQ 群**: 751406884, 545120699, 170902713, 616787804

---

## 许可证

MIT License

Copyright (c) 2024 秦天

---

## 更新日志

### v1.4.0 (2024-10-21)
- 修复 Unicode 编码问题
- 修复平台检测问题（使用 `sys.maxsize`）
- 添加镜像节点延迟检测
- 优化下载体验

### v1.3.3
- 基础版本发布

