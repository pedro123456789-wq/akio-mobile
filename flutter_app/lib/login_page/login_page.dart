import 'package:flutter/material.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() {
    return _LoginPageState();
  }
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();

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
            key: _formKey,
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
