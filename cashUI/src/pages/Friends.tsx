import React from "react";
// import { useParams } from "react-router-dom";
import "./Friends.css";
import Friend from "../components/Friend";
const Friends: React.FC = () => {
  //   const { id } = useParams();
  return (
    <>
      <main className="hmain">
        <article className="cmain">
          <section className="contain">
            <h1>
              <input
                className="lo ainp sear"
                type="text"
                required
                placeholder="Add New Friend"
              />
              <button className="log">Search</button>
            </h1>
            <h1 className="frtitle">Your Friend List</h1>
            <section className="list">
              <Friend />
              <Friend />
              <Friend />
              <Friend />
              <Friend />
              <Friend />
              <Friend />
              <Friend />
              <Friend />
            </section>
          </section>
        </article>
      </main>
    </>
  );
};

export default Friends;
