
/**
 * Created by gero on 2018/1/26.
 */
$(".gnosql_info_items_li").hover(function(){

    $("#hover_audio")[0].play();
    //$(this).animate({backgroundColor: "rgb(190,190,190)"}, 500);
},function(){
    $("#hover_audio")[0].pause();
    //$(this).animate({backgroundColor: "rgb(150,150,150)"}, 500);
});