import { createStore } from "solid-js/store";
import { SolidApexCharts } from "solid-apexcharts";

function TodayPie() {
  const apiGetData = () => {
    fetch("http://127.0.0.1:5000/today/pie")
      .then((response) => response.json())
      .then((json) => {
        setSeries({
          list: json.series,
        });
        setSecs(json.series)
      });
  };
  
  const [secs, setSecs] = createStore([])

  const [series, setSeries] = createStore({
    list: [0, 0, 0, 0, 0, 0, 0],
  });
  const [options, setOptions] = createStore({
    chart: {
      type: "pie",
      background: "#3c3836",
      foreColor: "#ebdbb2",
      width: "100%",
      height: "300px"
    },
    labels: [
      "study",
      "hobby",
      "social",
      "media",
      "leisure",
      "waste",
      "uncategorised",
    ],
    colors: [
      "#83a598",
      "#458588",
      "#689d6a",
      "#d65d0e",
      "#fabd2f",
      "#7c6f64",
      "#504945",
    ],
    legend: {
      position: "bottom",
    },
    stroke: {
      width: 0,
    },
    dataLabels: {
      formatter(val, opts) {
        const name = opts.w.globals.labels[opts.seriesIndex]
        const sec_sum = secs.reduce((a, b) => a + b, 0) 
        const mins = Math.round(val * sec_sum / 6000)
        return [mins + " min"]
      }
    }
  });

  apiGetData();

  return <SolidApexCharts series={series.list} options={options} />;
}

export default TodayPie;
