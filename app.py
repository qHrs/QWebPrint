from flask import Flask, render_template
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    printList = getPrints()

    return render_template("test.html")

def getPrints():
    '获取打印机列表'
    (status, output) = subprocess.getstatusoutput("lpstat -p | grep printer |awk '{print $2}'")
    return output.split('\n')

def getDefaultPrint():
    '获取默认打印机列表'
    (status, output) = subprocess.getstatusoutput("lpstat -d | grep  'system default destination'| awk -F ':[ ]' '{print $2}'")
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
