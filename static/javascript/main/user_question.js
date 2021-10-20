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


    // 뒤로가기
    $('.header_back_box').click(function(){
        window.history.back();
    })


    // 해당 질문 클릭시 내용 보여주기
    $(".hide_and_seek").hide();
            
    $('.hot_recent_list').click(function(){
        
        var tab_id = $(this).attr('data-tab');

        if($("#"+tab_id).css("display") == "none"){
            $("#"+tab_id).show();
        } else {
            $("#"+tab_id).hide();
        }
    });

    // 작성하기
    $('.question_write').click(function(){
        location.href='/user_question_write';
    })
})