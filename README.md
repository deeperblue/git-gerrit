#Git-Gerrit

##Name
　git-gerrit是一系列封装git指令集，试用于gerrit管理代码使用
　
##Decription
　gerrit管理的codereview系统，与gitosis管理代码有点不一样，它是通过先将代码上传到ref/for的暂缓分支，代码通过审核后，才合并到入库分支上。
　
## Usage
 　init:
 　　初始化git仓库的hooks脚本,方便进行commit-msg做校验
 　　
　update:
 　　脚本自升级更新函数,后续如果脚本有更新,只需要执行该指令完成更新
 　　
　config:
　　支持设置gerrit用户名和默认审核人邮箱
　　config set-reviewer xxx@chinaxuhu.com可以设置默认审核人邮箱;　　
　　config get-reviewer 查看默认审核人邮箱设置
　　config set-username xxname 设置默认用户(本人名字),设置后请按提示重启一下终端或者是执行下source ~/.bashrc;
　　config get-username 查看默认用户
　　config -l (--list) 查看gerrit默认配置

　clone:
　　下载代码功能(特别注意本功能需要提前设置默认用户 (请参考1.c设置)
　　clone 将会罗列当前服务器现有的代码仓库提供下载
　　git-gerrit xxx_仓库名 直接下载xxx_仓库
　　git-gerrit xxx_仓库名 xxx_本地文件夹名 下载xxx_仓库到本地bbbb_本地文件夹
	
　commit:
　　自动提交,辅助alps+teksun架构,将第一次入库的文件做一次底包提交,以便于在gerrit网站显示diff差异
		
　push:
　　自动push提交,提交前做git pull origin --rebase更新代码,并且封装打包push到for审核分支
　　新增主动增加默认审核人邮箱功能,如果配置了默认审核人的邮箱,那么如果你在push时候不需要加审核人的邮箱,脚本会主动加上默认审核人邮箱.

　changeProject:
　　旧项目转化为alps+teksun新架构快速转换指令
		
　open:
　　快速打开当前修改对应gerrit审核界面
	
　verbose:
　　调试信息打印开关
	
　version:
　　版本显示
		
　help:
　　显示本帮助




