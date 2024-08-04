import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Detail from "./pages/ExpenseDetail";
import Profile from "./pages/Profile";
import AddExpense from "./pages/AddExpense";
import Friends from "./pages/Friends";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/profile/:id" element={<Profile />} />
        <Route path="/friends" element={<Friends />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/add-expense" element={<AddExpense />} />
        <Route path="/expense-detail/:id" element={<Detail />} />
      </Routes>
    </BrowserRouter>
  );
}
//Make error interface
export default App;
