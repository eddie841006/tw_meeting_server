$(document).ready(function(){
    $(".video_list_inner tr").click(function(){
        $("#_video")[0].src="static\\video\\outputVideo5.mp4";
        setInterval(subtitle_method,500);
    });
    
    $(".word_check").change(function(data){
        if(this.checked == true){
            $(this).parent().parent().parent().find(".word_style").find("div").css("display","contents");
        }
        else{
            $(this).parent().parent().parent().find(".word_style").find("div").css("display","none");
        }        
    });
 
 function subtitle_method(){
    // 	$.getJSON("json/subtitles_with_ASR_speaker.json",function(data){
    // 	    $.each(data,function(key,val){
    // 		alert(key+":"+val);
    //      });
    //    });
            $.each(subtitle,function(key,val){
                var currentTime = $("#_video")[0].currentTime;
                if(key == 0){
                    $(".accuracy").text("");
                    $(".accuracy").append(function(){
                        var str = "語音辨識&nbsp;&nbsp;:&nbsp;&nbsp;"+val.speaker_accuracy+"<br>"+"語者辨識&nbsp;&nbsp;:&nbsp;&nbsp;"+val.speech_accuracy;
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