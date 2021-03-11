var year = [2015];
var arable_land_brazil = [33.81];
var country_brazil = 'Brazil';

var arable_land_germany = [47.95];
var country_germany = 'Germany';

var arable_land_china = [56.22];
var country_china = 'China';

var trace1 = {
  x: [country_brazil, country_germany, country_china],
  y: [arable_land_brazil[0], arable_land_germany[0], arable_land_china[0]],
  type: 'bar'
};

var layout = {
  title: 'Hectares Arable Land per Person 2015',
  xaxis: {
    title: 'country',
  },
  
  yaxis: {
    title: 'hectares per person'
  }
  
};

var data = [trace1];

Plotly.newPlot('plot2', data, layout);

// var trace3 = {
//     x: [country_name_china],
//     y: [arable_land_china[0]],
//     type: 'bar',
//     name: country_name_china
//   };

// var data = [trace1, trace2, trace3];
