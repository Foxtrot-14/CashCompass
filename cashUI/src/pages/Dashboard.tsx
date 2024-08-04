import { useEffect, useState } from "react";
import React from "react";
import "./Dashboard.css";
import Card from "../components/Card";
import { Helmet } from "react-helmet";
import axiosInstance from "../Request";
import image from "../assets/expenses-page.svg";
import { useNavigate } from "react-router-dom";

interface Expense {
  id: number;
  title: string;
  description: string;
  admin: number;
  type: number;
  cost: number;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [expenses, setExpenses] = useState<Expense[] | undefined>(undefined);

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        const token = localStorage.getItem("access");
        if (!token) {
          navigate("/login");
          return; // Exit early if there's no token
        }
        const result = await axiosInstance.request({
          url: "api/expense/",
          method: "get",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setExpenses(result.data.expenses);
      } catch (error: unknown) {
        console.error(error);
      }
    };
    fetchExpenses();
  }, [navigate]);

  return (
    <>
      <Helmet>
        <title>Dashboard</title>
      </Helmet>
      <main className="back">
        <section className="cont">
          <h1 className="htitle">
            <img src={image} className="exp-img" alt="Expenses" />
            Your Expenses
          </h1>
          <section className="exp-container">
            {expenses &&
              expenses.map((item) => (
                <Card
                  key={item.id}
                  title={item.title}
                  cost={item.cost}
                  id={item.id}
                />
              ))}
          </section>
          <button className="add-button log">Add New</button>
          <button className="search-button log">Profile</button>
        </section>
      </main>
    </>
  );
};

export default Dashboard;
