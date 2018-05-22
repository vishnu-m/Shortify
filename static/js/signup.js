
// validating username, email and phone number ( whether already exists )

$('#signup_form').on('submit',function(event){

    event.preventDefault();
    

    var first_name = $('#first_name').val();
    var last_name = $('#last_name').val();
    var email = $('#email').val();
    var phone = $('#phone').val();
    var username = $('#username').val();
    var password = $('#password').val();
    var confirm_pass = $('#confirm_password').val();

    if ( password != confirm_pass ){
        show_warning('Passwords does not match');
        return false;
    }

    $.post('/signup/',{
        first_name:first_name,
        last_name:last_name,
        email:email,
        phone:phone,
        username:username,
        password:password,
    })
    .done(function(response){
        // request successfull 
        if ( response.status == '200'){
            // redirect to home page
            window.location = "/login/";
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