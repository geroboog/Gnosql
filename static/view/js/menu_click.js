/**
 * Created by gero on 2018/1/24.
 */
$('.main_menu_item').click(function(){
    console.log($(this).attr('id'));
    var label=$(this).find('.main_menu_item_label');
    var icon=$(this).find('.main_menu_item_icon');
    $('.click_li').removeClass("click_li");
    $('.icon_open').addClass("icon_close");
    $('.icon_open').removeClass("icon_open");
    $(this).parent().addClass('click_li');
    var labelText=label.text();
    icon.removeClass("icon_close");
    icon.addClass("icon_open");

    switch(labelText) {
        // case "数据库管理":
        //     showTab("main_iframe_right","main_iframe","/gnosqlUser/gnosql_info");
        //     break;
        // case "数据统计":
        //     showTab("main_iframe_right","main_iframe","/gnosqlUser/data_analysis");
        //     break;
        // case "接入文档":
        //     showTab("main_iframe","main_iframe_right","https://www.showdoc.cc/web/#/23914755783764");
        //     break;
        // case "关于我们":
        //     showTab("main_iframe_right","main_iframe","/gnosqlUser/about_us");
        //     break;

        case "Management":
            showTab("main_iframe_right","main_iframe","/gnosqlUser/gnosql_info");
            break;
        case "Data Analysis":
            showTab("main_iframe_right","main_iframe","/gnosqlUser/data_analysis");
            break;
        case "Api Document":
            showTab("main_iframe","main_iframe_right","https://www.showdoc.cc/web/#/23914755783764");
            break;
        case "About Us":
            showTab("main_iframe_right","main_iframe","/gnosqlUser/about_us");
            break;

        default:
            showTab("main_iframe_right","main_iframe","/gnosqlUser/gnosql_info");
            break;
    }
})

function showTab(reClass,addClass,urlAddress)
{           
    var iframe=$('#main_iframe');
    iframe.removeClass(reClass);
    iframe.addClass(addClass);
    iframe.attr("src",urlAddress);
}