// baseUrl="http://192.168.30.38:8000";
baseUrl="http://127.0.0.1:5000/gnosql";
gnosqlId="15209091325241521304107985";
token="15213493262711520909132524";
rows=null;

function getData(jsonPram,url,postType,fun){
    var url =baseUrl+ url;
    jsonPram["gnosqlId"]=gnosqlId;
    jsonPram["token"]=token;
    $.ajax({
        dataType : "json",
        type : postType,
        url :url,
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
function submit()
{
	var title=$("#title").val();
	var content=$("#content").val();
	var table="article";
	var jsonData={};
	var insertData=[];
	insertData[0]={"title":title,"content":content};
	jsonData['where']=table+"@"+ JSON.stringify(insertData);
	$("#label").val(JSON.stringify(jsonData));
	getData(jsonData,"/insert","POST",function(data)
			{
				alert("ok");
			});
}

function getArticleList()
{
    var table="article";
    var jsonData={};
    var insertData=[];
    insertData[0]={"@title":"%%"};
    jsonData['where']=table+"@"+ JSON.stringify(insertData);
    $("#label").val(JSON.stringify(jsonData));
    getData(jsonData,"/select","POST",function(data){
        var articleListObj=$("#ariticleList")
        var rows=data.data;
        var thisHtml="";
        for(var i=0;i<rows.length;i++)
        {
            thisHtml+="<li>"+rows[i]["title"]+"</li>"
        }
        articleListObj.html(thisHtml)
    });
}
getArticleList()

