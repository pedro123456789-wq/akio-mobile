import 'package:akio_mobile/home_page/home_page.dart';
import 'package:akio_mobile/themes.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const AppRoot());
}

class AppRoot extends StatelessWidget {
  const AppRoot({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: Themes.globalTheme,
      title: "akio.",
      home: const HomePage(),
    );
  }
}
