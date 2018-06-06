var events_shown = false;
var about_shown = false;
var map;

//########################################################################
// Init Stuff
//########################################################################

window.onload = function init() {
  mapboxgl.accessToken = 'pk.eyJ1IjoianVsaWFua29wcCIsImEiOiJjamh4ZTB1Y2kwOXZjM3FvZW04NHB0bTE5In0.tdWPsXH-HWeuO22fW4jyjA';
  map = new mapboxgl.Map({
    container: document.getElementById('map_wrapper'),
    style: 'mapbox://styles/mapbox/dark-v9',
    zoom: 11.5,
    center: [-74.0, 40.760],
    minZoom: 11,
    maxZoom: 14,
    attributionControl: false,
  });
  map.addControl(new mapboxgl.AttributionControl(), 'top-right');

  $.get('http://127.0.0.1:5000/api/v1.0/places', function(data) {
    loadPlaces(data);
  })
  $('.details').css("margin-left", -$('#places_container').outerWidth());

  map.on('load', function() {
      map.addSource('cell', {
        'type':'geojson',
        'data':{
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[]]]
            }
        }
      })

      map.addSource('circle', {
        'type':'geojson',
        'data':{
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[]]]
            }
        }
      })

      map.addLayer({
          'id': 'cirlce',
          'type': 'fill',
          'source': 'circle',
          'paint': {
              'fill-color': '#022735',
              'fill-opacity': 0.6
          }
      });

      map.addLayer({
          'id': 'cell',
          'type': 'fill',
          'source': 'cell',
          'paint': {
              'fill-color': '#3E0906',
              'fill-opacity': 0.8
          }
      });

    })// end of map.on('load')
}//end of init()

function loadPlaces(data) {
  console.log('orig data', data);
  for (item in data) {
    text = "Date & Time: <br>" + new Date(data[item]['timestamp']).toISOString().slice(0,10) +
      "<br>Place: <br>" + data[item]['x'] + ',' + data[item]['y']
    //create elements in template string, put them in array and
    // push the array as one(!) thing to the dom -> more efficient
    event_ = document.createElement('div');
    element = `
     <div >
    `
    $(event_).addClass("card text-white bg-dark")
      .html(text)
      .attr('id', 'place' + item)
      .attr('timestamp', data[item]['timestamp'])
      .attr('x', data[item]['x'])
      .attr('y', data[item]['y'])
      .attr('amount', data[item]['tweet_amount'])
      .click(function(event) {
        event.preventDefault()
        loadPlaceDetails(event.target.id);
      })
    $("#places_container").append(event_);
  }
}//end of LoadPlaces

//########################################################################
// View Stuff
//########################################################################

function toggleAbout() {
  if (about_shown === true) {
    hideDetails();}else{
    if (events_shown === true) {
      hideDetails();
      loadAbout();
    }else{
      loadAbout();
    }
  }
}


function loadAbout() {
  about_text = "This demo shows the capabilities of ACC a system to detect Anomalous\
  Croded Places. It helps urban planners to automatically get information about\
  what is happening in their city. The System was built was build by Julian Kopp\
  for his Bachelor Thesis supervised by Haytham Assem. \n The click on a place \
  in the left navigation bar. For the clicked place occured topics will be shown \
  in the slide out window. Additionally The area of the event is visualised on the\
  map."

  $(".titleII").text("About ACC");
  about_card = document.createElement('div');
  $(about_card).addClass("card text-white bg-dark about")
    .text(about_text)
  $("#details_container").append(about_card);
  showDetails("about");
}

function showDetails(type){
  $(".footerII, .details_container, .titleII")
    .animate({
      marginLeft: '0px'
    }, {
      duration: 500
    });
    if(type == "about"){
      about_shown = true;
    } else {
      events_shown = true;
    }
}

function hideDetails() {
  $(".footerII, .details_container, .titleII")
    .animate({
      marginLeft: -$('.places_container').outerWidth()
    }, {
      duration: 500
    });
  $('.details_container').empty()
  about_shown = false;
  events_shown = false;
}

function loadPlaceDetails(elementID) {
  timestamp = new Date($('#' + elementID).attr('timestamp')).toISOString().slice(0,19);
  x = $('#' + elementID).attr('x');
  y = $('#' + elementID).attr('y');
  amount = $('#' + elementID).attr('amount');

  //http://127.0.0.1:5000/api/v1.0/events/'2018-04-15%2000:00:00'/1.0/1.0/63
  api_call = `http://127.0.0.1:5000/api/v1.0/events/${timestamp}/${x}/${y}/${amount}`

  $.get(api_call, function(data) {
    console.log(data);
    showPlaceDetails(data, timestamp, x, y, amount);
  })
  drawCell(x,y);
}

