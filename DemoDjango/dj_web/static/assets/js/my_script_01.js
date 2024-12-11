
const base_url = 'http://backend-fastapi:5001';

// Call api: /api/default_info
axios.get(base_url + "/api/default_info")
    .then(function (response){              
            let obj = response.data; 
            console.log(obj.count, obj.loan_amnt);          
            mongo_pie(obj.count);}
         )                 

// Call api: /api/default_age
axios.get(base_url + "/api/default_age")
.then(function (response){              
        let obj = response.data; 
        console.log(obj.age, obj.count, obj.loan, obj.income)          
        mongo_bar(obj.age, obj.count, obj.loan, obj.income);}
     ) 


// Function for pie chart with mongodb
function mongo_pie(dicts){    
    // let colors = ['#99bbff','#ff9999'] 
    let total = dicts[0]['value'] + dicts[1]['value']  
    var chartDom = document.getElementById('container_01');
    var myChart = echarts.init(chartDom);
    var option;
    option = {
        title: {
            text: 'Counts',
            subtext: '',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        // color: colors,
        series: [
            {
                name: '人數',
                type: 'pie',
                radius: '50%',
                itemStyle: {
                    normal:{
                        color: function(colors){
                            var colorlist=['#ff9999','#99bbff'];
                            return colorlist[colors.dataIndex];
                        }
                    }
                },                
                tooltip: {
                    valueFormatter: function (value) {
                    return value + ' (' + (value/total).toFixed(2)*100 +"%)";
                    }
                },
                data: dicts,                
            }
        ]
    };
    option && myChart.setOption(option);
    window.addEventListener('resize', function() {
        myChart.resize();
      });
}    


// Function for bar chart with monogdb
function mongo_bar(age, count, loan, income){
    var dom = document.getElementById('container_02');
    var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
    });
    var app = {};

    var option;

    option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
        type: 'cross',
        crossStyle: {
            color: '#999'
        }
        }
    },
    legend: {
        data: ['Loan_amnt', 'Person_income', 'Count']
    },
    xAxis: [
        {
        type: 'category',
        // name: 'Age',
        data: age,
        axisPointer: {
            type: 'shadow'
        }
        }
    ],
    yAxis: [
        {
        type: 'value',
        name: 'Loan & Income\n(USD, 單位：百萬)',
        min: 0,
        max: 250,
        interval: 50,
        axisLabel: {
            formatter: '{value} '
        }
        },
        {
        type: 'value',
        name: 'Count (人數)',
        min: 0,
        max: 5000,
        interval: 1000,
        axisLabel: {
            formatter: '{value}'
        }
        }
    ],
    series: [
        {
        name: 'Loan_amnt',
        type: 'bar',
        tooltip: {
            valueFormatter: function (value) {
            return value + ' 百萬';
            }
        },
        data: loan            
        },
        {
        name: 'Person_income',
        type: 'bar',
        tooltip: {
            valueFormatter: function (value) {
            return value + ' 百萬';
            }
        },
        data: income                    
        },
        {
        name: 'Count',
        type: 'line',
        yAxisIndex: 1,
        tooltip: {
            valueFormatter: function (value) {
            return value + '人';
            }
        },
        data: count
        }
    ]
    };

    if (option && typeof option === 'object') {
    myChart.setOption(option);
    }

    window.addEventListener('resize', myChart.resize);

}