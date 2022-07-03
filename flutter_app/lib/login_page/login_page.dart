import 'package:flutter/material.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Center(
            child: Text(
              "Login",
              style: Theme.of(context).textTheme.headline1,
            ),
          ),
          backgroundColor: Colors.black,
        ),
        body: Form(
            child: Padding(
          padding: const EdgeInsets.fromLTRB(60, 50, 60, 0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              TextFormField(
                textAlign: TextAlign.center,
                autocorrect: false,
                decoration: const InputDecoration(
                  labelText: "Username",
                ),
              ),
              const SizedBox(height: 50),
              TextFormField(
                textAlign: TextAlign.center,
                autocorrect: false,
                obscureText: true,
                obscuringCharacter: '*',
                decoration: const InputDecoration(labelText: "Password"),
              )
            ],
          ),
        )));
  }
}
