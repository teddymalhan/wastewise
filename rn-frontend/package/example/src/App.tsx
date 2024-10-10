import { NavigationContainer } from '@react-navigation/native'
import React, { useEffect, useState } from 'react'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { PermissionsPage } from './PermissionsPage'
import { LandingPage } from './LandingPage'
import { CameraPage } from './CameraPage'
import { CodeScannerPage } from './CodeScannerPage'
import type { Routes } from './Routes'
import { Camera } from 'react-native-vision-camera'
import { GestureHandlerRootView } from 'react-native-gesture-handler'
import { StyleSheet } from 'react-native'
import { DevicesPage } from './DevicesPage'

const Stack = createNativeStackNavigator<Routes>()

export function App(): React.ReactElement | null {
  const [cameraPermission, setCameraPermission] = useState<string | null>(null)

  // Check the camera permission status when the app loads
  useEffect(() => {
    const checkCameraPermission = async () => {
      const permission = await Camera.getCameraPermissionStatus()
      setCameraPermission(permission)
    }
    checkCameraPermission()
  }, [])

  // If permission is not checked yet, show a loading state
  if (cameraPermission === null) {
    return null // Can return a loading indicator here
  }

  // Determine whether to show PermissionsPage or LandingPage
  const showPermissionsPage = cameraPermission !== 'granted'

  return (
    <NavigationContainer>
      <GestureHandlerRootView style={styles.root}>
        <Stack.Navigator
          screenOptions={{
            headerShown: false,
            statusBarStyle: 'dark',
            animationTypeForReplace: 'push',
          }}
          initialRouteName={showPermissionsPage ? 'PermissionsPage' : 'LandingPage'}
        >
          <Stack.Screen name="PermissionsPage" component={PermissionsPage} />
          <Stack.Screen name="LandingPage" component={LandingPage} />
          <Stack.Screen name="CameraPage" component={CameraPage} />
          <Stack.Screen name="CodeScannerPage" component={CodeScannerPage} />
          <Stack.Screen name="Devices" component={DevicesPage} />
        </Stack.Navigator>
      </GestureHandlerRootView>
    </NavigationContainer>
  )
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
  },
})
