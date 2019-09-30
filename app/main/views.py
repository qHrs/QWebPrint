from flask import render_template, Blueprint, request, current_app, jsonify
from werkzeug.utils import secure_filename
import subprocess
import app
import os
import time

# 创建蓝本对象
main = Blueprint('main', __name__)


@main.route('/')
def index():
    printerList = getPrints()
    return render_template("index.html", printerList=printerList)


@main.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            # return jsonify({'code': 0, 'filename': filename, 'msg': 'success'})
            origin_file_name = file.filename
            # filename = secure_filename(file.filename)
            filename = origin_file_name

            if os.path.exists(current_app.config['UPLOAD_FOLDER']):
                pass
            else:
                os.makedirs(current_app.config['UPLOAD_FOLDER'])

            newFileName = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())) + '_'
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName + filename))
            return jsonify({'code': 0, 'filename': origin_file_name, 'msg': newFileName + filename})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


@main.route('/toprint', methods=['POST'])
def toPrint():
    '执行打印程序  lp -d HP_LaserJet_1020 filename'
    printer = request.form.get('printer')
    filename = request.form.get('filename')
    password = request.form.get('password')

    if password == '101022':
        if printer:
            if filename:
                filename = current_app.config['UPLOAD_FOLDER'] + filename
                printComm = 'lp -d {0} {1}'
                # (status, output) = (0, 'test')
                print(printComm.format(printer, filename))
                (status, output) = subprocess.getstatusoutput(printComm.format(printer, filename))
                if status == 0:
                    return jsonify({'code': 0, 'output': str(output), 'msg': 'success'})
                else:
                    return jsonify({'code': -1, 'output': str(output), 'msg': 'fail'})
            else:
                return jsonify({'code': -1, 'output': '', 'msg': 'No file'})
        else:
            return jsonify({'code': -1, 'output': '', 'msg': 'no printer'})
    else:
        return jsonify({'code': -1, 'output': '', 'msg': 'password error'})

# ['hp1020'] None
def getPrints():
    '获取打印机列表'
    (status, output) = subprocess.getstatusoutput("lpstat -p | grep printer |awk '{print $2}'")
    if status == 0:
        return output.split('\n')
    else:
        return None


def getDefaultPrint():
    '获取默认打印机列表'
    (status, output) = subprocess.getstatusoutput("lpstat -d | grep  'system default destination'| awk -F ':[ ]' '{print $2}'")
    return str(output)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config.ALLOWED_EXTENSIONS

# https://gitlab.com/byygyy/ddns_ipv6/blob/master/ddns.py
# lpstat -p -d | grep printer |awk '{print $2}'
# commands.getstatusoutput("lpstat -p -d | grep printer |awk '{print $2}'")
# b1list = b1.split('\n')
# lpstat -p -d | grep  'system default destination'| awk -F ':[ ]' '{print $2}'
# 显示作业 lpstat -W all
# lpstat: Error - need "completed", "not-completed", or "all" after "-W" option.
# 系统状态 lpstat -t  scheduler is running
# lp -d HP_LaserJet_1020 uploads/2019-09-30-21_48_49_国庆阅兵.pdf
# request id is HP_LaserJet_1020-30 (1 file(s))
