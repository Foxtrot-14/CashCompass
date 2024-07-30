import { useState } from "react";
import React from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../Request";
import { Helmet } from "react-helmet";
import login from "../assets/login.svg";
import "./LogIn.css";
const Auth: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const result = await axiosInstance.request({
        url: "account/login/",
        method: "post",
        data: {
          email: email,
          password: password,
        },
      });
      localStorage.setItem("access", result.data.access);
      localStorage.setItem("refresh", result.data.refresh);
      navigate("/dashboard");
    } catch (error: any) {
      setError(error.response.data.error || "An unexpected error occurred");
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
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
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
              <button type="submit" className="log">
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
export default Auth;
