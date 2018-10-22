说明：

1、堡垒机程序通过POST方式跟CMDB通信，进行用户认证、主机列表获取。

2、堡垒机记录远程服务器的返回文本到日志中，可以利用其实现回放功能。

3、如果在服务器上使用专门的账号运行堡垒机，需要确保该账号下也安装了pyenv和python。然后在其~/.bashrc中追加：
    python /opt/jumpserver/jumpserver.py run
    logout
