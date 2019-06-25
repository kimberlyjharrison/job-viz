console.log('logic.js working')

var searchTerm

$('#inputText').attr('placeholder', searchTerm)


function loader() {
  $('#mapText').after('<div class="loader"></div>')
}

function enterSearch() {
    // Fetch new data each time a new sample is selected

     loader()
    $ ("#scrapeText").empty()
    $ ('#mapText').empty()

    var searchurl = 'https://job-viz.herokuapp.com/search/'+$('#inputText').val() 
    $(location).attr('href', searchurl)
    $ ("#scrapeText").append('<h3>Gathering Data for Search Term: "' + $('#inputText').val() + '"</h3>') 
  };

function mapResults() {
  $ ('#mapText').empty()
   $ ("#scrapeText").empty()
  const apiurl = 'https://job-viz.herokuapp.com/api'

 d3.json(apiurl, function(data) {
   var searchTerm = data[0].Search_Term
   $ ("#mapText").append('<h3>Showing Data for Search Term: "' + searchTerm + '"</h3>') 
 })
 
  var data = d3.json(apiurl, function(data) {
  createPoints(data)
})
};


var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
});

var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.dark",
  accessToken: API_KEY
});

var baseMaps = {
    "Street Map": streetmap,
    "Dark Map": darkmap
  };

var myMap = L.map("map", {
    center: [37.09, -95.71],
    zoom: 5,
    layers: [streetmap]
  });

function createPoints(data) {

  map.remove()
  $('#mapholder').after('<div id="map"></div>')
  

  var jobPostingsArray = [];
  for (var i = 0; i < data.length; i++) {
      var jobPosting = data[i];
      if (jobPosting.Coordinates && jobPosting.Location) {
          jobPostingsArray.push(L.marker(jobPosting.Coordinates)
              .bindPopup("<h2>" + jobPosting.Title + "</h2>" + "<h3>" + jobPosting.Company + "</h3> <hr> <h4>" + jobPosting.Location +
              "</h4> <h5>" + jobPosting.Salary_Info + "</h5> <a href=\"" + jobPosting.Link + "\" target=\"_blank\">Find Job Posting Here</a>"));
      }
  };

  var heatArray = [];
  for (var i = 0; i < data.length; i++) {
      var jobPosting = data[i];

      if (jobPosting.Location) {
        heatArray.push(jobPosting.Coordinates);
      };

      var heat = L.heatLayer(heatArray, {
        radius: 80,
        blur: 28,
        minOpacity: 0.55
      });
  };

  var zillowArray = [];
  for (var i = 0; i < zillow.length; i++) {

      if (zillow[i].lat && zillow[i].lng) {
          zillowArray.push([zillow[i].lat, zillow[i].lng])
      }

      var zillowHeat = L.heatLayer(zillowArray, {
          radius: 10,
          blur: 1,
          minOpacity: 0.2,
          gradient: {
              '.2': 'blue',
              '.4': 'green',
              '.6': 'yellow',
              '.8': 'orange',
              '.99': 'red'
          },
      });
  };


  jobPostingsLayer = L.layerGroup(jobPostingsArray);

  var overlayMaps = {
    "Job Postings": jobPostingsLayer,
    "HeatMap of Job Posts": heat,
    "Median $/sqft (Housing)": zillowHeat
  };


  var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
});

var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.dark",
  accessToken: API_KEY
});

var baseMaps = {
    "Street Map": streetmap,
    "Dark Map": darkmap
  };
  var myMap = L.map("map", {
    center: [37.09, -95.71],
    zoom: 4.5,
    layers: [streetmap, heat, jobPostingsLayer]
  });


  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(myMap);
}