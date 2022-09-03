import requests
import re
from lxml import etree
import os
import time
# 伪造假请求头
from faker import Faker
faker = Faker('zh_CN')


class Create:
    def __init__(self , save_path):
        headers = {
            "user-agent" : str(faker.chrome())
            }
        '''
        save_path = 是保存文件的路径位置
        '''
        self.save_path = save_path
        self.headers = headers


    # 创建每一个大分类的文件夹的函数
    def create_sort_doc(self , name):#name是分类的名称
        doc_name = name
        try:
            os.mkdir(f'{self.save_path}/{doc_name}')
        except FileExistsError:
            print('该分类已存在')


    def create_app_doc(self,doc_name,app_name,page_targets):
        '''
        doc_name 保存文件夹的名字
        app_name 一款软件自己的名字,保存图片时,将为这个软件自己建一个文件夹
        page_targets 获取到的图片自身url的列表
        '''
    # 创建对应文件夹
        try:
            os.mkdir(f'{self.save_path}/{doc_name}/{app_name}')
        except FileExistsError:
            print('该文件夹已经存在')
        num = 1
        for page_target in page_targets:
            resp_app_page = requests.get(url = page_target , headers = self.headers).content
            with open(f'{self.save_path}/{doc_name}/{app_name}/{num}.jpg','wb')as file_obj:
                file_obj.write(resp_app_page)
                # 提示进度
            print(f'已获取{app_name}第{num}/{len(page_targets)}')
            num += 1
            time.sleep(0.8)


# 获取一个分类中的app的appid
class GetAppid:
    def __init__(self, all_sort_params, ctoken, need_app_num, save_path):
        headers = {
            "user-agent" : str(faker.chrome())
            }
        '''
        all_sort_params是 = {" " : [ , ]}形式,
            字典中第1个参数是分类的名字 
            第2个列表中第1个是豌豆荚ajax页面中的catId 第2个参数是ajax页面中的subCatId
        ctoken 是豌豆荚网页ajax页面中url中的令牌,每一天的ctoken都不一样
        need_app_num 是你需要爬取的软件数量
        save_path 是保存文件位置的路径
        '''
        self.headers = headers
        self.all_sort_params = all_sort_params
        self.ctoken = ctoken
        self.need_app_num = need_app_num
        self.create = Create(save_path=save_path)
        # 正则表达式,用来在豌豆荚ajax页面中筛选appid
        self.obj_1 = re.compile(r'data-appid=\\"(?P<app_id>.*?)\\"',re.S)

    def get_appid(self):
        for name , params in self.all_sort_params.items():
            # 依次从字典中提取，分类的名字，以及其url中的两个参数
            catId = params[0]
            subcatId = params[1]
            # 创建分类文件夹
            self.create.create_sort_doc(name = name)
            # 用来存储data_appid
            real_data_appids = []
            data_appids = []
            page_num = 1
            # 死循环直到存够两百个软件的data_appid为止
            while len(data_appids) <= self.need_app_num:
                # 记下上一轮的列表长度，如果上一轮和本轮列表长度相同，证明没有新的元素加入，用来防止全部的app数量加起来也不足200而陷入死循环
                last_app_num = len(data_appids)
                # 请求数据
                url = f"https://www.wandoujia.com/wdjweb/api/category/more?catId={catId}&subCatId={subcatId}&page={page_num}&ctoken={self.ctoken}"
                # 请求html文本
                resp_text = requests.get(url = url , headers = self.headers).text
                print(f'已经获取{name}的第{page_num}页html文本')
                # 筛选出软件的appid
                targets = self.obj_1.finditer(resp_text)
                for target in targets:
                    data_appids.append(target.group('app_id'))
                # 记录本轮的app数量
                now_app_num = len(data_appids)
                if last_app_num == now_app_num:
                    break
                # 翻页
                page_num += 1
                # 防止被封ip
                time.sleep(1)
            # 跳出循环，data_appids中的id数量一定>=200,截取出200个
            data_appids = data_appids[:self.need_app_num]
            real_data_appids = list(set(data_appids))
        return real_data_appids


class GetPage(GetAppid):
    def __init__(self, real_data_appids, doc_name , save_path):
        '''
        real_data_appids 是所有软件appid的一个列表
        doc_name 是分类的名称
        sace_path 直接继承父类的
        '''
        headers = {
            "user-agent" : str(faker.chrome())
            }
        self.create = Create(save_path=save_path)
        self.data_appids = real_data_appids
        self.doc_name = doc_name
        self.headers = headers

    def get_app_page(self):
        # 统计下载第__个软件
        num =1
        for data_appid in self.data_appids:
            print(f'第 {num}/{len(self.data_appids)} 个软件')
            history_url = f"https://www.wandoujia.com/apps/{data_appid}/history"
            app_history_text = requests.get(url = history_url, headers = self.headers).text

            # 分页html文本找到所有图标的url
            tree = etree.HTML(app_history_text)
            if str(tree.xpath('//body/@param-f')[0]) == 'appshistory':
                # 筛选一个软件的每一个版本的url
                page_targets = tree.xpath('//div[@class="all-version"]//li//img/@src')
                # 筛选每一款软件的名字
                app_name = str(tree.xpath('//body/@data-title')[0])
                # 创建文件夹
                self.create.create_app_doc(doc_name = self.doc_name, app_name = app_name, page_targets = page_targets)
            # 如果值等于404说明网页不存在
            elif int(tree.xpath('//body/@param-f')[0]) == 404:
                num += 1
                print(f'{data_appid}需要手动提取')
                continue
            num += 1
            time.sleep(1)


if __name__ == '__main__':
    get_app_1 = GetAppid(all_sort_params = {'金融理财' : [5023,0]}, ctoken = 'QYOVWfScAluGWfUufI22IC7-', need_app_num = 20, save_path = r'D:\vs code\vs  code file\test')
    app_ids = get_app_1.get_appid()

    get_page_1 = GetPage(real_data_appids = app_ids , doc_name='金融理财', save_path = r'D:\vs code\vs  code file\test' )
    page = get_page_1.get_app_page()








