var interval; // Variable to store the interval ID
var dom = document.getElementById("chart-container");
var myChart = echarts.init(dom, null, {
  renderer: "canvas",
  useDirtyRect: false,
});

var option;

function updateChart(data) {
  option = {
    xAxis: {
      type: "category",
      data: ["Total Power","WH", "Oven", "IC"],
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: data,
        type: "bar",
      },
    ],
  };

  if (option && typeof option === "object") {
   myChart.setOption(option);
   }
}

interval = setInterval(function () {
  fetch("/update_chart", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ switch_state: "always on" }),
  })
    .then((response) => response.json())
    .then((data) => updateChart(data));
}, 1000);