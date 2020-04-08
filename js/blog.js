var status;
function getContent(){
    try {
        var url = window.location.pathname.split('/')[1];
        blogYear = url.slice(0,4);
        blogMonth = url.slice(4,6);
        blogDate = url.slice(6,8);
        $.get("blog/"+url+".md", function(result){
            if(result) {
                hljs.initHighlightingOnLoad();
                marked.setOptions({
                    highlight: function (code) {
                        return hljs.highlightAuto(code).value;
                    }
                });
                var blogTime = blogYear+' · '+blogMonth+' · '+blogDate+'\n\n';
                var license = "\n\n---\n> 版权声明：本文为[@Saafo](https://github.com/Saafo)的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。\n> \n> 原文链接："+window.location.href;
                $("#main-content").html(marked(blogTime+result+license));
            }
        });
    } catch (TypeError) {
        return 1; //url格式问题，报错
    }
}

function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

function checkExist() {
    try {
        document.getElementsByTagName("h1")[1].textContent;        
    } catch (TypeError) {
        return 1; //没有获取到文章，报错
    }
    return 0;
}

$(document).ready(function() {
    status = getContent();
})

$(window).on('load',async function() {
    await sleep(100);
    status = await checkExist();
    if(status == 0) {
        document.getElementById("markdown-toc").innerHTML=""; //删掉原来的内容
        var top = document.getElementsByClassName('blog-sidebar-content')[0].offsetTop;
        new Toc('main-content',{
            'level': 2,
            'top': top,
            'class': 'toc',
            'targetId': 'markdown-toc'
        });
    
        var title = document.getElementsByTagName("h1")[1].textContent;
        document.title = title + " - Mintsky's Blog"
    }else{
        document.title = "你来到了一片荒芜之地 - Mintsky's Blog"
    }
})

(function(window) {
    window.onscroll = function(){
        var t = document.documentElement.scrollTop || document.body.scrollTop;
        var lis = document.getElementById('markdown-toc').getElementsByTagName('li');
        var lisPositions = new Array();
        for(let i = 0; i < lis.length; i++) {
            lisPositions[i] = lis[i].offsetTop;
        }
        for(let i = 0; i < lisPositions.length - 1; i++) {
            if(t > lisPositions[i] && t < lisPositions[i + 1]) {
                for(let i = 0; i < lis.length; i++) {
                    lis[i].getElementsByTagName('a')[0].style.color='#000000';
                }
                lis[i].getElementsByTagName('a')[0].style.color='red';
            }
        }

    }
})(window);