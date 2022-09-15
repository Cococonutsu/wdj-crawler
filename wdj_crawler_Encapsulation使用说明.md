# wdj_crawler_Encapsulation使用说明



## 背景

爬取[**豌豆荚网站**](https://www.wandoujia.com/)  [**软件分类**](https://www.wandoujia.com/category/app)页面 或者 [**游戏分类**](https://www.wandoujia.com/category/game)页面  每一个**单独分类**的**软件图标**，爬取软件数量可以自定。





## demo

```python
if __name__ == '__main__':
    get_app_1 = GetAppid(all_sort_params = {'系统工具' : [5018,0]}, ctoken = 'QYOVWfScAluGWfUufI22IC7-', need_app_num = 20, save_path = r'D:\vs code\vs  code file\test')
    app_ids = get_app_1.get_appid()

    get_page_1 = GetPage(real_data_appids = app_ids , doc_name='系统工具', save_path = r'D:\vs code\vs  code file\test' )
    page = get_page_1.get_app_page()
## 本程序最终输出即为需要爬取的图片文件
```





## 使用说明

该文件内有三个类，使用者只需要调用 **GetAppid** 和 **Getpage** 这两个类即可获取一个分类的图标。



  ### GetAppid使用

  #### 1.GetAppid参数 

`all_sort_params`：

* **传参形式**：`{ '分类名称' : [ 'catId' , 'subcatId' ] }`

* **参数说明**：

  1.分类名称即为需要爬取的分类名称

  2.catId 和 subcatId 是每一个分类自己唯一的参数

* **catId 和 subcatId 获取参数方式如下**

  1.此处以爬取系统工具为例，**参数中的分类名称可以自定义**

  * <img src="https://github.com/Cococonutsu/wdj-crawler/blob/main/page/1.png" />

  

  2.右击页面空白处，点击检查

  * <img src="D:\python learning\假期自学计划\python算法\屏幕截图(2).png" style="zoom: 25%;" />

  

  3. 点击检查后   
        1. 将主页面下拉到查看更多位置 
        2. 选择网络
        3. 并点击禁止标志清空该页面

  * <img src="D:\python learning\假期自学计划\python算法\微信截图_20220827234531.png" style="zoom: 33%;" />



  4. 点击查看更多，右侧会刷新出新的文件包，双击右侧网络中以**more**开头得文件包

	* ![](D:\python learning\假期自学计划\python算法\微信截图_20220827234531.png)  

  5. 双击该文件包后，为我们会看到这个页面，其中就有**catId** 和 **subcatId** 和 **ctoken**

	* <img src="D:\python learning\假期自学计划\python算法\微信截图_20220827235140.png" style="zoom:150%;" />

  `ctoken`：

* **传参形式**：`string`
* **参数说明**：ctoken获取方法和上面一样**（注意：豌豆荚的ctoken每天都会换，需要及时更换）**

`need_app_num`：

* **传参形式**：`int`
* **参数说明**：需要获取的软件数量

 `save_path`:

* **传参形式**：`string`
* **参数说明**：将文件保存在电脑什么位置（路径）



#### 2.GetAppid输出
 豌豆荚中每一个软件都有自己唯一的appid ，GetAppid返回一个包含所有需要爬取的软件的appid列表。





### GetPage使用

#### 1.GetPage参数 

`real_data_ppids`:

* **传参形式**：`list`
* **参数说明**：将GetAppid返回的列表赋给这个参数即可 

`doc_name`:

* **传参形式**：`string`
* **参数说明**：doc_name 的名字务必和 GetAppid中的all_sort_params中的分类名称**务必一模一样**

`save_path`:

* **传参形式**：`string`
* **参数说明**：和GetAppid中的save_path**务必一模一样**



#### 2.GetPage输出

GetPage输出即为需要爬取的图片文件

