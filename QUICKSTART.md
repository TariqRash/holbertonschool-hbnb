# Quick Start Guide - Deploy HBnB on Any Device

This guide shows you how to quickly set up the HBnB application on a new device with all sample data.

## 📦 One-Command Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/TariqRash/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

### Step 2: Set Up Part 3 (Backend API)
```bash
cd part3

# Install dependencies
pip3 install -r requirements.txt

# Set up database with sample data (one command!)
./setup_database.sh

# Run the API server
python3 run.py
```

The API will be available at `http://localhost:5000`

### Step 3: Set Up Part 4 (Frontend)
```bash
# Open a new terminal
cd part4

# Start the frontend server (Python 3)
python3 -m http.server 8080
```

The frontend will be available at `http://localhost:8080`

### Step 4: Open in Browser
```
http://localhost:8080/index.html
```

## 🎉 That's It!

Your HBnB application is now running with:
- ✅ 5 users (including admin and team members)
- ✅ 4 places (Cozy Beach House, Modern City Apartment, etc.)
- ✅ 4 amenities (WiFi, Swimming Pool, Air Conditioning, Parking)
- ✅ 4 reviews from users

## 🔐 Login Credentials

### Admin Access
- **Email**: `admin@hbnb.io`
- **Password**: `admin1234`
- **Access**: Full admin panel at `http://localhost:8080/admin/`

### Regular User
- **Email**: `john@example.com`
- **Password**: `123456`
- **Access**: Regular user features

### Team Members (Test Accounts)
- **Tariq**: `Tariq@ib.com.sa`
- **Shaden**: `Shaden@ib.com.sa`
- **Norah**: `Norah@ib.com`

*(Note: Team member passwords are pre-hashed in the database)*

## 🔧 Troubleshooting

### Port 5000 Already in Use (macOS)
If you get "Address already in use" on macOS:

```bash
# Option 1: Disable AirPlay Receiver
# System Preferences → Sharing → Uncheck "AirPlay Receiver"

# Option 2: Use a different port
cd part3
python3 run.py --port 5001
# Then update part4 API URLs to use port 5001
```

### Database Doesn't Exist
If you get database errors:

```bash
cd part3
./setup_database.sh
```

### Reset Everything
To start fresh:

```bash
cd part3
rm -f instance/development.db
./setup_database.sh
```

## 📚 Features Available

### Frontend Features
- 🏠 Browse places with images, prices, ratings
- 💱 Currency converter (USD, EUR, GBP, SAR, AED, JPY, TRY)
- ⭐ Favorites system (localStorage)
- 🔍 Search and filter places
- 🌙 Dark mode toggle
- 🌐 Language switcher (English/Arabic with RTL)
- ✍️ Add reviews with character counter (150 max)
- 📤 Share places
- 🔝 Scroll-to-top button
- 🚪 Logout functionality

### Admin Panel Features (`/admin/`)
- 👥 User management (CRUD)
- 🏠 Place management (CRUD)
- ⭐ Review management (CRUD)
- ✨ Amenity management (CRUD)
- 📊 Dashboard with statistics

### API Features
- 🔐 JWT authentication
- 👤 User endpoints
- 🏠 Place endpoints
- ⭐ Review endpoints
- ✨ Amenity endpoints
- 📖 Swagger documentation at `http://localhost:5000/api/v1/docs`

## 🗂️ Sample Data Included

### Places
1. **Cozy Beach House** - $150/night
   - Miami Beach location
   - WiFi, Swimming Pool, Air Conditioning

2. **Modern City Apartment** - $95/night
   - Downtown location
   - WiFi, Air Conditioning

3. **Mountain Retreat Cabin** - $200/night
   - Colorado mountains
   - WiFi only

4. **Luxury Penthouse Suite** - $450/night
   - Los Angeles downtown
   - All amenities

### Users
- **Admin HBnB** (administrator)
- **John Doe** (regular user with reviews)
- **Tariq Almutairi** (team member)
- **Shaden Almansour** (team member)
- **Norah Alskran** (team member)

## 🚀 Development Workflow

### Making Changes
```bash
# Backend changes (part3)
cd part3
# Edit Python files
python3 run.py  # Test changes

# Frontend changes (part4)
cd part4
# Edit HTML/CSS/JS files
# Refresh browser to see changes
```

### Pushing Changes
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### Pulling on Another Device
```bash
cd holbertonschool-hbnb
git pull origin main
cd part3
./setup_database.sh  # Reset database with latest data
```

## 📞 Support

For issues or questions:
- Check `part3/DATABASE.md` for detailed database info
- Check `part4/README.md` for frontend features
- Review API docs at `http://localhost:5000/api/v1/docs`

---

**Team**: Tariq Almutairi, Shaden Almansour, Norah Alskran  
**Repository**: https://github.com/TariqRash/holbertonschool-hbnb  
**Project**: Holberton School HBnB - Airbnb Clone
