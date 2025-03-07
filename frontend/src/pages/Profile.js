import React, { useEffect, useState } from "react";
import { api } from "../api";
import { getToken } from "../utils";

const Profile = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = getToken();
        const response = await api.get("/users/1", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUser(response.data);
      } catch (error) {
        console.error("Error fetching user:", error); 
      }
    };

    fetchUser();
  }, []);

  return user ? <div>Welcome, {user.username}</div> : <div>Loading...</div>;
};

export default Profile;
