import React, { useEffect, useState } from "react";
import api from "../../api";
import { handleApiError } from "../../utils";

const EntityList = () => {
  const [entities, setEntities] = useState([]);

  useEffect(() => {
    api
      .get("/entities")
      .then((response) => setEntities(response.data))
      .catch(handleApiError);
  }, []);

  return (
    <div>
      <h1>Entities</h1>
      <ul>
        {entities.map((entity) => (
          <li key={entity.id}>{entity.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default EntityList;