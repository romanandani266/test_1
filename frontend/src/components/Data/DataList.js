import React, { useEffect, useState } from "react";
import { api } from "../../api";
import { getToken } from "../../utils";

const DataList = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = getToken();
        const response = await api.get("/data", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>Data List</h2>
      <ul>
        {data.map((item) => (
          <li key={item.id}>{item.content}</li>
        ))}
      </ul>
    </div>
  );
};

export default DataList;
