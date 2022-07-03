import 'package:akio_mobile/collections/collection_item.dart';
import 'package:akio_mobile/login_page/login_page.dart';
import 'package:akio_mobile/scan_item/scan_item_page.dart';
import 'package:akio_mobile/state.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

class _HomeRoute extends StatelessWidget {
  void _nfcPressed(BuildContext context) {
    Navigator.of(context).pushNamed('/scan');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Center(
          child: Row(
            children: [
              Text(
                'Collections',
                style: Theme
                    .of(context)
                    .textTheme
                    .headline1,
              ),
              ElevatedButton(
                onPressed: () => _nfcPressed(context),
                child: const Icon(
                  Icons.contactless_outlined,
                ),
              )
            ],
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
          ),
        ),
      ),
      body: Container(
        margin: const EdgeInsets.only(
          top: 30,
        ),
        child: GridView(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            mainAxisSpacing: 15,
          ),
          children: const [
            CollectionItem(
              copies: 200,
            ),
            CollectionItem(
              copies: 300,
            ),
            CollectionItem(
              copies: 500,
            ),
            CollectionItem(
              copies: 200,
            ),
            CollectionItem(
              copies: 400,
            ),
            CollectionItem(
              copies: 600,
            ),
            CollectionItem(
              copies: 700,
            )
          ],
        ),
      ),
    );
  }

}

class CollectionsPage extends StatefulWidget {
  const CollectionsPage({Key? key}) : super(key: key);

  @override
  _CollectionsPageState createState() => _CollectionsPageState();
}

class _CollectionsPageState extends State<CollectionsPage> {
  // WillPopScope MUST be outside a navigator for it to handle the back button,
  //    so this is used so that the inner navigator can be popped from the outside
  //    https://github.com/flutter/flutter/issues/14083
  final innerNavkey = GlobalKey<NavigatorState>();

  Future<bool> _canPop(BuildContext context) async {
    // If scan page is open, the return to collections page
    // else, close the app
    if (innerNavkey.currentState?.canPop() == true) {
      innerNavkey.currentState?.pushNamed("/");
    } else {
      // This function won't work on iOS, but this code should also never be reached on iOS.
      SystemChannels.platform.invokeMethod('SystemNavigator.pop');
    }

    return false;
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<AppModel>(
      builder: (context, value, child) {
        if (value.loggedIn) {
          return WillPopScope(
              child: Navigator(
                key: innerNavkey,
                initialRoute: '/',
                onGenerateRoute: (RouteSettings settings) {
                  WidgetBuilder builder;

                  switch (settings.name) {
                    case '/scan':
                      builder = (BuildContext context) => const ScanItemPage();
                      break;
                    default:
                      builder = (BuildContext context) => _HomeRoute();
                      break;
                  }

                  return MaterialPageRoute(
                      builder: builder, settings: settings);
                },
              ),
              onWillPop: () => _canPop(context));
        } else {
          return const LoginPage();
        }
      },
    );
  }
}
