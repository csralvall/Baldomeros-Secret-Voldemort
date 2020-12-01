import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { PieChart } from "react-minimal-pie-chart";
import "./css/Profile.css";

function ProfileStats() {
  const user = useSelector((state) => state.user);
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetchProfileStats();
  }, []);

  const fetchProfileStats = async () => {
    const url = "http://181.165.189.87:8000";

    await fetch(url + `/game/history?user_id=${user.id}`, {
      method: "POST",
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Didn't find user");
          } else {
            alert("Could not fetch profile info. Unknown Error.");
          }
        } else {
          setStats(responseData);
          console.log(responseData);
          console.log(responseData.record.length);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div className="stats-module">
      <h1 className="profile-info-title">Profile Statistics</h1>
      {stats.winrates === undefined ||
      (stats.record !== undefined && stats.record.length === 0) ? (
        <h1 className="profile-stats-msg">No matches on record</h1>
      ) : (
        <div>
          <div>
            <h1 className="chart-title">Total Winrate</h1>
            <PieChart
              className="winrate-total-chart"
              data={[
                { value: stats.winrates["winrate total"], color: "#FFFFFF" },
              ]}
              totalValue={100}
              lineWidth={20}
              label={({ dataEntry }) => `${dataEntry.value}%`}
              labelStyle={{
                fontSize: "4vmin",
                fontFamily: "Harry P",
                fill: "#FFFFFF",
              }}
              labelPosition={0}
            />
          </div>
          <div className="charts-and-titles">
            <div>
              <h1 id="bottom-chart-titles" className="chart-title">
                Winrate as Voldemort
              </h1>
              <PieChart
                className="winrate-chart"
                data={[
                  {
                    value: stats.winrates["winrate as Voldemort"],
                    color: "#FFFFFF",
                  },
                ]}
                totalValue={100}
                lineWidth={20}
                label={({ dataEntry }) => `${dataEntry.value}%`}
                labelStyle={{
                  fontSize: "4vmin",
                  fontFamily: "Harry P",
                  fill: "#FFFFFF",
                }}
                labelPosition={0}
              />
            </div>
            <div>
              <h1 id="bottom-chart-titles" className="chart-title">
                Winrate as Death Eater
              </h1>
              <PieChart
                className="winrate-chart"
                data={[
                  {
                    value: stats.winrates["winrate as Death eater"],
                    color: "#FFFFFF",
                  },
                ]}
                totalValue={100}
                lineWidth={20}
                label={({ dataEntry }) => `${dataEntry.value}%`}
                labelStyle={{
                  fontSize: "4vmin",
                  fontFamily: "Harry P",
                  fill: "#FFFFFF",
                }}
                labelPosition={0}
              />
            </div>
            <div>
              <h1 id="bottom-chart-titles" className="chart-title">
                Winrate as Phoenix
              </h1>{" "}
              <PieChart
                className="winrate-chart"
                data={[
                  {
                    value: stats.winrates["winrate as Phoenix"],
                    color: "#FFFFFF",
                  },
                ]}
                totalValue={100}
                lineWidth={20}
                label={({ dataEntry }) => `${dataEntry.value}%`}
                labelStyle={{
                  fontSize: "4vmin",
                  fontFamily: "Harry P",
                  fill: "#FFFFFF",
                }}
                labelPosition={0}
              />
            </div>
          </div>
          <hr className="line" />
          <h1 className="profile-info-title">Match History</h1>
          {stats.record.map((match) => (
            <div
              className="match-history-item"
              style={{
                backgroundColor: match["amIWinner"] ? "#2c580f" : "#6e2b2b",
              }}
            >
              <h1 className="match-history-item-text">
                Match by: {match["Match name"]}
              </h1>
              <h1>Your Role: {match["secret rol"]}</h1>
              {match["winner"] === "Voldemort is the director" ||
              match["winner"] === "death eater" ? (
                <h1>Winner: Death Eaters</h1>
              ) : (
                <h1>Winner: Order of the Phoenix</h1>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
export default ProfileStats;
