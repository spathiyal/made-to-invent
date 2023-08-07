$$ = function () {
  return document.querySelectorAll.apply(document, arguments);
}
for (var i in $$('canvas')) {
  canvas = $$('canvas')[i];
  canvas.width = canvas.width + 100
  canvas.height = canvas.height + 100
}


let patents = []
let count = [];
let issuedDate = []
const counts = {};

$("table > tbody > tr").each(function () {


  patent_num = $(this).find('td').eq(0).text();
  issued = $(this).find('td').eq(2).text();
  patents.push(patent_num.trim())

  issuedDate.push(issued.slice(7, 11))


});
issuedDate = issuedDate.sort()
issuedDate.forEach(function (x) { counts[x] = (counts[x] || 0) + 1; });

var key = [];
var value = [];
// key.push(0)
// value.push(0)
for (var property in counts) {

  if (!counts.hasOwnProperty(property)) {
    continue;
  }

  key.push(property);
  value.push(counts[property]);

}




new Chart(document.getElementById("chartdiv1"), {

  type: 'bar',
  data: {
    labels: key,
    datasets: [
      {
        label: "Number of Patents issued per year",
        backgroundColor: 'rgb(0,99,132)',
        borderColor: "#c45850",
        // barPercentage: 0.5,
        // barThickness: 2,
        // maxBarThickness: 8,
        // minBarLength: 2,
        data: value
      }
    ]
  }, options: {
    barThickness: 1,
    responsive: false, // Instruct chart js to respond nicely.
    scales: {
      yAxes: [{
        display: true,
        ticks: {
          beginAtZero: true,

          min: 0
        }
      }],
      xAxes: [{
        display: true,
        ticks: {
          beginAtZero: true,

          min: 0
        }
      }],
    },
  },

});


new Chart(document.getElementById("chartdiv2"), {

  type: 'bar',
  data: {
    labels: key,
    datasets: [
      {
        label: "Number of Patents issued per year",
        backgroundColor: 'rgb(0,99,132)',
        borderColor: "#c45850",
        // barPercentage: 0.5,
        // barThickness: 2,
        // maxBarThickness: 8,
        // minBarLength: 2,
        data: value
      }
    ]
  }, options: {
    barThickness: 1,
    responsive: false, // Instruct chart js to respond nicely.
    scales: {
      yAxes: [{
        display: true,
        ticks: {
          beginAtZero: true,

          min: 0
        }
      }],
      xAxes: [{
        display: true,
        ticks: {
          beginAtZero: true,

          min: 0
        }
      }],
    },
  },

});


