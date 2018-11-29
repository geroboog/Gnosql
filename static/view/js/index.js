/**
 * Created by Administrator on 2017/9/23.
 */


function next()
{
    $('#index_username_border').css('display',"none");
    $('#index_username_button').css('display',"none");
    $('#index_password_border').css('display',"block");
    $('#index_password_button').css('display',"block");
    $('#index_label_content').empty();
    $('#index_label_content').append($('#username').val());
}
function nextKeyPress(){
    if (event.keyCode==13)  //回车键的键值为13
        next();
}
function login()
{
    var username=$('#username').val();
    var password=$('#password').val();
    var param={"username":username,"password":password};
    var apiUrl="/userLogin";
    getData(param,apiUrl,"post",false,function (data) {

            if(data.code==0){
                $.cookie("userId",data.data.userId);
                $.cookie("username",data.data.username);
                window.location.href='/gnosqlUser/main';
            }else if(data.code==1){
                $("#password").tips({
                    side:1,
                    msg:'密码错误',
                    color:'#FFF',
                    bg:'#005da6',
                    time:3,
                    x:0,
                    y:0
                });
            }else {
                $('#index_username_border').css('display',"block");
                $('#index_username_button').css('display',"block");
                $('#index_password_border').css('display',"none");
                $('#index_password_button').css('display',"none");
                $('#index_label_content').empty();
                $("#username").tips({
                    side:1,
                    msg:'账号不存在',
                    color:'#FFF',
                    bg:'#005da6',
                    time:3,
                    x:0,
                    y:0
                });
            }
        }
    );
}

function loginKeyPress(){
    if (event.keyCode==13)  //回车键的键值为13
        login();
}

$(".index_body").animate({
	opacity:1
},500);
