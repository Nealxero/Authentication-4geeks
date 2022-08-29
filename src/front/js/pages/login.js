import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";

export const Login = () => {
  // This returns the object that we've set up previously using the provider or the store
  const { store, actions } = useContext(Context);

  // This is a hook and returns an array of [state, setState]
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const logClick = async (e) => {
    // This is necessary if we are using a form
    // Whit this we are overrinding the default behaviour of the form so it doesn't refresh
    e.preventDefault();
    const loginOptions = {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    };

    const promiseResponse = await fetch(
      "https://3002-nealxero-authentication-cf8499sax29.ws-eu63.gitpod.io/api/login",
      loginOptions,
      {
        headers: {
          "Access-Control-Allow-Origin": "*",
        },
      }
    )
      .then((resp) => resp.json())
      .then((res) => {
        alert("Login in successfull");
        return res;
      })
      .catch((error) => console.error("Something went wrong", error));

    localStorage.setItem("jwt-token", promiseResponse.token);
  };

  // Private --> useEffect that checks if the token exists, if not redirect to login
  // useNavigate -->

  return (
    <div>
      <h1> Log In </h1>
      <form>
        <div className="form-group">
          <label htmlFor="exampleInputEmail1">Email address</label>
          <input
            type="email"
            className="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <small id="emailHelp" className="form-text text-muted">
            We'll never share your email with anyone else.
          </small>
        </div>
        <div className="form-group">
          <label htmlFor="exampleInputPassword1">Password</label>
          <input
            type="password"
            className="form-control"
            id="exampleInputPassword1"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="form-check">
          <input
            type="checkbox"
            className="form-check-input"
            id="exampleCheck1"
          />
          <label className="form-check-label" htmlFor="exampleCheck1">
            Check me out
          </label>
        </div>
        <button className="btn btn-primary" onClick={(e) => logClick(e)}>
          Submit
        </button>
      </form>
    </div>
  );
};
