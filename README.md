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

## Deployment on Render

This application is configured for easy deployment on Render.com:

1. Fork or clone this repository
2. Connect your GitHub account to Render
3. Create a new Web Service in Render
4. Select "Deploy from GitHub repo"
5. Choose this repository
6. Select "Docker" as the environment
7. Click "Create Web Service"

Render will automatically detect the Dockerfile and deploy the application.

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
   flask run
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
