import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '@/contexts/AuthContext';
import { LogIn } from 'lucide-react-native';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { signIn, signUp } = useAuth();
  const router = useRouter();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter email and password');
      return;
    }

    try {
      setLoading(true);
      await signIn(email, password);
      router.replace('/(tabs)/home');
    } catch (error: any) {
      Alert.alert('Login Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSignUp = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter email and password');
      return;
    }

    try {
      setLoading(true);
      await signUp(email, password);
      Alert.alert('Success', 'Account created! Please check your email to verify.');
    } catch (error: any) {
      Alert.alert('Sign Up Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1 bg-gradient-to-b from-blue-900 to-teal-800 items-center justify-center px-6">
      <View className="w-full max-w-md">
        <Text className="text-4xl font-bold text-white mb-2 text-center">NearMatch</Text>
        <Text className="text-blue-200 text-center mb-8">Find people nearby</Text>

        <View className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
          <TextInput
            className="bg-white/20 rounded-lg px-4 py-3 text-white mb-4"
            placeholder="Email"
            placeholderTextColor="#A0AEC0"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />

          <TextInput
            className="bg-white/20 rounded-lg px-4 py-3 text-white mb-6"
            placeholder="Password"
            placeholderTextColor="#A0AEC0"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />

          <TouchableOpacity
            className="bg-teal-500 rounded-lg py-4 items-center mb-4"
            onPress={handleLogin}
            disabled={loading}
          >
            <Text className="text-white font-semibold text-lg">Login</Text>
          </TouchableOpacity>

          <TouchableOpacity
            className="bg-orange-500 rounded-lg py-4 items-center"
            onPress={handleSignUp}
            disabled={loading}
          >
            <Text className="text-white font-semibold text-lg">Sign Up</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

