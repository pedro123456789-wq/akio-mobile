import 'package:flutter/material.dart';

class ScanItemPage extends StatefulWidget {
  const ScanItemPage({Key? key}) : super(key: key);

  @override
  _ScanItemPageState createState() => _ScanItemPageState();
}

class _ScanItemPageState extends State<ScanItemPage> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Center(
          child: Text(
            'Scan Item',
            style: Theme.of(context).textTheme.headline1,
          ),
        )
      ],
    );
  }
}
