import os
import re
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

    postList = []

    for i in range(len(mdFiles)):
        postList.append(Post('', '', '', ''))

    content = ''
    blogAbstractsMD = []

    for i in range(len(mdFiles)):
        postList[i].blogName = mdFiles[i][0:-3]

    for i in range(len(mdFiles)):
        postList[i].blogTime = mdFiles[i][0:8]

    for i in range(len(mdFiles)):
        content = ''
        with open('./blog/'+mdFiles[i], mode='r', encoding='utf8') as f:
            for j in range(10):
                content += f.readline()

            rawTitle = re.search(r'# .*\n',content).group()
            title = rawTitle[2:-1]
            postList[i].blogTitle = title

            rawAbstract = re.search(rawTitle+'[\s\S]{1,}',content).group()
            abstract = rawAbstract[len(rawTitle):]
            blogAbstractsMD.append(abstract)
    for i in range(len(blogAbstractsMD)): #将Abstract转化为html格式
        postList[i].blogAbstract = markdown.markdown(blogAbstractsMD[i])

    return postList

#写入html
def writeHTML(postList):
    #处理原始index.html
    with open('index.html', mode='r', encoding='utf8') as f:
        original = f.read()
        part1 = original.split('id="main-content">\n')[0] #main-content之前的内容
        part2 = original.split('            </div>\n        </div>\n        <aside')[1] #main-content之后的内容
    
    #构造新main-content
    tab = '    '#方便处理缩进
    space28 = '                            '#方便处理缩进
    newMainContent = ''
    for i in range(len(postList)): 
        blogLink = 'http://blog.mintsky.xyz/'+postList[i].blogName
        newMainContent += "                <div class='post'>\n                    <header class='post-header'>\n                        <h1 class='post-title'>\n                            <a href='{blogLink}' class='random-color'>\n                                {blogTitle}\n                            </a>\n                        </h1>\n                        <div class='post-meta'>\n                            <span class='post-time'>{blogYear}·{blogMonth}·{blogDay}</span>\n                        </div>\n                    </header>\n                    <div class='post-body markdown-body'>\n                        {blogAbstract}                    </div>\n                    <div class='post-button random-bg-color'>\n                        <a href='{blogLink}'>\n                            阅读全文\n                        </a>\n                    </div>\n                </div>\n".format(blogLink=blogLink, blogTitle=postList[i].blogTitle, blogYear=postList[i].blogTime[0:4], blogMonth=postList[i].blogTime[4:6], blogDay=postList[i].blogTime[6:8],blogAbstract=re.sub('\n','\n'+space28, postList[i].blogAbstract)) #space28:处理缩进

    #备份
    os.rename('index.html', 'index.html.old')
    #合成新html
    with open('index.html',mode='w',encoding='utf8') as f:
        f.write(part1)
        f.write('id="main-content">\n')
        f.write(newMainContent)
        f.write('            </div>\n        </div>\n        <aside')
        f.write(part2)

def writeRSS(postList): #TODORSS
    pass 

def main():
    postList = []
    postList = getInfo()
    writeHTML(postList)
    writeRSS(postList)


if __name__ == "__main__":
    main()