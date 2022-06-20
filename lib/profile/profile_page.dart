import 'package:akio_mobile/device_info.dart';
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
        Container(
          padding: EdgeInsets.only(
            top: DeviceInfo.deviceHeight(context) * 0.01,
          ),
          alignment: Alignment.topLeft,
          child: Text(
            'Profile',
            style: Theme.of(context).textTheme.headline1,
            textAlign: TextAlign.left,
          ),
        ),
        Container(
          margin: EdgeInsets.only(
            top: DeviceInfo.deviceHeight(context) * 0.25,
          ),
          height: DeviceInfo.deviceHeight(context) * 0.55,
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
                    padding:
                        EdgeInsets.all(DeviceInfo.deviceWidth(context) * 0.15),
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
      ],
    );
  }
}
