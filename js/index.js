window.onload = function changeBackgroundColor() {
    var colorCollections = [
        '#000000', //黑色
        '#333333', //灰色
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