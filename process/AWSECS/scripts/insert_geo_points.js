const fs = require('fs');
const Redis = require('ioredis');
const ngeohash = require('ngeohash');

const REDIS_HOST = process.env.REDIS_HOST

const redis = new Redis({
  host: REDIS_HOST,
  port: 6379,
  /*tls: {
    rejectUnauthorized: false, // Disable SSL verification
  },*/
});

const inputFilePath = process.argv[2];

fs.readFile(inputFilePath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading file:', err);
    return;
  }

  const pipeline = redis.pipeline(); // Start Redis pipelining
  const lines = data.split('\n'); // Split file content into lines

  lines.forEach((line) => {
    const [latStr, lonStr, lsmStr] = line.trim().split(/\s+/); // Split line into components
    const lat = parseFloat(latStr);
    const lon = parseFloat(lonStr);
    const lsm = parseFloat(lsmStr);
    // Apply filtering logic
    if (/*lsm > 0.75 &&*/ lat <= 70.0 && lat >= -70.0) {
      const geohash = ngeohash.encode(lat, lon); // Encode latitude and longitude into geohash
      pipeline.geoadd('points', lon, lat, geohash); // Add entry to Redis pipeline
    }
  });

  // Execute the pipeline commands
  pipeline.exec()
    .then(() => {
      console.log('Data successfully added to Redis.');
      redis.quit(); // Close the Redis connection
    })
    .catch((error) => {
      console.error('Error executing pipeline:', error);
      redis.quit(); // Close the Redis connection on error
    });
});

