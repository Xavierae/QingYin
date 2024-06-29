import pymysql
from dtw import dtw
from numpy.linalg import norm
from numpy import array
import numpy as np
import librosa
import pyaudio
import wave
import os


# 获取数据库连接
def get_db_connection():
    return pymysql.connect(
        host='10.130.219.69',
        user='root',
        password='123456',
        db='QingYin',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


# 加载录音文件并提取节奏特征
def extract_beat_features_from_audio(filename):
    y, sr = librosa.load(filename)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_frames = librosa.feature.delta(beat_frames)
    return beat_frames.flatten()


# 匹配录音文件的节奏特征与数据库中的音乐文件
def match_audio_to_database(audio_filename):
    # 提取录音文件的节奏特征
    x = extract_beat_features_from_audio(audio_filename)

    # 初始化匹配结果字典
    compare_result = {}

    # 数据库查询
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 查询数据库中所有音乐文件的节奏特征
            sql = "SELECT filename, beat_features FROM music_beat_features"
            cursor.execute(sql)
            results = cursor.fetchall()

            for result in results:
                filename = result['filename']
                beat_features_str = result['beat_features']

                # 将数据库中的节奏特征字符串转换为数组
                y = np.array(list(map(float, beat_features_str.split(',')))).reshape(-1, 1)

                # 计算录音文件节奏特征与数据库中每个音乐文件的距离
                dist, _, _, _ = dtw(x.reshape(-1, 1), y, dist=lambda x, y: norm(x - y, ord=1))
                compare_result[filename] = dist

    finally:
        # 关闭数据库连接
        connection.close()

    # 找到最匹配的音乐文件名
    matched_song = min(compare_result, key=compare_result.get)

    return matched_song


# 示例使用录音并匹配
def example_usage():
    # 录音并保存为 WAV 文件
    sr = 44100
    chunk = sr
    recording_seconds = 30  # 录制音频的时长（秒）

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sr,
                    input=True,
                    frames_per_buffer=chunk)
    frames = []
    print("开始录音，请说话或播放音乐...")
    for i in range(0, int(sr / chunk * recording_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    print("录音结束.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # 将录制的音频保存为 WAV 文件
    wf = wave.open('music_test/test.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sr)
    wf.writeframes(b''.join(frames))
    wf.close()

    # 匹配录音文件与数据库中的音乐
    matched_song = match_audio_to_database('music_test/test.wav')
    print("匹配到的音乐文件名:", matched_song)


# 执行示例使用
example_usage()
