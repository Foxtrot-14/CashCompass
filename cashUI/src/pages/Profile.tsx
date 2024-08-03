import React from "react";
import { Helmet } from "react-helmet";
import profile from "../assets/profile.svg";
import "./Profile.css";
// interface User {
//   id: number;
//   name: string;
//   email: string;
//   phone: number;
//   friends: number[];
// }
const Profile: React.FC = () => {
  return (
    <>
      <Helmet>
        <title>Profile Page</title>
      </Helmet>
      <main className="hmain">
        <article className="cmain">
          <section className="pro">
            <img src={profile} alt="img" className="pro-pic" />
            <h1 className="ex-title">Name:</h1>
            <h1 className="exp-val">Jhon Doe</h1>
            <h1 className="ex-title">Email:</h1>
            <h1 className="exp-val">jhondoe@gmail.com</h1>
            <h1 className="ex-title">Phone:</h1>
            <h1 className="exp-val">123456</h1>
            <h1 className="ex-title fr">35 Friends</h1>
          </section>
        </article>
      </main>
    </>
  );
};

export default Profile;