function showPlaceDetails(data, timestamp, x, y, amount){
  if (about_shown === true || events_shown === true){
    hideDetails();
  }
    $(".titleII").text(`Events at ${timestamp} in (${x},${y})`);
    for (item in data) {
      start = new Date(data[item]['start_end'][0]).toISOString().slice(11,16);
      end = new Date(data[item]['start_end'][1]).toISOString().slice(11,16);

      text = "Start - End:<br> " + start + " - " + end +
        "\n <br>Main Words: <br> " + data[item]['main_words'].join(', ') +
        "\n <br>Rel Words: <br>" + data[item]['rel_words'].join(', ')
      event_ = document.createElement('div');
      $(event_).addClass("card text-white bg-dark")
        .css('word-wrap', "break-word")
        .css('cursor', 'default')
        .html(text)
        .attr('id', 'event' + item)
        .attr('timestamp', timestamp)
        .attr('x', x)
        .attr('y', y)
        .attr('amount', amount)
        .attr('event', item)
        .click(function(event) {
          loadTweets(event.target.id)
        });
      $("#details_container").append(event_);
    }
    showDetails("events");
}

function formatTime(timestamp){
  hour = timestamp.getHours();
  min = timestamp.getMinutes();
  return ('0' + hour).slice(-2) + ":" + ('0' + min).slice(-2)
}

function formatTimestamp(timestamp) {
  return new Date(timestamp).toISOString().slice(0,10);
}

//########################################################################
// Map Stuff
//########################################################################

function drawCell(x,y){
all_points = calc_cell_coords(x,y);

map.getSource('cell').setData(
  {
    'type': 'Feature',
    'geometry': {
        'type': 'Polygon',
        'coordinates': [all_points[0]]
      }
  })

map.getSource('circle').setData(
  {
    'type': 'Feature',
    'geometry': {
        'type': 'Polygon',
        'coordinates': [all_points[1]]
      }
  })
}

function calc_cell_coords(y,x) {//swap is intentional
  y = parseInt(y);
  x = parseInt(x);

  lr=[-73.96825980, 40.67916214]//base
  ll=[-74.03050115, 40.70654844]
  ul=[-73.94697020, 40.89639086]
  ur=[-73.88472922, 40.86900372]
  map_size = 24

//i and j are the axis of the bounding box
  i_lat_step = (ul[0]-ll[0])/map_size;
  j_lat_step = (lr[0]-ll[0])/map_size;
  i_lon_step = (ul[1]-ll[1])/map_size;
  j_lon_step = (lr[1]-ll[1])/map_size;

  A_lat = ll[0] + (x+1) * i_lat_step + y * j_lat_step;//ul of cell
  A_lon = ll[1] + (x+1) * i_lon_step + y * j_lon_step;
  B_lat = ll[0] + (x+1) * i_lat_step + (y+1) * j_lat_step;//ur of cell
  B_lon = ll[1] + (x+1) * i_lon_step + (y+1) * j_lon_step;
  C_lat = ll[0] + (x) * i_lat_step + (y+1) * j_lat_step;//lr of cell
  C_lon = ll[1] + (x) * i_lon_step + (y+1) * j_lon_step;
  D_lat = ll[0] + (x) * i_lat_step + (y) * j_lat_step;//ur of cell
  D_lon = ll[1] + (x) * i_lon_step + (y) * j_lon_step;
  cell = [[A_lat,A_lon], [B_lat, B_lon], [C_lat, C_lon],[D_lat, D_lon]]
  return [cell,calc_circle(cell, i_lat_step, j_lat_step, i_lon_step, j_lon_step)]
}

function calc_circle(coords, i_lat_step, j_lat_step, i_lon_step, j_lon_step){
a_lat = coords[0][0] + 3*i_lat_step - 1*j_lat_step;
a_lon = coords[0][1] + 3*i_lon_step - 1*j_lon_step;
b_lat = coords[1][0] + 3*i_lat_step + 1*j_lat_step;
b_lon = coords[1][1] + 3*i_lon_step + 1*j_lon_step;
c_lat = coords[1][0] + 1*i_lat_step + 3*j_lat_step;
c_lon = coords[1][1] + 1*i_lon_step + 3*j_lon_step;
d_lat = coords[2][0] - 1*i_lat_step + 3*j_lat_step;
d_lon = coords[2][1] - 1*i_lon_step + 3*j_lon_step;
e_lat = coords[2][0] - 3*i_lat_step + 1*j_lat_step;
e_lon = coords[2][1] - 3*i_lon_step + 1*j_lon_step;
f_lat = coords[3][0] - 3*i_lat_step - 1*j_lat_step;
f_lon = coords[3][1] - 3*i_lon_step - 1*j_lon_step;
g_lat = coords[3][0] - 1*i_lat_step - 3*j_lat_step;
g_lon = coords[3][1] - 1*i_lon_step - 3*j_lon_step;
h_lat = coords[0][0] + 1*i_lat_step - 3*j_lat_step;
h_lon = coords[0][1] + 1*i_lon_step - 3*j_lon_step;

return [[a_lat, a_lon],[b_lat, b_lon],[c_lat, c_lon],[d_lat, d_lon],
[e_lat, e_lon],[f_lat, f_lon],[g_lat, g_lon],[h_lat, h_lon]]
}
