import React, { useState } from "react";
import login from "../assets/signup.svg";
import "./Signup.css";
import axiosInstance from "../Request";
import { Helmet } from "react-helmet";
import { useNavigate } from "react-router-dom";
const SignUp: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [phone, setPhone] = useState<string>("");
  const [password1, setPassword1] = useState<string>("");
  const [password2, setPassword2] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const result = await axiosInstance.request({
        url: "account/register/",
        method: "post",
        data: {
          email: email,
          name:name,
          phone:phone,
          password1: password1,
          password2: password2,
        },
      });
      console.log(result.data)
      setError(result.data.success);
      localStorage.setItem("access", result.data.access);
      localStorage.setItem("refresh", result.data.refresh);
      setTimeout(() => {
        navigate("/dashboard");
      }, 3000);
    } catch (error:any) {
      setError(error.response.data.error || "An unexpected error occurred");
    }
  };
  return (
    <main>
      <Helmet>
        <title>Sign Up Page</title>
      </Helmet>
      <article className="amain">
        <section className="acen">
          <img className="aside" src={login} alt="login" />
          <section className="lform">
            <h1 className="quick">Sign Up</h1>
            <form className="sigor" onSubmit={handleSubmit}>
              <input
                className="ainp"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
              />
              <br />
              <input
                className="ainp"
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your name"
              />
              <br />
              <input
                className="ainp"
                type="tel"
                required
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="Enter your phone"
              />
              <br />
              <input
                className="ainp"
                type="password"
                required
                value={password1}
                onChange={(e) => setPassword1(e.target.value)}
                placeholder="Enter your password"
              />
              <br />
              <input
                className="ainp"
                type="password"
                required
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                placeholder="Re-enter your password"
              />
              <button type="submit" className="log">
                Sign Up
              </button>
            </form>
            <h3>
              Already have an account? <a href="/login">LogIn</a>
            </h3>
            {error && <p className="error-message">{error}</p>}
          </section>
        </section>
      </article>
    </main>
  );
};
export default SignUp;
