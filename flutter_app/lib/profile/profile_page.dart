import 'package:akio_mobile/device_info.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({Key? key}) : super(key: key);

  @override
  _ProfilePageState createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage>
    with TickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Offset> _expandAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
        duration: const Duration(milliseconds: 400),
        vsync: this,
        animationBehavior: AnimationBehavior.preserve);

    _expandAnimation = Tween<Offset>(
      begin: const Offset(0.0, 1.0),
      end: Offset.zero,
    ).chain(CurveTween(curve: Curves.easeOut)).animate(_controller);

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    var username = Provider.of<AppModel>(context, listen: false).username;

    return Column(
      children: [
        Container(
          padding: EdgeInsets.only(
            top: DeviceInfo.deviceHeight(context) * 0.01,
          ),
          alignment: Alignment.center,
          child: Text(
            'Profile',
            style: Theme.of(context).textTheme.headline1,
            textAlign: TextAlign.left,
          ),
        ),
        SlideTransition(
          child: Container(
            margin: EdgeInsets.only(
              top: DeviceInfo.deviceHeight(context) * 0.1,
            ),
            height: DeviceInfo.deviceHeight(context) * 0.7,
            decoration: const BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.all(
                Radius.circular(5),
              ),
            ),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Container(
                      padding: EdgeInsets.all(
                          DeviceInfo.deviceWidth(context) * 0.15),
                      child: Text(
                        username!,
                        style: const TextStyle(
                            color: Colors.black,
                            fontSize: 27.0,
                            fontFamily: 'LibreBodoni'),
                      ),
                    ),
                    Icon(
                      Icons.account_circle,
                      color: Colors.black,
                      size: DeviceInfo.deviceHeight(context) * 0.12,
                    )
                  ],
                ),
                Container(
                  margin: EdgeInsets.only(
                    top: DeviceInfo.deviceHeight(context) * 0.05,
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Column(
                        children: [
                          Icon(
                            Icons.monitor_heart,
                            color: Colors.black,
                            size: DeviceInfo.deviceWidth(context) * 0.15,
                          ),
                          const Text(
                            'Likes: 2',
                            style: TextStyle(color: Colors.black),
                          )
                        ],
                      ),
                      Column(
                        children: [
                          Icon(
                            Icons.image,
                            color: Colors.black,
                            size: DeviceInfo.deviceWidth(context) * 0.15,
                          ),
                          const Text(
                            'Posts: 5',
                            style: TextStyle(color: Colors.black),
                          )
                        ],
                      )
                    ],
                  ),
                ),
                Container(
                  margin: EdgeInsets.only(
                    top: DeviceInfo.deviceHeight(context) * 0.12,
                  ),
                  width: DeviceInfo.deviceWidth(context) * 0.85,
                  child: ElevatedButton(
                    style: ButtonStyle(
                        backgroundColor:
                            MaterialStateProperty.all(Colors.black)),
                    onPressed: null,
                    child: const Text(
                      'Your Posts',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                      ),
                    ),
                  ),
                ),
                Container(
                  margin: EdgeInsets.only(
                      top: DeviceInfo.deviceHeight(context) * 0.01),
                  width: DeviceInfo.deviceWidth(context) * 0.85,
                  child: ElevatedButton(
                    onPressed: null,
                    style: ButtonStyle(
                      backgroundColor: MaterialStateProperty.all(
                        Colors.black,
                      ),
                    ),
                    child: const Text(
                      'Your Icon',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                      ),
                    ),
                  ),
                )
              ],
            ),
          ),
          position: _expandAnimation,
        ),
      ],
    );
  }
}
