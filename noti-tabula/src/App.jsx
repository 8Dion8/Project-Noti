import { Col, Container, Row, Nav, Button, NavDropdown } from "solid-bootstrap";
import TodayChart from "./components/TodayChart.jsx";
import TodayPie from "./components/TodayPie.jsx";
import WeekArea from "./components/WeekArea";

function App() {
  return (
    <>
      <Container fluid>
        <Nav defaultActiveKey="#" variant="tabs">
          <Nav.Link href="#">Dashboard</Nav.Link>
          <Nav.Link eventKey="2">Table</Nav.Link>
          <NavDropdown title="Trends" id="nav-dropdown">
            <NavDropdown.Item eventKey="4.1">Weekly</NavDropdown.Item>
            <NavDropdown.Item eventKey="4.2">Monthly</NavDropdown.Item>
            <NavDropdown.Item eventKey="4.3">Daily</NavDropdown.Item>
          </NavDropdown>
        </Nav>
        <Button variant="primary">Update</Button>
      </Container>
      <Container fluid>
        <Row>
          <Col lg={9}>
            <TodayChart class="chart" />
          </Col>
          <Col lg={3}>
            <TodayPie class="chart" />
          </Col>
        </Row>
        <Row>
          <Col lg={5}>
            <WeekArea class="chart" />
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default App;
