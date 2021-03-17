$(document).ready(function(){
    var masr_url="http://172.16.120.124:1111/"; 
    var subtitle_json={}; 
    var time;
    var flag = false;  
    load_video_list();    
    $(".video_list_inner").on('click','tr',function(data){
        $("#ncsist").text("語者身分：語音逐字稿");
        $("#google").text("語者身分：語音逐字稿");
        $("#answer").text("語者身分：語音逐字稿");
        Get_Subtitle($(this).find("td")[1].id);
        $("#_video")[0].src="static\\video\\"+$(this).find("td")[1].id+".mp4";        
        var v = document.getElementsByTagName("video")[0];
        v.addEventListener("playing", function() 
        { 
            if(flag == false){
                time = setInterval(subtitle_method,500,subtitle_json);
                flag = true;
            }   
            else{
                clearInterval(time);
                time = setInterval(subtitle_method,500,subtitle_json);
            }         
        }, true);
    });
    
    $(".word_check").change(function(data){
        if(this.checked == true){
            $(this).parent().parent().parent().find(".word_style").find("div").css("display","contents");
        }
        else{
            $(this).parent().parent().parent().find(".word_style").find("div").css("display","none");
        }        
    });
 
    function load_video_list(){
        $.ajax({ 
            type:'POST',  
            url:masr_url+"video_list", 
            data:"",   
            contentType: "application/json; charset=utf-8",         
            dataType:'json', 
            success:function(data){ 
                $.each(data,function(key,val){                    
                    // $("#list_body").text("");
                    $("#list_body").append(function(){
                        var str = "<tr>"+
                        "<td><img src=\"static\\img\\video.png\" style=\"width:inherit\" /></td>"+
                        "<td id=\""+val.video_name.split(".")[0]+"\" style=\"width:40%\">"+val.name+"<br>"+val.video_time+"</td>"+     
		                "</tr>";
                        return str;
                    });
                });    
            } 
        });
    }

    function Get_Subtitle(video_name){
        var dataJSON = {};
        dataJSON["video_name"] = video_name;               
        $.ajax({ 
            type:'POST',  
            url:masr_url+"video_json", 
            async : false,
            data:JSON.stringify(dataJSON),   
            contentType: "application/json; charset=utf-8",         
            dataType:'json', 
            success:function(data){ 
                subtitle_json = data;
            } 
        });                        
    }

    function subtitle_method(data){        
        $.each(data,function(key,val){
            var currentTime = $("#_video")[0].currentTime;
            if(key == 0){
                $(".accuracy").text("");
                $(".accuracy").append(function(){
                    var str = "語音辨識&nbsp;&nbsp;:&nbsp;&nbsp;"+val.ASR_wer+"%"+"<br>"+"語者辨識&nbsp;&nbsp;:&nbsp;&nbsp;"+val.speaker_wer+"%";
                    return str;
                });
            }
            else{
                if(currentTime >= val.start_time && currentTime <= val.end_time && val.MASR_results != "null"){
                    $("#ncsist").text(val.speaker+"："+val.MASR_results);
                    $("#google").text(val.speaker+"："+val.google_asr_results);
                    $("#answer").text(val.speaker+"："+val.labels);
                }
            }
        });                  
    }
});