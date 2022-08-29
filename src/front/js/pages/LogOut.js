import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { Link } from "react-router-dom";

export const Logout = () => {
    localStorage.removeItem('jwt-token')
    
    return <div>
       <h1> Log Out </h1>
       <button className="btn btn-primary" onClick={Logout}> Log Out</button>
    </div>
}