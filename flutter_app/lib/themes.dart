import 'package:flutter/material.dart';

class Themes {
  static ThemeData globalTheme = ThemeData.dark().copyWith(
    brightness: Brightness.dark,
    backgroundColor: Colors.black,
    scaffoldBackgroundColor: Colors.black,
    canvasColor: Colors.black,
    appBarTheme: const AppBarTheme(
      centerTitle: true,
      color: Colors.black,
    ),
    inputDecorationTheme: const InputDecorationTheme(
      // Login page input text field border colour
      enabledBorder:
          OutlineInputBorder(borderSide: BorderSide(color: Colors.orange)),
    ),
    colorScheme: ColorScheme.fromSwatch().copyWith(
        // Trying to figure out which colour is which
        primary: Colors.white,
        background: Colors.black,
        secondary: Colors.green,
        outline: Colors.red,
        onSecondary: Colors.purple,
        surface: Colors.amber),
    textTheme: const TextTheme(
      headline1: TextStyle(
        fontSize: 30.0,
        fontWeight: FontWeight.bold,
        fontFamily: 'LibreBodoni',
      ),
      headline2: TextStyle(
        fontSize: 36.0,
        fontFamily: 'LibreBodoni',
      ),
      caption: TextStyle(
        fontSize: 20.0,
        fontFamily: 'LibreBodoni',
        color: Colors.black,
      ),
    ),
  );
}
