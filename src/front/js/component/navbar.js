import React from "react";
import { Link } from "react-router-dom";


export const Navbar = () => {
  return (
    <nav className="navbar navbar-light bg-light">
      <div className="container">
        <Link to="/Signup">
          <span className="navbar-brand mb-0 h1">React Boilerplate</span>
        </Link>
        <div className="ml-auto">
          <Link to="/demo">
            <button className="btn btn-primary">
              Check the Context in action
            </button>
          </Link>
        </div>
        <button><Link to="/SignUp"> Sign Up </Link> </button>
		<button><Link to="/Login"> Log In </Link> </button>
    <button><Link to="/Private"> Private </Link> </button>
    <button><Link to="/Logout"> Log Out </Link> </button>
      </div>
    </nav>
  );
};
