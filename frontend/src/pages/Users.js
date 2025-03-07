import React, { useEffect, useState } from "react";
import api from "../api";
import { handleApiError } from "../utils";

const Users = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    api
      .get("/users")
      .then((response) => setUsers(response.data))
      .catch(handleApiError);
  }, []);

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.username}</li>
        ))}
      </ul>
    </div>
  );
};

export default Users;