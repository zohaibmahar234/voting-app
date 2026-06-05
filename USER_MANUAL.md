# VoteNow Application - Complete User Manual

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Running the Application Locally](#running-the-application-locally)
5. [Using the Application](#using-the-application)
6. [Server Hosting Guide](#server-hosting-guide)
7. [Troubleshooting](#troubleshooting)
8. [API Documentation](#api-documentation)
9. [Advanced Configuration](#advanced-configuration)

---

## Overview

VoteNow is a full-stack voting application consisting of:
- **Frontend**: Python Flask web application serving the user interface
- **Backend**: Java Spring Boot REST API handling data and business logic
- **Database**: SQLite database for data persistence

### Key Features
- 🚀 Create polls in seconds
- 📱 Mobile-responsive design
- 🔗 Share polls via links or QR codes
- 📊 Real-time voting results with charts
- 🔒 Anonymous voting (no registration required)
- 👥 Admin panel for poll management

---

## System Requirements

### Prerequisites
- **Python 3.7 or higher**
- **Java 17 or higher**
- **Maven 3.6 or higher** (for building the backend)
- **Modern web browser** (Chrome 60+, Firefox 60+, Safari 12+, Edge 79+)

### Hardware Requirements
- **RAM**: Minimum 2GB, Recommended 4GB
- **Storage**: 500MB free space
- **Network**: Internet connection for package downloads during installation

---

## Installation Guide

### Step 1: Download and Extract
1. Download or clone the VoteNow application
2. Extract to your desired directory (e.g., `C:\votenow\` or `/home/user/votenow/`)

### Step 2: Install Python Dependencies
```bash
# Navigate to the frontend directory
cd voting-frontend

# Install required Python packages
pip install -r requirements.txt
```

### Step 3: Install Java Dependencies
```bash
# Navigate to the backend directory
cd voting-backend

# Build the Spring Boot application
mvn clean install
```

---

## Running the Application Locally

### Quick Start (Recommended)

#### Option 1: Automated Startup Script
```bash
# From the root directory
python start_votenow.py
```
This script will:
- Install Python dependencies automatically
- Start the Flask frontend on port 5000
- Display helpful startup information

#### Option 2: PowerShell Script (Windows)
```powershell
# From the root directory
.\start-servers.ps1
```

#### Option 3: Manual Startup

**Step 1: Start the Backend (Java Spring Boot)**
```bash
cd voting-backend
mvn spring-boot:run
```
The backend will start on `http://localhost:8080`

**Step 2: Start the Frontend (Python Flask)**
```bash
cd voting-frontend
python app.py
```
The frontend will start on `http://localhost:5000`

### Accessing the Application
Once both servers are running:
1. Open your web browser
2. Navigate to `http://localhost:5000`
3. You should see the VoteNow homepage

---

## Using the Application

### For Poll Creators

#### Creating a New Poll
1. **Access the Application**: Go to `http://localhost:5000`
2. **Click "Create Poll"** on the homepage
3. **Fill in Poll Details**:
   - Enter your question (e.g., "What is your favorite programming language?")
   - Add 2-4 answer options
   - Click "Create Poll"
4. **Share Your Poll**:
   - Copy the generated link
   - Share the QR code (great for mobile users)
   - Send the poll ID to participants

#### Managing Polls (Admin Features)
1. **Access Admin Panel**: Navigate to `http://localhost:5000/admin`
2. **View All Polls**: See a list of all created polls
3. **Reset Votes**: Clear all votes for a specific poll
4. **Add Candidates**: Add new options to existing polls

### For Voters

#### Joining a Poll
1. **From Homepage**: Click "Join Poll" and enter the poll ID or full link
2. **Via Direct Link**: Click on the shared poll link
3. **Via QR Code**: Scan the QR code with your phone camera

#### Casting Your Vote
1. Review the poll question and options
2. Select your preferred option
3. Click "Vote"
4. View the confirmation page

#### Viewing Results
- Results are displayed immediately after voting
- Real-time updates as new votes come in
- Beautiful charts showing vote distribution
- Detailed statistics with percentages

---

## Server Hosting Guide

### Production Deployment

#### Option 1: Cloud Hosting (Recommended)

**For Small to Medium Applications:**

1. **Using Heroku**
   ```bash
   # Install Heroku CLI
   # Create Procfile for frontend:
   echo "web: python app.py" > voting-frontend/Procfile
   
   # Deploy frontend
   cd voting-frontend
   git init
   heroku create your-app-name-frontend
   git add .
   git commit -m "Deploy frontend"
   git push heroku main
   
   # Deploy backend similarly
   cd ../voting-backend
   # Create Procfile: echo "web: java -jar target/voting-1.0.0.jar" > Procfile
   ```

2. **Using DigitalOcean/AWS/Google Cloud**
   - Create a virtual server (minimum 1GB RAM)
   - Install Java 17 and Python 3.7+
   - Upload your application files
   - Follow the local installation steps
   - Configure reverse proxy (nginx) for production

#### Option 2: VPS/Dedicated Server

**Server Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Java 17
sudo apt install openjdk-17-jdk -y

# Install Python 3 and pip
sudo apt install python3 python3-pip -y

# Install Maven
sudo apt install maven -y

# Clone/upload your application
# Follow installation guide above
```

**Production Configuration:**
1. **Environment Variables**: Set production database URLs, ports, etc.
2. **Reverse Proxy**: Use nginx to serve the application
3. **SSL Certificate**: Use Let's Encrypt for HTTPS
4. **Process Management**: Use systemd or PM2 to keep services running

#### Option 3: Docker Deployment

**Frontend Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY voting-frontend/ .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
```

**Backend Dockerfile:**
```dockerfile
FROM openjdk:17-jdk-slim

WORKDIR /app
COPY voting-backend/target/voting-1.0.0.jar app.jar

EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  backend:
    build: ./voting-backend
    ports:
      - "8080:8080"
    
  frontend:
    build: ./voting-frontend
    ports:
      - "5000:5000"
    depends_on:
      - backend
```

### Domain and SSL Setup

1. **Domain Configuration**: Point your domain to your server's IP
2. **SSL Certificate**: 
   ```bash
   # Using Let's Encrypt
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```
3. **Nginx Configuration**: Configure reverse proxy for both frontend and backend

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Port already in use"
**Solution:**
```bash
# Find process using the port
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux

# Kill the process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                # macOS/Linux
```

#### Issue: "Module not found" errors
**Solution:**
```bash
# Reinstall Python dependencies
cd voting-frontend
pip install --upgrade -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

#### Issue: Java compilation errors
**Solution:**
```bash
# Clean and rebuild
cd voting-backend
mvn clean
mvn compile
mvn install
```

#### Issue: Database connection errors
**Solution:**
1. Check if `voting.db` file exists in the backend directory
2. Ensure SQLite permissions are correct
3. Restart the backend application

#### Issue: CORS errors in browser
**Solution:**
- Backend includes CORS configuration
- If issues persist, check that frontend is accessing backend on correct port (8080)

### Performance Issues

#### Slow Loading
1. **Check system resources**: Ensure adequate RAM and CPU
2. **Database optimization**: For large datasets, consider upgrading to PostgreSQL
3. **Network issues**: Check internet connection for external dependencies

#### High Memory Usage
1. **Java Backend**: Adjust JVM heap size: `java -Xmx512m -jar app.jar`
2. **Python Frontend**: Monitor with `htop` or Task Manager

### Logging and Debugging

#### Backend Logs
```bash
# View Spring Boot logs
cd voting-backend
mvn spring-boot:run | tee application.log
```

#### Frontend Logs
```bash
# Enable Flask debug mode
export FLASK_DEBUG=1  # Linux/macOS
set FLASK_DEBUG=1     # Windows
python app.py
```

---

## API Documentation

### Backend REST API Endpoints

#### Vote Management
- **GET** `/api/votes` - Get all votes
- **POST** `/api/votes` - Cast a vote
  ```json
  {
    "candidateId": 1,
    "userId": "user123"
  }
  ```

#### Candidate Management
- **GET** `/api/candidates` - Get all candidates
- **POST** `/api/candidates` - Create new candidate
  ```json
  {
    "name": "Candidate Name"
  }
  ```

#### Admin Functions
- **POST** `/api/admin/reset-votes` - Reset all votes
- **GET** `/api/admin/candidates` - Get candidates with vote counts

### Frontend Routes
- **/** - Homepage
- **/create** - Create new poll
- **/poll/<id>** - View/vote on poll
- **/results/<id>** - View poll results
- **/admin** - Admin panel

---

## Advanced Configuration

### Environment Variables

#### Backend Configuration
```bash
# Database configuration
SPRING_DATASOURCE_URL=jdbc:sqlite:voting.db

# Server port
SERVER_PORT=8080

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:5000
```

#### Frontend Configuration
```bash
# Flask settings
FLASK_ENV=production
FLASK_DEBUG=false

# Backend API URL
BACKEND_URL=http://localhost:8080

# Security
SECRET_KEY=your-secret-key-here
```

### Database Migration

To switch from SQLite to PostgreSQL:

1. **Update pom.xml** (backend):
```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
</dependency>
```

2. **Update application.properties**:
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/voting
spring.datasource.username=your-username
spring.datasource.password=your-password
```

### Scaling Considerations

#### Load Balancing
- Use nginx or Apache as load balancer
- Deploy multiple backend instances
- Share session state via Redis

#### Database Optimization
- Add database indexes for frequently queried columns
- Implement connection pooling
- Consider read replicas for heavy read loads

---

## Support and Contributing

### Getting Help
1. **Check Logs**: Review application logs for error messages
2. **Common Issues**: Refer to the troubleshooting section
3. **System Requirements**: Verify all prerequisites are met

### Contributing
The VoteNow application is open source. Contributions are welcome:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

### License
This project is available under the MIT License.

---

*Last updated: $(date)*
*For additional support, please check the project repository or create an issue.*
