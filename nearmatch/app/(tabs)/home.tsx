import { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, RefreshControl, Image } from 'react-native';
import { useAuth } from '@/contexts/AuthContext';
import { useLocation } from '@/hooks/useLocation';
import { supabase, Profile } from '@/lib/supabase';
import { RefreshCw, MapPin } from 'lucide-react-native';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const { user } = useAuth();
  const { location, loading: locationLoading, refreshLocation } = useLocation();
  const [nearbyUsers, setNearbyUsers] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (location && user) {
      findNearbyUsers();
    }
  }, [location, user]);

  const findNearbyUsers = async () => {
    if (!location || !user) return;

    try {
      setLoading(true);
      
      // Call the PostGIS function to find nearby users
      const point = `POINT(${location.longitude} ${location.latitude})`;
      
      const { data, error } = await supabase.rpc('find_nearby_users', {
        user_location: point,
        radius_meters: 50,
      });

      if (error) {
        console.error('Error finding nearby users:', error);
        // Fallback: use direct query if function doesn't exist
        const { data: profiles, error: queryError } = await supabase
          .from('profiles')
          .select('*')
          .neq('id', user.id)
          .not('location', 'is', null)
          .limit(20);

        if (!queryError && profiles) {
          setNearbyUsers(profiles as Profile[]);
        }
      } else {
        setNearbyUsers(data || []);
      }
    } catch (err) {
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    await refreshLocation();
    await findNearbyUsers();
  };

  if (locationLoading) {
    return (
      <View className="flex-1 bg-gray-900 items-center justify-center">
        <Text className="text-white text-lg">Getting your location...</Text>
      </View>
    );
  }

  if (!location) {
    return (
      <View className="flex-1 bg-gray-900 items-center justify-center px-6">
        <MapPin size={48} color="#4FD1C7" />
        <Text className="text-white text-xl font-semibold mt-4 text-center">
          Location permission required
        </Text>
        <Text className="text-gray-400 text-center mt-2">
          Please enable location services to find people nearby
        </Text>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-gray-900">
      {/* Header */}
      <View className="bg-gray-800 pt-12 pb-4 px-4 border-b border-gray-700">
        <View className="flex-row items-center justify-between">
          <View>
            <Text className="text-white text-2xl font-bold">NearMatch</Text>
            <Text className="text-gray-400 text-sm">People within 50m</Text>
          </View>
          <TouchableOpacity
            onPress={handleRefresh}
            disabled={loading}
            className="bg-teal-500 rounded-full p-3"
          >
            <RefreshCw size={20} color="white" />
          </TouchableOpacity>
        </View>
      </View>

      {/* Nearby Users List */}
      <FlatList
        data={nearbyUsers}
        keyExtractor={(item) => item.id}
        refreshControl={
          <RefreshControl
            refreshing={loading}
            onRefresh={handleRefresh}
            tintColor="#4FD1C7"
          />
        }
        contentContainerClassName="p-4"
        ListEmptyComponent={
          <View className="items-center justify-center py-20">
            <Text className="text-gray-400 text-lg">No one nearby</Text>
            <Text className="text-gray-500 text-sm mt-2">
              Try refreshing or moving to a different location
            </Text>
          </View>
        }
        renderItem={({ item }) => (
          <TouchableOpacity
            className="bg-gray-800 rounded-xl p-4 mb-3 flex-row items-center border border-gray-700"
            onPress={() => router.push(`/(tabs)/chat?userId=${item.id}`)}
          >
            <View className="w-16 h-16 rounded-full bg-teal-500 items-center justify-center mr-4">
              {item.avatar_url ? (
                <Image
                  source={{ uri: item.avatar_url }}
                  className="w-16 h-16 rounded-full"
                />
              ) : (
                <Text className="text-white text-xl font-bold">
                  {item.username?.[0]?.toUpperCase() || '?'}
                </Text>
              )}
            </View>
            <View className="flex-1">
              <Text className="text-white text-lg font-semibold">
                {item.username}
              </Text>
              {item.interests && item.interests.length > 0 && (
                <Text className="text-gray-400 text-sm mt-1">
                  {item.interests.slice(0, 3).join(', ')}
                </Text>
              )}
            </View>
            <View className="items-end">
              <Text className="text-teal-400 text-xs">Nearby</Text>
            </View>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

