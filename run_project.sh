# Change directory to server and reindex Elasticsearch
cd server
# Install Python dependencies
pip install -r requirements.txt
flask reindex

# Run Flask server
start "" flask run
cd ..

# Change directory to frontend and install npm dependencies
cd frontend
npm install

# Run npm start
npm start
