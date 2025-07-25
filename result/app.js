const express = require("express");
const { Pool } = require("pg");
const app = express();
app.use(express.static("public"));
app.get("/", async (req, res) => {
    const pool = new Pool({ user: "postgres", host: "postgres", database: "votes", password: "postgres", port: 5432 });
    const result = await pool.query("SELECT vote, COUNT(*) as count FROM votes GROUP BY vote");
    const votes = { Dogs: 0, Cats: 0 };
    let total = 0;
    result.rows.forEach(row => {
        votes[row.vote] = parseInt(row.count);
        total += parseInt(row.count);
    });
    const dogPercent = total ? ((votes.Dogs / total) * 100).toFixed(2) : 0;
    const catPercent = total ? ((votes.Cats / total) * 100).toFixed(2) : 0;
    res.send(`
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            <link rel="stylesheet" href="/css/style.css">
        </head>
        <body class="bg-dark text-white">
            <div class="container mt-5 text-center">
                <h3>Number of Votes</h3>
                <div class="list-group">
                    <div class="list-group-item fs-4" style="background-color: #ff0000; color: white;">Dogs: ${votes.Dogs} (${dogPercent}%)</div>
                    <div class="list-group-item fs-4" style="background-color: #0000ff; color: white;">Cats: ${votes.Cats} (${catPercent}%)</div>
                </div>
            </div>
        </body>
        </html>
    `);
    await pool.end();
});
const https = require("https");
const fs = require("fs");
const options = {
    cert: fs.readFileSync("/app/server.crt"),
    key: fs.readFileSync("/app/server.key")
};
https.createServer(options, app).listen(443);
