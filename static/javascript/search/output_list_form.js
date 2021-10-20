// 아래로 불러오기 하기 위한 변수 (10개씩 불러오기)
var txt_current_count = 10;

$( document ).ready( function() {

    // 엔터 입력시 검색
    $("#text").keyup(function(event){
        if(event.keyCode == 13){
            $(".search_image").click();
        }
    });

    // 함량단위 처음 불러올 때 오류 발생 -> 일단 이렇게 처리
    // 한번 불러와서 오류 없애기 
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

    
    // 클릭하면 넘어가는 함수
    // &, + 두개가 오류를 야기시킴. 그래서 검색어에서 그 것들을 대체
    // 전체 대체하면 &가 씹혀서 GET방식으로 못넘어감
    $(document).on("click","div.small_box",function(){
        var this_name = $(this).attr(('for_change'));
        location.href='/output_text?name=' + this_name.replace(/&/g,"%26").replace(/\+/g,"%2B");
    })


    // 상세검색
    $(".option_search_box").hide();
    $(".option_delete").hide();
    
    $(".after_change").click(function() {
        $(".option_search_box").slideDown(3);
        $(".after_change").hide();
        $(".option_delete").show();
    });

    $(".option_delete").click(function() {
        $(".option_search_box").slideUp(3);
        $(".after_change").show();
        $(".option_delete").hide();
    });

    // 브랜드 옵션
    $('#select_brand_big div').click(function(){
        if ($(this).hasClass('current') == true){
            $('#select_brand_big div').removeClass('current');
        }
        else{
            $('#select_brand_big div').removeClass('current');
            $(this).addClass('current');
        }
    });

    // 효능 옵션
    $('#select_effects_big div').click(function(){
        if ($(this).hasClass('current') == true){
            $('#select_effects_big div').removeClass('current');
        }
        else{
            $('#select_effects_big div').removeClass('current');
            $(this).addClass('current');
        }
    });

    $('#select_brand_big').hide();
    $('#select_extract_big').hide();
    $('#select_effects_big').hide();

    // 펼치기 숨기기 
    $('#effects_title').click(function(){
        if ($('#select_effects_big').is(':visible')){
            $('#select_effects_big').hide();
        }
        else{
            $('#select_effects_big').show();
        }
    });
    $('#extract_title').click(function(){
        if ($('#select_extract_big').is(':visible')){
            $('#select_extract_big').hide();
            $('.option_range_box').hide();
        }
        else{
            $('#select_extract_big').show();
            $('.option_range_box').show();
        }
    });
    $('#brand_title').click(function(){
        if ($('#select_brand_big').is(':visible')){
            $('#select_brand_big').hide();
        }
        else{
            $('#select_brand_big').show();
        }
    });



    // 성분 옵션

    var extract_list = [];
    var current_unit = '';
    var min = [];
    var max = [];
    

    // 성분 입력 할 때 단위 가져와주기
    $('#select_extract_big div').click(function(){
        var current_unit = '';

        if ($(this).hasClass('current') == true){
            $(this).removeClass('current');

            extract_list.splice(extract_list.indexOf($(this).text()), 1)
            $('#option_' + $(this).text().replace(' ','').replace('(','').replace(')','')).remove();
        }
        else{
            $(this).addClass('current');
            extract_list.push($(this).text());
            var tmp = $(this).text();

            $.ajax({
                    url:'/extract_unit_return?extract_name='+tmp,
                    type:'get',
                    dataType:'json',
                    success:function(response){
                        // alert('asdfas');
                        current_unit = JSON.stringify(response.unit['regular_unit']).replace(/"/gi, "");

                        var append_query = '<div class = "option_range_box" id = "option_' + tmp.replace(' ','').replace('(','').replace(')','') + '">\
                                    <div class = "option_range_box_title">'+
                                        tmp +
                                    '</div>\
                                    <input type="number" name="number" id = "min_' + tmp + '" placeholder="함량 최소치"> ~\
                                    <input type="number" name="number" id = "max_' + tmp + '" placeholder="함량 최대치">\
                                    <div class="unit_select">' +
                                        current_unit +
                                    '</div>\
                                </div>';
            
                        $('#extract_big_box').append(append_query);
                    },
                    error : function(xhr, error){
                        alert("서버와의 통신에서 문제가 발생했습니다.");
                        console.error("error : " + error);
                    }
            })

            
            
        }
    });

    $(document).on("click",".search_image",function(){


        // 한글자 이상 확인
        var search =  document.getElementById('text').value;
        if(search == "" & document.getElementsByClassName('select_brand_option_list current')[0] == null & 
        document.getElementsByClassName('select_effects_option_list current')[0] == null & extract_list == null) {
            alert("한글자 이상 입력해주세요");
            return false;
        }

        if(search == ""){
            search = '.';
        }

        // 브랜드 값 가져오기
        if (document.getElementsByClassName('select_brand_option_list current')[0] == null){
            var brand = '.';
        }
        else{
            var brand = document.getElementsByClassName('select_brand_option_list current')[0].innerHTML;
        }

        // 효능 값 가져오기
        if (document.getElementsByClassName('select_effects_option_list current')[0] == null){
            var effects = '.';
        }
        else{
            var effects = document.getElementsByClassName('select_effects_option_list current')[0].innerHTML;
        }

        // 성분 값 가져오기
        if (extract_list != null){
            
            for (var i = 0; i < extract_list.length ; i++){

                if(document.getElementById('min_'+ extract_list[i]).value == ""){
                    min.push(0);
                }
                else{
                    min.push(document.getElementById('min_'+ extract_list[i]).value);
                }


                if(document.getElementById('max_'+ extract_list[i]).value == ""){
                    max.push(99999999);
                }
                else{
                    max.push(document.getElementById('max_'+ extract_list[i]).value);
                }

            }

            
        }
        
        location.href='/output_list_form?name=' + search.replace(/&/g,"%26").replace(/\+/g,"%2B") + '&brand=' + brand.replace(/&/g,"%26").replace(/\+/g,"%2B") + '&effects=' + effects + '&extract=' + extract_list + '&min=' + min + '&max=' + max;
        }) 

        // 아래로 계속 불러오기용 URL과 파라미터 변수 설정
        // 현재 URL에서 값들을 가져온다
        const url = new URL(window.location.href);
        down_name = url.searchParams.get('name');
        down_brand = url.searchParams.get('brand');
        down_effects = url.searchParams.get('effects');
        down_extract = url.searchParams.get('extract');
        down_min = url.searchParams.get('min');
        down_max = url.searchParams.get('max');
    
    $( window ).scroll( function() {
        
        if((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {

            var plus_name = document.getElementById("plus").innerHTML;
            var txt_limit_conut = document.getElementById('text_count').innerHTML;
                
            if (txt_current_count > txt_limit_conut){
                return false;
            }


            $.ajax({
                url:'/txt_plus_list?name=' + down_name + '&num='+txt_current_count+ '&brand=' + down_brand + '&effects=' + down_effects + '&extract=' + down_extract + '&min=' + down_min + '&max=' + down_max,
                type:'get',
                dataType:'json',
                success:function(response){

                    for (var cnt = 0 ; cnt < response.txt_result.length ; cnt++){

                        tmp = '<div class = "small_box" for_change = ' + JSON.stringify(response.txt_result[cnt]['name']) + '>\
                                <div class = "image_box">\
                                    <img src=' + JSON.stringify(response.txt_result[cnt]['image']) + " >\
                                </div>\
                                <div class = "+"text_box"+'>\
                                    <span id = "name_brand" style="font-size: 85%; font-weight: bold;">'+JSON.stringify(response.txt_result[cnt]['brand']).replace(/"/gi, "") +'</span><br>\
                                    <span id = "name_name" style="font-size: 95%; font-weight:bolder;" >'+JSON.stringify(response.txt_result[cnt]['name']).replace(/"/gi, "")+'</span><br>\
                                    <span id = "name_name" style="font-size:75%; color: #b0b0b0;">'+JSON.stringify(response.txt_result[cnt]['keyword']).replace(/"/gi, "")+'</span><br>\
                                </div>\
                            </div>';
                        $('.title_box').append(tmp);
                                    
                    }
                    txt_current_count += 10;
                        
                },
                error : function(xhr, error){
                    alert("서버와의 통신에서 문제가 발생했습니다.");
                    console.error("error : " + error);
                }
            })
            
        } 
    });
});