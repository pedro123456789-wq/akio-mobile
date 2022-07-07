import 'package:akio_mobile/api.dart';
import 'package:akio_mobile/state.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() {
    return _LoginPageState();
  }
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _userController = TextEditingController();
  final _passController = TextEditingController();
  final _confirmPassController = TextEditingController();
  bool _usernameTaken = false;

  @override
  void dispose() {
    _userController.dispose();
    _passController.dispose();
    _confirmPassController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const loginSnackbar = SnackBar(content: Text("Login successful!"));
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
          // Probably isn't necessary to use a form here
            key: _formKey,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(60, 50, 60, 0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  const SizedBox(height: 50),
                  TextFormField(
                    textAlign: TextAlign.center,
                    autocorrect: false,
                    decoration: const InputDecoration(
                      labelText: "Username",
                    ),
                    controller: _userController,
                  ),
                  const SizedBox(height: 80),
                  TextFormField(
                    textAlign: TextAlign.center,
                    autocorrect: false,
                    obscureText: true,
                    obscuringCharacter: '*',
                    decoration: const InputDecoration(labelText: "Password"),
                    controller: _passController,
                  ),
                  const SizedBox(height: 80),
                  ElevatedButton(
                      onPressed: () async {
                        bool success = await login(
                            _userController.text, _passController.text);

                        if (success) {
                          print("Updating provider.");
                          Provider.of<AppModel>(context, listen: false)
                              .username = _userController.text;
                        } else {
                          Provider.of<AppModel>(context, listen: false)
                              .username = null;
                        }
                        // Todo: fix this snackbar not showing
                        ScaffoldMessenger.of(context)
                            .showSnackBar(loginSnackbar);
                      },
                      child: const Padding(
                        padding: EdgeInsets.fromLTRB(32, 8, 32, 8),
                        child: Text("Login",
                            style: TextStyle(
                              fontSize: 16,
                            )),
                      )),
                  const SizedBox(height: 80),
                  TextButton(
                      onPressed: () {
                        _usernameTaken = false;
                        showDialog(
                            context: context,
                            builder: (BuildContext context) => AlertDialog(
                                  title: const Text("Register for akio."),
                                  content: Column(
                                    children: [
                                      const Text(
                                          "Please confirm your password."),
                                      TextField(
                                        controller: _confirmPassController,
                                        textAlign: TextAlign.center,
                                        autocorrect: false,
                                        obscureText: true,
                                        obscuringCharacter: '*',
                                        decoration: const InputDecoration(
                                            labelText: "Password"),
                                      ),
                                      Text(_usernameTaken
                                          ? "Username taken"
                                          : ""),
                                    ],
                                  ),
                                  actions: [
                                    TextButton(
                                        onPressed: () =>
                                            Navigator.of(context).pop(),
                                        child: const Text("Cancel")),
                                    TextButton(
                                        onPressed: () async {
                                          bool passwordsMatch =
                                              (_passController.text ==
                                                  _confirmPassController.text);
                                          if (passwordsMatch) {
                                            var result = await register(
                                                _userController.text,
                                                _passController.text);
                                            if (result) {
                                              Navigator.of(context).pop();
                                            } else {
                                              _usernameTaken = true;
                                            }
                                          }
                                        },
                                        child: const Text("Confirm")),
                                  ],
                                ));
                      },
                      child: const Text("Sign up..."))
                ],
              ),
            )));
  }
}
