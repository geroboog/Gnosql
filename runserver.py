from flask import Flask
from flask_cors import *
from controller import controllers
# from flask_socketio import SocketIO, emit

apple = Flask(__name__,
              template_folder='templates',  # 指定模板路径，可以是相对路径，也可以是绝对路径。
              static_folder='static',  # 指定静态文件前缀，默认静态文件路径同前缀
              # static_url_path='/opt/auras/static',     #指定静态文件存放路径。
              )
apple.config['SECRET_KEY'] = 'GnosqlSecretKey'
apple.register_blueprint(controllers)  # 注册controller蓝图，并没有指定前缀。
CORS(apple,supports_credentials=True)


if __name__ == '__main__':
    apple.run(host='127.0.0.1', port=5000, debug=True)  # 运行flask http程序，host指定监听IP，port指定监听端口，调试时需要开启debug模式。
    # apple.run(host='103.204.177.4', port=5000)  # 运行flask http程序，host指定监听IP，port指定监听端口，调试时需要开启debug模式。
    #apple.run(host='192.168.1.179', port=5000, debug=True)  # 运行flask http程序，host指定监听IP，port指定监听端口，调试时需要开启debug模式。
