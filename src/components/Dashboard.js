import React, { useEffect, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/stats")
      .then((response) => setStats(response.data))
      .catch((error) => console.error("Error fetching stats:", error));
  }, []);

  if (!stats) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>SEO Статистика</h1>
      <div>
        <p><strong>Всего посещений:</strong> {stats.total_visits}</p>
        <p><strong>Уникальных страниц:</strong> {stats.unique_pages}</p>
      </div>
      <h2>Посещения по датам</h2>
      <table>
        <thead>
          <tr>
            <th>Дата</th>
            <th>Количество посещений</th>
          </tr>
        </thead>
        <tbody>
          {stats.visits_by_date.map((entry) => (
            <tr key={entry.date}>
              <td>{entry.date}</td>
              <td>{entry.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
