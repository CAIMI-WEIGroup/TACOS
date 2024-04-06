import os
import requests
import argparse


def download_resource(source=None, target=None):
    if source is None or target is None:
        # 在这里执行默认操作，比如下载一个默认资源或显示帮助信息
        print("No source or target specified. Executing default action...")
        # 这里以打印信息作为示例，默认操作可以根据您的需求定制
        # 例如，下载一个默认资源或者显示更多帮助信息
        return

    # 假设 URL 的构建方式如下，根据实际情况调整
    base_url = "http://example.com/resources"
    url = f"{base_url}/{source}/{target}.txt"

    # 目标文件夹路径
    target_folder = "../resources/coefficient/"

    # 确保目标文件夹存在，如果不存在，则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 尝试下载资源
    response = requests.get(url)

    if response.status_code == 200:
        # 构建目标文件的完整路径
        file_path = os.path.join(target_folder, f"{target}.txt")

        # 写入文件
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded resource successfully to '{file_path}'.")
    else:
        print("Failed to download the resource. Please check the source and target names.")


if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(
        description='Download a specific resource to the resources/coefficient/ directory.')
    # 添加 'source' 参数，不强制要求，以允许默认操作
    parser.add_argument('source', type=str, nargs='?', help='Part of the URL that specifies the resource source.',
                        default=None)
    # 添加 'target' 参数，同样不强制要求，以允许默认操作
    parser.add_argument('target', type=str, nargs='?', help='The specific resource name to download.', default=None)

    # 解析命令行参数
    args = parser.parse_args()

    # 调用下载函数
    download_resource(args.source, args.target)
