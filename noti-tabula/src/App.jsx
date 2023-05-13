import { Tab } from "@hope-ui/solid";
import MenuDrawer from "./components/Menu";
import TableMain from "./components/Table";
import TodayChart from "./components/TodayChart.jsx";
import TodayPie from "./components/TodayPie.jsx";
import WeekArea from "./components/WeekArea";

function App() {


  return (
    <>
    <WeekArea />
    <TodayPie /> <TodayChart />
    </>
      
  );
}

export default App;
