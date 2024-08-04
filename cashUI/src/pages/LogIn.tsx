import { useState } from "react";
import React from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../Request";
import { Helmet } from "react-helmet";
import login from "../assets/login.svg";
import "./LogIn.css";

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [identifier, setIdentifier] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Prevent the default form submission behavior

    try {
      const result = await axiosInstance.request({
        url: "account/login/",
        method: "post",
        data: {
          identifier: identifier,
          password: password,
        },
      });
      if (result.status === 404) {
        setError("User Not Found");
      }
      localStorage.setItem("access", result.data.tokens.access);
      localStorage.setItem("refresh", result.data.tokens.refresh);
      navigate("/dashboard");
    } catch (error: unknown) {
      //
    }
  };
  return (
    <main>
      <Helmet>
        <title>Log In Page</title>
      </Helmet>
      <article className="amain">
        <section className="acen">
          <img className="aside" src={login} alt="login" />
          <section className="lform">
            <h1 className="quick">Log In</h1>
            <form onSubmit={handleSubmit}>
              <input
                className="lo ainp"
                type="text"
                required
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                placeholder="Enter your email or phone"
              />
              <br />
              <input
                className="lo ainp"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
              />
              <br />
              <button className="log" type="submit">
                Login
              </button>
            </form>
            <h3>
              Don't have an account? <a href="/signup">SignUp</a>
            </h3>
            {error && <p className="error-message">{error}</p>}
          </section>
        </section>
      </article>
    </main>
  );
};
export default Login;
