/**
 * Created by Administrator on 2017/9/23.
 */

$(document).ready(function (){
    getLoginUserInfo();
});
function getLoginUserInfo()
{
    var userId=$.cookie("userId");
    var param={"userId":userId};
    var apiUrl="/api/user/getUserInfo.do";
    getData(param,apiUrl,"post",function (data) {
            if(data.code==0){
                var userInfo=data.data
                var logo=userInfo.logo;
                var username=userInfo.username;
                $('#user_icon').attr("src",logo);
                $('#user_name').html(username);
            }
        }
    );
}

