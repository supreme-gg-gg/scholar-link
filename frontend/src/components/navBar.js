import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

const NavBar = () => {
  return (
    <div className="navbar bg-base-300 bg-white font-Fustat">
      <div className="flex-1 items-center">
        <Link to="/" className="btn btn-ghost normal-case text-3xl text-primary font-Fustat font-black">
          <img 
            src="/logo_link.png" 
            alt="Scholar Link Logo" 
            className="w-6 h-8"
          />
          scholar-link
        </Link>
      </div>
      <div className="flex-none text-black">
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