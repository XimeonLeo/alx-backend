import redis from 'redis';
import util from 'util';
import kue from 'kue';
const express = require('express');

const promisify = util.promisify;
let reservationEnabled;
// create kue
const queue = kue.createQueue();

// redis client
const client = redis.createClient();
client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});


// --- express app ---
const app = express();
const hostname = 'localhost';
const port = 1245;

app.use(express.json());

// local functions
const reserveSeat = (number) => {
  client.set('available_seats', number, redis.print);
};

const getCurrentAvailableSeats = () => {
  const getAsync = promisify(client.get).bind(client);
  const seats = getAsync('available_seats');
  return seats;
};

// routes
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
})

app.get('/reserve_seat', (req, res) => {
  if (reservationEnabled === false) return res.json({ status: 'Reservation are blocked' });

  const job = queue.create('reserve_seat', {});

  job.save((err) => {
    if (err) return res.json({ status: 'Reservation failed' });
    return res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    console.log('available in process', availableSeats);

    if (availableSeats <= 0) {
      done(new Error('Not enough seats available'));
    }

    reserveSeat(Number(availableSeats) - 1);
    if (availableSeats <= 0) reservationEnabled = false;
    done();
  });
  return res.json({ status: 'Queue processing' });
});

app.listen(port, () => {
  reserveSeat(50);
  reservationEnabled = true;
  console.log(`API available on ${hostname} port ${port}`);
});

module.exports = app;
