$( document ).ready( function() {

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
            $(document).on("click","div.small_box",function(){
                var this_name = $(this).attr(('for_change'));
                location.replace('/output_text?name=' + this_name);
            })
    
    
            // 검색별로 보여주기
            $('ul.tabs li').click(function(){
                var tab_id = $(this).attr('data-tab');
    
                $('ul.tabs li').removeClass('current');
                $('.tab-content').removeClass('current');
    
                $(this).addClass('current');
                $("#"+tab_id).addClass('current');
    
            });
    
        });
        
        function concate(){
    
    
            var date = document.getElementById('date').value;
    
            if (date == null){
                $('#day_alert').show();
                return false;
            }
            else{
                $('#day_alert').hide();
            }
        }