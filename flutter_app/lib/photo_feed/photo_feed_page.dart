import 'package:akio_mobile/photo_feed/post.dart';
import 'package:flutter/material.dart';
import 'package:akio_mobile/api.dart';

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
            'akio.',
            style: Theme.of(context).textTheme.headline1,
          ),
        ),
      ),
      body: FutureBuilder(
        future: getPosts(10),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return SingleChildScrollView(
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
            );
          }else if (snapshot.hasError){
            return Text('${snapshot.error}');
          }

          return const CircularProgressIndicator();
        }
      ),
    );
    // shrinkWrap:
  }
}
