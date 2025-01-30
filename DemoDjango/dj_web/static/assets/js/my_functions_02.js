// Scorecard - clean input and output
function scorecard_clean()
{        
    document.getElementById("annual_inc_bin").value="";
    document.getElementById("loan_amnt_bin").value="";
    document.getElementById("int_rate_bin").value="";  
    document.querySelector("#purpose").value="";
    document.querySelector("#grade").value="";
    document.querySelector("#home_ownership").value="";
    document.querySelector("#pub_rec_bankruptcies").value="";
    document.getElementById("scorecard_outputs").innerHTML="";  
    var dom = document.getElementById("chart_container");
    var myChart = echarts.init(dom);
    myChart.clear();     
}

// Scorecard - submit form data to API
function scorecard_predict()
{       
    let v0 = document.getElementById("annual_inc_bin").value;
    let v1 = document.getElementById("loan_amnt_bin").value;
    let v2 = document.getElementById("int_rate_bin").value;    
    let v3 = document.querySelector('#purpose option:checked').value;  
    let v4 = document.querySelector('#grade option:checked').value;              
    let v5 = document.querySelector('#home_ownership option:checked').value;              
    let v6 = document.querySelector('#pub_rec_bankruptcies option:checked').value;                          

    let post_data = JSON.stringify({annual_inc_bin: parseInt(v0), 
                                    loan_amnt_bin: parseInt(v1), 
                                    int_rate_bin: parseFloat(v2), 
                                    purpose: v3, 
                                    grade: v4,
                                    home_ownership: v5,
                                    pub_rec_bankruptcies: v6,});    
    console.log("post: \n"+post_data);
    
    const base_url = 'http://backend-fastapi:5001';                 
    axios({
        method: 'post',
        url: base_url + "/api/ml/scorecard_predict",
        headers: {'Content-Type': 'application/json'},                      
        data: post_data 
    }).then(function (response){              
        let obj = response.data; 
        console.log("obj \n"+obj.score.toString()+"\n"+obj.rating);          
        let outputs = JSON.stringify({score: parseInt(obj.score), 
                                      level: obj.rating});                                      
        document.getElementById("scorecard_outputs").innerHTML=outputs;          
        guage_chart(obj.score, obj.rating);           
    })                                        
}

// Scorecard - guage chart
function guage_chart(score, rating){
    var dom = document.getElementById('chart_container');
    var myChart = echarts.init(dom, null, {
        renderer: 'canvas',
        useDirtyRect: false
    });

    var app = {};    
    var option;
        option = {
            series: [
                {
                type: 'gauge',
                startAngle: 180,
                endAngle: 0,
                center: ['50%', '75%'],
                radius: '90%',
                min: 0,
                max: 1,
                splitNumber: 10,
                axisLine: {
                    lineStyle: {
                    width: 16,
                    color: [
                        [0.25, '#ff0000'],
                        [0.3, '#ff66ff'],
                        [0.4, '#cc00ff'],
                        [0.5, '#6600cc'],
                        [0.6, '#80aaff'],
                        [0.7, '#6666ff'],
                        [1, '#0000e6']
                    ]
                    }
                },
                pointer: {
                    icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                    length: '10%',
                    width: 16,
                    offsetCenter: [0, '-60%'],
                    itemStyle: {
                    color: 'black' //'auto'
                    }
                },
                axisTick: {
                    length: 12,
                    lineStyle: {
                    color: 'auto',
                    width: 2
                    }
                },
                splitLine: {
                    length: 20,
                    lineStyle: {
                    color: 'auto',
                    width: 5
                    }
                },
                axisLabel: {
                    color: '#464646',
                    fontSize: 16,
                    distance: -85,
                    rotate: 'radial',
                    formatter: function (value) {
                    if (value == 0.9) {
                        return 'Excellent';                                   
                    } else if (value == 0.7) {
                        return 'Exceptional'; 
                    } else if (value == 0.6) {
                        return 'Very Good';        
                    } else if (value == 0.5) {
                        return 'Good';  
                    } else if (value == 0.4) {
                        return 'Fair';        
                    } else if (value == 0.3) {
                        return 'Poor';                                         
                    } else if (value == 0.1) {
                        return 'Very Poor';
                    }
                    return '';
                    }
                },
                title: {
                    offsetCenter: [0, '-10%'],
                    fontSize: 20
                },
                detail: {
                    fontSize: 16,
                    offsetCenter: [0, '-35%'],
                    valueAnimation: true,
                    formatter: function (value) {
                    return Math.round(value * 1000) + ' (' + rating + ')';
                    },
                    color: 'inherit'
                },
                data: [
                    {
                    value: score/1000,       
                    name: 'Credit Score',                
                    }
                ]
                }
            ]
        };

    if (option && typeof option === 'object') {
        myChart.setOption(option);
    };

    window.addEventListener('resize', myChart.resize);
    
}