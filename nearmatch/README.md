# NearMatch - Hyper-local Dating App

A React Native app built with Expo that helps users discover and chat with people nearby (within 50 meters).

## Tech Stack

- **Frontend**: React Native with Expo (Managed Workflow)
- **Routing**: Expo Router (File-based routing)
- **Language**: TypeScript
- **Styling**: NativeWind (Tailwind CSS for React Native)
- **Backend**: Supabase (PostgreSQL, Authentication, Realtime)
- **Location**: expo-location with PostGIS for geospatial queries
- **Icons**: Lucide React Native

## Setup Instructions

### 1. Install Dependencies

```bash
cd nearmatch
npm install
```

### 2. Configure Supabase

1. Create a new Supabase project at https://supabase.com
2. Copy your project URL and anon key
3. Create a `.env` file:

```env
EXPO_PUBLIC_SUPABASE_URL=your_supabase_project_url
EXPO_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Setup Database

1. Go to your Supabase project SQL Editor
2. Run the SQL script from `supabase_schema.sql`
3. This will:
   - Enable PostGIS extension
   - Create `profiles` and `messages` tables
   - Set up Row Level Security (RLS) policies
   - Create the `find_nearby_users` function

### 4. Run the App

```bash
npm start
```

Then press `i` for iOS simulator or `a` for Android emulator.

## Features

- ✅ Email/Password authentication
- ✅ Location tracking (updates every 5 minutes)
- ✅ Find users within 50-meter radius using PostGIS
- ✅ Real-time chat using Supabase Realtime
- ✅ User profiles with interests

## Project Structure

```
nearmatch/
├── app/
│   ├── (auth)/
│   │   └── login.tsx
│   ├── (tabs)/
│   │   ├── home.tsx      # Discover nearby users
│   │   ├── chat.tsx      # Chat interface
│   │   └── profile.tsx   # User profile
│   ├── _layout.tsx
│   └── index.tsx
├── components/
│   └── LoadingScreen.tsx
├── contexts/
│   └── AuthContext.tsx
├── hooks/
│   └── useLocation.ts
├── lib/
│   └── supabase.ts
└── supabase_schema.sql
```

## Important Notes

- Location permissions are required for the app to function
- Users must be within 50 meters to appear in discovery
- Only users active in the last hour are shown
- All location data is stored securely in Supabase with PostGIS

