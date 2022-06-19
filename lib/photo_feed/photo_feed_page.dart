import 'package:akioo_mobile/photo_feed/post.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class PhotoFeedPage extends StatefulWidget {
  const PhotoFeedPage({Key? key}) : super(key: key);

  @override
  _PhotoFeedPageState createState() => _PhotoFeedPageState();
}

class _PhotoFeedPageState extends State<PhotoFeedPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text(
            'Akio',
            style: Theme.of(context).textTheme.headline1,
          ),
        ),
        backgroundColor: Colors.black,
      ),
      body: SingleChildScrollView(
        child: Column(
          children: const [
            Post(
              imageUrl: "https://picsum.photos/250?image=1",
            ),
            Post(
              imageUrl: "https://picsum.photos/250?image=2",
            ),
            Post(
              imageUrl: "https://picsum.photos/250?image=3",
            )
          ],
        ),
      ),
    );
    // shrinkWrap:
  }
}
