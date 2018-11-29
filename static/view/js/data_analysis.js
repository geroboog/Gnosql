/**
 * Created by gero on 2018/3/4.
 */

function genData(count) {
    var legendData = ['赵', '钱', '孙', '李'];
    var seriesData = [{name: '赵', value: 10}, {name: '钱', value: 20}, {name: '孙', value: 30}, {name: '李', value: 40}];
    var selected = {'赵': true,'钱': true,'孙': false,'李': false};

    return {
        legendData: legendData,
        seriesData: seriesData,
        selected: selected
    };
}


function onSelectGraphy()
{
	var selectedGraphy=document.getElementById(this.value);
	if(selectedGraphy!=null)
		{
			document.getElementById("data_analysis_content").scrollTop=selectedGraphy.offset().top;
		}
}


function draw_line_charts(date,dataIn)
{
// 访问折线图
//     var base = +new Date(2010, 1, 3);
//     var oneDay = 24 * 3600 * 1000;
//     var date = [];
//     var dataIn = [1];
//     for (var i = 1; i < 20; i++) {
//         var now = new Date(base += oneDay);
//         date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('-'));
//         var d1=Math.abs(Math.round((Math.random() - 0.5) * 20 + dataIn[i - 1]));
//         dataIn.push(d1);
//     }
    var data_line = echarts.init(document.getElementById('data_line'));
    var colors = ['#B2CFEB'];

    option1 = {
        color: colors,
        tooltip: {
            trigger: 'none',
            axisPointer: {
                type: 'cross'
            }
        },
        title: {
            left: '10%',
            text: 'USER ACCESS CHART',
            textStyle: {
                fontWeight: 'Bold',              //标题颜色
                color: '#E9E9E9'
            }
        },
        tooltip: {
            trigger: 'axis'
        },
        grid: {
            top: '15%'
        },
        xAxis:
            {
                type: 'category',
                data: date
            },
        yAxis: [
            {
                type: 'value'
            }
        ],
        dataZoom: [{
            type: 'inside',
            start: 0,
            end: 100
        }, {
            start: 0,
            end: 100,
            height:20,
            bottom:0,
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '60%',
            handleStyle: {
                color: '#fff',
                shadowBlur: 3,
                shadowColor: 'rgba(0, 0, 0, 0.6)',
                shadowOffsetX: 2,
                shadowOffsetY: 2
            }
        }],
        series: [
            {
                name:'访问',
                type:'line',
                smooth: true,
                data: dataIn
            }
        ]
    };
    data_line.setOption(option1);
}
function draw_pie(rows)
{
    var data=rows
    var data_pie_in = echarts.init(document.getElementById('data_pie_in'));
    pie_in = {
        title: {
            left: '10%',
            text: 'ACCESS TYPE PIE',
            textStyle: {
                fontWeight: 'Bold',              //标题颜色
                color: '#E9E9E9'
            }
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20,
            data: data.legendData,

            selected: data.selected
        },
        series : [
            {
                name: '姓名',
                type: 'pie',
                radius : '55%',
                center: ['40%', '50%'],
                data: data.seriesData,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    data_pie_in.setOption(pie_in);
}


function init_select()
{
    $('.chosen-select').chosen({allow_single_deselect:true});
    $(window)
        .off('resize.chosen')
        .on('resize.chosen', function() {
            $('.chosen-select').each(function() {
                var $this = $(this);
                $this.next().css({'width': $this.parent().width()});
            });
        }).trigger('resize.chosen');
    $(document).on('settings.ace.chosen', function(e, event_name, event_val) {
        if(event_name != 'sidebar_collapsed') return;
        $('.chosen-select').each(function() {
            var $this = $(this);
            $this.next().css({'width': $this.parent().width()});
        });
    });
    $('#chosen-multiple-style .btn').on('click', function(e){
        var target = $(this).find('input[type=radio]');
        var which = parseInt(target.val());
        if(which == 2) $('#form-field-select-4').addClass('tag-input-style');
        else $('#form-field-select-4').removeClass('tag-input-style');
    });

    $("#graphys").change(function(){
        var selectedGraphy=$("#"+this.value);
        if(selectedGraphy!=null)
        {
            $("#data_analysis").animate({scrollTop:selectedGraphy.offset().top}, 500);
        }
    });
}

function drawGraphys() {
    getGnosqlAllDataAnalysis("","");
}
function getGnosqlAllDataAnalysis(startDate,endDate)
{
    var apiUrl="/getGnosqlAllDataAnalysis";
    var param={"startDate":startDate,"endDate":endDate};
    getData(param,apiUrl,"post",true,function (data) {
        if(data.code==0){
            var rows=data.data;
            draw_line_charts(rows['dateArr'],rows['valueArr']);
        }
    });
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
            getGnosqlAllDataAnalysis(startDate,endDate);
            getGnosqlAllDataType(startDate,endDate);
        }
        else {
            alert("endDate has to be bigger than startDate");
        }
    }
}



