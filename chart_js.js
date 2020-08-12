var options = {
  chart: {
    type: 'line'
  },
  series: [{
    name: 'price',
    data: [3233.337,3193.785,3191.071,3158.909,3167.382,3171.519,3167.277,3159.751]
  }],
  xaxis: {
    categories: ['09:30','10:00','12:00','13:00','14:00','15:00','15:30','16:00']
  }
}

var chart = new ApexCharts(document.querySelector("#chart"), options);

chart.render();


