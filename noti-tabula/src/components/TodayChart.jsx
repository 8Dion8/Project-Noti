import { createStore } from "solid-js/store";
import { SolidApexCharts } from "solid-apexcharts";

function TodayChart() {
    const [options] = createStore({
        chart: {
            type: "rangeBar",
            height: 500,
            width: 1000,
        },
        plotOptions: {
            bar: {
                horizontal: true,
                rangeBarGroupRows: true,
            },
        },
        xaxis: {
            type: "datetime",
        },
    });

    const apiGetData = () => {
        fetch("http://127.0.0.1:5000/today")
            .then((response) => response.json())
            .then((json) => {
                console.log(json);
            });
    };

    apiGetData()

    const [series] = createStore({
        list: [
            {
                name: "csgo",
                data: [
                    {
                        x: "Leisure",
                        y: [
                            new Date(2023, 4, 21, 0, 0, 4, 608).getTime(),
                            new Date(2023, 4, 21, 0, 10, 28, 781).getTime(),
                        ],
                    },

                    {
                        x: "Leisure",
                        y: [
                            new Date(2023, 4, 21, 0, 15, 28, 781).getTime(),
                            new Date(2023, 4, 21, 0, 17, 28, 781).getTime(),
                        ],
                    },
                ],
            },
            {
                name: "code",
                data: [
                    {
                        x: "Hobby",
                        y: [
                            new Date(2023, 4, 21, 0, 20, 4, 608).getTime(),
                            new Date(2023, 4, 21, 0, 30, 28, 781).getTime(),
                        ],
                    },
                ],
            },
        ],
    });

    return <SolidApexCharts options={options} series={series.list} />;
}

export default TodayChart;
