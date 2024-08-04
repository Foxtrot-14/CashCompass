import { useState, ChangeEvent } from "react";
import "./AddExpense.css";
import { Helmet } from "react-helmet";
const AddExpense: React.FC = () => {
  const [participant, setParticipant] = useState<number>(1);
  const [type, setType] = useState<string>("");
  const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = event.target.value;
    setType(selectedValue);
  };
  const handleAdd = () => {
    setParticipant(participant + 1);
  };
  const inputFields = [];
  for (let i = 1; i <= participant; i++) {
    inputFields.push(
      <>
        <h3>{`${i}`}</h3>
        <input
          className="lo ainp"
          type="text"
          required
          placeholder="Enter Name"
        />
        {type !== "1" && (
          <input
            className="lo ainp"
            type="number"
            required
            placeholder="Enter Contribution"
          />
        )}
      </>
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
          <form className="form">
            <section className="expense">
              <input
                className="lo ainp"
                type="text"
                required
                placeholder="Enter Title"
              />
              <select
                className="dropdown"
                id="type"
                value={type}
                onChange={handleChange}
              >
                <option value="">Select Type</option>
                <option value="1" className="dropdown">
                  Equal
                </option>
                <option value="2" className="dropdown">
                  Exact
                </option>
                <option value="3" className="dropdown">
                  Percentage
                </option>
              </select>
              <br />
              <textarea
                className="lo ainp desc"
                required
                placeholder="Enter Desctiption"
              />
              <br />
              <input
                className="lo ainp"
                type="number"
                required
                placeholder="Enter Total Cost"
              />
              <br />
            </section>
            <section className="add-list">
              <h1 className="quick lo par">Participants</h1>
              {inputFields}
            </section>
            <button className="log" onClick={handleAdd}>
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
