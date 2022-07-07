import 'package:flutter/material.dart';

class AppModel extends ChangeNotifier {
  String? _username;

  String? get username => _username;

  set username(String? username) {
    _username = username;
    notifyListeners();
  } // If null then not logged in
}