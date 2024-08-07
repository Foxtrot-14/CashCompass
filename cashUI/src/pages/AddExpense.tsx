import { useState, ChangeEvent, FormEvent, useEffect } from "react";
import "./AddExpense.css";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet";
import axiosInstance from "../Request";
import axios from "axios";
interface Participant {
  participant: number;
  contribution?: number;
}

interface Request {
  title: string;
  description: string;
  cost: number;
  type: number;
  participants: Participant[];
}
const AddExpense: React.FC = () => {
  const [token, setToken] = useState<string>("");
  const [error, setError] = useState<string | null>(
    "Your contribution will be calculated automatically just add your friends"
  );
  const [partiCount, setPartiCount] = useState<number>(1);
  const [title, setTitle] = useState<string>("");
  const [desc, setDesc] = useState<string>("");
  const [cost, setCost] = useState<number | undefined>(undefined);
  const [type, setType] = useState<number>(0);
  const [participants, setParticipants] = useState<Participant[]>([
    { participant: 0 },
  ]);
  const navigate = useNavigate();
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
  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    const data: Request = {
      title,
      description: desc,
      type,
      cost: cost ?? 0,
      participants,
    };

    try {
      const result = await axiosInstance.request({
        url: "/api/expense-create/",
        method: "post",
        data: data,
        headers: { Authorization: `Bearer ${token}` },
      });

      if (result.status === 201) {
        setError("Added Successfully... redirecting");
        setTimeout(() => {
          navigate("/dashboard");
        }, 2000);
      } else {
        // Handle unexpected status codes
        setError("Unexpected response from server");
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 400) {
          setError("Server error: Don't Add yourself");
          //handle 401 for expired tokens
        } else {
          setError(`Request failed with status ${error.response?.status}`);
        }
      } else {
        // Handle unexpected errors
        setError("An unexpected error occurred");
      }
    }
  };
  const handleTypeChange = (event: ChangeEvent<HTMLSelectElement>) => {
    setType(Number(event.target.value));
  };

  const handleAdd = () => {
    setPartiCount(partiCount + 1);
    setParticipants([...participants, { participant: 0 }]);
  };

  const handleParticipantChange = (index: number, value: number) => {
    const newParticipants = [...participants];
    newParticipants[index].participant = value;
    setParticipants(newParticipants);
  };

  const handleContributionChange = (index: number, value: number) => {
    const newParticipants = [...participants];
    newParticipants[index].contribution = value;
    setParticipants(newParticipants);
  };

  const inputFields = [];
  for (let i = 0; i < partiCount; i++) {
    inputFields.push(
      <section key={i}>
        <h3>{`${i + 1}`}</h3>
        <input
          className="lo ainp"
          type="number"
          required
          onChange={(e) => handleParticipantChange(i, Number(e.target.value))}
          placeholder="Enter Name"
        />
        {type !== 1 && (
          <input
            className="lo ainp"
            type="number"
            required
            onChange={(e) =>
              handleContributionChange(i, Number(e.target.value))
            }
            placeholder="Enter Contribution"
          />
        )}
      </section>
    );
  }

  return (
    <>
      <Helmet>
        <title>Add Expense | CashCompass</title>
      </Helmet>
      <main className="hmain">
        <article className="expense-form">
          <h1 className="quick">Enter Details</h1>
          {error && <p className="error-message">{error}</p>}
          <form className="form" onSubmit={handleSubmit}>
            <section className="expense">
              <input
                className="lo ainp"
                type="text"
                required
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter Title"
              />
              <select
                className="dropdown"
                id="type"
                value={type}
                onChange={handleTypeChange}
              >
                <option value="0">Select Type</option>
                <option value="1">Equal</option>
                <option value="2">Exact</option>
                <option value="3">Percentage</option>
              </select>
              <br />
              <textarea
                className="lo ainp desc"
                required
                onChange={(e) => setDesc(e.target.value)}
                placeholder="Enter Description"
              />
              <br />
              <input
                className="lo ainp"
                type="number"
                required
                onChange={(e) => setCost(Number(e.target.value))}
                placeholder="Enter Total Cost"
              />
              <br />
            </section>
            <section className="add-list">
              <h1 className="quick lo par">Participants</h1>
              {inputFields}
            </section>
            <button type="button" className="log" onClick={handleAdd}>
              Add
            </button>
            <button type="submit" className="log sub">
              Submit
            </button>
          </form>
        </article>
      </main>
    </>
  );
};
export default AddExpense;
