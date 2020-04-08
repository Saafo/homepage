function getContent(){
    $.get("blog/ali.md", function(result){
        hljs.initHighlightingOnLoad();
        marked.setOptions({
            highlight: function (code) {
                return hljs.highlightAuto(code).value;
            }
        });
        $("#main-content").html(marked(result));
    });
}

function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

$(document).ready(function() {
    // changeBackgroundColor();
    getContent();
})

$(window).on('load',function() {
    document.getElementById("markdown-toc").innerHTML="";
    new Toc('main-content',{
        'level': 2,
        'top': 460,
        'class': 'toc',
        'targetId': 'markdown-toc'
    });

    var title = document.getElementsByTagName("h1")[1].textContent;
    document.title = title + " - Mintsky's Blog"
})