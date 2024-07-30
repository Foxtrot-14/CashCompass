import "./Home.css";
import React from "react";
import home from "../assets/home.svg"
import { useNavigate } from "react-router-dom";
const Home: React.FC = () => {
  const navigate = useNavigate();
  const login = () => {
    navigate("/login");
  };
  return (
    <>
      <main className="hmain">
        <button className="log hlog" onClick={login}>
          Login
        </button>
        <article className="cmain">
          <h1 className="htitle">CashCompass</h1>
          <img src={home} alt="back" className="mback" />
        </article>
        <article className="text">
          <p>Track, Split, and Balance with Ease Using CashCompass</p>
        </article>
      </main>
    </>
  );
};

export default Home;
