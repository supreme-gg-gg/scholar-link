import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

const NavBar = () => {
  return (
    <div className="navbar bg-base-300">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost normal-case text-xl">Connected Papers</Link>
      </div>
      <div className="flex-none">
        <ul className="menu menu-horizontal px-1">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/">About</Link></li>
          <li><Link to="/contact">Pricing</Link></li>
        </ul>
      </div>
    </div>
  );
};

export default NavBar;