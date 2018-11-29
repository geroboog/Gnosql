/**
 * Created by gero on 2018/3/11.
 */
function getMyBlogs()
{
    $("#myBlogs").removeClass("icon_close");
    $("#myBlogs").addClass("icon_open");
    $("#myFollows").removeClass("icon_open");
    $("#myFollows").addClass("icon_close");
    $("#blog_follow_content_area").css("display","none");
    $("#blog_content_area").css("opacity","0");
    $("#blog_content_area").css("display","block");
    $("#blog_content_area").animate({opacity:1}, 500,function(){	
    });
}

function getMyFollows()
{
    $("#myBlogs").removeClass("icon_open");
    $("#myBlogs").addClass("icon_close");
    $("#myFollows").removeClass("icon_close");
    $("#myFollows").addClass("icon_open");
    $("#blog_content_area").css("display","none");
    $("#blog_follow_content_area").css("display","block"); 
    $("#blog_follow_content_area").css("opacity","0");
    $("#blog_follow_content_area").css("display","block");
    $("#blog_follow_content_area").animate({opacity:1}, 500,function(){	
    });
}

$(".blog_follows_ul").hover(function(){
    $(this).animate({backgroundColor: "rgb(180,180,180)"}, 500);
},function(){
    $(this).animate({backgroundColor: "rgb(164,164,164)"}, 500);
});