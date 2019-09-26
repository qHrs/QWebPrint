from flask import Flask
import commands

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

def getPrints():
    '获取打印机列表'
    (status, output) = commands.getstatusoutput("lpstat -p | grep printer |awk '{print $2}'")
    printList = output.split('\n')
    return printList

def getDefaultPrint():
    '获取默认打印机列表'
    (status, output) = commands.getstatusoutput("lpstat -d | grep  'system default destination'| awk -F ':[ ]' '{print $2}'")
    return str(output)

# https://gitlab.com/byygyy/ddns_ipv6/blob/master/ddns.py
# lpstat -p -d | grep printer |awk '{print $2}'
# commands.getstatusoutput("lpstat -p -d | grep printer |awk '{print $2}'")
# b1list = b1.split('\n')
# lpstat -p -d | grep  'system default destination'| awk -F ':[ ]' '{print $2}'
# 显示作业 lpstat -W all
# lpstat: Error - need "completed", "not-completed", or "all" after "-W" option.
# 系统状态 lpstat -t  scheduler is running



if __name__ == '__main__':
    app.run()
