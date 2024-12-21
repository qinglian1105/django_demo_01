# **django_demo_01**


## **Django - 簡單網站展示**

### **目錄** 

* [Ⅰ. 目的](#1)
* [Ⅱ. 使用相關框架或套件](#2)
* [Ⅲ. 簡介](#3)
* [Ⅳ. 網頁展示](#4)
* [Ⅴ. References](#5)

<br>

---

<h4 id="1">Ⅰ. 目的</h4>
以Django框架實作簡單網站，瞭解目前掌握技術知識點，並配合過去所學結合機器學習及數據分析之應用。
<br><br>

<h4 id="2">Ⅱ. 使用相關框架或套件</h4>
前端：Django、JavaScript、Boostrap、Chart.js、ECharts<br>
後端：FastAPI、PostgreSQL、MongoDB<br>
其他：Scikit-learn、YOLOv5
<br><br>

<h4 id="3">Ⅲ. 簡介</h4>

1.架構<br>
(1)前端使用Django web framework及JavaScript處理網頁，樣式套用Boostrap-simple-admin，圖表庫為Chart.js、ECharts。<br>
(2)後端則以FastAPI建立API操作資料庫PostgreSQL及MongoDB、處理資料及模型推論運算，供前端調用渲染網頁。<br>
(3)最後，由Docker Compose佈署前端、後端、資料庫及相關服務。<br>

2.資料<br>
網頁內容所使用之資料來自Kaggle，分別為Lending Club Loan Data及Credit Risk Dataset。<br>
(1)Lending Club Loan Data資料集<br>
匯入PostgreSQL，作簡易的探索性分析(Exploratory Data Analysis, EDA)，並且分別建立機器學習模型作違約預測、信用評分卡(Credit Scorecards)模型作評分預測。<br>
(2)Credit Risk Dataset<br>
該資料集則匯入MongoDB，僅作簡單違約分析，主要為ECharts展示。<br>

3.網頁內容<br>
於帳密登入後，頁面為左方導覽列(side navigation menu)，右方呈現內容。左側七個選單功能說明如下：<br>
[選單一]即為「首頁」，內容為簡介說明。<br>
[選單二]是「資料視覺化分析」，下拉式選單切換年度更新各圖表數據。<br>
[選單三]為「機器學習」作違約預測分析，於後端部署模型預測API前以供前端調用，於Form選擇模型並輸入各項數據送出後，將於在下方返回預測結果。<br>
[選單四]是「信用評分預測」，即 Credit Scorecards，送出輸入資料，調用模型API計算，於下方返回預測結果(分數、評級)。<br>
[選單五]為「物件檢測」，檢測物件為食物，可將圖片檔上傳給後端YOLOv5封裝之API處理，於下方返回檢測圖片。<br>
[選單六]是「違約分析」，調用API取MongoDB資料，再使用 ECharts 呈現違約狀況圖表。<br>
[選單七]僅為測試 - 404網頁。<br><br>

<h4 id="4">Ⅳ. 網頁展示</h4>

1.登入、登出及Django自帶後台管理<br>

依序如下所示：<br>

![avatar](./README_png/page_login.png)
![avatar](./README_png/page_logout.png)
![avatar](./README_png/page_admin.png)
<br><br>

2.選單一 - 首頁<br>

如前述，首頁作介簡說明，頁面為左方導覽列，右方呈現內容。樣式套用Bootsrap-simple-admin ([詳見](<https://github.com/pro-dev-ph/bootstrap-simple-admin-template>))作簡化。

![avatar](./README_png/page_home.png) 
<br><br>

3.選單二 - 資料視覺化分析(儀表板)<br>

有4個指標(Metrics)、1個長條圖(Bar chart)、1個折線圖(Line chart)及2個統計表格。<br>
下拉式選單可切換分析「年度」，調用API從資料庫擷取數據處理後渲染網頁，此處圖表以Chart.js繪製。

![avatar](./README_png/page_dashboard.png)
<br><br>

4.選單三 - 機器學習<br>

可點選演算法及填寫變數資料送出Form，調用模型API運算，預測結果(藍色文字)返回網頁。<br>
(1: 可能會違約, 0: 可能不會違約)

![avatar](./README_png/page_ml.png)
<br><br>

5.選單四 - 信用評分預測(Credit Scorecards)<br>

於Form填寫變數資料送出，調用模型API作運算，預測結果(分數、評級)於下方以藍色文字及儀表盤呈現。<br>
此處Credit Scorecards之模型訓練及推論為另一專案 (credit_scorecards_demo_01  [詳見](<https://github.com/qinglian1105/credit_scorecards_demo_01/tree/main>) )。

![avatar](./README_png/page_scorecard.png)
<br><br>

6.選單五 - 物件檢測<br>

可於Form點選圖片檔上傳，調用YOLOv5模型API作推論，檢測結果返回網頁。<br>此處目的僅是YOLO模型推論佈署之練習，引用之模型及內容 ([詳見](<https://medium.com/@auliyafirdaus03/step-by-step-deploy-yolov5-ultralytics-machine-learning-model-with-fastapi-ef6faacea4ee>))。另外，圖中食物截圖([詳見](<https://www.facebook.com/ohshotaiwan/posts/%E6%BC%A2%E7%A5%9E%E6%88%90%E5%8A%9F%E5%BA%97%E9%99%90%E5%AE%9A%E6%96%99%E7%90%86-%E5%A4%A7%E5%AE%B6%E4%BE%86%E9%A4%83%E5%AD%90%E3%81%AE%E7%8E%8B%E5%B0%87%E9%83%BD%E9%BB%9E%E4%BB%80%E9%BA%BC%E6%96%99%E7%90%86%E5%91%A2%E5%A6%82%E6%9E%9C%E6%AF%AB%E7%84%A1%E9%A0%AD%E7%B7%92%E7%9A%84%E8%A9%B1%E5%B0%8F%E7%B7%A8%E8%B6%85%E6%8E%A8%E8%96%A6%E6%96%B0%E6%89%8B%E5%85%A5%E9%96%80%E6%AC%BE%E7%8E%8B%E5%B0%87%E6%8B%89%E9%BA%B5%E5%A5%97%E9%A4%90%E7%8E%8B%E5%B0%87%E4%BA%BA%E6%B0%A3%E6%96%99%E7%90%86%E4%B8%80%E6%AC%A1%E6%94%B6%E9%9B%86%E7%8E%8B%E5%B0%87%E7%85%8E%E9%A4%83%E7%8E%8B%E5%B0%87%E7%82%92%E9%A3%AF%E7%8E%8B%E5%B0%87%E9%86%AC%E6%B2%B9%E8%B1%9A%E9%AA%A8%E6%8B%89%E9%BA%B5%E7%86%B1%E9%96%80%E8%8F%9C%E5%96%AE%E4%B8%80/380404612371913/>))。

![avatar](./README_png/page_yolov5.png)
<br><br>

7.選單六 - 違約分析<br>

調用API取MongoDB資料，再由 ECharts 渲染網頁，以呈現違約狀況圖表：<br>
圓餅圖(Pie chart) - 違約佔比。<br>
長條折線混合圖(Mixed Line and Bar) - 違約分佈(貸款金額、個人收入、人數 by 年齡)。<br>



![avatar](./README_png/page_default.png)
<br><br>

8.API接口<br>

FastAPI建立不同功能的API接口，資料來自二個資料庫PostgreSQL及MongoDB，如："/api/default_info取得違約及非違約人數及金額，其他接口詳見程式碼(專案資料夾 DemoFastApi)。

![avatar](./README_png/page_api.png)

<br>

---

<h4 id="5">Ⅴ. References</h4>

[1] [Getting started with Django](<https://www.djangoproject.com/start/>)

[2] [pro-dev-ph/bootstrap-simple-admin-template](<https://github.com/pro-dev-ph/bootstrap-simple-admin-template>)

[3] [Chart.js](<https://www.chartjs.org/>)

[4] [Apache ECharts](<https://echarts.apache.org/zh/index.html>)

[5] [Lending Club Loan Data](<https://www.kaggle.com/datasets/adarshsng/lending-club-loan-data-csv/data>)

[6] [Credit Risk Dataset](<https://www.kaggle.com/datasets/laotse/credit-risk-dataset/data>)

[7] [Logistic Regression in Building Credit Scorecard](<https://medium.com/@rachmanto.rian/logistic-regression-in-building-credit-scorecard-924bece9f953>)

[8] [Step-by-Step: Deploy YOLOv5 Ultralytics Machine Learning Model with FastAPI](<https://medium.com/@auliyafirdaus03/step-by-step-deploy-yolov5-ultralytics-machine-learning-model-with-fastapi-ef6faacea4ee>)

[9] [餃子の王將—台灣的貼文](<https://www.facebook.com/ohshotaiwan/posts/%E6%BC%A2%E7%A5%9E%E6%88%90%E5%8A%9F%E5%BA%97%E9%99%90%E5%AE%9A%E6%96%99%E7%90%86-%E5%A4%A7%E5%AE%B6%E4%BE%86%E9%A4%83%E5%AD%90%E3%81%AE%E7%8E%8B%E5%B0%87%E9%83%BD%E9%BB%9E%E4%BB%80%E9%BA%BC%E6%96%99%E7%90%86%E5%91%A2%E5%A6%82%E6%9E%9C%E6%AF%AB%E7%84%A1%E9%A0%AD%E7%B7%92%E7%9A%84%E8%A9%B1%E5%B0%8F%E7%B7%A8%E8%B6%85%E6%8E%A8%E8%96%A6%E6%96%B0%E6%89%8B%E5%85%A5%E9%96%80%E6%AC%BE%E7%8E%8B%E5%B0%87%E6%8B%89%E9%BA%B5%E5%A5%97%E9%A4%90%E7%8E%8B%E5%B0%87%E4%BA%BA%E6%B0%A3%E6%96%99%E7%90%86%E4%B8%80%E6%AC%A1%E6%94%B6%E9%9B%86%E7%8E%8B%E5%B0%87%E7%85%8E%E9%A4%83%E7%8E%8B%E5%B0%87%E7%82%92%E9%A3%AF%E7%8E%8B%E5%B0%87%E9%86%AC%E6%B2%B9%E8%B1%9A%E9%AA%A8%E6%8B%89%E9%BA%B5%E7%86%B1%E9%96%80%E8%8F%9C%E5%96%AE%E4%B8%80/380404612371913/>)
