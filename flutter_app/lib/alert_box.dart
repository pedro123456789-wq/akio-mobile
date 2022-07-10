import 'package:flutter/material.dart';

class AlertBox extends StatelessWidget {
  final bool isSuccess;
  final String message;

  const AlertBox({Key? key, required this.isSuccess, required this.message})
      : super(key: key);

  @override
  SnackBar build(BuildContext context) {
    return SnackBar(
      backgroundColor: Colors.white,
      content: Text(
        message,
        style: const TextStyle(
          fontSize: 18.0,
        ),
      ),
    );
  }
}
