/**
 * Created by Administrator on 2017/8/28.
 */
function setMedia()
{
    var screenWidth= document.body.clientWidth;
    var screenHeight= document.body.clientHeight;
    var fontSize =0;
    if(screenWidth>1020) {
        fontSize = (screenWidth / 1920) * 72;
    }else
    {
        fontSize = (screenHeight* window.devicePixelRatio / 1920) * 72;
    }
    fontSize=fontSize+"px";
    $('html').css("font-size",fontSize);
}

setMedia();

function showBody()
{
	$(".body").animate({
		opacity:1
	},500);
}

function cleanText(obj) {
    if(obj.value=="password"||obj.value=="email address"||obj.value=="input ip address or appName") {
        obj.value = "";
    }
}

