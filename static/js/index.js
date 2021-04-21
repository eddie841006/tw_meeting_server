$(document).ready(function(){
    // var masr_url="http://127.0.0.1:1111/"; 
    var masr_url="http://172.16.120.124:1111/";
    var subtitle_json={}; 
    var time;
    var flag = false;  
    var subtitle_json;
    load_video_list();    
    $(".video_list_inner").on('click','tr',function(data){
        $("#ncsist").text("語者身分：語音逐字稿");
        $("#google").text("語者身分：語音逐字稿");
        $("#answer").text("語者身分：語音逐字稿");
        $("#_video")[0].src="";        
        $("#_video")[0].src="static\\video\\"+$(this).find("td")[1].id+".mp4";        
        // $("#_video")[0].load();                
        var v = document.getElementsByTagName("video")[0];
        var name = $(this).find("td")[1].id;        
        Get_Subtitle(name);
        console.log(subtitle_json);
        clearInterval(time);        
        time = setInterval(subtitle_method,500,subtitle_json);
        // v.addEventListener("playing", function() 
        // { 
        //     if(flag == false){
        //         // Get_Subtitle(name);                
        //         time = setInterval(Get_Subtitle,500,name);
        //         flag = true;
        //         console.log(test);
        //     }   
        //     else{
        //         // Get_Subtitle(name);                
        //         clearInterval(time);
        //         time = setInterval(Get_Subtitle,500,name);
        //         console.log(test);
        //     }         
        // }, true);
        // var name = $(this).find("td")[1].id;
        // clearInterval(time);
        // setInterval(Get_Subtitle,500,name);
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
            async:false,
            url:masr_url+"video_json", 
            data:JSON.stringify(dataJSON),   
            contentType: "application/json; charset=utf-8",         
            dataType:'json', 
            success:function(data){ 
                // $.each(data,function(key,val){
                //     var currentTime = $("#_video")[0].currentTime;
                //     if(key == 0){
                //         // console.log("%%");
                //         $(".accuracy").text("");
                //         $(".accuracy").append(function(){
                //             var str = "語音辨識&nbsp;&nbsp;:&nbsp;&nbsp;"+val.speech_accuracy+"%"+"<br>"+"語者辨識&nbsp;&nbsp;:&nbsp;&nbsp;"+val.speaker_accuracy+"%";
                //             return str;
                //         });
                //     }
                //     else{
                //         // console.log("subtitle");
                //         if(currentTime >= val.start_time && currentTime <= val.end_time && val.MASR_results != "null"){
                //             $("#ncsist").text(val.MASR_results);
                //             $("#google").text(val.google_asr_results);
                //             $("#answer").text(val.labels);
                //         }
                //     }
                // });
                // clearInterval(time);
                // time = setInterval(Get_Subtitle,500,video_name);
                // console.log(data);
                subtitle_json={};
                subtitle_json = data;
                // console.log(subtitle_json);
                return data;
            },
            error:function(data){
                // console.log(data);
            },
            complete: function(xhr, textStatus) {
                // console.log(xhr.status);
            }, 
            statusCode: {
                206: function() {
                //   console.log("No");
                }, 
                200: function() {
                    // console.log("ok");
                  }
              }
        });                        
    }

    function subtitle_method(data){        
        $.each(data,function(key,val){
            var currentTime = $("#_video")[0].currentTime;
            if(key == 0){
                $(".accuracy").text("");
                $(".accuracy").append(function(){
                    var str = "NCSIST語音辨識&nbsp;:&nbsp;"+val.speech_accuracy+"%&nbsp;"+
                    "<br>NCSIST語者辨識&nbsp;:&nbsp"+val.speaker_accuracy+"%&nbsp;";
                    return str;
                });
                $(".accuracy_").text("");
                $(".accuracy_").append(function(){
                    var str = "Google語音辨識&nbsp;:&nbsp;"+val.google_speech_accuracy+"%&nbsp;";
                    return str;
                });
            }
            else{
                if(currentTime >= val.start_time && currentTime <= val.end_time && val.MASR_results != "null"){
                    $("#ncsist").text(val.MASR_results);
                    $("#google").text(val.google_asr_results);
                    $("#answer").text(val.labels);
                }
            }
        });                  
    }
});
