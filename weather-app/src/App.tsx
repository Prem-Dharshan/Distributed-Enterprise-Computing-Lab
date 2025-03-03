import { Routes, Route } from "react-router-dom";
import CurrentWeather from "./components/CurrentWeather";

function App() {
  return (
    <Routes>
      <Route path="/" element={<CurrentWeather />} />
    </Routes>
  );
}

export default App;
