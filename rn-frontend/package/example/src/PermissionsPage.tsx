import type { NativeStackScreenProps } from '@react-navigation/native-stack'
import React, { useCallback, useEffect, useState } from 'react'
import type { CameraPermissionStatus } from 'react-native-vision-camera'
import { Camera } from 'react-native-vision-camera'
import { StyleSheet, View, Text, ImageBackground, Linking } from 'react-native'
import type { Routes } from './Routes'

const bg1 = require('./bg1.jpg') // Adjust path if needed

type Props = NativeStackScreenProps<Routes, 'PermissionsPage'>
export function PermissionsPage({ navigation }: Props): React.ReactElement {
  const [cameraPermissionStatus, setCameraPermissionStatus] = useState<CameraPermissionStatus>('not-determined')

  // Function to request camera permission
  const requestCameraPermission = useCallback(async () => {
    const permission = await Camera.requestCameraPermission()

    if (permission === 'denied') {
      await Linking.openSettings()
    }
    setCameraPermissionStatus(permission)
  }, [])

  useEffect(() => {
    // Navigate to LandingPage once the permission is granted
    if (cameraPermissionStatus === 'granted') {
      navigation.replace('LandingPage')
    }
  }, [cameraPermissionStatus, navigation])

  return (
    <ImageBackground source={bg1} style={styles.background}>
      <View style={styles.container}>
        <Text style={styles.wasteWiseText}>waste-wise</Text>
        <View style={styles.permissionsContainer}>
          {cameraPermissionStatus !== 'granted' && (
            <Text style={styles.permissionText}>
              Allow <Text style={styles.bold}>camera permission</Text> for WasteWise.{' '}
              <Text style={styles.hyperlink} onPress={requestCameraPermission}>
                Grant
              </Text>
            </Text>
          )}
        </View>
      </View>
    </ImageBackground>
  )
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  wasteWiseText: {
    fontSize: 30,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  permissionsContainer: {
    marginTop: 20,
  },
  permissionText: {
    fontSize: 17,
    textAlign: 'center',
  },
  hyperlink: {
    color: '#007aff',
    fontWeight: 'bold',
  },
  bold: {
    fontWeight: 'bold',
  },
})
