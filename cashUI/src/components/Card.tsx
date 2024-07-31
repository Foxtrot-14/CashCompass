import React from "react";
import "./Card.css";
import icon from "../assets/icon.svg";
interface Cardprops {
  title: string;
  cost: string;
}
const Card: React.FC<Cardprops> = (prop: Cardprops) => {
  return (
    <article className="card">
      <h1 className="ex-title">Title:</h1>
      <h1 className="exp-val">{prop.title}</h1>
      <h1 className="ex-title">Total Cost:</h1>
      <h1 className="exp-val">{prop.cost}</h1>
      <button className="exp-log">Details</button>
      <img src={icon} alt="" className="card-img" />
    </article>
  );
};

export default Card;
