import { createStore } from "solid-js/store";
import { SolidApexCharts } from "solid-apexcharts";

function TableMain() {
    const [options] = createStore({
        chart: {
            type: "rangeBar",
            height: 500,
            width: 1000,
        },
        plotOptions: {
            bar: {
                horizontal: true,
            },
        },
        xaxis: {
            type: "datetime",
        },
        yaxis: {
            type: "datetime",
        }
    });

    const [series] = createStore({
        list: [
            {
                name: 'csgo',
                data: [
                    {
                        x: "2023-04-20",
                        y: [
                            new Date(2023, 4, 21, 0, 0, 4, 608).getTime(),
                            new Date(2023, 4, 21, 0, 10, 28, 781).getTime(),
                        ],
                        
                    },
                    {
                        x: "2023-04-21",
                        y: [
                            
                        ],
                        
                    },
                    {
                        x: "2023-04-22",
                        y: [
                            new Date(2023, 4, 21, 0, 0, 4, 608).getTime(),
                            new Date(2023, 4, 22, 0, 10, 28, 781).getTime(),
                        ],
                        
                    },
                    {
                        x: "2023-04-23",
                        y: [
                            new Date(2023, 4, 21, 0, 0, 4, 608).getTime(),
                            new Date(2023, 4, 21, 0, 10, 28, 781).getTime(),
                        ],
                        
                    },
                    
                    {
                        x: "2023-04-24",
                        y: [
                            new Date(2023, 4, 21, 0, 15, 28, 781).getTime(),
                            new Date(2023, 4, 21, 0, 19, 28, 781).getTime(),
                        ],
                    },
                ],
            },
        ],
    });

    return <SolidApexCharts options={options} series={series.list} />;
}

export default TableMain;
