# coding:utf-8
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer

# 配置数据库连接信息
config = {
    "database": {
        "host": "192.168.233.28",
        "user": "root",
        "passwd": "123456",
        "db": "QingYin2",
    },
    "database_type": "mysql"
}

djv = Dejavu(config)

# 识别文件
song = djv.recognize(FileRecognizer, "D:/python class hupo/yunlvshibie/Music/1.mp3")
print(song)

# 识别从mic输入的音频
secs = 8
song = djv.recognize(MicrophoneRecognizer, seconds=secs)
if song is None:
    print
    "No Match"
else:
    print(song)