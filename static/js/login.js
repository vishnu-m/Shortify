$('#login_form').on('submit',function(event){

    event.preventDefault();
    
    var username = $('#username').val();
    var password = $('#password').val();

    $.post('/login/', {username:username, password:password})
    .done(function(response){
        // request success
        console.log(typeof(response.status));
        if ( response.status == '200'){
            // redirect to home page
            console.log('ok');
            window.location = "/";
            
        }
        else{
            show_warning(response.text);
        }
    })
    .fail(function(){
        // request failed
        show_warning('Something went wrong');
    });
});


function show_warning(warning){
    $('#warning_txt').html(warning);
    $('#warning_txt').css('color','#fff');
}