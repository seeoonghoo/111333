    // 이미지 썸네일 변경 하려고 했는데 어려움이 있다
    function setThumbnail(event) { 
        var reader = new FileReader();

        reader.onload = function(event) { 

            var div = document.getElementById('image_container');
            while(div.firstChild){
                div.removeChild(div.firstChild);
            }

            var img = document.createElement("img"); 
            img.setAttribute("src", event.target.result); 
            img.width=90;
            img.height=90;
            document.querySelector("div#image_container").appendChild(img); 
        }; 
        reader.readAsDataURL(event.target.files[0]); 

    } 

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

        $('ul.tabs li').click(function(){
            var tab_id = $(this).attr('data-tab');

            $('ul.tabs li').removeClass('current');
            $('.tab-content').removeClass('current');

            $(this).addClass('current');
            $("#"+tab_id).addClass('current');

            $( 'html, body' ).animate( { scrollTop : 0 }, 400 );
        });

        $('.header_back_box').click(function(){
            window.history.back();
        })


})