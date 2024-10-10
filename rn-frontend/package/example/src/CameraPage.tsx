import React, { useRef, useEffect, useState } from 'react'
import { StyleSheet, View, Text } from 'react-native'
import { Camera, useCameraDevices } from 'react-native-vision-camera'

export function CameraPage(): React.ReactElement {
  const cameraRef = useRef<Camera>(null)
  const devices = useCameraDevices()
  const device = devices.find((d) => d.position === 'back')
  const [isCameraReady, setIsCameraReady] = useState(false)

  useEffect(() => {
    const checkPermissions = async () => {
      const cameraPermission = await Camera.getCameraPermissionStatus()
      if (cameraPermission !== 'granted') {
        await Camera.requestCameraPermission()
      }
      setIsCameraReady(true)
    }
    checkPermissions()
  }, [])

  if (!device || !isCameraReady) {
    return (
      <View style={styles.container}>
        <Text style={styles.text}>Loading Camera...</Text>
      </View>
    )
  }

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true}
      />
      <View style={styles.overlay}>
        <Text style={styles.scanningText}>Scanning...</Text>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'black',
  },
  overlay: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: [{ translateX: -50 }, { translateY: -50 }],
    zIndex: 1,
  },
  scanningText: {
    fontSize: 24,
    color: 'white',
  },
  text: {
    color: 'white',
  },
})
