import React from "react";
import "./Friend.css";
import friend from "../assets/friend.svg";
const Friend: React.FC = () => {
  return (
    <article className="friend-card">
      <h1 className="ex-title">Name:</h1>
      <h1 className="exp-val">Jhon Doe</h1>
      <h1 className="ex-title">Email:</h1>
      <h1 className="exp-val">jhondoe@gmail.com</h1>
      <img src={friend} alt="img" className="friend-img" />
    </article>
  );
};

export default Friend;
