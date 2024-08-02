import React from "react";
import "./Dashboard.css";
import Card from "../components/Card";
import { Helmet } from "react-helmet";
import image from "../assets/expenses-page.svg";
const Dashboard: React.FC = () => {
  return (
    <>
      <Helmet>
        <title>Dashboard</title>
      </Helmet>
      <main className="back">
        <section className="cont">
          <h1 className="htitle">
            <img src={image} className="exp-img" />
            Your Expenses
          </h1>
          <section className="exp-contianer">
            <Card title="Office Expenses" cost="2000" />
            <Card title="Shopping for Fun" cost="1000" />
            <Card title="Gaming and Clothes" cost="500" />
            <Card title="Grocery and Dail" cost="2000" />
            <Card title="Office Expenses" cost="2000" />
          </section>
          <button className="add-button log">Add New</button>
        </section>
      </main>
    </>
  );
};

export default Dashboard;
