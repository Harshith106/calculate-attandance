# Attendance Calculator

A web application that calculates attendance percentages for students by scraping data from the college portal.

## Features

- Secure login to the college portal
- Retrieval of attendance data for all courses
- Calculation of overall attendance percentage
- Calculation of attendance percentage excluding technical training
- Responsive UI for all device sizes

## Technologies Used

- Flask (Python web framework)
- Selenium (Web scraping)
- HTML/CSS/JavaScript (Frontend)
- Docker (Containerization)

## Deployment Options

### Deployment on Railway.app (Recommended)

This application is configured for easy deployment on Railway.app:

1. Fork or clone this repository
2. Sign up at [railway.app](https://railway.app/) (free tier available)
3. Install the Railway CLI (optional):
   ```
   npm i -g @railway/cli
   ```
4. Login to Railway:
   ```
   railway login
   ```
5. Create a new project:
   ```
   railway init
   ```
6. Deploy the application:
   ```
   railway up
   ```

Alternatively, you can deploy directly from the Railway dashboard:

1. Go to [railway.app](https://railway.app/) and log in
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub account and select your repository
4. Railway will automatically detect the Dockerfile and deploy the application

**Benefits of Railway.app Deployment**:

- **Generous Free Tier**: $5 credit per month
- **No Strict Timeouts**: Unlike Vercel's 10-second limit
- **Sufficient Memory**: Up to 512MB RAM in free tier
- **Container Support**: Perfect for Selenium applications
- **Easy Setup**: Simple GitHub integration

### Deployment on Render

This application can also be deployed on Render.com:

1. Fork or clone this repository
2. Connect your GitHub account to Render
3. Create a new Web Service in Render
4. Select "Deploy from GitHub repo"
5. Choose this repository
6. Select "Docker" as the environment
7. Click "Create Web Service"

Render will automatically detect the Dockerfile and deploy the application.

### Deployment on Vercel

Vercel deployment is possible but not recommended for this application due to limitations:

- **Execution Time**: Functions have a maximum execution time of 10 seconds in the free tier
- **Memory**: Limited to 1GB RAM
- **Selenium**: Running Selenium in serverless environments is challenging

## Local Development

### Prerequisites

- Python 3.9+
- Chrome browser
- Git

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/attendance-calculator.git
   cd attendance-calculator
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   # Run directly
   python api/index.py

   # OR using Flask
   flask run

   # OR using Docker
   docker build -t attendance-calculator .
   docker run -p 8080:8080 attendance-calculator
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Docker Development

1. Build the Docker image:
   ```
   docker build -t attendance-calculator .
   ```

2. Run the container:
   ```
   docker run -p 8080:8080 attendance-calculator
   ```

3. Open your browser and navigate to `http://localhost:8080`

## License

MIT
