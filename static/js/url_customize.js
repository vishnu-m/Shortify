var status = false;
// this displays the customize section and hides the home section

    $('#customize_btn').on('click',function(){
        // hide the url shortening section
            $('#shorten_section').slideUp(300);
            $('#or_line').slideUp(300);
            $('#customize_btn').slideUp(300);
            $('#tag_line').slideUp(300);
        // hidden

        // show the customization section after a moment
            setTimeout(function(){
                $('#customiz_section').fadeIn(500);
            }, 400);    
        // shown

        // hide the url show section
        $('#url_show').hide();
        // hidden

        // place the url in the input field
            var url = $('#url').val()
            $('#url_custom').val(url);
        // placed

        // place the current site address
            var url = get_hostname();
            $('#site_address').text(url);
        //placed
    });
// displayed




// this displays the home page and hides the customize section

    $('#back_to_home_btn').on('click',function(){

        // show the customization section 
            $('#customiz_section').fadeOut(500);        
        // shown

        // show the url shortening section after a moment
            setTimeout(function(){
                $('#shorten_section').slideDown(300);
                $('#or_line').slideDown(300);
                $('#customize_btn').slideDown(300);
                $('#tag_line').slideDown(300);        
            }, 400);            
        // shown  

        // place the url in the input field
            var url = $('#url_custom').val()
            $('#url').val(url);
        // placed


    });

// displayed

// to trigger the request sending func when the typing is done
    typeTimer('#url_shortened', doneTagTyping);
    
    function typeTimer(id, callback){
        var typingtimer;
        $(id).on('keydown', function(event){
            // get the character from the keyCode
            var keyCode = String.fromCharCode(event.keyCode);

            // filters keys other than alpha numeric char ( except backspace and shift )
            // refer this link for keycodes https://www.cambiaresearch.com/articles/15/javascript-char-codes-key-codes
            // if (/[a-zA-Z0-9_]/.test(keyCode) || event.keyCode == 8 || event.keyCode == 16){
            if((event.keyCode >= 46 && event.keyCode <= 90 ) ||
                (event.keyCode >= 96 && event.keyCode <= 111) ||
                (event.keyCode >= 186 && event.keyCode <= 222) || event.keyCode == 8){
                
                // clear the exisiting timer and start a new one since the key is not being pressed
                clearTimeout(typingtimer);
                typingtimer = setTimeout(callback, 3000);

                // hide any other status icons or warnings and show the loader
                $('#done_img').hide();
                $('#fail_img').hide();
                hide_warning();
                $('#loader').show();        
            }
        });
    }
// triggered

// this validates URL after typing
    function doneURLtyping(){
        $('#loader').show();

        var url = $('#url_custom').val();

        if( ! validate_url(url)){
            show_warning('Invalid URL');
        }
        
    }
//
    

// this send an ajax request to the back end and verifies whether the requested URL is available or not
    function doneTagTyping () {
        //show the loader first
        $('#loader').show();
        
        var tag = $('#url_shortened').val();

        if( tag.length < 4){
            show_warning('The tag should contain atleast 4 characters');
            return;
        }

        

        for(var i = 0 ; i < tag.length; i++){
            if( !((/[a-zA-Z0-9_]/).test(tag[i]))){
                show_warning('The tag should contain letters, digits and underscore _ only');
                return;
            }
        }

        hide_warning();

        if ( tag.toString == '')
            return;

        // send the request
        $.post('verify/', {'hash':tag})
        .done(function(response){
            if( response.status == '200'){
                // requested URL is available
                // hide the loader
                $('#loader').hide();
                //show the status
                $('#fail_img').hide();
                $('#done_img').show();
                status = true;
            }
            else{
                // it is not available
                // hide the loader
                $('#loader').hide();
                //show the status
                $('#done_img').hide();
                $('#fail_img').show();

                // show warning
                show_warning('It is already taken');
            }
        })
        .fail(function(){
            show_warning('Something went wrong');
        });
    }



// verified




// this extracts the hostname from the URL
    function get_hostname(){
        var url = window.location.toString();
        url = url.split('/');     // it returns something like 'http','','domain.com','text after the /'
        var http = url[0];
        var hostname = url[2];
        url = http + '//' + hostname + '/';
        return url;
    }
// extracted


// this shows a warning of the given warning text
    function show_warning (warning_text) {
        $('#warning_txt').text(warning_text);
        $('#warning_txt').show();
        $('#done_img').hide();
        $('#loader').hide();
        $('#fail_img').show();
        status = false;
    }
// shown

// this hides the above created warning
    function hide_warning(){
        $('#warning_txt').hide();
    }
// hidden


// this shortens the URL to the given tag
    $('#custom_cut_btn').on('click', function(event){

        

        event.preventDefault();


        console.log('it is submitting');

        // if anything is wrong
        if ( status == false ){
            show_warning('Invalid Tag');
            return;
        }
        
        var url = $('#url_custom').val();

        // if the url is empty
        if( url.length == 0){
            show_warning('URL cannot be empty');
            return;
        }
        
        if( ! validate_url(url)){
            show_warning('Invalid URL');
            return;
        }


        var tag = $('#url_shortened').val();

        // confirm that the tag is not empty
        if ( tag.length == 0){
            show_warning('Tag cannot be empty');
            return;
        }
        
        // if everything is well
        // send an ajax request to shorten the Given URL to the given tag
        $.post('custom_shorten/', {'url':url, 'tag':tag})
        .done(function(response){
            // request success

            if( response.status == '200')
            {
                // URL shortened successfully
                // show the shortened URL
                // $('#shorten_custom_url').hide();
                $('#warning_txt').html('<a href="' + response.text + '" target="_blank" class="title title-white short" id="short_url">' + response.text + '</a>');
                $('#warning_txt').show();
            }
            else{
                // unsuccessful
                var warning = 'URL could not be shortened';
                if( typeof response.text != undefined &&  response.text.length != 0 )
                    warning = response.text;
                show_warning(warning);
            }
        })
        .fail(function(){
            // request failed
            show_warning('Something went wrong');
        });
    });
// shortened


// this resets the customiz section to the beginnning state
    $('#reset_btn').on('click', function(){
        $('#url_custom').val('');
        $('#url_shortened').val('');
        $('#done_img').hide();
        $('#fail_img').hide();
        $('#loader').hide();
        $('#shorten_custom_url').show();
        hide_warning();
    });

// set

// this validate whether the entered URL is in correct form
    function validate_url(url){
        var pattern = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9:\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/i;
        return pattern.test(url);
    }
// validated


// this copies the shortened URL to clipboard
$('#copy_btn').on('click',function(){
    // select the auto geneated link section
    $('#short_url').focus();
    $('#short_url').select();

    document.execCommand('copy');



});
// copied