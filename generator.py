import os
import re
import time
import markdown

class Post:
    def __init__(self, blogName, blogTime, blogTitle, blogAbstract):
        self.blogName = blogName
        self.blogTime = blogTime
        self.blogTitle = blogTitle
        self.blogAbstract = blogAbstract


#读取信息
def getInfo():
    allFiles = os.listdir('blog/')
    mdFiles = []
    for i in allFiles:
        if '.md' in i:
            mdFiles.append(i)
    mdFiles.sort()
    mdFiles.reverse()

    blogList = []

    for i in range(len(mdFiles)):
        blogList.append(Post('', '', '', ''))

    content = ''
    blogAbstractsMD = []

    for i in range(len(mdFiles)):
        blogList[i].blogName = mdFiles[i][0:-3]

    for i in range(len(mdFiles)):
        blogList[i].blogTime = mdFiles[i][0:8]

    for i in range(len(mdFiles)):
        content = ''
        with open('./blog/'+mdFiles[i], mode='r', encoding='utf8') as f:
            for j in range(10):
                content += f.readline()

            rawTitle = re.search(r'# .*\n',content).group()
            title = rawTitle[2:-1]
            blogList[i].blogTitle = title

            rawAbstract = re.search(rawTitle+'[\s\S]{1,}',content).group()
            abstract = rawAbstract[len(rawTitle):]
            blogAbstractsMD.append(abstract)
    for i in range(len(blogAbstractsMD)): #将Abstract转化为html格式
        blogList[i].blogAbstract = markdown.markdown(blogAbstractsMD[i])

    return blogList

#写入html
def writeHTML(blogList):
    if(os.path.exists('index.html') == False):
        print('不存在原始index.html文件，生成失败')
        return
    #处理原始index.html
    with open('index.html', mode='r', encoding='utf8') as f:
        original = f.read()
        part1 = original.split('id="main-content">\n')[0] #main-content之前的内容
        part2 = original.split('            </div>\n        </div>\n        <aside')[1] #main-content之后的内容
    
    #构造新main-content
    tab = '    '#方便处理缩进
    space28 = '                            '#方便处理缩进
    newMainContent = ''
    for i in range(len(blogList)): 
        blogLink = 'http://blog.mintsky.xyz/'+blogList[i].blogName
        newMainContent += "                <div class='post'>\n                    <header class='post-header'>\n                        <h1 class='post-title'>\n                            <a href='{blogLink}' class='random-color'>\n                                {blogTitle}\n                            </a>\n                        </h1>\n                        <div class='post-meta'>\n                            <span class='post-time'>{blogYear}·{blogMonth}·{blogDay}</span>\n                        </div>\n                    </header>\n                    <div class='post-body markdown-body'>\n                        {blogAbstract}                    </div>\n                    <div class='post-button random-bg-color'>\n                        <a href='{blogLink}'>\n                            阅读全文\n                        </a>\n                    </div>\n                </div>\n".format(blogLink=blogLink, blogTitle=blogList[i].blogTitle, blogYear=blogList[i].blogTime[0:4], blogMonth=blogList[i].blogTime[4:6], blogDay=blogList[i].blogTime[6:8],blogAbstract=re.sub('\n','\n'+space28, blogList[i].blogAbstract)) #space28:处理缩进

    #备份
    os.rename('index.html', 'index.html.old')
    #合成新html
    with open('index.html',mode='w',encoding='utf8') as f:
        f.write(part1)
        f.write('id="main-content">\n')
        f.write(newMainContent)
        f.write('            </div>\n        </div>\n        <aside')
        f.write(part2)

def timeFormat(blogTime):
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT',time.strptime(blogTime,'%Y%m%d'))

def writeRSS(blogList):
    part1 = "<?xml version='1.0' encoding='utf-8'?>\n<rss version='2.0'>\n    <channel>\n        <title>Mintsky's Blog</title>\n        <link>http://mintsky.xyz/rss.xml</link>\n        <description>Posts' Abstracts on Mintsky's Blog</description>\n        <lastBuildDate>{buildTime}</lastBuildDate>\n        <language>zh-CN</language>\n        <generator>https://github.com/saafo/homepage/blob/master/generator.py</generator>\n        <copyright>Copyright 2020 Mintsky All Rights Reserved</copyright>\n\n".format(buildTime=timeFormat(blogList[0].blogTime))
    part2 = "\n    </channel>\n</rss>"

    #构造新main-content
    space16 = "                "
    newMainContent = ''
    for i in range(len(blogList)):
        blogLink = 'http://blog.mintsky.xyz/'+blogList[i].blogName
        newMainContent += "        <item>\n            <title>{blogTitle}</title>\n            <link>{blogLink}</link>\n            <guid>{blogLink}</guid>\n            <pubDate>{blogTime}</pubDate>\n            <description>\n                <![CDATA[{blogAbstract}]]>\n            </description>\n        </item>\n".format(blogLink=blogLink, blogTitle=blogList[i].blogTitle, blogTime=timeFormat(blogList[i].blogTime),blogAbstract=re.sub('\n','\n'+space16, blogList[i].blogAbstract + "\n<p>阅读更多...</p>\n"))
    
    #备份
    if(os.path.exists('rss.xml')):
        os.rename('rss.xml', 'rss.xml.old')
    #合成新html
    with open('rss.xml',mode='w',encoding='utf8') as f:
        f.write(part1)
        f.write(newMainContent)
        f.write(part2)


def main():
    blogList = []
    blogList = getInfo()
    writeHTML(blogList)
    writeRSS(blogList)


if __name__ == "__main__":
    main()