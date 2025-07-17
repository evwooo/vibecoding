const express = require('express');
const cors = require('cors');

const app = express();
const port = 5001;

app.use(cors());
app.use(express.json());

// Endpoint that intentionally causes a server error
app.get('/api/server-error', (req, res) => {
  res.status(500).json({ message: 'This is an intentional server error.' });
});

// Endpoint for a resource that doesn't exist
app.get('/api/not-found', (req, res) => {
    res.status(404).json({ message: 'This resource was not found.' });
});

app.listen(port, () => {
  console.log(`Server is running on port: ${port}`);
});
