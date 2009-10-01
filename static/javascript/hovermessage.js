var sep_x = 0;    // メッセージのマウス位置からのX方向離れ（右方向＋）
var sep_y = 20;   // メッセージのマウス位置からのY方向離れ（下方向＋）
var message = new Array();

// ポップアップメニューのメッセージ
// ファイルの文字コードをeucにしてもメッセージが字化けしたので、英語で。。。
message[0] = "I'll recommend this !!"

var disp_flg = 0;
var ms = 0;
var ms2= 0;
var x = -300;
var y = -100;
var ie4 = (navigator.appVersion.indexOf('MSIE 4')>=0);
var op6 = (navigator.userAgent.indexOf('Opera 6')>=0)||(navigator.userAgent.indexOf('Opera/6')>=0);

// メッセージデーターの先読み
for (i=0;i<message.length;i++){
    document.write("<div id='span"+i+"' class='spanstyle'");
    if(ie4){document.write(" style='width:10;'><table><tr><td nowrap");}
    document.write(">");
	document.write(message[i]);
    if(ie4){document.write("</td></tr></table>");}
    document.write("</div>");
}

// マウス座標位置取得
function handlerMM(e){
    x = (document.all) ? document.body.scrollLeft+event.clientX : (op6)?event.clientX : e.pageX;
    y = (document.all) ? document.body.scrollTop+event.clientY : (op6)?event.clientY : e.pageY;
    flg=1;
    if(disp_flg ==1){ disp_mess(ms2);}else{del_mess(ms2);}
}

// フローティングメッセージの表示
function disp_mess(ms){
   disp_flg = 1;
   if (flg==1 && document.all){
       var thisspan = document.all("span"+ms).style;
       thisspan.posLeft=x+sep_x;
       thisspan.posTop =y+sep_y;
       thisspan.visibility="visible"
   }
   if (flg==1 && document.layers){
       var thisspan = eval("document.span"+ms);
       thisspan.left=x+sep_x;
       thisspan.top=y+sep_y;
       thisspan.visibility="visible"
   }
   if (flg==1 && !document.all && document.getElementById){
       var thisspan = document.getElementById("span"+ms);
       thisspan.style.left=x+sep_x;
       thisspan.style.top =y+sep_y;
       thisspan.style.visibility="visible"
   }
   ms2=ms;
}

// フローティングメッセージの非表示
function del_mess(ms){
    disp_flg = 0;
   if (document.all){
       var thisspan = document.all("span"+ms).style;
       thisspan.visibility="hidden";
   }
   if (document.layers){
       var thisspan = eval("document.span"+ms);
       thisspan.visibility="hidden";
   }
   if (!document.all && document.getElementById){
       var thisspan = document.getElementById("span"+ms).style;
       thisspan.visibility="hidden";
   }
   ms2=ms;
}

function NN_reload(){
      if (document.layers) location.reload();// ネスケリロード（リサイズ時）
}

// マウスイベント設定
if (document.layers){
    document.captureEvents(Event.MOUSEMOVE);
}
if (!document.all && document.getElementById && !op6){
    window.onmousemove = handlerMM;
    window.captureEvents(Event.MOUSEMOVE);
}else{
    document.onmousemove = handlerMM;
}
window.onresize = NN_reload;
