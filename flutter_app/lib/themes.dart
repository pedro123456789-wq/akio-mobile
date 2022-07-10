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
    elevatedButtonTheme: ElevatedButtonThemeData(
        style: ButtonStyle(
            foregroundColor: MaterialStateProperty.all(Colors.black),
            backgroundColor: MaterialStateProperty.all(Colors.white),
            overlayColor: MaterialStateProperty.all(Colors.grey))),
    inputDecorationTheme: const InputDecorationTheme(
        // Login page input text field border colour
        enabledBorder:
            OutlineInputBorder(borderSide: BorderSide(color: Colors.grey)),
        focusedBorder:
            OutlineInputBorder(borderSide: BorderSide(color: Colors.white))),
    colorScheme: ColorScheme.fromSwatch().copyWith(
        // Trying to figure out which colour is which
        primary: Colors.white,
        background: Colors.black,
        secondary: Colors.green,
        outline: Colors.red,
        onSecondary: Colors.purple,
        surface: Colors.white),
    textTheme: const TextTheme(
      headline1: TextStyle(
        fontSize: 30.0,
        fontWeight: FontWeight.bold,
        fontFamily: 'LibreBodoni',
      ),
      headline2: TextStyle(
        fontSize: 27.0,
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
