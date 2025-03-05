import { Routes, Route } from "react-router-dom";
import CurrentWeather from "./components/CurrentWeather";
import Dashboard from "./components/Dashboard";
import Cuisines from "./pages/Cuisines";
import Searched from "./pages/Searched";
import Home from "./pages/Home";
import Recipe from "./pages/Recipe";

function App() {

  return (
    <>
      
      <div className="pt-16">
        <Routes>
          {/* Existing routes */}
          <Route path="/current" element={<CurrentWeather />} />
          <Route path="/dashboard" element={<Dashboard />} />

          {/* Recipe-related routes */}
          <Route path="/home" element={<Home />} />
          <Route path="/cuisines/:type" element={<Cuisines />} />
          <Route path="/searched/:search" element={<Searched />} />
          <Route path="/recipe/:id" element={<Recipe />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
