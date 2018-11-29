
/**
 * Created by gero on 2018/1/26.
 */
$(".vote_info_items_li").hover(function(){
    thisTop=$(this).offset().top+$(this).height()/2;
    $("#vote_info_function_select").css("display","block")
    $("#vote_info_function_select").animate({top:thisTop}, 500);
},function(){

});
$("#purchase_table_button").click(function(){
    $("#purchase_table_cover").show();
});
$("#purchase_table_close").click(function () {
    $("#purchase_table_cover").hide();
});