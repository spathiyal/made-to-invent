


$(".selection").on({

  mouseenter: function () {

    let data;
    let inventors;
    data = $(this).parents('tr:eq(0)');
    // console.log("data" , data)
    patent_number = $(data).find('td:eq(0)').text();
    inventors = $(data).find('td:eq(3)').text()
    // console.log("inventors---",inventors)

    tippy(".selection", {
      content: `<strong>  <span style="color: aqua;">${inventors}</span></strong>`,
      // allowHTML: true,
      // arrow: false,
      // delay: [1000, 200],
      // placement: "top",
      // maxWidth:1000,
      allowHTML: true,
      followCursor: false,
      animation: "scale",
      duration: 200,
      placement: "bottom",
      delay: [500, 200],

    })

  },
  mouseleave: function() {
    tippy(".selection", {
      content: 'all done',
      // allowHTML: true,
      // arrow: false,
      // delay: [1000, 200],
      // placement: "top",
      // maxWidth:1000,
      allowHTML: true,
      followCursor: false,
      animation: "scale",
      duration: 200,
      placement: "bottom",
      delay: [500, 200],

    })
  }

})

$(".selection").on({
    mouseenter: function () {
        $(this).show().closest('td').css({   height: 'auto', overflow: 'auto', textOverflow: 'unset', whiteSpace: 'nowrap' });

    },
    mouseleave: function () {
        $(this).show().closest('td').css({ height: 'auto', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' });
    }
});



$(".checkAll").click(function () {

    $('input:checkbox').not(this).prop('checked', this.checked);

});





$("input[name='select[]']").click(addSelectedPatent)

async function addSelectedPatent() {
  let data = $(this).parents('tr:eq(0)');
  patent_number = $(data).find('td:eq(0)').text()
  patent_number = patent_number.trim();

  try {
    const response = await axios.get("/add-to-dashboard", {
      params: { patent_number: patent_number },
    });
    patent_number = response.data.data;
    $(this).parents('tr').remove()
  } catch (err) {
    console.log(err);
  }
}



// source sample https://jsfiddle.net/hU89p/215/




// $('.floating-button-div').ready(function(){
//   var scrollY = window.scrollY;
//   var floatingButtonContainer = document.querySelector('.floating-button-div');
//   var scrollY = window.scrollY;


//   window.addEventListener('scroll', function() {
//     scrollY = window.scrollY;
//     floatingButtonContainer.style.top = scrollY + window.innerHeight - 50 + 'px';
//   });

// })

/**
 * ---------------------------------------
 * This demo was created using amCharts 5.
 *
 * For more information visit:
 * https://www.amcharts.com/
 *
 * Documentation is available at:
 * https://www.amcharts.com/docs/v5/
 * ---------------------------------------
 */

// // Create root and chart
// var root = am5.Root.new("chartdiv");

// // Set themes
// root.setThemes([
//   am5themes_Animated.new(root)
// ]);

// var chart = root.container.children.push(
//   am5map.MapChart.new(root, {
//     panX: "rotateX",
//     projection: am5map.geoNaturalEarth1()
//   })
// );

// // Create polygon series
// var polygonSeries = chart.series.push(
//   am5map.MapPolygonSeries.new(root, {
//     geoJSON: am5geodata_worldLow,
//     exclude: ["AQ"]
//   })
// );

// polygonSeries.mapPolygons.template.setAll({
//   tooltipText: "{name}",
//   interactive: true
// });

// polygonSeries.mapPolygons.template.states.create("hover", {
//   fill: am5.color(0x677935)
// });
