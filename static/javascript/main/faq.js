$( document ).ready( function() {

    // 사이트맵 탭 선택
    $('ul.tabs_map li').click(function(){
        var tab_id = $(this).attr('data-tab_map');

        $('ul.tabs_map li').removeClass('current');
        $('.tab-content_map').removeClass('current');

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');
    });

    // 사이트맵 내리고 올리기
    $(".header_menu_html").hide();
            
    $(".header_menu_box").click(function() {
        $(".header_menu_html").slideDown(300);
        $(".header_menu_box").hide();
    });

    $(".header_menu_box_back").click(function() {
        $(".header_menu_html").slideUp(300);
        $(".header_menu_box").show();
    });

    // 뒤로가기
    $('.header_back_box').click(function(){
        window.history.back();
    })

    // FAQ 답변 숨기기
    $(".hide_and_seek").hide();
    
    // FAQ 질문 클릭시 답변 보이기
    $('.hot_recent_list').click(function(){
        var tab_id = $(this).attr('data-tab');

        if($("#"+tab_id).css("display") == "none"){
            $("#"+tab_id).show();
        } else {
            $("#"+tab_id).hide();
        }
    });

    // 해당 TYPE(CATEGORY)에 해당하는 FAQ들만 보여주기
    $('#select_brand_big div').click(function(){
        var faq_tab = $(this).text();
        if ($(this).hasClass('current') == true){
            $('#select_brand_big div').removeClass('current');
            $('.hot_recent_list').show();
        }
        else{
            $('#select_brand_big div').removeClass('current');
            $(this).addClass('current');
            $('.hot_recent_list').hide();
            $('#'+faq_tab).show();
        }
    });

})