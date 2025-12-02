import { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert, ScrollView } from 'react-native';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/lib/supabase';
import { LogOut, Save } from 'lucide-react-native';
import { useRouter } from 'expo-router';

export default function ProfileScreen() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [gender, setGender] = useState('');
  const [interests, setInterests] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (user) {
      loadProfile();
    }
  }, [user]);

  const loadProfile = async () => {
    if (!user) return;

    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', user.id)
        .single();

      if (error && error.code !== 'PGRST116') throw error; // PGRST116 = not found

      if (data) {
        setUsername(data.username || '');
        setGender(data.gender || '');
        setInterests(data.interests?.join(', ') || '');
      } else {
        // Create profile if doesn't exist
        await supabase.from('profiles').insert({
          id: user.id,
          username: user.email?.split('@')[0] || 'User',
        });
      }
    } catch (err) {
      console.error('Error loading profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const saveProfile = async () => {
    if (!user) return;

    try {
      setSaving(true);
      const interestsArray = interests
        .split(',')
        .map((i) => i.trim())
        .filter((i) => i.length > 0);

      const { error } = await supabase
        .from('profiles')
        .upsert({
          id: user.id,
          username,
          gender: gender || null,
          interests: interestsArray.length > 0 ? interestsArray : null,
        });

      if (error) throw error;

      Alert.alert('Success', 'Profile updated!');
    } catch (err: any) {
      Alert.alert('Error', err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      router.replace('/(auth)/login');
    } catch (err: any) {
      Alert.alert('Error', err.message);
    }
  };

  if (loading) {
    return (
      <View className="flex-1 bg-gray-900 items-center justify-center">
        <Text className="text-white">Loading profile...</Text>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-gray-900">
      <View className="p-6">
        <Text className="text-white text-3xl font-bold mb-6">Profile</Text>

        <View className="bg-gray-800 rounded-xl p-6 mb-4">
          <Text className="text-gray-400 text-sm mb-2">Username</Text>
          <TextInput
            className="bg-gray-700 rounded-lg px-4 py-3 text-white mb-4"
            value={username}
            onChangeText={setUsername}
            placeholder="Enter username"
            placeholderTextColor="#9CA3AF"
          />

          <Text className="text-gray-400 text-sm mb-2">Gender</Text>
          <TextInput
            className="bg-gray-700 rounded-lg px-4 py-3 text-white mb-4"
            value={gender}
            onChangeText={setGender}
            placeholder="male, female, other, prefer_not_to_say"
            placeholderTextColor="#9CA3AF"
          />

          <Text className="text-gray-400 text-sm mb-2">Interests (comma-separated)</Text>
          <TextInput
            className="bg-gray-700 rounded-lg px-4 py-3 text-white"
            value={interests}
            onChangeText={setInterests}
            placeholder="tech, music, sports..."
            placeholderTextColor="#9CA3AF"
            multiline
          />
        </View>

        <TouchableOpacity
          className="bg-teal-500 rounded-lg py-4 items-center mb-4 flex-row justify-center"
          onPress={saveProfile}
          disabled={saving}
        >
          <Save size={20} color="white" className="mr-2" />
          <Text className="text-white font-semibold text-lg">Save Profile</Text>
        </TouchableOpacity>

        <TouchableOpacity
          className="bg-red-500 rounded-lg py-4 items-center flex-row justify-center"
          onPress={handleSignOut}
        >
          <LogOut size={20} color="white" className="mr-2" />
          <Text className="text-white font-semibold text-lg">Sign Out</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

