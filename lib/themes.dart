import 'package:flutter/material.dart';

class Themes {
  static ThemeData globalTheme = ThemeData.dark().copyWith(
    brightness: Brightness.light,
    backgroundColor: Colors.black,
    scaffoldBackgroundColor: Colors.black,
    canvasColor: Colors.black,
    colorScheme: ColorScheme.fromSwatch().copyWith(secondary: Colors.white),
    textTheme: const TextTheme(
      headline1: TextStyle(
        fontSize: 40.0,
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
