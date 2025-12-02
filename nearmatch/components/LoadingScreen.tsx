import React from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Lightbulb, Rocket, Code, BarChart3, Compass, Cog } from 'lucide-react-native';

export function LoadingScreen() {
  return (
    <LinearGradient
      colors={['#1e3a8a', '#0f766e', '#1e3a8a']}
      style={styles.container}
    >
      {/* Animated Elements Container */}
      <View style={styles.contentContainer}>
        
        {/* Lightbulb Icon - Center */}
        <View style={styles.lightbulbContainer}>
          <Lightbulb 
            size={80} 
            color="#FFA500" 
            style={styles.lightbulb}
          />
        </View>

        {/* Rocket - Above lightbulb */}
        <View style={styles.rocketContainer}>
          <Rocket 
            size={40} 
            color="#FF6B35" 
            style={{ transform: [{ rotate: '-45deg' }] }}
          />
        </View>

        {/* Floating Elements */}
        {/* Top Left - Gears */}
        <View style={styles.topLeft}>
          <Cog size={24} color="#4FD1C7" />
        </View>

        {/* Top Right - Code */}
        <View style={styles.topRight}>
          <Code size={24} color="#4FD1C7" />
        </View>

        {/* Bottom Left - Chart */}
        <View style={styles.bottomLeft}>
          <BarChart3 size={24} color="#FFA500" />
        </View>

        {/* Bottom Right - Compass */}
        <View style={styles.bottomRight}>
          <Compass size={24} color="#4FD1C7" />
        </View>

        {/* Loading Indicator */}
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#4FD1C7" />
          <Text style={styles.loadingText}>
            Loading NearMatch...
          </Text>
          <Text style={styles.subText}>
            Finding people near you
          </Text>
        </View>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  contentContainer: {
    width: '100%',
    height: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  lightbulbContainer: {
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'center',
  },
  lightbulb: {
    shadowColor: '#FFA500',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 20,
    elevation: 10,
  },
  rocketContainer: {
    position: 'absolute',
    top: -80,
    alignItems: 'center',
  },
  topLeft: {
    position: 'absolute',
    top: 128,
    left: 32,
  },
  topRight: {
    position: 'absolute',
    top: 128,
    right: 32,
  },
  bottomLeft: {
    position: 'absolute',
    bottom: 128,
    left: 32,
  },
  bottomRight: {
    position: 'absolute',
    bottom: 128,
    right: 32,
  },
  loadingContainer: {
    position: 'absolute',
    bottom: 192,
    alignItems: 'center',
  },
  loadingText: {
    color: '#81E6D9',
    fontSize: 18,
    fontWeight: '600',
    marginTop: 16,
  },
  subText: {
    color: '#BFDBFE',
    fontSize: 14,
    marginTop: 8,
  },
});
