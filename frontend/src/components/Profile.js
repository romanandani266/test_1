import React, { useEffect, useState } from "react";
import { api } from "../api";

const Profile = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await api.getProfile(token);
        setProfile(response.data);
      } catch (error) {
        alert("Failed to fetch profile!");
      }
    };
    fetchProfile();
  }, []);

  return profile ? <div>{JSON.stringify(profile)}</div> : <p>Loading...</p>;
};

export default Profile;
