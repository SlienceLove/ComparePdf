# ComparePdf

初试PDF对比工具  包含文字以及图片查重
使用工具： Python3.11以及PDF.js 插件库

具体思路： 仅个人使用，利用python的插件搭建一个本地服务器，在服务器下创建一个静态文件夹存放资源以及所需要的文件 例如PDFjs中的workjs和minjs
          编写一个Server.py 用于创建本地flask服务器，一个文字对比脚本 一个图片对比  一个index主页面 存放到templates文件夹下 利用flask中的render_template来通讯
          文字对比 首先从本地选择俩个pdf文件， 利用PyMuPDF库 查找获取所有的文字内容进行对比 然后将其序列化存储到json中 再由showpdf页面去将json的内容解析展示
          图片对比 获取俩个pdf文件 将各自的图片全部输出到输出目录下，生成一个图片对比页面 将这些相同的图片对比展示

![image](https://github.com/user-attachments/assets/ae88cc66-c95c-4a3f-9e5c-3895e458fd66)
![image](https://github.com/user-attachments/assets/cf1fab40-1e03-478b-b1b0-03532f39e337)

![Uploading image.png…]()

