#爬取51job网的数据，并将其中选定的类目下的数据写入excel表中
'''
引入相关库
'''
from bs4 import BeautifulSoup
import requests
import  time
import xlwt


#自动化爬取多页码数据，可设置要抓取的页面的页码
def get_more_pages(start,end):
    newTable = "51job.xls"
    wb = xlwt.Workbook(encoding='utf-8')  # 创建excel文件
    ws = wb.add_sheet('sheet1',cell_overwrite_ok=True)  # 创建表的名称,如果对一个单元格重复操作，会引发,所以在打开时加cell_overwrite_ok=True 解决
    headDate = ['职位', '公司', '地址', '工资', '发布时间']  # 表头数据
    for tableHead in range(0, 5):
        ws.write(0, tableHead, headDate[tableHead], xlwt.easyxf('font: bold on'))  # 写入表头
    rows= 1

#对页码的自动化调整
    for ones in range(start,end+1):
        global one
        one = str(ones)
        global url
        url = 'https://search.51job.com/list/030200,000000,0107,01,9,99,%2520,1,{}.html?'.format(one)
        #调整抓取速率
        time.sleep(5)

        wb_data = requests.get(url)  # 请求网页
        wb_data.encoding = 'gbk'  # 51job的编码
        soup = BeautifulSoup(wb_data.text, 'lxml')  # 解析网页
        positions = soup.select('#resultList > div > p > span > a')
        companies = soup.select('#resultList > div > span.t2 > a')
        locations = soup.select('#resultList > div.el > span.t3')[1:]  # 因为同标签下还有标题的文本影响
        salaries = soup.select('#resultList > div > span.t4')[1:]
        dates = soup.select('#resultList > div > span.t5')[1:]

        # 格式化输出
        for position, company, location, salary, date in zip(positions, companies, locations, salaries, dates):
            data = [
                # '职位' :
                position.get_text(strip=True),
                # '公司' :
                company.get_text(),
                # '地址' :
                location.get_text(),
                # '工资' :
                salary.get_text(),
                # '发布时间' :
                date.get_text()
            ]
            print(data)

#将数据写入excel表
            for i in range(0,5):
                ws.write(rows,i,data[i])
            rows+=1
    wb.save(newTable)                               #保存表格




#调用函数，如爬取第1~10页的数据
get_more_pages(1,10)

