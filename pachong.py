from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Define the path to the ChromeDriver executable
chromedriver_path = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe"

# Create a ChromeDriver service
service = Service(chromedriver_path)

# Create Chrome browser object
driver = webdriver.Chrome(service=service)

# Open the QQ music page for Jay Chou
driver.get("https://y.qq.com/n/yqq/singer/001t94rh4OpQn0.html")

# Configuration
csv_file = open('songs_jaychou.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
start = time.time()

# Write header row to CSV
writer.writerow(["歌曲名", "流派", "发行时间", "评论数"])


# Function to get song details
def getSongResource(url):
    song_resource = {}
    driver.get(url)

    try:
        # Wait for the song name element to be visible
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "data__name_txt")))

        # Get song name
        song_name = driver.find_element(By.CLASS_NAME, "data__name_txt").text.strip()
        print(f"开始获取歌曲《{song_name}》的基本信息")

        # Get genre, release time, and number of comments
        song_genre = driver.find_element(By.CSS_SELECTOR, ".data_info__data .data_info__item:nth-child(1)").text[
                     3:].strip()
        song_time = driver.find_element(By.CSS_SELECTOR, ".data_info__data .data_info__item:nth-child(2)").text[
                    5:].strip()
        song_comment_num = driver.find_element(By.CSS_SELECTOR, ".data_info__data .data_info__item:nth-child(3)").text[
                           3:-1].strip()
        print(f"歌曲《{song_name}》基本信息获取完毕")

        # Store song details in dictionary
        song_resource = {
            "歌曲名": song_name,
            "流派": song_genre,
            "发行时间": song_time,
            "评论数": song_comment_num
        }
    except Exception as e:
        print(f"获取歌曲信息时出错: {e}")

    return song_resource


# Specify URLs for Jay Chou's top 5 songs
song_urls = [
    "https://y.qq.com/n/yqq/song/000IB5aG3VsZrD.html",
    "https://y.qq.com/n/yqq/song/003uM2Fw1zpvnS.html",
    "https://y.qq.com/n/yqq/song/004B5qtI0x4Q7P.html",
    "https://y.qq.com/n/yqq/song/004akN0y0BLfHj.html",
    "https://y.qq.com/n/yqq/song/004NfMSx08BvVT.html"
]

# Get resources for each song
song_resources = []
for song_page in song_urls:
    print(f"开始处理歌曲页面：{song_page}")
    song_resource = getSongResource(song_page)
    if song_resource:
        song_resources.append(song_resource)
    print(f"歌曲页面处理完毕：{song_page}")

# Write to CSV
print("正在写入CSV文件...")
for song in song_resources:
    writer.writerow([song["歌曲名"], song["流派"], song["发行时间"], song["评论数"]])

csv_file.close()
driver.quit()
end = time.time()
print(f"爬取完成，总耗时{end - start}秒")
