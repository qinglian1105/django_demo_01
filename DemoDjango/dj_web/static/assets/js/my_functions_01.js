// ML - submit form data to API
function ml_predict()
{   
    let v0 = document.querySelector('[name=ml_select]:checked').value;    
    let v1 = document.getElementById("f_islongloan").value;
    let v2 = document.getElementById("f_loan_amnt").value;
    let v3 = document.getElementById("f_int_rate").value;
    let v4 = document.getElementById("f_annual_inc").value;    
    
    let post_data = JSON.stringify({model_name: v0, islongloan: parseInt(v1), 
                                    loan_amnt: parseFloat(v2), int_rate: parseFloat(v3), 
                                    annual_inc: parseFloat(v4)});    
    console.log("post: \n"+post_data);

    const base_url = 'http://backend-fastapi:5001';              
    axios({
        method: 'post',
        url: base_url + "/api/ml_predict",
        headers: {'Content-Type': 'application/json'},                      
        data: post_data 
    }).then(function (response){              
        let obj = response.data; 
        console.log("obj \n"+obj.res);  
        let show_res = "預測結果： " + obj.res.toString();                                   
        document.getElementById("ml_predict_result").textContent = show_res;        
    })                           
}

// ML - clean input and output
function ml_clean()
{      
   document.querySelector('[name=ml_select]:checked').checked=false;  
   document.getElementById("f_islongloan").value = "";
   document.getElementById("f_loan_amnt").value = ""; 
   document.getElementById("f_int_rate").value = "";
   document.getElementById("f_annual_inc").value = "";
   document.getElementById("ml_predict_result").textContent = ""; 
}
