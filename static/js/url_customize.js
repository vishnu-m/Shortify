
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

    
// this send an ajax request to the back end and verifies whether the requested URL is available or not
    $('#url_shortened').change(function () {
        //show the loader first
        $('#loader').show();
        
        var tag = $('#url_shortened').val();

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
            }
            else{
                // it is not available
                // hide the loader
                $('#loader').hide();
                //show the status
                $('#done_img').hide();
                $('#fail_img').show();
            }
        })
        .fail(function(){

        });
    });

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