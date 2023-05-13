import { createStore } from "solid-js/store";
import { SolidApexCharts } from "solid-apexcharts";

function WeekArea() {
  const apiGetData = () => {
    fetch("http://127.0.0.1:5000/week/area")
      .then((response) => response.json())
      .then((json) => {
        setSeries({
          list: json.series,
        });
      });
  };

  const date_list = [];
  const today = new Date();
  for (let i = 6; i > -1; i--) {
    date_list.push(today - i * 86400000);
  }

  console.log(date_list);

  const [options] = createStore({
    options: {
      chart: {
        type: "area",
        background: "#3c3836",
        foreColor: "#ebdbb2",
        height: "100%",
        width: "100%",
      },
      stroke: {
        curve: "smooth",
      },
      colors: [
        "#83a598",
        "#458588",
        "#689d6a",
        "#d65d0e",
        "#fabd2f",
        "#7c6f64",
        "#504945",
      ],

      xaxis: {
        type: "datetime",
        categories: date_list,
      },
      fill: {
        opacity: 0.1,
        type: "solid",
      },
      dataLabels: {
        enabled: false,
      },
    },
  });

  const [series, setSeries] = createStore({
    list: [
      {
        name: "2023-05-06",
        data: [4, 1, 2, 1, 4, 5, 2, 5, 4, 2, 3, 1, 3, 6, 4],
      },
      {
        name: "2023-05-07",
        data: [5, 3, 2, 5, 3, 6, 3, 1, 2, 3, 4, 6, 5, 6, 6],
      },
    ],
  });

  apiGetData();

  return <SolidApexCharts series={series.list} options={options.options} />;
}

export default WeekArea;
