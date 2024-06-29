from flask import Flask, request, redirect, url_for, render_template, flash, session, send_file, jsonify
import pymysql
import secrets
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# 定义音乐文件夹路径
music_folder = "D:/python class hupo/yunlvshibie/Music"

# Dejavu 配置
config = {
    "database": {
        "host": "10.130.124.73",
        "user": "root",
        "passwd": "123456",
        "db": "QingYin2",
    },
    "database_type": "mysql"
}

# 创建 Dejavu 实例
djv = Dejavu(config)

# MySQL连接配置
db_config = {
    'host': '10.130.124.73',
    'user': 'root',
    'password': '123456',
    'database': 'QingYin2'
}

def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def execute_query(query, params=None, fetchone=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchone() if fetchone else cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print(f"Error executing query: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    uid = request.form.get('uid')
    password = request.form.get('password')

    if not uid or not password:
        flash('请输入用户ID和密码。', 'error')
        return redirect(url_for('index'))

    user = execute_query('SELECT * FROM user WHERE uid=%s AND password=%s', (uid, password), fetchone=True)

    if user:
        session['uid'] = user['uid']
        session['uname'] = user['uname']
        flash('登录成功！', 'success')
        return redirect(url_for('operation'))
    else:
        flash('用户ID或密码错误，请重试。', 'error')
        return redirect(url_for('index'))

@app.route('/operation')
def operation():
    if 'uid' in session:
        return render_template('operation.html', uname=session['uname'])
    else:
        flash('请先登录。', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uid = request.form.get('uid')
        uphone = request.form.get('uphone')
        uname = request.form.get('uname')
        password = request.form.get('password')

        if not (uid and uphone and uname and password):
            flash('请填写所有必填项。', 'error')
            return redirect(url_for('register'))

        existing_user = execute_query('SELECT * FROM user WHERE uphone=%s', (uphone,), fetchone=True)

        if existing_user:
            flash('该手机号已注册，请直接登录或找回密码。', 'error')
            return redirect(url_for('index'))

        try:
            execute_query('INSERT INTO user (uid, uphone, uname, password) VALUES (%s, %s, %s, %s)', (uid, uphone, uname, password))
            flash('注册成功！请登录。', 'success')
        except Exception as e:
            flash(f'注册失败：{str(e)}', 'error')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/forgetpassword', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        uid = request.form.get('uid')
        uphone = request.form.get('uphone')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not uid or not uphone or not new_password or not confirm_password:
            flash('请填写完整信息。', 'error')
            return redirect(url_for('forget_password'))

        if new_password != confirm_password:
            flash('两次输入的密码不一致，请重新输入。', 'error')
            return redirect(url_for('forget_password'))

        user = execute_query('SELECT * FROM user WHERE uid=%s AND uphone=%s', (uid, uphone), fetchone=True)

        if user:
            try:
                execute_query('UPDATE user SET password=%s WHERE uid=%s', (new_password, uid))
                flash('密码修改成功！请使用新密码登录。', 'success')
            except Exception as e:
                flash(f'密码修改失败：{str(e)}', 'error')
            return redirect(url_for('index'))
        else:
            flash('用户ID与授权手机号不一致，请重新输入。', 'error')
            return redirect(url_for('forget_password'))

    return render_template('forgetpassword.html')

@app.route('/recognize')
def recognize():
    return render_template('recognize.html')

@app.route('/play')
def play_song():
    song_name = request.args.get('song_name')

    if not song_name:
        return "歌曲名称不能为空。"

    song_path = None

    for root, dirs, files in os.walk(music_folder):
        for file in files:
            if song_name.lower() in file.lower():
                song_path = os.path.join(root, file)
                break
        if song_path:
            break

    if song_path:
        return send_file(song_path, as_attachment=False)
    else:
        return f"未找到名称为 '{song_name}' 的歌曲。"

@app.route('/save_record', methods=['POST'])
def save_record():
    if 'uid' in session:
        uid = session['uid']
        song_name = request.form.get('song_name')

        try:
            execute_query('INSERT INTO records (uid, song_name) VALUES (%s, %s)', (uid, song_name))
            flash('保存记录成功！', 'success')
        except Exception as e:
            flash(f'保存记录失败：{str(e)}', 'error')
        return render_template('recognize.html')
    else:
        flash('请先登录。', 'error')
        return redirect(url_for('index'))

@app.route('/recognize_file', methods=['POST'])
def recognize_file():
    file_path = request.json.get('file_path')
    if file_path:
        song = djv.recognize(FileRecognizer, file_path)
        return jsonify({'song_name': song['song_name']}) if song else jsonify({'message': 'No match'})
    return jsonify({'error': 'File path not provided'}), 400

@app.route('/recognize_microphone', methods=['POST'])
def recognize_microphone():
    seconds = int(request.json.get('seconds', 20))
    song = djv.recognize(MicrophoneRecognizer, seconds=seconds)

    print(song)

    if song and isinstance(song, tuple) and len(song) > 0:
        song_info_list = song[0]
        if isinstance(song_info_list, list) and len(song_info_list) > 0:
            song_info = song_info_list[0]
            if isinstance(song_info, dict) and 'song_name' in song_info:
                song_name = song_info['song_name'].decode('utf-8') if isinstance(song_info['song_name'], bytes) else song_info['song_name']
                return jsonify({'song_name': song_name})

    return jsonify({'message': 'No match'})

@app.route('/like_song', methods=['POST'])
def like_song():
    if 'uid' in session:
        uid = session['uid']
        song_name = request.json.get('song_name')

        if not song_name:
            return jsonify({"message": "歌曲名称不能为空"}), 400

        try:
            execute_query('INSERT INTO likes (uid, song_name) VALUES (%s, %s)', (uid, song_name))
            return jsonify({"message": "收藏成功"})
        except Exception as e:
            print(f"收藏失败：{str(e)}")
            return jsonify({"message": "收藏失败"}), 500
    else:
        return jsonify({"message": "请先登录"}), 401

@app.route('/fetch_history_records')
def fetch_history_records():
    if 'uid' in session:
        uid = session['uid']
        try:
            records = execute_query('SELECT record_id, song_name, time FROM records WHERE uid = %s', (uid,))
            records_data = [{'record_id': record['record_id'], 'song_name': record['song_name'], 'time': record['time'].strftime("%Y-%m-%d %H:%M:%S")} for record in records]
            return jsonify({"records": records_data})
        except Exception as e:
            print(f"Error fetching history records: {str(e)}")
            return jsonify({"error": "Error fetching history records", "details": str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/fetch_liked_records')
def fetch_liked_records():
    if 'uid' in session:
        uid = session['uid']
        try:
            likes = execute_query('SELECT like_id, song_name, time FROM likes WHERE uid = %s', (uid,))
            likes_data = [{'like_id': like['like_id'], 'song_name': like['song_name'], 'time': like['time'].strftime("%Y-%m-%d %H:%M:%S")} for like in likes]
            return jsonify({"likes": likes_data})
        except Exception as e:
            print(f"Error fetching liked records: {str(e)}")
            return jsonify({"error": "Error fetching liked records", "details": str(e)}), 500
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/get_username')
def get_username():
    if 'uid' in session:
        uid = session['uid']
        user = execute_query('SELECT uname FROM user WHERE uid = %s', (uid,), fetchone=True)
        if user:
            return jsonify({'username': user['uname']})
    return jsonify({'username': 'Guest'})

@app.route('/Mine.html')
def mine():
    if 'uid' in session:
        return render_template('Mine.html')
    else:
        return redirect(url_for('index'))

client_id = '39f0de13ec6f458594c6bc16b59b07a9'
client_secret = 'a4284b9465314453a6681994cc415d61'
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route('/recommend')
def recommend():
    artist_name = request.args.get('artist_name')
    results = sp.search(q='artist:' + artist_name, type='artist', limit=1)

    if len(results['artists']['items']) == 0:
        return jsonify(recommendations=[])

    artist = results['artists']['items'][0]
    top_tracks = sp.artist_top_tracks(artist['id'], country='US')

    recommendations = [track['name'] for track in top_tracks['tracks'][:3]]

    related_artists = sp.artist_related_artists(artist['id'])
    for related_artist in related_artists['artists'][:2]:
        related_tracks = sp.artist_top_tracks(related_artist['id'], country='US')
        for track in related_tracks['tracks'][:3]:
            recommendations.append(f"{related_artist['name']} - {track['name']}")

    return jsonify(recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

