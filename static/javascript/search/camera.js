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

    $( document ).ready( function() {

        // 엔터 클릭시 검색
        $("#text").keyup(function(event){
            if(event.keyCode == 13){
                $(".search_image").click();
            }
        });

        

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

        // 검색별로 보여주기
        $('ul.tabs li').click(function(){
            var tab_id = $(this).attr('data-tab');

            $('ul.tabs li').removeClass('current');
            $('.tab-content').removeClass('current');

            $(this).addClass('current');
            $("#"+tab_id).addClass('current');

        });

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


        // 검색 할 떄 카메라 화면 숨기고 나타내기
        $('.for_text_search').hide();
        $('.header_text_hide').hide()

        $('.input_box').click(function(){
            $('.for_text_search').show();
            $('.header_text_hide').show();
            $('.header_back_box').hide();
            $('#coldbrew').hide();
        })

        $('.header_text_hide').click(function(){
            $('.for_text_search').hide();
            $('.header_text_hide').hide();
            $('.header_back_box').show();
            $('#coldbrew').show();
        })



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

        // 성분 옵션

        var extract_list = [];
        
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
        // 검색하기 누를 때
        $(document).on("click",".search_image",function(){

            // 한글자 이상 확인
            var search =  document.getElementById('text').value;
            if(search == "" & document.getElementsByClassName('select_brand_option_list current')[0] == null & 
            document.getElementsByClassName('select_effects_option_list current')[0] == null & extract_list == '') {
                // alert(extract_list);
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

        // 추천 검색어
        $(document).on("click","div.hot_product",function(){
            var hot_name = $(this).text();
            location.href='/output_text?name=' + hot_name.replace(/&/g,"%26").replace(/\+/g,"%2B");
        }) 

        // 인기 검색어
        $(document).on("click","div.hot_recent_list",function(){
            var ingi_name = $(this).children('.hot_recent_list_text').text();
            location.href='/output_text?name=' + ingi_name.replace(/&/g,"%26").replace(/\+/g,"%2B");
        }) 

        $('.unit_select').click(function(){
            if ($(this).hasClass('current') == true){
                $('#select_brand_big div').removeClass('current');
            }
            else{
                $('#select_brand_big div').removeClass('current');
                $(this).addClass('current');
            }
        });
 
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
    })

    function camera_check(){
        if (document.getElementById('image').value == ''){
            alert('사진을 입력해주세요.');
            return false;
        }
    }