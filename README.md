# 微博用户信息全网爬虫系统 (weibo_user_info)
### 目录 
<ul>
  <li><a href="#system">环境要求</a></li>
  <li><a href="#use">相关配置</a></li>
  <li><a href="#theory">实现原理</a></li>
  <li><a href="#example">使用实例</a></li>
  <li><a href="#view">数据可视化</a></li>
  <li><a href="#use">说明</a></li>
</ul>

#
### <div id="system"/>1. 环境要求</div>
> • python3 <br/>
> • mongodb数据库 <br/>
> • python库（pymongo，requests） <br/>


#
### <div id="use"/>2. 相关配置</div>
> 需要在config.py文件中进行mongodb数据库，是否使用代理，是否使用cookie，最多重试次数，初始微博URL等的相关配置。

#
### <div id="theory"/>3. 实现原理</div>
> 1) 全用户爬取原理：根据微博用户的粉丝数和关注数，来一直递归循环获取所有的用户（0粉丝，0关注的用户则爬取不到）
> 2) 分析原理：从微博移动版m.weibo.cn的ajax接口请求进行分析，以姚晨为例(主页为https://m.weibo.cn/profile/1266321801)
![image](https://www.google.ie/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)
#
### <div id="example"/>4. 使用实例</div>
#
### <div id="view"/>5. 数据可视化</div>
#
### <div id="explain"/>6. 说明</div>
