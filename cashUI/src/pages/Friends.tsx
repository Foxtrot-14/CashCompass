import React, { useRef, useEffect, useState } from "react";
import "./Friends.css";
import Friend from "../components/Friend";
import axiosInstance from "../Request";
import { useNavigate } from "react-router-dom";

interface User {
  email: string;
  id: number;
  name: string;
  phone: string;
}
interface FriendData {
  user: User;
}
interface Friends {
  friend_2: number;
}

const Friends: React.FC = () => {
  const navigate = useNavigate();
  const [isVisible, setIsVisible] = useState<boolean>(false);
  const [query, setQuery] = useState<string>("");
  const [users, setUsers] = useState<User[]>([]);
  const [token, setToken] = useState<string | null>(null);
  const [ids, setIds] = useState<Friends[]>([]);
  const [friends, setFriends] = useState<FriendData[]>([]);
  const sectionRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/login");
      return;
    }
    setToken(token);

    const getFriends = async () => {
      try {
        const result = await axiosInstance.request({
          url: `/account/friends/`,
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

    getFriends();
  }, [navigate]);

  useEffect(() => {
    if (!ids.length) return;

    const getUsers = async () => {
      try {
        const userRequests = ids.map((id) =>
          axiosInstance.request({
            url: `/account/user/${id.friend_2}`,
            method: "get",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })
        );
        const responses = await Promise.all(userRequests);
        const friendsData = responses.map((response) => response.data);
        setFriends(friendsData);
      } catch (error) {
        console.error("Failed to fetch users", error);
      }
    };

    getUsers();
  }, [ids, token]);

  const handleClickOutside = (event: MouseEvent): void => {
    if (
      sectionRef.current &&
      !sectionRef.current.contains(event.target as Node)
    ) {
      setIsVisible(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleChange = async () => {
    try {
      const result = await axiosInstance.request({
        url: `/account/search-user/?q=${query}`,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUsers(result.data["users"]);
      setIsVisible(true);
    } catch (error) {
      console.error("Failed to search users", error);
    }
  };

  return (
    <>
      <main className="hmain">
        <article className="cmain">
          <section className="contain">
            <h1>
              <input
                className="lo ainp sear"
                type="text"
                value={query}
                onChange={(e) => {
                  setQuery(e.target.value);
                  handleChange();
                }}
                placeholder="Add New Friend"
              />
              <button className="log" onClick={handleChange}>
                Search
              </button>
            </h1>
            {isVisible && (
              <section className="sugg" ref={sectionRef}>
                {users.map((user) => (
                  <section
                    className="sugg-cont"
                    key={user.id}
                    onClick={() => {
                      navigate(`/profile/${user.id}`);
                    }}
                  >
                    <h1 className="sugg-name">{user.name}</h1>
                    <h1 className="sugg-email">{user.email}</h1>
                  </section>
                ))}
              </section>
            )}
            <h1 className="frtitle">Your Friend List</h1>
            <section className="list">
              {friends.length > 0 ? (
                friends.map((friend, index) => (
                  <Friend
                    key={index}
                    id={friend.user.id}
                    name={friend.user.name}
                    email={friend.user.email}
                    phone={friend.user.phone}
                  />
                ))
              ) : (
                <h1 className="quick non">You don't have any friends</h1>
              )}
            </section>
          </section>
        </article>
      </main>
    </>
  );
};

export default Friends;
