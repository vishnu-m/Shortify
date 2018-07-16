$('#shorten').on('submit',function(event){

    event.preventDefault();

    // show loader
    $("#cut_btn").after('<div class="loader" id="load"></div>');
    
    var url = $('#url').val()
    $.post('short/',{url:url})
    .done(function(response){
        //success
        show_url(response);
    })
    .fail(function(){
        //failed
        console.log('failed');
        error_on_fetching();
    });

    //hide the loader
    $("#load").remove();
    
});


function show_url(response){
    var host = window.get_hostname();
    $('#url_show').html('<a href="' + host + response + '" target="_blank">' + host + response + '</a>');
    $("#url_show").css('display','block');
}

function error_on_fetching(){
    $('#url_show').html('Something went wrong');
    $("#url_show").css('display','block');
}
