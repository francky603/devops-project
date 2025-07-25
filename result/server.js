const express = require('express');
const { Pool } = require('pg');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const pool = new Pool({
  user: process.env.DB_USER,
  host: 'db',
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: 5432
});

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

io.on('connection', async (socket) => {
  const update = async () => {
    try {
      const result = await pool.query('SELECT vote, COUNT(*) as count FROM votes GROUP BY vote');
      let aCount = 0, bCount = 0, total = 0;
      result.rows.forEach(row => {
        if (row.vote === 'a') aCount = parseInt(row.count);
        if (row.vote === 'b') bCount = parseInt(row.count);
      });
      total = aCount + bCount;
      const aPercent = total ? (aCount / total * 100) : 0;
      const bPercent = total ? (bCount / total * 100) : 0;
      socket.emit('update', { aPercent, bPercent, total });
    } catch (err) {
      console.error('Database query error:', err);
    }
  };
  update();
  setInterval(update, 5000);
});

server.listen(80, () => console.log('Listening on port 80'));
