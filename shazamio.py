import pyaudio
import wave
import shazamio
import asyncio

# 录制音频
def record_audio(output_file, record_seconds=5, sample_rate=44100, chunk_size=1024):
    audio_format = pyaudio.paInt16
    channels = 1

    p = pyaudio.PyAudio()

    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Recording...")

    frames = []

    for _ in range(0, int(sample_rate / chunk_size * record_seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

async def recognize_song(file_path):
    shazam = shazamio.Shazam()
    out = await shazam.recognize_song(file_path)
    return out

# 示例使用
if __name__ == "__main__":
    audio_file = "recorded_audio.wav"  # 录制音频的文件名
    record_audio(audio_file, record_seconds=10)  # 录制10秒的音频

    # 使用shazamio识别录制的音频
    result = asyncio.run(recognize_song(audio_file))
    print(result)
