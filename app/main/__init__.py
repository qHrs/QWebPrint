from flask import Blueprint
# 创建蓝本对象
main = Blueprint('main', __name__)

from . import views