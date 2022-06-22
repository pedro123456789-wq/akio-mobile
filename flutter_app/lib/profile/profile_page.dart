import 'package:akio_mobile/device_info.dart';
import 'package:flutter/material.dart';

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
    ).chain(CurveTween(curve: Curves.easeOut))
        .animate(_controller);

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          padding: EdgeInsets.only(
            top: DeviceInfo.deviceHeight(context) * 0.01,
          ),
          alignment: Alignment.topLeft,
          child: Container(
            margin: EdgeInsets.only(
              left: DeviceInfo.deviceWidth(context) * 0.1,
            ),
            child: Text(
              'Profile',
              style: Theme.of(context).textTheme.headline1,
              textAlign: TextAlign.left,
            ),
          ),
        ),
        SlideTransition(
          child: Container(
            margin: EdgeInsets.only(
              top: DeviceInfo.deviceHeight(context) * 0.20,
            ),
            height: DeviceInfo.deviceHeight(context) * 0.60,
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
                      child: const Text(
                        'Name',
                        style: TextStyle(
                            color: Colors.black,
                            fontSize: 25.0,
                            fontFamily: 'LibreBodoni'),
                      ),
                    ),
                    Icon(
                      Icons.account_circle,
                      color: Colors.black,
                      size: DeviceInfo.deviceHeight(context) * 0.12,
                    )
                  ],
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
