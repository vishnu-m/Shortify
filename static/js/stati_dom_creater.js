

$(document).ready(function(){
    var url_list = $('#url_list');
    fetch_data();
    // get_meta_data();
    // add_list_item();
});


function fetch_data(){
    $.get('/get_statistics/')
    .done(function(response){
        // hide the loader that has been spinning
        $('#loader').hide();

        // if the user has no statistic data show a message
        if( response.data.length == 0){
            var message = $('<div></div>');
            message.addClass('w3-card row-card row-item title empty-message-sec');
            
            var title_sec = $('<div></div>');
            title_sec.addClass('empty-message-title');
            title_sec.text('There is nothing up here yet !');

            var sub_title_sec = $('<div></div>');
            sub_title_sec.addClass('empty-message-subtitle');
            sub_title_sec.html('<a href="/">Get back to home</a>');

            var message_sec = $('<div></div>');
            message_sec.addClass('empty-message-content');
            message_sec.html('Shorten links, Save Them, Share it to your Circles<br>Here shows all the saved URLs you have got');

            message.append(title_sec);
            message.append(sub_title_sec);
            message.append(message_sec);
            

            $('#url_list').append(message);
            return;
        }
        // else show all the statistical data he has got
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
    row_item.addClass('w3-bar w3-card row-card row-item title');

    // avatar in the left
    var avatar = $('<img/>');
    // if page icon url is present in the database set it else set to default
    if ( row['icon_url'] != '' ){
        avatar.attr('src', row['icon_url']);    
        avatar.addClass('w3-bar-item avatar-sec');
    }
    else{
        avatar.attr('src',"/static/images/link.png");
        avatar.addClass('w3-bar-item w3-circle avatar-sec');
    }
    

    // the block which shows the title of the site in that URL
    // var url_sec = $('<p></p>');
    // var title = get_meta_data(row['url']);
    // if ( title == undefined){
    //     title = '';
    // }
    // url_sec.text(title);

    // the block which shows the Actual URL and the date added
    // In that, the actual URL section and the date section
    // all are declared here
    var title_and_date_sec = $('<div></div>');
    var title_sec = $('<div></div>');
    var date_sec = $('<div></div>');

    // defining the URL section and setting the date in it
    title_sec.addClass('w3-half title-sec');    
    title_sec.text(row['title']);
    
    // defining the date section and setting the date in it
    date_sec.addClass('w3-half date-sec');
    date_sec.css('text-align','right');
    date_sec.text(row['date_added']);


    // setting up the hash URL and Date block by adding both URL section and date section
    title_and_date_sec.addClass('w3-row-padding');
    title_and_date_sec.append(title_sec);
    title_and_date_sec.append(date_sec);

    
    // the block which shows the title of the page and the actual URL
    // In that, the URL section and the title section
    // all are declared here
    var url_and_hash_sec = $('<div></div>');
    var hash_sec = $('<div></div>');
    var url_sec = $('<span></span>');
    

    // defining the title section and setting the date in it
    url_sec.addClass('w3-half url-sec');
    url_sec.html('<a href="'+ row['url'] +'" target="_blank">' + row['url'] +'</a>');

    // defining the hash URL section and setting the text inside it
    // getting the current host name and concatenate with the hash text
    hash_sec.addClass('w3-half hash-sec');
    hash_sec.css('text-align','right');
    var hash = window.location.origin + '/' + row['hash'];
    hash_sec.html('<a href="'+ hash +'" target="_blank">' + hash +'</a>');
    

    // setting up the URL and title block by adding both URL section and title section
    url_and_hash_sec.addClass('w3-row-padding');
    url_and_hash_sec.append(url_sec);
    url_and_hash_sec.append(hash_sec);
    
    

    // makes the text content section ( both title and URL-Date section )
    var content_div = $('<div></div>');
    content_div.addClass('w3-bar-item');
    content_div.attr('style','width:88%;');
    content_div.append(title_and_date_sec);
    content_div.append(url_and_hash_sec);

    // for showing detailed view of this card
    var detail_view = $('<div></div>');
    detail_view.addClass('detail-view');

    // completes the row by adding both avatar ad text content
    row_item.append(avatar);
    row_item.append(content_div);
    row_item.append(detail_view);

    // show statistics in detail on clicking the corresponding row
    row_item.on('click',function(event){
        if( $(event.target).is($('#'+row['hash']))){
            event.preventDefault();
            return;
        }
        show_details(this, row);

    });

    // appends the row to the main list
    url_list.append(row_item);
    row_item.slideDown(500);
}


function show_details(card, data){

    // get the detail view DOM object and toggles it 
    var detail_view = $(card).children()[2];
    $(detail_view).toggle();

    // if the details section is visible do nothing
    if ( !($(detail_view).is(':visible'))){
        return;
    }

    // hide all the other detail sections and show only the currently engaged one
    toggle_detail_view(detail_view);

    // get the DOM object and chart section id for detail view and chart
    var detail =  create_detail_view(data);
    var detail_sec = detail[0];
    var chart_sec_id = detail[1];

    // set the detail view section
    $(detail_view).html(detail_sec);

    // if clicks are non zero, invoke function to show the graph
    if ( data['clicks'] != 0){
        show_graph(data['stati'], chart_sec_id);
    }
        
}

// shows the currently engaged detail view and hides all the others
function toggle_detail_view(current_card){
    // hides all the detail cards first
    var detail_cards = $('.detail-view');
    for( let card of Array(detail_cards)){
        $(card).hide();
    }

    // and then show the currently engaged card only
    $(current_card).show();

}


// creates the detail view main object and return the created DOM object and the id of the chart section
function create_detail_view(data){

    // creates the parent card in which total clicks and the chart will be displayed
    var detail_card = $('<div></div>');

    // creates the shortened url section
    var date_sec = $('<span></span>');
    date_sec.addClass('date-sec-detail-view');
    date_sec.text(data['date_added']);


    // creates the page description section
    var desc_sec = $('<div></div>');
    desc_sec.addClass('desc-sec');
    desc_sec.text(data['desc']);
    
    // creates the section for displaying the total no of clicks and add some styles
    var no_of_clicks = $('<div></div>');
    no_of_clicks.addClass('no_of_click');

    // set the value
    no_of_clicks.text('Total Clicks : ' + data['clicks']);
    
    // set the id for chart section in this row
    var chart_sec_id = data['hash'];
    
    // creates the canvas for chart with the above chart sec id
    var chart_sec = $('<canvas class = "myChart" id=' + chart_sec_id + '></canvas>');
    
    // adds the styles and appends the no of clicks section to the parent
    detail_card.addClass('w3-bar detail-card');
    detail_card.append(date_sec);
    detail_card.append(no_of_clicks);
    detail_card.append(desc_sec);
    

    // if clicks are non zero add the chart section to parent object
    if ( data['clicks'] != 0)
        detail_card.append(chart_sec);

    // return the chart sec id and the parent object
    return [detail_card, chart_sec_id];
}


function show_graph(data, chart_id){
    // get the canvas context
    var ctx = document.getElementById(chart_id).getContext('2d');
    
    // get all the dates and remove duplicate values
    var labels = []
    for ( let date of data){
        if( labels.includes(date['x']) == false)
            labels.push(date['x']);
    }
    // labels.sort();
    // create the line chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Visitors',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1,
                fill : false
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
    
}