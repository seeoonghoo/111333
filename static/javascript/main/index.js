$( document ).ready( function() {

    // 자동으로 이미지 넘어가는 함수
    var idx_lgth = $("#visual>div").length;
    var srt = 1;
  
    $("section>a").click(function(){
        var idx = $(this).index();
        srt = idx;
        $(this).addClass('on').siblings().removeClass('on');
        $("#visual>div").eq(idx).addClass('on').siblings().removeClass('on');
    });
  
    setInterval(AutoRun, 3000);
  
    function AutoRun(){
        if(srt == idx_lgth){
        srt = 0;  
        }
        $("section>a").eq(srt).addClass('on').siblings().removeClass('on');
        $("#visual>div").eq(srt).addClass('on').siblings().removeClass('on');
        srt++;  
    }
    

    // 검색별로 보여주기
    $('ul.tabs li').click(function(){
        var tab_id = $(this).attr('data-tab');

        $('ul.tabs li').removeClass('current');
        $('.tab-content').removeClass('current');

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');


    });

    
    // 4개짜리 셀렉
    $('ul.tabs_4 li').click(function(){
        var tab_id = $(this).attr('data-tab_4');

        $('ul.tabs_4 li').removeClass('current');
        $('.tab-content_4').removeClass('current');

        if(tab_id == 'tab-11'){
            var tmp = document.querySelector('#two');
			tmp.setAttribute("src",'/static/images/home.png');
            var tmp = document.querySelector('#three');
			tmp.setAttribute("src",'/static/images/home.png');
            var tmp = document.querySelector('#four');
			tmp.setAttribute("src",'/static/images/home.png');
		}
		else if(tab_id == 'tab-22'){
			var tmp = document.querySelector('#one');
			tmp.setAttribute("src",'/static/images/home.png');
            var tmp = document.querySelector('#three');
			tmp.setAttribute("src",'/static/images/home.png');
            var tmp = document.querySelector('#four');
			tmp.setAttribute("src",'/static/images/home.png');
		}
		else if(tab_id == 'tab-33'){
			var tmp = document.querySelector('#one');
			tmp.setAttribute("src",'/static/images/home.png');
            var tmp = document.querySelector('#two');
			tmp.setAttribute("src",'/static/images/home.png');
            var tmp = document.querySelector('#four');
			tmp.setAttribute("src",'/static/images/home.png');
		}
		else if(tab_id == 'tab-44'){
			var tmp = document.querySelector('#one');
			tmp.setAttribute("src",'/static/images/home.png');
            var tmp = document.querySelector('#two');
			tmp.setAttribute("src",'/static/images/home.png');
            var tmp = document.querySelector('#three');
			tmp.setAttribute("src",'/static/images/home.png');
		}

        $(this).addClass('current');
        $("#"+tab_id).addClass('current');

        if(tab_id == 'tab-11'){
            var tmp = document.querySelector('#one');
			tmp.setAttribute("src",'/static/images/home_color.png');
		}
		else if(tab_id == 'tab-22'){
			var tmp = document.querySelector('#two');
			tmp.setAttribute("src",'/static/images/home_color.png');
		}
		else if(tab_id == 'tab-33'){
			var tmp = document.querySelector('#three');
			tmp.setAttribute("src",'/static/images/home_color.png');
		}
		else if(tab_id == 'tab-44'){
			var tmp = document.querySelector('#four');
			tmp.setAttribute("src",'/static/images/home_color.png');
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

    // 클릭하면 넘어가는 함수
    $(document).on("click","div.white_box_click",function(){
        var this_name = $(this).attr(('for_change'));
        location.replace('/output_text?name=' + this_name.replace(/&/g,"%26").replace(/\+/g,"%2B"));
    })

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
})