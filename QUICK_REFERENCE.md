# VoteNow - Quick Reference Guide

## 🚀 Quick Start Commands

### Local Development
```bash
# Option 1: Automated (Recommended)
python start_votenow.py

# Option 2: Manual
# Terminal 1 - Backend
cd voting-backend && mvn spring-boot:run

# Terminal 2 - Frontend  
cd voting-frontend && python app.py
```

### Access Points
- **Main Application**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Backend API**: http://localhost:8080/api

---

## 📋 Common Tasks

### Creating a Poll
1. Go to http://localhost:5000
2. Click "Create Poll"
3. Enter question and 2-4 options
4. Share the generated link or QR code

### Managing Polls (Admin)
1. Go to http://localhost:5000/admin
2. View all polls and their statistics
3. Reset votes or add new candidates

### Troubleshooting
```bash
# Check if ports are in use
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux

# Reinstall dependencies
pip install -r voting-frontend/requirements.txt
cd voting-backend && mvn clean install
```

---

## 🌐 Server Hosting Quick Setup

### Basic VPS Deployment
```bash
# 1. Install prerequisites
sudo apt update && sudo apt install openjdk-17-jdk python3 python3-pip maven -y

# 2. Upload application files to server
# 3. Install dependencies
cd voting-frontend && pip install -r requirements.txt
cd ../voting-backend && mvn clean install

# 4. Start services
cd voting-backend && nohup mvn spring-boot:run &
cd ../voting-frontend && nohup python app.py &
```

### Using Docker
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Environment Variables for Production
```bash
# Backend
export SERVER_PORT=8080
export SPRING_PROFILES_ACTIVE=production

# Frontend  
export FLASK_ENV=production
export BACKEND_URL=http://your-server:8080
```

---

## 🔧 Configuration Files

### Key Files to Modify for Production
- `voting-backend/src/main/resources/application.properties` - Backend config
- `voting-frontend/app.py` - Frontend config and backend URL
- `voting-backend/pom.xml` - Java dependencies
- `voting-frontend/requirements.txt` - Python dependencies

### Default Ports
- Frontend: 5000
- Backend: 8080
- Database: SQLite file (no port)

---

## 📞 Support Checklist

Before asking for help:
- ✅ Python 3.7+ installed
- ✅ Java 17+ installed  
- ✅ Maven 3.6+ installed
- ✅ All dependencies installed successfully
- ✅ Ports 5000 and 8080 available
- ✅ No error messages in console
- ✅ Browser supports modern JavaScript

---

**Need the full manual?** See `USER_MANUAL.md` for complete installation, usage, and hosting instructions.
