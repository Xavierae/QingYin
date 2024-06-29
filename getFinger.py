import pymysql

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

# 将节奏特征数据存储到数据库中
def store_beat_features_to_db(music_folder):
    import os
    import librosa
    import numpy as np

    # 初始化数据库连接
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # 遍历音乐文件夹中的所有 .mp3 文件
            for filename in os.listdir(music_folder):
                if filename.endswith('.mp3'):
                    filepath = os.path.join(music_folder, filename)
                    try:
                        # 加载音频文件并提取节奏特征
                        y, sr = librosa.load(filepath)
                        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
                        beat_frames = librosa.feature.delta(beat_frames)

                        # 将节奏特征转换为字符串形式
                        beat_frames_str = ','.join(map(str, beat_frames.flatten()))

                        # 将数据插入数据库
                        sql = "INSERT INTO music_beat_features (filename, beat_features) VALUES (%s, %s)"
                        cursor.execute(sql, (filename, beat_frames_str))

                        print(f"Stored beat features for {filename}")

                    except Exception as e:
                        print(f"Error processing {filename}: {e}")

            # 提交更改
            connection.commit()

    finally:
        # 关闭数据库连接
        connection.close()


# 执行存储函数，传入音乐文件夹路径作为参数
if __name__ == "__main__":
    music_folder_path = r"D:\python class hupo\yunlvshibie\Music"
    store_beat_features_to_db(music_folder_path)
