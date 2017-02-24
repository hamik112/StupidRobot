# StupidRobot
Find and click your item in Amazon automaticlly, using Python and Selenium.

噢这是个傻逼的自动脚本，可以帮你在亚马逊上自动搜索某个关键字，然后在搜索页面中找到你想要的商品，点击进去。
如果不能增加商品在该搜索页面的排序的话，真的是，毫无卵用...(捂脸)
看到A9算法里就没提到点击率，为啥会影响到排名...(懵逼)

**使用方式**

1. 初始化git子项目：`git submodule update --init --recursive`
2. 按照[IPProxyPool](https://github.com/qiyeboy/IPProxyPool)的说明，把代理池跑起来。搞不定的话...自己想办法吧这个跟我没关系啊...(捂脸)
4. 启动docker，哥们你自己装docker和docker-compose啊，然后：`docker-compose up -d`
3. 安装依赖：`pip install -r requirements.txt`
5. 启动celery：`celery -A utils.tasks worker -l=info`
6. 好了开始跑脚本吧：`python main.py`，自己修改里面的值，跑挂了别打我...

**Bug**

提Issue吧，反正我也不会修的，这个项目太蠢了(捂脸)

相关技术：Python3、Celery、Docker、Selenium
