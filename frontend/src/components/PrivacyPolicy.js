import React, { useEffect, useState } from "react";
import { api } from "../api";

const PrivacyPolicy = () => {
  const [policy, setPolicy] = useState("");

  useEffect(() => {
    const fetchPolicy = async () => {
      try {
        const response = await api.getPrivacyPolicy();
        setPolicy(response.data.policy);
      } catch (error) {
        alert("Failed to fetch privacy policy!");
      }
    };
    fetchPolicy();
  }, []);

  return <div>{policy}</div>;
};

export default PrivacyPolicy;
