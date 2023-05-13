import { Container, Row, Col } from "solid-bootstrap";
import TodayChart from "./components/TodayChart.jsx";
import TodayPie from "./components/TodayPie.jsx";
import WeekArea from "./components/WeekArea";

function App() {


  return (
    <>
      <Container fluid>
        <Row>
          <Col><TodayChart class="chart"/></Col>
        </Row>
        <Row>
          <Col xs={2}><TodayPie class="chart"/></Col>
          <Col xs={10}><WeekArea class="chart"/></Col>
        </Row>
      </Container >
    </>
      
  );
}

export default App;
