window.onload = function changeBackgroundColor() {
    var colorCollections = [
        '#000000', //黑色
        '#333333', //灰色
        '#2e77ff', //深蓝
        '#31e4eb', //蓝绿
        '#b6d333', //青绿
        '#38e032', //浅绿
        '#F6D656', //黄色
        '#F7695A', //浅红
        '#f13636', //正红
        '#a981ef', //浅紫
    ];
    var randomColor = colorCollections[Math.floor(Math.random()*colorCollections.length)];
    this.document.getElementsByTagName('nav')[0].style.backgroundColor = randomColor;
    this.document.getElementsByClassName('title-container')[0].style.backgroundColor = randomColor;
    this.document.getElementsByTagName("h1")[0].style.color = randomColor;
}