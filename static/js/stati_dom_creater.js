

$(document).ready(function(){
    var url_list = $('#url_list');
    fetch_data();
    // get_meta_data();
    // add_list_item();
});


function fetch_data(){
    $.get('/get_statistics/')
    .done(function(response){
        for ( let row of response.data){
            add_list_item(row);
        }
    })
    .fail(function(){
        console.log('something went wrong');
    });
}


function add_list_item(row){
    //  gets the main list
    var url_list = $('#url_list');

    // a row element
    var row_item = $('<div></div>');
    row_item.addClass('w3-bar w3-card row-card row-item');

    // avatar in the left
    var avatar = $('<img/>');
    avatar.attr('src',"/static/images/img_avatar2.png");
    avatar.addClass('w3-bar-item w3-circle w3-hide-small');
    avatar.attr('style','width:12%')

    // the block which shows the title of the site in that URL
    // var title_sec = $('<p></p>');
    // var title = get_meta_data(row['url']);
    // if ( title == undefined){
    //     title = '';
    // }
    // title_sec.text(title);

    // the block which shows the actual URL and the date added
    // In that, the URL section and the date section
    // all are declared here
    var url_and_date_sec = $('<div></div>');
    var url_sec = $('<div></div>');
    var date_sec = $('<div></div>');

    get_meta_data(row['url']);

    // defining the URL section and setting the text inside it
    url_sec.addClass('w3-half');
    url_sec.text(row['url'] );

    // defining the date section and setting the date in it
    date_sec.addClass('w3-half');
    date_sec.text(row['date_added']);


    // setting up the URL and Date block by adding both URL section and date section
    url_and_date_sec.addClass('w3-row-padding');
    url_and_date_sec.append(url_sec);
    url_and_date_sec.append(date_sec);

    // makes the shortened URL by concatenating the host name and hash text
    // and defines the main title of the row
    // it contains the shortened and the actual URLs
    var hash = window.location.origin + '/' + row['hash'];
    var hash_url = $('<span></span>');
    hash_url.addClass('w3-large');
    hash_url.html('<a class="short-link" href="'+ hash +'" target="_blank">' + hash +'</a>');

    // makes the text content section ( both title and URL-Date section )
    var content_div = $('<div></div>');
    content_div.addClass('w3-bar-item');
    content_div.attr('style','width:88%;color: rgb(0,0,0,0.6)')
    content_div.append(hash_url);
    // content_div.append(title_sec);
    content_div.append(url_and_date_sec);

    // completes the row by adding both avatar ad text content
    row_item.append(avatar);
    row_item.append(content_div);

    // appends the row to the main list
    url_list.append(row_item);
}

function get_meta_data(url){
        // var text = ''
        // $.ajax({
        //     url: url,
        //     type: 'GET',
        //     beforeSend: function(xmlhttp){
        //         // xmlhttp.setRequestHeader( "Pragma", "no-cache" );
        //         // xmlhttp.setRequestHeader( "Cache-Control", "no-cache" );
        //         xmlhttp.setRequestHeader("Access-Control-Allow-Origin","*");
        //         xmlhttp.setRequestHeader("Access-Control-Allow-Credentials", "true");
        //         xmlhttp.setRequestHeader("Access-Control-Allow-Methods", "GET");
        //         xmlhttp.setRequestHeader("Access-Control-Allow-Headers", "Content-Type");
        //     },
        //     success: function(response){
        //         var el = $('<html></html');
        //         el.html(response);

        //         var title = $('title',el)[0];
        //         window.text = $(title).text();
        //     }
        // });
        // console.log(window.text);
        // return window.text;
        // $.get(url).done(function(response){
        //     console.log(url);
        //     // console.log(response);
        //     var pattern = /<title>/i ///^<title>.+<\/title>/i;
        //     result = pattern.exec(response);
        //     console.log(result);
        //     var start = result.index;

        //     var pattern = /<\/title>/i;
        //     result = pattern.exec(response);
        //     console.log(result);
        //     var stop = result.index;

        //     r = '';
        //     for( var i = start + 7; i < stop; i++){
        //         r += response[i];
        //     }
        //     console.log(r);
        //     return r;
            
        //     // var desc = $(response).filter('title').attr('content');
        //     // console.log(desc);
        // }).fail(function(){
    
        // });

        var xhr = createCORSRequest('GET',url);
        xhr.setRequestHeader(
            'X-Custom-Header', 'value');

        if( !xhr){
            console.log("CORS not supported");
        }
        console.log('in get');
        xhr.onload = function() {
        var responseText = xhr.responseText;
        console.log(getTitle(responseText));
        console.log(url);
        // process the response.
        };
        
        xhr.onerror = function() {
            console.log('There was an error!');
        };
           
        xhr.send();
    
}

function getTitle(text) {
    return text.match('<title>(.*)?</title>')[1];
  }


function createCORSRequest(method, url) {
    var xhr = new XMLHttpRequest();
    if ("withCredentials" in xhr) {
  
      // Check if the XMLHttpRequest object has a "withCredentials" property.
      // "withCredentials" only exists on XMLHTTPRequest2 objects.
      xhr.open(method, url, true);
  
    } else if (typeof XDomainRequest != "undefined") {
  
      // Otherwise, check if XDomainRequest.
      // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
      xhr = new XDomainRequest();
      xhr.open(method, url);
  
    } else {
  
      // Otherwise, CORS is not supported by the browser.
      xhr = null;
  
    }
    return xhr;
  }