import requests as req
from lxml import etree
import random
import threading
import os


# 通过fiddler，打开群精华获取
p_skey = ""
skey = ""
# QQ号
qq_account = ""
# 群号
group_id = ""
download_thread_num = 3
illegal_chars = ["\\", "/", "*", "?", ":", '"', "<", ">", "|"]


# 创建img文件夹
if not os.path.exists("img"):
    os.makedirs("img")


def random_len(length):
    return random.randrange(int("1" + "0" * (length - 1)), int("9" * length))


url = (
    "https://qun.qq.com/essence/indexPc?gc="
    + group_id
    + "&seq="
    + str(random_len(8))
    + "&random="
    + str(random_len(10))
)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) QQ/9.6.5.28778 "
    "Chrome/43.0.2357.134 Safari/537.36 QBCore/3.43.1298.400 QQBrowser/9.0.2524.400",
    "Host": "qun.qq.com",
    "Cookie": "p_skey="
    + p_skey
    + "; p_uin=o"
    + qq_account
    + "; uin=o"
    + qq_account
    + "; skey="
    + skey,
}

response = req.get(url, headers=headers)
response.encoding = "UTF-8"
data = etree.HTML(response.text)
totalData = []
# 记录所有图片链接
download_list = []

for i in range(1, len(data.xpath('//*[@id="app"]/div[2]/*'))):
    essence = {"qq_account": "", "qq_name": "", "send_time": "", "content": []}
    current_pos = '//*[@id="app"]/div[2]/div[' + str(i) + "]"

    # 获取QQ账号
    try:
        essence["qq_account"] = data.xpath(current_pos + "/div[1]/@style")[0][
            10:-2
        ].split("/")[5]
    except:
        essence["qq_account"] = "unknown"

    # 获取QQ昵称
    try:
        essence["qq_name"] = data.xpath(current_pos + "/div[2]")[0].text.strip(" \n")
    except:
        essence["qq_name"] = "unknown"

    # 获取发送时间
    try:
        essence["send_time"] = data.xpath(current_pos + "/div[3]")[0].text.strip(" \n")
    except:
        essence["send_time"] = "unknown"

    # 处理内容div
    content_node_class = data.xpath(current_pos + "/div[last()-1]/@class")

    # 图文/纯文本
    if len(content_node_class) > 0 and content_node_class[0] == "short":
        for j in data.xpath(current_pos + "/div[last()-1]/*"):
            if j.tag == "span":
                content = j.text
                essence["content"].append(content)
            elif j.tag == "img":
                content = j.attrib.get("src")[0:-10]
                essence["content"].append(content)
                download_list.append(content)
    else:
        inside_node_class = data.xpath(current_pos + "/div[last()-1]/div/@class")

        # 外部引用
        if len(inside_node_class) > 0:
            if inside_node_class[0] == "img_wrap":
                # 图片包装
                try:
                    img = data.xpath(current_pos + "/div[last()-1]/div/img/@src")[0]
                    filename = data.xpath(
                        current_pos + "/div[last()-1]/div/div[last()]"
                    )[0].text.strip(" \n")
                    essence["content"].append(img)
                    download_list.append(img)
                    essence["content"].append(filename)
                except:
                    essence["content"].append("图片解析失败")

            elif inside_node_class[0] == "doc_wrap":
                # 文档包装
                try:
                    title = data.xpath(current_pos + "/div[last()-1]/div/div[1]")[
                        0
                    ].text.strip(" \n")
                    image = data.xpath(current_pos + "/div[last()-1]/div/i/@style")[0][
                        21:
                    ].split(")")[0]
                    source = data.xpath(current_pos + "/div[last()-1]/div/div[2]")[
                        0
                    ].text.strip(" \n")
                    essence["content"].append(title)
                    essence["content"].append(image)
                    download_list.append(image)
                    essence["content"].append(source)
                except:
                    essence["content"].append("文档解析失败")

            elif inside_node_class[0] == "file_wrap":
                # 文件包装 - 新增处理
                try:
                    file_name = data.xpath(current_pos + "/div[last()-1]/div/div[1]")[
                        0
                    ].text.strip(" \n")
                    file_icon = data.xpath(current_pos + "/div[last()-1]/div/i/@style")[
                        0
                    ][21:].split(")")[0]
                    file_size = data.xpath(current_pos + "/div[last()-1]/div/div[2]")[
                        0
                    ].text.strip(" \n")
                    essence["content"].append(f"文件: {file_name}")
                    essence["content"].append(file_icon)
                    download_list.append(file_icon)
                    essence["content"].append(f"大小: {file_size}")
                except:
                    essence["content"].append("文件解析失败")

            else:
                print(f"未知类型: inside_node_class={inside_node_class[0]}")
                essence["content"].append(f"未知类型: {inside_node_class[0]}")

        # 纯图片
        else:
            try:
                img = data.xpath(current_pos + "/div[last()-1]/div/img/@src")[0][0:-10]
                essence["content"].append(img)
                download_list.append(img)
            except:
                essence["content"].append("图片解析失败")

    totalData.append(essence)

# 输出txt文件
with open("output.txt", "w", encoding="utf-8") as file:
    for i in totalData:
        file.write(repr(i))
        file.write("\n")

print(f"成功解析 {len(totalData)} 条精华消息")
print(f"发现 {len(download_list)} 个图片/文件链接")


# 下载图片/文件
def download(imglist):
    session = req.Session()  # 使用Session提高效率
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
    )

    for idx, i in enumerate(imglist):
        try:
            response = session.get(i, timeout=10)
            response.raise_for_status()

            # 生成文件名
            name = i.split("/")[-1].split("&")[0].split("=")[-1]

            # 处理文件名
            if not "." in name[-5:]:
                # 根据响应头判断文件类型
                content_type = response.headers.get("content-type", "")
                if "image/jpeg" in content_type or "image/jpg" in content_type:
                    name += ".jpg"
                elif "image/png" in content_type:
                    name += ".png"
                elif "image/gif" in content_type:
                    name += ".gif"
                else:
                    name += ".jfif"

            # 替换非法字符
            for char in illegal_chars:
                name = name.replace(char, "_")

            # 保存文件
            filepath = os.path.join("img", name)
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"下载完成: {name} ({idx+1}/{len(imglist)})")

        except Exception as e:
            print(f"下载失败: {i} - {str(e)}")


# 多线程下载图片至img文件夹下
def download_pic(download_list):
    if not download_list:
        print("没有需要下载的内容")
        return

    # 去重
    download_list = list(set(download_list))
    print(f"去重后剩余 {len(download_list)} 个文件需要下载")

    length = len(download_list) // download_thread_num
    threads = []

    for i in range(download_thread_num):
        if i != download_thread_num - 1:
            part_list = download_list[i * length : (i + 1) * length]
        else:
            part_list = download_list[i * length :]

        if part_list:  # 只有当有内容时才创建线程
            download_thread = threading.Thread(target=download, args=(part_list,))
            threads.append(download_thread)
            download_thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("所有下载任务完成")


# 执行下载
if __name__ == "__main__":
    download_pic(download_list)
