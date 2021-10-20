// 로딩 페이지
$(window).on('load', function () {
    $('#load').hide();
 });


function change(str) {
    location.href = str;
}

$(document).ready(function(){

    // 하단 메뉴 이미지 색 변경
    var current_page = document.location.href;
    var test = ['info','faq']

    if (current_page.includes('hibiti')){
        $('#one_base').addClass('current');
        var tmp = document.querySelector('#one_img');
        tmp.setAttribute("src",'/static/images/exhibitions_color.png');
    }
    else if (current_page.includes('info') | current_page.includes('faq') | current_page.includes('notice') | current_page.includes('question') ){
        $('#five_base').addClass('current');
        var tmp = document.querySelector('#five_img');
        tmp.setAttribute("src",'/static/images/more_color.png');
    }
    else if (current_page.includes('camera')){
        $('#two_base').addClass('current');
        var tmp = document.querySelector('#two_img');
        tmp.setAttribute("src",'/static/images/search_color.png');
    }
    else if (current_page.includes('output')){
        $('#two_base').addClass('current');
        var tmp = document.querySelector('#two_img');
        tmp.setAttribute("src",'/static/images/search_color.png');
    }
    else{
        $('#four_base').addClass('current');
        var tmp = document.querySelector('#four_img');
        tmp.setAttribute("src",'/static/images/medicine_color.png');
        // $('#araf').
    }


    // 하단 메뉴 선택시 이동
    $('ul.tabs1 li').click(function(){

        var tab_id = $(this).attr('data-tab1');

        if(tab_id == 'tab-1'){
            location.href = '/exhibitions';
        }
        else if(tab_id == 'tab-2'){
            location.href = '/camera';
        }
        else if(tab_id == 'tab-4'){
            location.href = '/';
        }
        else if(tab_id == 'tab-5'){
            location.href = '/info_form';
        }
    
    })
})