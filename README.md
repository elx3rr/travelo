# 🛕 Travelo - Indian Travel Agency & Cultural Exploration Platform

**Travelo** is a full-featured travel agency web application built with **Django (Python)**, **HTML5**, **CSS3**, and **Vanilla JavaScript**, connected directly to **MySQL (XAMPP)** without any virtual environment (`venv`).

---

## 🌟 Key Features

1. **Collapsible Responsive Sidebar Navigation**:
   - Quick drawer menu accessible via the **Menu** button.
   - Includes:
     - 🏠 **Home**
     - 🎒 **Tour Packages** (Filter by budget, region, duration)
     - 🛕 **Indian Culture & States** (Expandable accordion with all 12+ states grouped by North, South, West, East, and North-East India)
     - 📝 **Book a Tour Package** (with realistic UPI checkout)
     - 📍 **Office Branches & HQ** (Address Directory)
     - 📞 **Contact Us**
     - 🖼️ **Customize Image Links** (Direct link to central image catalog file)
     - 🛡️ **Admin Dashboard** (Django + MySQL)

2. **Indian State Cultural Exploration**:
   - Deep-dive guides for Indian states: **Rajasthan, Kerala, Jammu & Kashmir, Goa, Himachal Pradesh, Tamil Nadu, West Bengal, Maharashtra, Punjab, Assam & North-East, Gujarat, Karnataka**.
   - For every state, discover:
     - 👗 **Traditional Attire & Textiles** (with authentic photos)
     - 🍛 **Authentic Cuisine & Gastronomy** (with food photos & signature dishes)
     - 💃 **Folk Dances & Living Festivals** (with cultural photos)
     - 🏰 **Iconic Heritage Sites & Landmarks**
     - 📸 **High-Resolution Photo Gallery**
     - 🎒 **Tour Packages in this State**

3. **Realistic UPI Payment Option**:
   - Dynamic **NPCI UPI QR Code** generation (`upi://pay?pa=travelo@icici&pn=...`).
   - Direct 1-tap launcher buttons for **Google Pay**, **PhonePe**, **Paytm**, and **BHIM**.
   - Copy UPI VPA (`travelo@icici`) with instant copy notification.
   - **5-Minute Live Countdown Timer** for payment security.
   - **12-Digit UTR / Transaction Reference ID** entry field with **"⚡ Auto-Generate UTR"** for instant demo verification.
   - Generates official printable **Booking Confirmation Voucher** with verified UPI badge.

4. **OTP Authentication Method (Registration & Login)**:
   - **Tourist Registration via OTP**: User enters Name, Mobile, Email, and Password -> Receives 6-digit OTP -> Auto-advancing digit boxes -> Account activated!
   - **Passwordless 1-Click Login via OTP**: Enter registered Mobile/Email -> Receive OTP -> Instant login!
   - **On-Screen Simulated SMS Notification Banner**: Pops up in the top-right corner with the 6-digit OTP code and a "Copy Code" button, and logs to terminal console for seamless testing without paid SMS gateways.
   - Standard password login is also supported.

5. **Centralized Image Links File**:
   - As requested, all images on the site are cataloged in a single HTML file:
     `travelo_app/templates/travelo_app/image_links.html` (and `travelo_app/image_config.py`).
   - Accessible at `/image-links/` in your browser.
   - Easily swap any photo URL (Hero banners, State attire/cuisine/dances, tour package covers) in this one file!

6. **MySQL Database (XAMPP)**:
   - Direct connection to XAMPP MariaDB/MySQL (`travelo_db` on `127.0.0.1:3306`).
   - Pre-configured MariaDB compatibility patches for Django.
   - All bookings, user accounts, OTP records, inquiries, and state data are safely stored in MySQL.

---

## 🚀 How to Run the Website

### Step 1: Start MySQL in XAMPP
Open your **XAMPP Control Panel** and click **Start** next to **MySQL** (Default port `3306`, user `root`, blank password).

### Step 2: Run the Automated Database Setup
Open PowerShell or Command Prompt in the project folder and run:

```powershell
python setup_db.py
```

This single command will:
- Check connection to XAMPP MySQL.
- Automatically create the `travelo_db` database if not present.
- Run all Django migrations.
- Seed initial data (12 Indian states, curated packages, sample reviews).
- Create the administrator account (`admin` / `admin123`).

### Step 3: Start the Website
```powershell
python manage.py runserver
```

### Step 4: Open in Your Browser
- 🌐 **Travelo Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 🖼️ **Image Links Catalog**: [http://127.0.0.1:8000/image-links/](http://127.0.0.1:8000/image-links/)
- 🛡️ **Django Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
  - **Username**: `admin`
  - **Password**: `admin123`

---

## 🎨 Changing Images

To change any image on the website:
1. Open `travelo_app/templates/travelo_app/image_links.html` or `travelo_app/image_config.py`.
2. Replace any `src="..."` or URL string with your desired image URL or local static path (`/static/...`).
3. To update database records for packages or state banners, run:
   ```powershell
   python manage.py update_images
   ```

---

## 📂 Project Architecture

```
travelo/
├── setup_db.py                # Automated MySQL (XAMPP) database initialization script
├── manage.py                  # Django CLI runner
├── travelo_project/
│   ├── settings.py            # MySQL database configuration & context processors
│   ├── urls.py                # Main project URL routing
│   ├── wsgi.py
│   └── asgi.py
├── travelo_app/
│   ├── models.py              # StateCulture, Package, Booking, OTPVerification, UserProfile
│   ├── views.py               # Views for OTP, UPI Booking, Culture Explorer, Search
│   ├── urls.py                # Routing for app & OTP APIs
│   ├── forms.py               # BookingForm (with UPI), RegistrationForm, LoginForm
│   ├── image_config.py        # Centralized image dictionary
│   ├── context_processors.py  # Global state & image injector
│   ├── tests.py               # Unit tests (10/10 passing)
│   ├── management/commands/
│   │   ├── seed_data.py       # Initial data seeder
│   │   └── update_images.py   # One-command image updater
│   └── templates/travelo_app/
│       ├── base.html          # Base layout with sidebar, navbar & SMS toast
│       ├── home.html          # Landing page with cultural spotlight
│       ├── packages.html      # Tour package catalog & filters
│       ├── package_detail.html# Day-by-day itinerary & inclusions
│       ├── culture_list.html  # Indian state culture explorer
│       ├── state_detail.html  # State deep-dive (Attire, Food, Dance, Heritage)
│       ├── booking.html       # Dynamic price calculation & Realistic UPI modal
│       ├── booking_confirmation.html # Verified UPI payment voucher
│       ├── register.html      # 6-digit OTP registration
│       ├── login.html         # Dual-tab Password / OTP login
│       ├── profile.html       # Tourist profile & booked trips
│       ├── contact.html       # Working contact form (saves to MySQL)
│       ├── address.html       # HQ & branch offices directory
│       ├── image_links.html   # Centralized image links file
│       └── search.html        # Global search
└── static/travelo_app/
    ├── css/style.css          # Modern Indian heritage stylesheet
    └── js/main.js             # Sidebar drawer & interactive helpers
```
