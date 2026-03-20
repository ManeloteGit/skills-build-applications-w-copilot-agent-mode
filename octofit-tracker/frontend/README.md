# OctoFit Tracker Frontend

This is the React frontend for the OctoFit Tracker fitness application, built with React 18, Bootstrap 5, and integrated with a Django REST API backend.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
- [Available Scripts](#available-scripts)
- [Architecture](#architecture)
- [API Integration](#api-integration)
- [Deployment](#deployment)

## ✨ Features

- **User Authentication**: Register and login with secure token-based authentication
- **Activity Tracking**: Log workouts (running, cycling, swimming, gym, yoga, sports)
- **Dashboard**: View personalized statistics and recommendations at a glance
- **Leaderboard**: See weekly rankings and compete with other users
- **Teams**: Create teams and manage team members
- **Recommendations**: Get personalized workout suggestions based on your profile
- **User Profile**: Manage your fitness profile including height, weight, and fitness level
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 📁 Project Structure

```
frontend/
├── public/
│   ├── index.html          # HTML entry point
│   └── favicon.ico         # App icon
├── src/
│   ├── components/
│   │   ├── Navigation.js   # Top navigation bar with conditional rendering
│   │   └── ProtectedRoute.js # Route wrapper for authenticated routes
│   ├── context/
│   │   └── AuthContext.js  # Authentication context provider
│   ├── hooks/
│   │   └── useAuth.js      # Custom hook for using auth context
│   ├── pages/
│   │   ├── Home.js         # Landing page
│   │   ├── Login.js        # Login form
│   │   ├── Register.js     # Registration form
│   │   ├── Dashboard.js    # Main hub after login
│   │   ├── Activities.js   # Activity logging and management
│   │   ├── Leaderboard.js  # Competitive rankings
│   │   ├── Teams.js        # Team management
│   │   ├── Recommendations.js # Personalized suggestions
│   │   ├── Profile.js      # User profile management
│   │   └── NotFound.js     # 404 error page
│   ├── services/
│   │   └── api.js          # Centralized API client with service modules
│   ├── App.js              # Main app component with routing
│   ├── App.css             # App styling
│   ├── index.js            # React DOM render
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
├── .env.example            # Environment configuration template
└── README.md               # This file
```

## 🚀 Installation

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Backend API running (see backend README)

### Steps

1. **Navigate to the frontend directory**:
   ```bash
   cd octofit-tracker/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment configuration**:
   ```bash
   cp .env.example .env
   ```

## ⚙️ Environment Setup

Edit the `.env` file with your configuration:

```bash
REACT_APP_API_URL=http://localhost:8000/api
```

### Configuration Options

- **REACT_APP_API_URL**: Backend API base URL
  - Local: `http://localhost:8000/api`
  - Production: Your deployed API URL

## ▶️ Running the Application

### Development Server

Start the development server with hot reload:

```bash
npm start
```

The application will open at `http://localhost:3000`

### Build for Production

Create an optimized production build:

```bash
npm run build
```

The build files will be in the `build/` directory.

### Run Production Build Locally

```bash
npm install -g serve
serve -s build
```

## 📜 Available Scripts

In the project directory, you can run:

### `npm start`
Runs the app in development mode.
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.
The page will reload when you make changes.

### `npm test`
Launches the test runner in interactive watch mode.

### `npm run build`
Builds the app for production to the `build` folder.

### `npm run eject`
**Note: this is a one-way operation. Once you eject, you can't go back!**

## 🏗️ Architecture

### Authentication Flow

1. User registers or logs in
2. Backend returns authentication token
3. Token stored in browser memory (context)
4. Token added to all API request headers
5. Protected routes check authentication status
6. Unauthorized requests redirect to login

### Component Hierarchy

```
App
├── AuthProvider (Context)
├── Router
│   ├── Navigation (conditional rendering)
│   └── Routes
│       ├── Public Routes (Home, Login, Register)
│       └── Protected Routes (Dashboard, Activities, etc.)
```

### State Management

- **Auth State**: Context API (`AuthContext.js`)
- **Component State**: React Hooks (useState, useEffect)
- **Form State**: Local component state
- **API State**: Loading, error, data handling

## 🔌 API Integration

The frontend communicates with the backend through a centralized API service (`src/services/api.js`).

### Service Modules

1. **authService**: User authentication
2. **userService**: User management
3. **activityService**: Activity tracking
4. **teamService**: Team management
5. **leaderboardService**: Rankings
6. **recommendationService**: Personalized suggestions

### Making API Calls

```javascript
import { activityService } from '../services/api';

useEffect(() => {
  const fetchActivities = async () => {
    try {
      const data = await activityService.getActivities();
      setActivities(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  fetchActivities();
}, []);
```

## 📱 Pages Overview

### Home (`/`)
Landing page with features overview and call-to-action buttons.

### Login (`/login`)
User authentication form with error handling.

### Register (`/register`)
New user signup form with fitness level selection.

### Dashboard (`/dashboard`)
Main hub showing activity statistics, recommendations, and quick actions.

### Activities (`/activities`)
Complete activity management with CRUD operations.

### Leaderboard (`/leaderboard`)
Competitive rankings with user statistics.

### Teams (`/teams`)
Team management and creation interface.

### Recommendations (`/recommendations`)
Personalized fitness suggestions with filtering.

### Profile (`/profile`)
User profile management with personal and security settings.

### NotFound (`*`)
404 error page for undefined routes.

## 🔗 Connecting to Backend

### Local Development

1. Start backend on port 8000:
   ```bash
   cd octofit-tracker/backend
   python manage.py runserver 0.0.0.0:8000
   ```

2. Update `.env`:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

3. Start frontend:
   ```bash
   npm start
   ```

## 🚢 Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Other Platforms

- **Netlify**: Drop the `build/` folder
- **AWS S3 + CloudFront**: Upload `build/` to S3
- **GitHub Pages**: Push `build/` to gh-pages branch

## 🐛 Troubleshooting

### "Cannot find module" errors
```bash
rm -rf node_modules
npm install
```

### CORS errors
Ensure backend has `CORS_ALLOWED_ORIGINS` configured for frontend URL.

### 401 Unauthorized
Check that the token is stored and being sent in request headers.

### API not responding
Verify backend is running and `REACT_APP_API_URL` is correct.

## 📚 Dependencies

- **react**: UI library
- **react-router-dom**: Client-side routing
- **axios**: HTTP client
- **bootstrap**: CSS framework

## 📝 License

This project is part of the OctoFit Tracker application.
