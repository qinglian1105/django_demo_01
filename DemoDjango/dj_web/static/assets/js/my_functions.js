// Dashboard - select years to update all data 
function update_all(input)
{
    if (input==1){
        yyyy='2018';
    } else if (input==2){
        yyyy='2017';
    } else if (input==3){
        yyyy='2016';
    } else if (input==4){
        yyyy='2015';    
    } else {
        yyyy='2014';
    }          
    const base_url = 'http://backend-fastapi:5001';      
    var post_data = JSON.stringify({yyyy: yyyy});
    
    // Four indexes
    const m_path_list = ["/api/loan_amt","/api/loan_count","/api/default_amt","/api/default_count"];
    const m_id_list = ["m01","m02","m03","m04"];    
    let i = 0;
    while (i < m_path_list.length)
    {
        let api_path = m_path_list[i];
        let find_id = m_id_list[i];
        api_url = base_url + api_path;
        axios({
            method: 'post',
            url: api_url,
            headers: {'Content-Type': 'application/json'},                      
            data: post_data 
        }).then(function (response){        
            let obj = response.data;
            let v = Object.values(obj);                        
            document.getElementById(find_id).textContent = v[0].toLocaleString();        
        })         
        i++;   
    }        

    // Two charts
    axios({
        method: 'post',
        url: base_url + "/api/month_loan",
        headers: {'Content-Type': 'application/json'},                      
        data: post_data 
    }).then(function (response){                
            let obj_l = response.data;           
            var chart_l = document.getElementById("left_chart");
            chart_l.removeChild(chart_l.children[0]);             
            document.getElementById("left_chart").innerHTML = '<canvas id="m_loan_amt"></canvas>'                              
            left_chart(obj_l.mm, obj_l.amt);           
    })    
    axios({
        method: 'post',
        url: base_url + "/api/month_count",
        headers: {'Content-Type': 'application/json'},                      
        data: post_data 
    }).then(function (response){                
            let obj_r = response.data;           
            var chart_r = document.getElementById("right_chart");
            chart_r.removeChild(chart_r.children[0]);             
            document.getElementById("right_chart").innerHTML = '<canvas id="m_loan_count"></canvas>'                              
            right_chart(obj_r.mm, obj_r.count);           
    })       
    
    // Two tables
    axios({
        method: 'post',
        url: base_url + "/api/purpose",
        headers: {'Content-Type': 'application/json'},                      
        data: post_data 
    }).then(function (response){                
            let html_str_l = response.data.tb;
            var div_table_l = document.getElementById("left_tb");
            div_table_l.removeChild(div_table_l.children[0]);
            document.getElementById("left_tb").innerHTML = html_str_l;
    })     
    axios({
        method: 'post',
        url: base_url + "/api/occupation",
        headers: {'Content-Type': 'application/json'},                      
        data: post_data 
    }).then(function (response){                 
            let html_str_r = response.data.tb;
            var div_table_r = document.getElementById("right_tb");
            div_table_r.removeChild(div_table_r.children[0]);
            document.getElementById("right_tb").innerHTML = html_str_r;
    })                        
}


// Dashboard - left chart
function left_chart(y, x)
{   
    var saleschart = document.getElementById("m_loan_amt");
    var myChart_01 = new Chart(saleschart, {
    type: 'bar',
    data: {
        labels: y,
        datasets: [{
                label: 'Income',
                data: x,
                backgroundColor: "rgba(76, 175, 80, 0.5)",
                borderColor: "#6da252",
                borderWidth: 1,
        }]
    },
    options: {
        animation: {
            duration: 2000,
            easing: 'easeOutQuart',
        },
        plugins: {
            legend: {
                display: false,
                position: 'top',
            },
            title: {
                display: true,
                text: 'Number of Sales',
                position: 'left',
            },
        },
    }
    });
}        


// Dashboard - right chart
function right_chart(y, x)
{   
    var trafficchart = document.getElementById("m_loan_count");        
    var myChart_02 = new Chart(trafficchart, {
    type: 'line',
    data: {
        labels: y,
        datasets: [{
            data: x,
            backgroundColor: "rgba(48, 164, 255, 0.2)",
            borderColor: "rgba(48, 164, 255, 0.8)",
            fill: true,
            borderWidth: 1
        }]
    },
    options: {
        animation: {
            duration: 2000,
            easing: 'easeOutQuart',
        },
        plugins: {
            legend: {
                display: false,
                position: 'right',
            },
            title: {
                display: true,
                text: 'Number of Visitors',
                position: 'left',
            },
        },
    }
    });
}

