import mysql.connector
from dejavu import Dejavu

def main():
    # 定义Dejavu的配置
    config = {
        "database": {
            "host": "10.130.219.69",  # 数据库主机地址
            "user": "root",  # 数据库用户名
            "passwd": "123456",  # 数据库密码
            "db": "QingYin2",  # 数据库名称
        },
        "database_type": "mysql",  # 数据库类型
    }

    # 初始化Dejavu
    try:
        djv = Dejavu(config)  # 使用配置创建Dejavu实例
        print("Dejavu初始化成功。")  # 输出初始化成功的信息
    except Exception as e:
        print(f"初始化Dejavu时出错: {e}")  # 捕捉并输出初始化过程中发生的错误
        return  # 退出函数

    # 对目录进行指纹识别
    try:
        fingerprinted_files = djv.fingerprint_directory("D:/python class hupo/yunlvshibie/Music", [".mp3"])
        # 从指定目录中的.mp3文件提取指纹
        if fingerprinted_files is None:
            print("指纹识别返回None，可能是文件路径不正确或没有有效的.mp3文件。")
            # 如果返回None，可能是路径不正确或没有找到有效的.mp3文件
        else:
            print(f"目录指纹识别成功，共处理 {len(fingerprinted_files)} 个文件。")
            # 如果指纹识别成功，输出处理的文件数量
    except Exception as e:
        print(f"指纹识别目录时出错: {e}")  # 捕捉并输出指纹识别过程中发生的错误
        return  # 退出函数

    # 获取数据库中的指纹数量
    try:
        num_fingerprints = djv.db.get_num_fingerprints()  # 获取数据库中的指纹数量
        print(f"数据库中的指纹数量: {num_fingerprints}")  # 输出数据库中的指纹数量
    except Exception as e:
        print(f"获取指纹数量时出错: {e}")  # 捕捉并输出获取指纹数量过程中发生的错误

if __name__ == '__main__':
    main()  # 调用主函数
