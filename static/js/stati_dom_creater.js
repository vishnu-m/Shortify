

$(document).ready(function(){
    var url_list = $('#url_list');
    fetch_data();
    // get_meta_data();
    // add_list_item();
});


function fetch_data(){
    $.get('/get_statistics/')
    .done(function(response){
        // var urls = Array();
        // for (const row of response.data) {
        //     urls.push(row['url']);
        // }
        // console.log(urls);
        // console.log(data);
        for ( let row of response.data){
            $('#loader').hide();
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

    // row_item.on('click',function(){
    //     show_details(this, row);
    // });
    // appends the row to the main list
    url_list.append(row_item);
    row_item.slideDown(500);
}


function show_details(card, data){
    

    var detail_view = $(card).children()[2];
    $(detail_view).toggle();

    if ( !($(detail_view).is(':visible'))){
        return;
    }
    var detail_sec =  create_detail_view(data);
    $(detail_view).html(detail_sec);

    show_graph(data['stati']);

    
}

function create_detail_view(data){
    var detail_card = $('<div></div>');
    detail_card.addClass('w3-bar detail-card');

    var no_of_clicks = $('<div></div>');
    no_of_clicks.text('Total Clicks : ' + data['clicks']);


    var chart_sec = $('<canvas id="myChart"></canvas>');
    
    detail_card.append(no_of_clicks);
    detail_card.append(chart_sec);

    return detail_card;
}

// window.onload = function () {

function show_graph(data){
    var ctx = document.getElementById("myChart").getContext('2d');
    var labels = []
    for ( let date of data){
        labels.push(date['x']);
    }
    console.log(data);
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
                borderWidth: 1
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