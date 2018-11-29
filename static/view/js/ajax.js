// urls="http://103.204.177.4:5000/gnosql";
urls="/gnosqlUser";
// baseUrl="http://192.168.30.38:8000";
baseUrl="";
function getData(jsonPram,url,postType,async,fun){
    var url =urls+ url;
    $.ajax({
        dataType : "json",
        type : postType,
        url :url,
        async: async,
        data : JSON.stringify(jsonPram),
        contentType: "application/json; charset=utf-8",
        success : function (data) {
            fun(data);
        },
        error : function (e) {
            console.log("数据异常[%s]",url);
        }
    });
}
