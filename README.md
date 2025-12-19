# QQessence
Python爬虫获取QQ群精华消息

修改借鉴自：User-Time/requests_qq_essence

支持所有格式的精华消息（2023.4.25）
ps:对转发群文件、外部链接（如qq音乐分享）等精华消息，仅支持获取标题、缩略图、文件名（群文件）

可选下载精华消息中的图片，默认3线程（群被封后图片链接都会失效）

## 项目依赖

本项目需要以下Python库：

```bash
pip install requests lxml
```

**依赖说明：**
- `requests`: 用于发送HTTP请求获取网页内容和下载文件
- `lxml`: 用于解析HTML内容，提取精华消息数据

## 使用方法

### 1. 获取必要参数

需要获取以下参数并填入`main.py`：

- `p_skey`: QQ登录凭证
- `skey`: QQ登录凭证
- `qq_account`: 你的QQ号
- `group_id`: 目标QQ群号

**获取方式：**

方法一：通过Fiddler抓包
- 打开Fiddler
- 在QQ客户端中打开群精华
- 在Fiddler中找到对应请求，查看Cookie获取`p_skey`和`skey`

方法二：通过QQ群官网（推荐）
- 登录QQ群官网: https://qun.qq.com
- 打开浏览器开发者工具(F12)
- 在Network标签下找到任意请求
- 查看Cookie，找到`p_skey`和`skey`参数

参考链接: https://www.52pojie.cn/thread-835096-1-1.html

### 2. 配置参数

编辑`main.py`，填入获取的参数：

```python
p_skey = "你的p_skey"
skey = "你的skey"
qq_account = "你的QQ号"
group_id = "目标群号"
```

可选配置：
```python
download_thread_num = 3  # 下载线程数，可根据网络情况调整
```

### 3. 运行程序

```bash
python main.py
```

程序会：
1. 自动创建`img`文件夹（如果不存在）
2. 爬取QQ群精华消息
3. 将结果保存到`output.txt`
4. 自动下载精华消息中的图片/文件到`img`文件夹

### 4. 导出HTML（可选）

如需更方便地查看精华消息，可以导出为HTML格式：

```bash
python output_html.py
```

感谢 @javayqy 提供的HTML导出功能

## 注意事项

- Cookie有效期有限，失效后需要重新获取
- 群被封后图片链接会失效，请及时备份
- 程序会自动创建`img`文件夹，无需手动创建
- 下载大量文件时请注意网络状况和存储空间

****
2023.10.18

由Maze-is-moon补充，p_skey及skey参数也可登录qq群官网：https://qun.qq.com 从cookie中获取

参考：https://www.52pojie.cn/thread-835096-1-1.html

****

谨以此项目悼念我被tx封掉的积累上百条精华消息的旧群(2022.11.4)![image](https://user-images.githubusercontent.com/105963780/234330957-7916ff46-f98a-42b0-bcb1-21d3c0b8eac6.png)
以上为原作者(original)

****
感谢@javayqy
添加导出html功能，主文件后，再运行output_html.py即可导出html，方便查看群精华
以上为 [@WhatETE](https://github.com/WhatETE) 

---

本次更新解决了旧项目报错无法使用的问题，代码来自 [@AllenWu233](https://github.com/AllenWu233) 在原仓库的 issue 中的留言

设置本 repo 一是方便存档记录，二是在Readme中更新了一些使用方法，并添加了 ChangeLog
2025.12.20 00:02