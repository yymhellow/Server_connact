# @Time    : 2020/3/24 3:02 下午
# @Author  : yym
# @Site : 
# @File    : ssh_paramiko.py
# @Software: PyCharm
import paramiko,getpass
# ssh = paramiko.SSHClient()      #实例化一个连接
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())       #跳过第一次连接机器的验证
# ssh.connect(hostname='192.168.0.49', port=1101, username='root', password='yumo1012')           #填写连接信息
# stdin, stdout, stderr = ssh.exec_command('cd / && ls')
# result = stdout.read()
# print(result)
# ssh.close()


#以上是最简单的ssh执行命令


user = input('请输入用户名')
pwd = getpass.getpass('password')           #隐藏输入的密码
if user == 'yym' and pwd == 'yumo1012':
    print('登录成功')
else:
    print('登录失败')

server_hosts = {
    'yym':{
            '192.168.0.49',
            '192.168,.0.114',
    },
    'kk':{
        '192.168.0.49'
    },
}
host_list = list(server_hosts[user])        #将取到的字典的值转变成一个队列
print(host_list)
print('请选择服务器')
for index,item in enumerate(host_list,1):       #分别取出索引和队列的内容
    print(index,item)

inp = input('你选择的是:')
inp = int(inp)
hostname = host_list[ inp - 1 ]
# port = 1101

# print(hostname)

transport = paramiko.Transport((hostname,1101))         #封装一个连接信息
transport.connect(username=user, password=pwd)
ssh = paramiko.SSHClient()
ssh._transport = transport
while True:
    comm = input('请输入需要执行的命令')
    # print('连接上了')
    stdin, stdout, stderr = ssh.exec_command(str(comm))
    print(stdout.read())
    if comm == 'quit':
        break

ssh.close()

# transport = paramiko.Transport(('192.168.0.49', 1101))
# transport.connect(username='root',password='yumo1012')
# ssh = paramiko.SSHClient()
# ssh._transport =transport
# stdin, stdout, stderr = ssh.exec_command('free -h')
# print(stdout.read())
# transport.close()
