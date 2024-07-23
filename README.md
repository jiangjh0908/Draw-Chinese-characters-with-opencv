# Draw-Chinese-characters-with-freetype
由于opencv不支持中文字符的绘制，转为Pillow绘制后再转为opencv格式对边缘设备的性能有一定负担，特别是处理图像实时检测任务时。此项目使用freetype库避免了格式的转换，缩短了时间。同时也避免了安装一些系统库什么的，比较方便。

效果图：
![Image text](https://github.com/jiangjh0908/Draw-Chinese-characters-with-freetype/blob/main/output_image.jpg)

实测在NVIDIA Jetson Nano上耗时0.001秒，用pillow转换格式的话要0.02秒。
本代码根据一篇csdn上的博客做了一点修改，但找不到原来的博客了，知道的话可以联系我，挂个链接。
