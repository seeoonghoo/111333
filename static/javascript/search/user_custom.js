// 이미지 썸네일
var img = '';

function setThumbnail(event) { 
    var reader = new FileReader();

    reader.onload = function(event) { 

        var div = document.getElementById('image_container');
        while(div.firstChild){
            div.removeChild(div.firstChild);
        }

        img = document.createElement("img"); 
        img.setAttribute("src", event.target.result); 
        // $(img).css('width','100%');
        img.width=div.clientWidth;
        img.height=div.clientHeight;

        document.querySelector("div#image_container").appendChild(img); 
    }; 
    reader.readAsDataURL(event.target.files[0]); 
} 

var extract_list = [];
var current_unit = '';
var dosage = [];

$( document ).ready( function() {

    // 함량 오류 있어서 일단 이렇게 처리
    $.ajax({
                    url:'/extract_unit_return?extract_name=비타민A',
                    type:'get',
                    dataType:'json',
                    success:function(response){

                        current_unit = JSON.stringify(response.unit['regular_unit']).replace(/"/gi, "");
                        
                    },
                    error : function(xhr, error){
                        alert("서버와의 통신에서 문제가 발생했습니다.");
                        console.error("error : " + error);
                    }
    })

    // 사이트맵 셀렉
    $('ul.tabs_map li').click(function(){
        var tab_id = $(this).attr('data-tab_map');

        $('ul.tabs_map li').removeClass('current');
        $('.tab-content_map').removeClass('current');

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');
    });


    // 사이트맵
    $(".header_menu_html").hide();
            
    $(".header_menu_box").click(function() {
        $(".header_menu_html").slideDown(300);
        $(".header_menu_box").hide();
    });

    $(".header_menu_box_back").click(function() {
        $(".header_menu_html").slideUp(300);
        $(".header_menu_box").show();
    });

    $('.header_back_box').click(function(){
        window.history.back();
    })

    // 성분 클릭시 박스 생기기
    $('#select_extract_big div').click(function(){

        $.ajax({
                    url:'/extract_unit_return?extract_name='+$(this).text(),
                    type:'get',
                    dataType:'json',
                    success:function(response){
                        current_unit = JSON.stringify(response.unit['regular_unit']).replace(/"/gi, "");   
                    },
                    error : function(xhr, error){
                        alert("서버와의 통신에서 문제가 발생했습니다.");
                        console.error("error : " + error);
                    }
        })

        if ($(this).hasClass('current') == true){
            $(this).removeClass('current');

            extract_list.splice(extract_list.indexOf($(this).text()), 1)
            $('#option_' + $(this).text().replace(' ','').replace('(','').replace(')','')).remove();
        }
        else{
            $(this).addClass('current');

            extract_list.push($(this).text());
            

            var append_query = '<div class = "option_range_box" id = "option_' + $(this).text().replace(' ','').replace('(','').replace(')','') + '">\
                                    <div class = "option_range_box_title">'+
                                        $(this).text() +
                                    '</div>\
                                    <input type="number" name="dododo" id = "dosage_' + $(this).text() + '" placeholder="함량 최소치" class = "for_dosage_input"> \
                                    <div class="unit_select">' +
                                        current_unit +
                                    '</div>\
                                </div>';
            
            $('#extract_big_box').append(append_query);
        }
    });

        // 성분 값 가져오기
        if (extract_list != null){
            
            for (var i = 0; i < extract_list.length ; i++){
                if(document.getElementById('dosage_'+ extract_list[i]).value == ""){
                    dosage.push(0);
                }
                else{
                    dosage.push(document.getElementById('dosage_'+ extract_list[i]).value);
                }
            }
        }

});

function concate(){

    var name = document.getElementById('name').value;
    var brand = document.getElementById('brand').value;
    var number = document.getElementById('number').value;
    var per_day = document.getElementById('per_day').value;
    var date = document.getElementById('date').value;
    var image = document.getElementsByName('bull');

        if (img == ''){
            $('.name_box').show();
            return false;
        }
        else{
            $('.name_box').hide();
        }
        if (name == ""){
            $('#name_alert').show();
            return false;
        }
        else{
            $('#name_alert').hide();
        }
        if (brand == ""){
            $('#brand_alert').show();
            return false;
        }
        else{
            $('#brand_alert').hide();
        }
        if (number == ""){
            $('#number_alert').show();
            return false;
        }
        else{
            $('#number_alert').hide();
        }
        if (per_day == ""){
            $('#per_day_alert').show();
            return false;
        }
        else{
            $('#per_day_alert').hide();
        }
        if (date == null){
            $('#day_alert').show();
            return false;
        }
        else{
            $('#day_alert').hide();
        }

        if (extract_list != null){
            
            for (var i = 0; i < extract_list.length ; i++){
                if(document.getElementById('dosage_'+ extract_list[i]).value == ""){
                    dosage.push(0);
                }
                else{
                    dosage.push(document.getElementById('dosage_'+ extract_list[i]).value);
                }
            }
        }

        document.getElementById('extract').value = extract_list;
        document.getElementById('dosage').value = dosage;
}