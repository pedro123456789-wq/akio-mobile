import 'package:akio_mobile/collections/collection_item.dart';
import 'package:akio_mobile/scan_item/scan_item_page.dart';
import 'package:flutter/material.dart';

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
  Future<bool> _canPop(BuildContext context) async {
    // print(await Navigator.of(context).maybePop());
    Navigator.of(context).pushNamed("/");
    return false;
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope( // This captures the android back button
        child: Navigator(
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

            return MaterialPageRoute(builder: builder, settings: settings);
          },
        ),
        onWillPop: () => _canPop(context)
    );
  }
}
