import React, { useEffect, useState } from "react";
import "./ExpenseDetail.css";
import { useNavigate, useParams } from "react-router-dom";
import One from "../assets/one-expense.svg";
import { Helmet } from "react-helmet";
import axiosInstance from "../Request";
interface Participant {
  participant: number;
  contribution: number;
}
interface Expense {
  id: number;
  title: string;
  description: string;
  admin: number;
  type: number;
  cost: number;
  created_at: string;
}
interface Participant {
  participant: number;
  contribution: number;
}
interface Response {
  expense: Expense;
  participants: Participant[];
}
const data: Response = {
  expense: {
    id: 23,
    title: "Office Supplies",
    description: "Purchase of office supplies including pens and paper.",
    admin: 2,
    type: 3,
    cost: 200,
    created_at: "2024-07-29T14:17:40.736516+05:30",
  },
  participants: [
    {
      participant: 3,
      contribution: 50.0,
    },
    {
      participant: 4,
      contribution: 100.0,
    },
    {
      participant: 2,
      contribution: 50.0,
    },
  ],
};
const ExpenseDetail: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<string>();
  const [response, setResponse] = useState<Response>();
  const [token, setToken] = useState<string>("");
  useEffect(() => {
    const getAccess = () => {
      try {
        const token = localStorage.getItem("access");
        if (!token) {
          navigate("/login");
          return;
        }
        setToken(token);
      } catch (error: unknown) {
        console.error(error);
      }
    };
    getAccess();
  }, [navigate]);
  useEffect(() => {
    const fetchExp = async () => {
      const result = await axiosInstance.request({
        url: `/api/expense/${id}`,
        method: "get",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setResponse(result.data);
      console.log(result);
    };
    fetchExp();
  }, [id, token, navigate]);
  const result: Response = data;
  return (
    <>
      <Helmet>
        <title>{result.expense.title} | Expense Details</title>
      </Helmet>
      <main className="hmain">
        <article className="cmain">
          <section className="button-group">
            <button className="log balance">Get Balance Sheet</button>
            <button className="log">Delete</button>
          </section>
          <section className="container">
            <img src={One} alt="img" className="detail-img" />
            <section>
              <h1 className="ex-title">Title</h1>
              <h1 className="exp-val">{response?.expense.title}</h1>
              <h1 className="ex-title">Total Cost</h1>
              <h1 className="exp-val">{response?.expense.cost}</h1>
              <h1 className="ex-title">Type</h1>
              <h1 className="exp-val">
                {response?.expense.type === 1
                  ? "Equal"
                  : response?.expense.type === 2
                  ? "Exact"
                  : response?.expense.type === 3
                  ? "Percentage"
                  : "Unknown"}
              </h1>
              <h1 className="ex-title">Admin</h1>
              <h1 className="exp-val">{response?.expense.admin}</h1>
              <h1 className="ex-title">Description</h1>
              <h1 className="exp-val">{response?.expense.description}</h1>
              <h1 className="ex-title">Created At</h1>
              <h1 className="exp-val">
                {response?.expense.created_at
                  .substring(0, 9)
                  .split("-")
                  .reverse()
                  .join("-")}
              </h1>
            </section>
            <section className="participants-container">
              {response?.participants.map((participant: Participant) => (
                <section>
                  <h1 className="ex-title">Participant</h1>
                  <h1 className="exp-val">{participant.participant}</h1>
                  <h1 className="ex-title">Contribution</h1>
                  <h1 className="exp-val">{participant.contribution}</h1>
                </section>
              ))}
            </section>
          </section>
        </article>
      </main>
    </>
  );
};

export default ExpenseDetail;
