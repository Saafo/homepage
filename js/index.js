function changeBackgroundColor() {
    var colorCollections = [
        // '#000000', //黑色
        '#444444', //灰色
        '#2e77ff', //深蓝
        '#31e4eb', //蓝绿
        '#b6d333', //青绿
        // '#38e032', //浅绿
        '#F6D656', //黄色
        '#F7695A', //浅红
        // '#f13636', //正红
        '#a981ef', //浅紫
    ];
    var randomColor = colorCollections[Math.floor(Math.random()*colorCollections.length)];

    randombgList = this.document.getElementsByClassName("random-bg-color");
    for(let i = 0, len = randombgList.length; i < len; i++) {
        randombgList[i].style.backgroundColor = randomColor;
    }
    randomList = this.document.getElementsByClassName("random-color");
    for(let i = 0, len = randomList.length; i < len; i++) {
        randomList[i].style.color = randomColor;
    }

}

$(document).ready(function() {
    changeBackgroundColor();
    navi = document.getElementsByClassName('sidebar-content')[0];
    naviTop = navi.offsetTop;
})

var naviTop = 0;
var navi = null;

window.onscroll = function(){
    if(window.innerWidth > 1080){
        var width = $('.sidebar-content').width(); //动态获取宽度
        
        var t = document.documentElement.scrollTop || document.body.scrollTop;
        if(t != 0 && t < naviTop){
            navi.setAttribute('style','position:absolute;top:'+ naviTop +'px;width:' + width + 'px;');
        }else 
        if(t == 0){
            navi.removeAttribute('style');
        }else{
            navi.setAttribute('style','position:fixed;top:10px;width:' + width + 'px;');
        }
    }
}