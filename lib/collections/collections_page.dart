import 'package:akio_mobile/collections/collection_item.dart';
import 'package:flutter/material.dart';

class CollectionsPage extends StatefulWidget {
  const CollectionsPage({Key? key}) : super(key: key);

  @override
  _CollectionsPageState createState() => _CollectionsPageState();
}

class _CollectionsPageState extends State<CollectionsPage> {
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
                onPressed: () => print('pressed'),
                child: const Icon(
                  Icons.qr_code_scanner,
                ),
              )
            ],
            mainAxisAlignment: MainAxisAlignment.center,
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
