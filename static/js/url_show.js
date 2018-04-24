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
    });

    //hide the loader
    $("#load").remove();
    
});


function show_url(response){
    $('#url_show').html('<a href="' + response + '" target="_blank">' + response + '</a>');
    $("#url_show").css('display','block');
}

