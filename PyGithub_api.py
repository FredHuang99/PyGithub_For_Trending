#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#需要先pip install PyGithub
from github import Github 
import os

#创建保存结果的文件
def create_file(new_file):
    if not os.path.exists(new_file):
        f = open(new_file,'w')
    return

filename='XXXXXX'
create_file(filename)

#爬取项目的stargazers
respository='XXX/YYY'#格式为：hpcaitech/ColossalAI
g=Github("Your_Token") #需要去github先申请自己的token

#获得目前的stargazers列表
repo=g.get_repo(respository)
stargazers=repo.get_stargazers_with_dates() #repo.stargazers_count可以看目前有多少人关注了

#把stargazers的用户名按行储存到刚才创建的文件中
with open(filename, 'w') as f:
    for people in stargazers:
        lis = str(people.user).split('"') 
        data = lis[1]+"\r\n" #也可用data = str(people.user.login)代替
        f.write(data)

#保存当前的关注者到列表中用于比较
def get_names(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            if line != '':
                data.append(line)
    return data
now_stargazers = get_names(filename) 

#找出新添关注者保存在new_stargazers中
new_stargazers='XXXXXX'
create_file(new_stargazers)
#获取已经关注了的用户名字，初始文件为ColossalAI.txt，后面把第A天的结果当作第A+1天的old_stargazers_file即可
old_name = get_names('old_stargazers_file_name')
#找出新关注的人并保存
with open(new_stargazers, 'r') as f:
    for name in now_stargazers:
        if name not in old_name:
            data = name+"\r\n"
            f.write(data)

#可以按上述代码对DeepSpeed、fairscale、PatrickStar进行同样的操作。
#如果要对比使用get_name后按照'找到新关注者的方式'对比即可

#其他api
#通过用户找到用户的followers数量来判断是不是大V，email和company以及bio可以区分国内和海外用户
users = get_names(filename)
for name in users:
    user = g.get_user(name)
    #user.followers
    #user.bio
    #user.company
    #user.email
#流量的api
repo.get_top_paths() # 点击量Top10的path
repo.get_clones_traffic(per="day") #如果per="week" 近14天每个周期clone流量
repo.get_views_traffic(per="day") #如果er="week" 近14天，每个周期总点击量

#画出关注量的曲线，找到那几天有大量的点击
import matplotlib.pyplot as plt
import pandas as pd

def plot_star_history_cumcount(repo_name, ax=None):
    repo = g.get_repo(repo_name)
    star_history = [[stargazer.user.login, stargazer.user.html_url, stargazer.starred_at]
                    for stargazer in repo.get_stargazers_with_dates()]
    star_history = pd.DataFrame(star_history, columns=['login', 'html_url', 'time'])
    star_history.set_index(keys='time', inplace=True)
    star_history_cumsum = star_history.drop('html_url', axis='columns').resample(rule='d').count().cumsum()
    star_history_cumsum.columns = [repo_name]
    star_history_cumsum.plot(ax=ax)
    plt.savefig("fig_name", dpi=)

g = Github("Your Token")
fig, ax = plt.subplots(1, 1)
plot_star_history_cumcount(repo_name="XXXXXX", ax=ax)

