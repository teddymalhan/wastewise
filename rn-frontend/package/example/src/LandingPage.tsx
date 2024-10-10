import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { Routes } from './Routes';

type Props = NativeStackScreenProps<Routes, 'LandingPage'>;

export function LandingPage({ navigation }: Props): React.ReactElement {
  return (
    <View style={styles.container}>
      <Text style={styles.wasteWiseText}>waste-wise</Text>
      <Button
        title="Start Scan"
        onPress={() => navigation.navigate('CameraPage')} // Navigate to CameraPage on button press
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  wasteWiseText: {
    fontSize: 30,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
});
