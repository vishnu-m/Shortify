
// validating email  ( whether already exists )

$('#edit_profile').on('submit',function(event){

    event.preventDefault();


    var first_name = $('#first_name').val();
    var last_name = $('#last_name').val();
    var email = $('#email').val();





    $.post('/editprofile/',{
        first_name:first_name,
        last_name:last_name,
        email:email,




    })
    .done(function(response){
        // request successfull
        if ( response.status == '200'){
            // redirect to home page
            window.location = "/";
        }
        show_warning(response.text);
    })
    .fail(function(response){
        // request failed
        show_warning('Something went wrong')
    });
});

function show_warning(warning){
    $('#warning_txt').html(warning);
    $('#warning_txt').css('color','#f00');
}