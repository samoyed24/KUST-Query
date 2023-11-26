# 昆明理工大学自助查询平台

### 前言

该项目为开源项目，基于Django 4.2框架开发，主要可以为昆明理工大学学生提供信息查询服务。

目前支持的查询类型有：成绩查询、课表查询。更多功能仍在更新中。

在网站菜单选择相应的查询服务，输入你在昆明理工大学教务网的学号与密码，稍等片刻，网站会自动下载你查询的信息，格式为xlsx。


### 使用方法

下载全部源码，安装所需要的全部第三方库，打开cmd(或Powershell)，cd到manage.py文件所在路径。

此处以源码目录为"D:\ChromeDownload\DjangoProject2\"为例：
```shell
cd D:\ChromeDownload\DjangoProject2\
```

确保你已经安装了所需要的第三方库，依次运行以下命令：
```shell
python manage.py makemigrations
python manage.py migrate
```

系统提示迁移全部完成后，输入：
```shell
python manage.py runserver 0.0.0.0:80
```

程序若无任何错误提示，就是已经在本地服务器成功开启。此时，浏览器访问"localhost"，即可进入网站主页。

请注意：为便于使用，开源服务端配置已将数据库类型选择为轻量级的SQLite3，而非服务端实际使用的MySQL。如有需要，请自行更改配置。为了安全着想，SECRET_KEY一项已被抹去，请自行替换为安全性更高的SECRET_KEY。关于服务器配置，请自行访问Django官方文档查询。

### 更新日志

> V1.0 
> 2023/11/26
> >添加了一些基础功能