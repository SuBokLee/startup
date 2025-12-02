import { useState, useEffect, useRef } from 'react';
import { Platform } from 'react-native';
import * as Location from 'expo-location';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/contexts/AuthContext';

interface LocationData {
  latitude: number;
  longitude: number;
}

export function useLocation() {
  const { user } = useAuth();
  const [location, setLocation] = useState<LocationData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Request location permissions and get initial location
  useEffect(() => {
    let isMounted = true;

    async function requestPermissionsAndGetLocation() {
      try {
        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
          if (isMounted) {
            setError('Location permission denied');
            setLoading(false);
          }
          return;
        }

        // Request background location permission for Android
        if (Platform.OS === 'android') {
          const { status: bgStatus } = await Location.requestBackgroundPermissionsAsync();
          if (bgStatus !== 'granted') {
            console.warn('Background location permission not granted');
          }
        }

        // Get initial location
        const currentLocation = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.High,
        });

        if (isMounted) {
          const loc = {
            latitude: currentLocation.coords.latitude,
            longitude: currentLocation.coords.longitude,
          };
          setLocation(loc);
          setError(null);
          setLoading(false);

          // Update location in Supabase
          if (user) {
            await updateLocationInSupabase(loc);
          }
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'Failed to get location');
          setLoading(false);
        }
      }
    }

    requestPermissionsAndGetLocation();

    return () => {
      isMounted = false;
    };
  }, [user]);

  // Update location every 5 minutes
  useEffect(() => {
    if (!user || !location) return;

    // Update immediately
    updateLocationInSupabase(location);

    // Then update every 5 minutes
    intervalRef.current = setInterval(async () => {
      try {
        const currentLocation = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.High,
        });
        const loc = {
          latitude: currentLocation.coords.latitude,
          longitude: currentLocation.coords.longitude,
        };
        setLocation(loc);
        await updateLocationInSupabase(loc);
      } catch (err) {
        console.error('Error updating location:', err);
      }
    }, 5 * 60 * 1000); // 5 minutes

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [user, location]);

  const updateLocationInSupabase = async (loc: LocationData) => {
    if (!user) return;

    try {
      // Convert to PostGIS geography point format: POINT(longitude latitude)
      const point = `POINT(${loc.longitude} ${loc.latitude})`;

      const { error } = await supabase
        .from('profiles')
        .update({
          location: point,
          last_seen: new Date().toISOString(),
        })
        .eq('id', user.id);

      if (error) {
        console.error('Error updating location:', error);
      }
    } catch (err) {
      console.error('Error updating location:', err);
    }
  };

  const refreshLocation = async () => {
    try {
      setLoading(true);
      const currentLocation = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.High,
      });
      const loc = {
        latitude: currentLocation.coords.latitude,
        longitude: currentLocation.coords.longitude,
      };
      setLocation(loc);
      setError(null);
      if (user) {
        await updateLocationInSupabase(loc);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh location');
    } finally {
      setLoading(false);
    }
  };

  return { location, error, loading, refreshLocation };
}

