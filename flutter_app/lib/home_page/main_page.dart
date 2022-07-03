import 'package:akio_mobile/photo_feed/photo_feed_page.dart';
import 'package:akio_mobile/profile/profile_page.dart';
import 'package:akio_mobile/scan_item/scan_item_page.dart';
import 'package:akio_mobile/collections/collections_page.dart';
import 'package:flutter/material.dart';

//Page which contains bottom navigation bar
//Other pages are loaded on top of this page through the body argument of the Scaffold widget
//All pages are stored in _pageOptions array

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int selectedPage = 0;

  final _pageOptions = const [
    PhotoFeedPage(),
    CollectionsPage(),
    ProfilePage()
  ];

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: _pageOptions[selectedPage],
        bottomNavigationBar: BottomNavigationBar(
          type: BottomNavigationBarType.shifting,
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.home),
              label: 'Home',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.checkroom),
              label: 'Collections',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.account_circle),
              label: 'Profile',
            ),
          ],
          currentIndex: selectedPage,
          onTap: (index) {
            setState(() {
              selectedPage = index;
            });
          },
        ),
      ),
    );
  }
}
