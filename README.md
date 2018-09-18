# ProxyPool
---  
*个人用代理池*  

&emsp;&emsp;本人在学习爬虫技术期间，遇到一些封ip的反爬机制，这种情况使用代理即可，参考了有关资料开了这个项目。主要是使用爬虫技术从网上爬取免费代理，然后再进行检测，检测完毕可用的存入mongodb，同时隔一段时间从mongodb中读取代理进行检测，剔除掉不能用的，如果可用的少于设定值就重新爬取。
## 运行截图：  
![微信图片_20180918213301.png](https://i.loli.net/2018/09/18/5ba0fea01efa6.png)  
![微信图片_20180918213428.png](https://i.loli.net/2018/09/18/5ba0ff046c6ae.png)
![微信图片_20180918213735.png](https://i.loli.net/2018/09/18/5ba0ffb670052.png)
![微信图片_20180918213550.png](https://i.loli.net/2018/09/18/5ba0fff36db91.png)
![微信图片_20180918213730.png](https://i.loli.net/2018/09/18/5ba0ffb671726.png)
![微信图片_20180918213718.png](https://i.loli.net/2018/09/18/5ba0ffb67657d.png)
## 使用说明：
### 一、 虚拟环境运行说明：
1. 本项目使用了pipenv，首先需要安装pipenv，详情参考 **[pipenv官网](https://pipenv.readthedocs.io/en/latest/)** 的介绍安装；
2. 使用代码 `pipenv install` 安装项目所需的模块；
3. 使用代码 `pipenv shell` 进入虚拟环境终端；
4. 同样的也可以直接查看Pipfile文件夹里 `[packages]` 下所有模块逐个安装，然后不在虚拟环境下运行；  
### 二、 代理池使用说明：
1. examples文件夹下面有使用示例，可以进行查看；
2. 首先请启动mongodb服务，相关请查阅mongodb有关资料(建议查看官方文档，如 [Debian系统mongodb安装配置说明](https://docs.mongodb.com/master/tutorial/install-mongodb-on-debian/?_ga=2.196215400.576766313.1537239502-183274682.1537153037) 这里的安装、配置及使用过程中，确实有些坑，具体相信你能搞定)；
3. 然后直接 `python main.py` 即可启动服务；
4. 之后访问你在config里设置的地址即可访问，返回数据是json格式；
5. `127.0.0.1:8000/`是欢迎页面；
6. `127.0.0.1:8000/proxy/`是单条代理数据；
7. `127.0.0.1:8000/proxies/`返回10条代理数据；
8. `127.0.0.1:8000/proxy/3/`返回3条代理数据数据；
### 三、未完待续...