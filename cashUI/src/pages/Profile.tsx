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
interface Friends {
  friend_2: number;
}
const Profile: React.FC = () => {
  const [user, setUser] = useState<Response | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [token, setToken] = useState<string>("");
  const { id } = useParams<{ id?: string }>();
  const navigate = useNavigate();
  const [isFriend, setFriend] = useState<boolean>(false);
  const [ids, setIds] = useState<Friends[]>([]);
  const fetchToken = () => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/login");
      return null;
    }
    return token;
  };
  const addFriend = async () => {
    try {
      const result = axiosInstance.request({
        url: "/account/friends/",
        method: "post",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        data: {
          friend: id,
        },
      });
      if ((await result).status == 201) {
        navigate("/friends/");
      }
    } catch (error) {
      console.error(error);
    }
  };
  useEffect(() => {
    const fetchUser = async () => {
      try {
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
    const getFriends = async () => {
      try {
        const result = await axiosInstance.request({
          url: `/account/friends`,
          method: "get",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setIds(result.data["friends"]);
      } catch (error) {
        console.error("Failed to fetch friends", error);
      }
    };
    const token = fetchToken();
    if (!token) {
      navigate("/login");
    } else if (token) {
      setToken(token);
      fetchUser();
      getFriends();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [navigate]);
  useEffect(() => {
    const check = (arr: Friends[]) => {
      arr.map((item) => {
        if (item.friend_2 === Number(id)) {
          setFriend(true);
          console.log("True");
        }
      });
    };
    check(ids);
  }, [id, ids]);
  return (
    <>
      <Helmet>
        <title>{user?.user.name || "Loading..."}</title>
      </Helmet>
      <main className="hmain">
        <article className="cmain">
          <section className="pro">
            <img src={profile} alt="Profile" className="pro-pic" />
            {error ? (
              <p className="error-message">{error}</p>
            ) : (
              <>
                {id && (
                  <>
                    <h1 className="ex-title">ID:</h1>
                    <h1 className="exp-val">{user?.user.id || "Loading..."}</h1>
                  </>
                )}
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
                {id && !isFriend && (
                  <button className="log" onClick={addFriend}>
                    Add
                  </button>
                )}
              </>
            )}
          </section>
        </article>
      </main>
    </>
  );
};

export default Profile;
