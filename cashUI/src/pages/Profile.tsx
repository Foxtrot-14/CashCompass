import React, { useEffect, useState } from "react";
import { Helmet } from "react-helmet";
import { useParams, useNavigate } from "react-router-dom";
import profile from "../assets/profile.svg";
import "./Profile.css";
import axiosInstance from "../Request";

interface User {
  email: string;
  id: number;
  name: string;
  phone: string;
}
interface Response {
  user: User;
}
const Profile: React.FC = () => {
  const [user, setUser] = useState<Response | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("access");
        if (!token) {
          navigate("/login");
          return;
        }
        const url = id ? `account/user/${id}` : "account/user/";
        const result = await axiosInstance.get(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(result.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
        setError("Failed to load user data. Please try again later.");
      }
    };

    fetchUser();
  }, [id, navigate]);

  return (
    <>
      <Helmet>
        <title>Profile Page</title>
      </Helmet>
      <main className="hmain">
        <article className="cmain">
          <section className="pro">
            <img src={profile} alt="Profile" className="pro-pic" />
            {error ? (
              <p className="error-message">{error}</p>
            ) : (
              <>
                <h1 className="ex-title">Name:</h1>
                <h1 className="exp-val">{user?.user.name || "Loading..."}</h1>
                <h1 className="ex-title">Email:</h1>
                <h1 className="exp-val">{user?.user.email || "Loading..."}</h1>
                <h1 className="ex-title">Phone:</h1>
                <h1 className="exp-val">{user?.user.phone || "Loading..."}</h1>
                {!id && (
                  <button
                    className="log"
                    onClick={() => {
                      navigate("/friends");
                    }}
                  >
                    Friends
                  </button>
                )}
                {id && <button className="log">Add</button>}
              </>
            )}
          </section>
        </article>
      </main>
    </>
  );
};

export default Profile;
