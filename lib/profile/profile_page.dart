import 'package:flutter/material.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({Key? key}) : super(key: key);

  @override
  _ProfilePageState createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Center(
          child: Text(
            'Profile',
            style: Theme.of(context).textTheme.headline1,
          ),
        ),
        Container(
          margin: EdgeInsets.only(top: 10),
          height: 40,
          decoration: const BoxDecoration(color: Colors.white),
        ),
      ],
    );
  }
}
