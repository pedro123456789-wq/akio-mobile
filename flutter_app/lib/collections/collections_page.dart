import 'package:akio_mobile/collections/collection_item.dart';
import 'package:akio_mobile/scan_item/scan_item_page.dart';
import 'package:flutter/material.dart';

class CollectionsPage extends StatefulWidget {
  const CollectionsPage({Key? key}) : super(key: key);

  @override
  _CollectionsPageState createState() => _CollectionsPageState();
}

class _CollectionsPageState extends State<CollectionsPage> {
  void _nfcPressed(BuildContext context) {
    print("Pressed");
    Navigator.of(context).push(MaterialPageRoute(
        builder: (BuildContext context) {
          print("Building...");
          return const ScanItemPage();
        }
    ));
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
                style: Theme.of(context).textTheme.headline1,
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
