import React, { useState } from 'react';
import { LogBox } from 'react-native';
import * as Font from 'expo-font';
import AppLoading from 'expo-app-loading';
import DrawerNav from './routes/DrawerNav';

export default function App() {

  LogBox.ignoreLogs([
    'Non-serializable values were found in the navigation state',
  ]);

  const [fontLoaded, setFontLoaded] = useState(false);

  const getFonts = () => Font.loadAsync({
    'cursive-regular': require('./assets/fonts/Yellowtail-Regular.ttf'),
  });

  if (fontLoaded){

    return (

      <DrawerNav />

    );

  } else {

    return (

      <AppLoading 
        startAsync= {getFonts}
        onFinish = {() => setFontLoaded(true)}
        onError = {err => console.log(err)}
      />
      
    );

  }

}



