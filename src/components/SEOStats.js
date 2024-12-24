import React, { useEffect, useState } from "react";
import axios from "axios";

const SEOStats = () => {
  const [visits, setVisits] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/visits")
      .then((response) => setVisits(response.data))
      .catch((error) => console.error("Error fetching visits:", error));
  }, []);

  return (
    <div>
      <h1>SEO Статистика</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>URL страницы</th>
            <th>Реферер</th>
            <th>Браузер</th>
            <th>Дата посещения</th>
          </tr>
        </thead>
        <tbody>
          {visits.map((visit) => (
            <tr key={visit.id}>
              <td>{visit.id}</td>
              <td>{visit.page_url}</td>
              <td>{visit.referrer}</td>
              <td>{visit.user_agent}</td>
              <td>{new Date(visit.visit_time).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SEOStats;
