import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';

// Import your error components here
import NotFound from './components/NotFound';
import ServerError from './components/ServerError';
import BrokenImages from './components/BrokenImages';
import UnresponsiveButton from './components/UnresponsiveButton';


function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <Link to="/" className="nav-logo">Website of Errors</Link>
          <ul className="nav-menu">
            <li><Link to="/404">404 Not Found</Link></li>
            <li><Link to="/500">500 Server Error</Link></li>
            <li><Link to="/broken-images">Broken Images</Link></li>
            <li><Link to="/unresponsive-ui">Unresponsive UI</Link></li>
          </ul>
        </nav>
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/404" element={<NotFound />} />
            <Route path="/500" element={<ServerError />} />
            <Route path="/broken-images" element={<BrokenImages />} />
            <Route path="/unresponsive-ui" element={<UnresponsiveButton />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

const Home = () => (
  <div className="home-container">
    <h1>Welcome to the Malfunctional Website</h1>
    <p>This website is designed to be an interactive learning tool.</p>
    <p>Select an error from the navigation bar to see it in action and learn how to prevent it.</p>
  </div>
);

export default App;