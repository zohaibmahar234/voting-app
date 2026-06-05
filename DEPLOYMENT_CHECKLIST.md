# VoteNow Deployment Checklist

## Pre-Deployment Requirements

### Server Specifications
- [ ] **OS**: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+
- [ ] **RAM**: Minimum 2GB, Recommended 4GB+
- [ ] **Storage**: 10GB+ free space
- [ ] **CPU**: 2+ cores recommended
- [ ] **Network**: Public IP address and domain (optional)

### Software Prerequisites
- [ ] **Java 17+** installed and configured
- [ ] **Python 3.7+** installed with pip
- [ ] **Maven 3.6+** installed
- [ ] **Git** for code deployment
- [ ] **Nginx** (recommended for reverse proxy)
- [ ] **Certbot** (for SSL certificates)

---

## Deployment Steps

### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Java 17
sudo apt install openjdk-17-jdk -y
java -version  # Verify installation

# Install Python and pip
sudo apt install python3 python3-pip -y
python3 --version  # Verify installation

# Install Maven
sudo apt install maven -y
mvn -version  # Verify installation

# Install Nginx (optional)
sudo apt install nginx -y
```

### 2. Application Deployment
```bash
# Create application directory
sudo mkdir -p /opt/votenow
sudo chown $USER:$USER /opt/votenow
cd /opt/votenow

# Upload/clone application files
# Option 1: Upload via SCP/SFTP
# Option 2: Git clone
git clone <your-repository-url> .

# Install Python dependencies
cd voting-frontend
pip3 install -r requirements.txt

# Build Java application
cd ../voting-backend
mvn clean install
```

### 3. Service Configuration

#### Create systemd service for Backend
```bash
sudo nano /etc/systemd/system/votenow-backend.service
```

```ini
[Unit]
Description=VoteNow Backend Service
After=network.target

[Service]
Type=simple
User=votenow
WorkingDirectory=/opt/votenow/voting-backend
ExecStart=/usr/bin/java -jar target/voting-1.0.0.jar
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Create systemd service for Frontend
```bash
sudo nano /etc/systemd/system/votenow-frontend.service
```

```ini
[Unit]
Description=VoteNow Frontend Service
After=network.target votenow-backend.service

[Service]
Type=simple
User=votenow
WorkingDirectory=/opt/votenow/voting-frontend
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Start Services
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable votenow-backend
sudo systemctl enable votenow-frontend
sudo systemctl start votenow-backend
sudo systemctl start votenow-frontend

# Check status
sudo systemctl status votenow-backend
sudo systemctl status votenow-frontend
```

### 5. Nginx Configuration (Optional but Recommended)
```bash
sudo nano /etc/nginx/sites-available/votenow
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8080/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/votenow /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

### 6. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (already configured by certbot)
sudo systemctl status certbot.timer
```

---

## Production Configuration

### Environment Variables
```bash
# Create environment file
sudo nano /opt/votenow/.env
```

```bash
# Backend settings
SPRING_PROFILES_ACTIVE=production
SERVER_PORT=8080
LOGGING_LEVEL_ROOT=WARN

# Frontend settings
FLASK_ENV=production
BACKEND_URL=http://localhost:8080
SECRET_KEY=your-very-secure-secret-key-here
```

### Database Configuration (Optional: PostgreSQL)
If using PostgreSQL instead of SQLite:
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database and user
sudo -u postgres psql
CREATE DATABASE votenow;
CREATE USER votenowuser WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE votenow TO votenowuser;
\q

# Update backend configuration
# Add to application-production.properties:
spring.datasource.url=jdbc:postgresql://localhost:5432/votenow
spring.datasource.username=votenowuser
spring.datasource.password=securepassword
```

---

## Security Checklist

### Server Security
- [ ] **Firewall configured** (only allow ports 22, 80, 443)
- [ ] **SSH key authentication** enabled
- [ ] **Root login disabled**
- [ ] **Regular security updates** scheduled
- [ ] **Fail2ban** installed for SSH protection

### Application Security
- [ ] **Strong secret keys** configured
- [ ] **Database access restricted** to application user only
- [ ] **CORS properly configured**
- [ ] **Input validation** enabled
- [ ] **HTTPS enforced** in production

### Firewall Configuration
```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status
```

---

## Monitoring and Maintenance

### Log Files
```bash
# System logs
sudo journalctl -u votenow-backend -f
sudo journalctl -u votenow-frontend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backup Strategy
```bash
# Database backup (SQLite)
cp /opt/votenow/voting-backend/voting.db /backup/voting-$(date +%Y%m%d).db

# Application backup
tar -czf /backup/votenow-$(date +%Y%m%d).tar.gz /opt/votenow/
```

### Performance Monitoring
```bash
# System resources
htop
df -h
free -h

# Application status
sudo systemctl status votenow-backend votenow-frontend
curl -I http://localhost:5000  # Check frontend
curl -I http://localhost:8080/api/candidates  # Check backend
```

---

## Troubleshooting

### Common Issues

#### Services won't start
```bash
# Check logs
sudo journalctl -u votenow-backend -n 50
sudo journalctl -u votenow-frontend -n 50

# Check file permissions
sudo chown -R votenow:votenow /opt/votenow
```

#### Port conflicts
```bash
# Check what's using the port
sudo netstat -tlnp | grep :8080
sudo netstat -tlnp | grep :5000

# Kill conflicting processes if necessary
sudo kill -9 <PID>
```

#### Database issues
```bash
# Check database file permissions
ls -la /opt/votenow/voting-backend/voting.db
sudo chown votenow:votenow /opt/votenow/voting-backend/voting.db
```

### Recovery Procedures

#### Restart services
```bash
sudo systemctl restart votenow-backend
sudo systemctl restart votenow-frontend
sudo systemctl restart nginx
```

#### Rollback deployment
```bash
# Keep previous version as backup
cp -r /opt/votenow /opt/votenow-backup-$(date +%Y%m%d)
# Restore from backup if needed
```

---

## Post-Deployment Verification

### Functionality Tests
- [ ] **Homepage loads** correctly
- [ ] **Create poll** functionality works
- [ ] **Vote casting** works
- [ ] **Results display** correctly
- [ ] **Admin panel** accessible
- [ ] **Mobile interface** responsive
- [ ] **QR codes generate** properly

### Performance Tests
- [ ] **Response time** < 2 seconds
- [ ] **Concurrent users** handling tested
- [ ] **Database queries** optimized
- [ ] **Memory usage** within limits

### Security Tests
- [ ] **HTTPS enforced**
- [ ] **CSRF protection** working
- [ ] **Input validation** active
- [ ] **SQL injection** prevented
- [ ] **XSS protection** enabled

---

## Contact and Support

### Emergency Contacts
- **System Administrator**: [Your contact]
- **Developer Team**: [Team contact]
- **Hosting Provider**: [Provider support]

### Documentation Links
- **User Manual**: USER_MANUAL.md
- **Quick Reference**: QUICK_REFERENCE.md
- **API Documentation**: See USER_MANUAL.md#api-documentation

---

**Deployment completed successfully!** ✅

Your VoteNow application should now be accessible at your domain/IP address.
