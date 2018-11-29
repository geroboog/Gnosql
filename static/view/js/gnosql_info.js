/**
 * Created by gero on 2018/3/9.
 */
gnosqlList=[];
gnosqlObj={};
function getGnosqlList()
{
    var apiUrl="/getGnosqlList";
    getData({},apiUrl,"post",true,function (data) {
        var thisHtml="";
        if(data.code==0){
            gnosqlList=data.data;
            for(var i=0;i<gnosqlList.length;i++)
            {
                thisHtml+="<li value=\""+i+"\" class=\"gnosql_info_items_li gnosql_info\"><div class=\"gnosql_info_items\"><div class=\"gnosql_info_items_content\">"
                            +"<div class=\"gnosql_info_items_content_title\">"+gnosqlList[i]["gnosqlName"]+"</div><div class=\"gnosql_info_items_content_detail\">"
                            +"<div class=\"gnosql_info_items_content_band\">tables&nbsp;"+gnosqlList[i]["tableNum"]+"</div>"
                            +"</div></div> </div> </li>"
            }
            $("#gnosql_info_content").html(thisHtml);
            $(".gnosql_info").click(function(){
                gnosqlObj=gnosqlList[$(this).val()];
                getGnosqlTableInfo();
                getGnosqlInfo();
                $(this).animate({opacity:0,width:2000,height:1000}, 500,function(){
                    $("#gnosql_info_content").css("margin-top","0px");
                    $(".gnosql_info").css("display","none");
                    $(".data_analysis").css("display","block");
                    getGnosqlDataAnalysis("","");
                    getGnosqlDataType("","");
                    init_select();
                    $(".data_analysis").css("width","0px");
                    $(".data_analysis").css("height","0px");
                    $(".data_analysis").animate({opacity:1,width:"80%",height:"96%"}, 2000,function(){

                    });
                });

            });
        }
    });
}

getGnosqlList();

function getGnosqlTableInfo()
{
    var apiUrl="/getGnosqlTableInfo";
    var param={"gnosqlId":gnosqlObj["gnosqlId"],"tableList":gnosqlObj["tableList"]}
    getData(param,apiUrl,"post",true,function (data) {
        var thisHtml="<thead><tr> <td width=\"24%\">tableName</td><td width=\"18%\">size</td><td width=\"33%\">createDate</td><td width=\"25%\">accessDate</td></tr></thead>";
        if(data.code==0){
            var rows=data.data;
            for(var i=0;i<rows.length;i++)
            {
                thisHtml+="<tr><td>"+rows[i]["tableName"]+"</td><td>"+rows[i]["size"]+"</td><td>"+rows[i]["createTime"]+"</td><td>"+rows[i]["accessTime"]+"</td></tr>"
            }
            $("#data_analysis_table").html(thisHtml);
        }
    });
}

function getGnosqlInfo()
{
    var apiUrl="/getGnosqlInfo";
    var param={"gnosqlId":gnosqlObj["gnosqlId"]}
    getData(param,apiUrl,"post",true,function (data) {
        var thisHtml="<thead><tr><td width=\"20%\">KeyName</td><td width=\"30%\">KeyValue</td><td width=\"30%\"></td></tr></thead>";
        if(data.code==0){
            var rows=data.data;
            for(thisKey in rows)
            {
                if(thisKey.indexOf("app")>-1)
                {
                    thisHtml+="<tr><td>"+thisKey+"</td><td>"+rows[thisKey]+"</td><td><div class='del_ip_button normal_button' onclick=\"delete_ip('"+rows[thisKey]+"')\">×</div></td></tr>"
                }else{
                    thisHtml+="<tr><td>"+thisKey+"</td><td>"+rows[thisKey]+"</td><td></td></tr>"
                }
            }
            $("#data_analysis_key_table").html(thisHtml);
        }
    });
}

function getGnosqlDataAnalysis(startDate,endDate)
{
    var apiUrl="/getGnosqlDataAnalysis";
    var param={"gnosqlId":gnosqlObj["gnosqlId"],"startDate":startDate,"endDate":endDate};
    getData(param,apiUrl,"post",true,function (data) {
        if(data.code==0){
            var rows=data.data;
            draw_line_charts(rows['dateArr'],rows['valueArr']);
        }
    });
}

function getGnosqlDataType(startDate,endDate)
{
    var apiUrl="/getGnosqlDataType";
    var param={"gnosqlId":gnosqlObj["gnosqlId"],"tableList":gnosqlObj["tableList"],"startDate":startDate,"endDate":endDate}
    getData(param,apiUrl,"post",true,function (data) {
        if(data.code==0){
            var rows=data.data;
            draw_pie(rows);
        }
    });
}
// $(".band_info").click(function(){
//     $(".band_info").animate({opacity:0,width:2000,height:1000}, 500,function(){
//         $(".band_info").css("display","none");
//         $(".store_info").css("display","block");
//         $(".store_info").animate({opacity:1, width:"6.08rem",height:"3.95rem"}, 500,function(){
//         });

//     });

// });

function submitIP() {
    var appIp = $("#app_id_input").val();
    if (appIp != "" && appIp!="input ip address or appName") {
        if (confirm("add an appIp or appName")) {
            var param = {}
            var apiUrl = ""
            if (appIp.indexOf("http") > -1) {
                param = {"gnosqlId": gnosqlObj["gnosqlId"], "appIp": appIp};
                apiUrl = "/addGnosqlAppIp"
            } else {
                param = {"gnosqlId": gnosqlObj["gnosqlId"], "appName": appIp};
                apiUrl = "/addGnosqlAppName"
            }
            getData(param, apiUrl, "post", true, function (data) {
                if (data.code == 0) {
                    getGnosqlInfo();
                }
            });
        }
    }
}

function delete_ip(appIp) {
    if (confirm("delete an appIp or appName")) {
        var param = {}
        var apiUrl = ""
        if (appIp.indexOf("http") > -1) {
            param = {"gnosqlId": gnosqlObj["gnosqlId"], "appIp": appIp};
            apiUrl = "/deleteGnosqlAppIp"
        } else {
            param = {"gnosqlId": gnosqlObj["gnosqlId"], "appName": appIp};
            apiUrl = "/deleteGnosqlAppName"
        }

        getData(param, apiUrl, "post", true, function (data) {
            if (data.code == 0) {
                getGnosqlInfo();
            }
        });
    }
}
function submitDate()
{
    var startDate=$("#startDate").html();
    var endDate=$("#endDate").html();
    var startDateValue=$("#startDate").val();
    var endDateValue=$("#endDate").val();
    if(startDateValue==null||endDateValue==null)
    {
        alert("please select startDate and endDate");
    }else {
        if(startDateValue<endDateValue)
        {
            getGnosqlDataAnalysis(startDate,endDate);
            getGnosqlDataType(startDate,endDate);
        }
        else {
            alert("endDate has to be bigger than startDate");
        }
    }
}


