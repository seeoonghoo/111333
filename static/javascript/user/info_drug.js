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

    // 임산부
    $('#good_woman').click(function(){
        $('#nice_woman').prop('checked',false);
        if($(this).prop('checked')){
            var state = '임산부'
            $.ajax({
                url:'/change_woman?state_woman='+state,
                type:'get',
                dataType:'json',
                success:function(response){
                    $('.total_box').hide();
                    for (var cnt = 0 ; cnt < response.extract_re.length ; cnt++){
                        var color = JSON.stringify(response.extract_re[cnt]['color']);

                        var limit = JSON.stringify(response.extract_re[cnt]['dosage_limit']);
                        if (limit.includes(".") == false){
                            limit = limit + '.0'
                        }

                        var b = JSON.stringify(response.extract_re[cnt]['b']);
                        if (b.includes(".") == false){
                            b = b + '.0'
                        }
                        
                        if (color.includes("yellow")){
                            tmp_color = '<span style="color: #f2ab06;">부족</span>';
                        }
                        else if(color.includes("blue")) {
                            tmp_color = '<span style="color: blue;">보통</span>';
                        } 
                        else if(color.includes("green")) {
                            tmp_color = '<span style="color: green;">충족</span>';
                        }
                        else{
                            tmp_color = '<span style="color: red;">과다</span>';
                        }

                        tmp = '<div class = "total_box_good" id = "for_good_woman">\
                                    <div class = "total_name_box">'+
                                        JSON.stringify(response.extract_re[cnt]['extract_name']).replace(/"/gi, "") +
                                    '</div>\
                                    <div class = "total_color_box">'+
                                        tmp_color +
                                    '</div>\
                                    <div class = "total_per_box">'+
                                        b + ' / '+ 
                                        limit +
                                        JSON.stringify(response.extract_re[cnt]['regular_unit']).replace(/"/gi, "")+ '<br>(' +
                                        JSON.stringify(response.extract_re[cnt]['percent'])+ '%)</span>' + 
                                '</div>\
                                </div>';
                        
                        $('#per_day').append(tmp);
                    }
                    $('.total_box_nice').hide();
                },
                error : function(xhr, error){
                    
                }
            })
        }
        else{
            $('.total_box').show();
            $('.total_box_good').remove();
        }
        
    });

    // 수유부
    $('#nice_woman').click(function(){
        $('#good_woman').prop('checked',false);
        if($(this).prop('checked')){
            var state = '수유부'
            $.ajax({
                url:'/change_woman?state_woman='+state,
                type:'get',
                dataType:'json',
                success:function(response){
                    $('.total_box').hide();
                    for (var cnt = 0 ; cnt < response.extract_re.length ; cnt++){
                        var color = JSON.stringify(response.extract_re[cnt]['color']);

                        var limit = JSON.stringify(response.extract_re[cnt]['dosage_limit']);
                        if (limit.includes(".") == false){
                            limit = limit + '.0'
                        }

                        var b = JSON.stringify(response.extract_re[cnt]['b']);
                        if (b.includes(".") == false){
                            b = b + '.0'
                        }

                        if (color.includes("yellow")){
                            tmp_color = '<span style="color: #f2ab06;">부족</span>';
                        }
                        else if(color.includes("blue")) {
                            tmp_color = '<span style="color: blue;">보통</span>';
                        } 
                        else if(color.includes("green")) {
                            tmp_color = '<span style="color: green;">충족</span>';
                        }
                        else{
                            tmp_color = '<span style="color: red;">과다</span>';
                        }

                        tmp = '<div class = "total_box_nice" id = "for_nice_woman">\
                                    <div class = "total_name_box">'+
                                        JSON.stringify(response.extract_re[cnt]['extract_name']).replace(/"/gi, "") +
                                    '</div>\
                                    <div class = "total_color_box">'+
                                        tmp_color +
                                    '</div>\
                                    <div class = "total_per_box">'+
                                        b + ' / '+ 
                                        limit +
                                        JSON.stringify(response.extract_re[cnt]['regular_unit']).replace(/"/gi, "")+ '<br>(' +
                                        JSON.stringify(response.extract_re[cnt]['percent'])+ '%)</span>' + 
                                '</div>\
                                </div>';
                        
                        $('#per_day').append(tmp);
                    }
                    $('.total_box_good').hide();
                },
                error : function(xhr, error){
                }
            })
        }
        else{
            $('.total_box').show();
            $('.total_box_nice').remove();
        }
    });
})

// 섭취 상태 변경
function intake_change(name, custom_noncustom) {
    var state = event.currentTarget.value;

    $.ajax({
			url:'/change_state?state='+state+'&name='+name+'&custom_noncustom=' + custom_noncustom,
			type:'get',
			dataType:'json',
			success:function(response){
				$('.total_box').remove();
                $('.total_box_except').remove();
                for (var cnt = 0 ; cnt < response.extract_re.length ; cnt++){
                    var color = JSON.stringify(response.extract_re[cnt]['color']);
                    var limit = JSON.stringify(response.extract_re[cnt]['dosage_limit']);

                    if (limit.includes(".") == false){
                        limit = limit + '.0'
                    }
                    var b = JSON.stringify(response.extract_re[cnt]['b']);
                    if (b.includes(".") == false){
                        b = b + '.0'
                    }

                    if (color.includes("yellow")){
                        tmp_color = '<span style="color: #f2ab06;">부족</span>';
                    }
                    else if(color.includes("blue")) {
                        tmp_color = '<span style="color: blue;">보통</span>';
                    } 
                    else if(color.includes("green")){
                        tmp_color = '<span style="color: green;">충족</span>';
                    }
                    else{
                        tmp_color = '<span style="color : red;">과다</span>'
                    }

                    tmp = '<div class = "total_box" id ="regular_limit">\
                                <div class = "total_name_box">'+
                                    JSON.stringify(response.extract_re[cnt]['extract_name']).replace(/"/gi, "") +
                                '</div>\
                                <div class = "total_color_box">'+
                                    tmp_color +
                                '</div>\
                                <div class = "total_per_box">'+
                                    b + ' / '+ 
                                    limit+
                                    JSON.stringify(response.extract_re[cnt]['regular_unit']).replace(/"/gi, "")+ '<br>(' +
                                    JSON.stringify(response.extract_re[cnt]['percent'])+ '%)</span>' + 
                               '</div>\
                            </div>';
                    
                    $('#per_day').append(tmp);
                }

                for (var cnt = 0 ; cnt < response.extract_except_recommend.length ; cnt++){

                    var b = JSON.stringify(response.extract_except_recommend[cnt]['b']);
                    if (b.includes(".") == false){
                        b = b + '.0'
                    }

                    tmp = '<div class = "total_box_except">\
                                <div class = "total_name_box">'+
                                    JSON.stringify(response.extract_except_recommend[cnt]['extract_name']).replace(/"/gi, "") +
                                '</div>\
                                <div class = "total_per_box">\
                                 '+  b + JSON.stringify(response.extract_except_recommend[cnt]['regular_unit']).replace(/"/gi, "")+
                               '</div>\
                            </div>';
                    
                    $('#except').append(tmp);
                }
			},
            error : function(xhr, error){
			}
		})
}

// 내 약 리스트에서 이미지 클릭시 해당 약 상세보기
function page_change(name) {
        location.href='/output_text?name=' + name;
    }