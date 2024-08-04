import React from "react";
import "./Card.css";
import { useNavigate } from "react-router-dom";
import icon from "../assets/icon.svg";
interface Cardprops {
  id: number;
  title: string;
  cost: number;
}
const Card: React.FC<Cardprops> = (prop: Cardprops) => {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate(`expense-detail/${prop.id}`);
  };
  return (
    <article className="card">
      <h1 className="ex-title">Title:</h1>
      <h1 className="exp-val">{prop.title}</h1>
      <h1 className="ex-title">Total Cost:</h1>
      <h1 className="exp-val">{prop.cost}</h1>
      <button className="exp-log" onClick={handleClick}>
        Details
      </button>
      <img src={icon} alt="" className="card-img" />
    </article>
  );
};

export default Card;
