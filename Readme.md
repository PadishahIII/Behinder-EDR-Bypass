<h1>Bypass EDR and establish Behinder connection</h1>

# Overview
- 场景
  
可RCE或文件上传，但有终端防护写不上webshell

- 方法
  
调用nashorn引擎，把冰蝎服务端代码放到js脚本里，恶意js代码通过http参数获取，让落地的jsp尽量不包含特征，然后用mitmproxy脚本实现无缝衔接原版冰蝎

- 前提
  
jdk≥8 <15，behinder客户端3/4均可

# Prerequisite
本项目需要使用[mitmproxy](https://mitmproxy.org/)项目搭建代理，下载依赖：
```
pip install -r requirements.txt
```

# Usage
1. 首先用RCE或文件上传漏洞把jsp写到web能访问到的地方，有两个版本可选：
- [behinder-server-base64.jsp](https://github.com/PadishahIII/Behinder-EDR-Bypass/blob/master/behinder-server-base64.jsp): 对nashorn代码仅base64编码，可能被WAF拦，但落地不容易被杀（**首选**）
- [behinder-server-aes.jsp](https://github.com/PadishahIII/Behinder-EDR-Bypass/blob/master/behinder-server-aes.jsp): 对nashorn代码进行AES加密，密钥硬编码，落地容易被杀，相对的，绕WAF很管用
2. 本地开启mitmproxy代理，同样是两个版本，需要与jsp的版本对应：
- [mitmBehinder-base64.py](https://github.com/PadishahIII/Behinder-EDR-Bypass/blob/master/mitmBehinder-base64.py)（**首选**）
- [mitmBehinder-aes.py](https://github.com/PadishahIII/Behinder-EDR-Bypass/blob/master/mitmBehinder-aes.py)

在本地8085端口开启mitmproxy代理：
```
mitmproxy -s mitmBehinder-base64.py --listen-host 0.0.0.0 -p 8085 -k
```
在本地8085端口开启mitmproxy代理，转发到8080端口：
```
mitmproxy -s mitmBehinder-base64.py --listen-host 0.0.0.0 -p 8085 --mode upstream:http://127.0.0.1:8080 -k
```
3. 冰蝎客户端设置mitmproxy的代理，连接即可，默认密码rebeyond，可在mitmproxy脚本中修改服务端密码
