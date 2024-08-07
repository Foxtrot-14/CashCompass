import React from "react";
import "./Friend.css";
import friend from "../assets/friend.svg";
interface User {
  email: string;
  id: number;
  name: string;
  phone: string;
}
const Friend: React.FC<User> = (user: User) => {
  const handleClick = () => {
    window.open(`/profile/${user.id}`, "_blank", "noopener,noreferrer");
  };
  return (
    <article className="friend-card" onClick={handleClick}>
      <h1 className="ex-title">Name:</h1>
      <h1 className="exp-val">{user.name}</h1>
      <h1 className="ex-title">Email:</h1>
      <h1 className="exp-val">{user.email}</h1>
      <img src={friend} alt="img" className="friend-img" />
    </article>
  );
};

export default Friend;
