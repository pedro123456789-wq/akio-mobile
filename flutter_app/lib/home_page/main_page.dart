import 'package:akio_mobile/collections/collections_page.dart';
import 'package:akio_mobile/photo_feed/photo_feed_page.dart';
import 'package:akio_mobile/profile/profile_page.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';

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

  List<BottomNavigationBarItem> generateItems(BuildContext context) {
    //check if user is logged in
    var username = Provider.of<AppModel>(context, listen: true).username;

    List<BottomNavigationBarItem> items = [
      const BottomNavigationBarItem(
        icon: Icon(Icons.home),
        label: 'Home',
      ),
      const BottomNavigationBarItem(
        icon: Icon(Icons.checkroom),
        label: 'Collections',
      ),
    ];

    //only show profile section if user is logged in
    if (username != null) {
      items.add(const BottomNavigationBarItem(
        icon: Icon(Icons.account_circle),
        label: 'Profile',
      ));
    }

    return items;
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: _pageOptions[selectedPage],
        bottomNavigationBar: BottomNavigationBar(
          type: BottomNavigationBarType.shifting,
          items: generateItems(context),
          currentIndex: selectedPage,
          onTap: (index) {
            setState(
              () {
                selectedPage = index;
              },
            );
          },
        ),
      ),
    );
  }
}
