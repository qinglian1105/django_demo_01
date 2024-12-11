$(document).ready(function(){
    $('#uploadForm').submit(function(e){                
        e.preventDefault();
        const base_url = 'http://127.0.0.1:8888/';
        var url = base_url + 'object-to-bs64';
        var formData = new FormData();
        var file_data = $('#imageFile').prop('files')[0];
        formData.append("file", file_data)                                                
        console.log(formData);
        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(response){
                if (response !=0) { 
                    var note_str = '<h5 class="card-title" style="color:blue;">檢測結果：</h5>'
                    var img_str =  '<img src="data:image/jpeg;base64,' + response + '" width="100%";/>'                     
                    $("#imageContainer").html(note_str + img_str);
                }  else {
                    alert("failed (response = 0) ");
                }                        
            },
            error: function (response){
                alert("failed to upload...");
            }
        });
    });
});
