import 'package:akio_mobile/photo_feed/post.dart';
import 'package:flutter/material.dart';
import 'package:akio_mobile/api.dart';

class PhotoFeedPage extends StatefulWidget {
  const PhotoFeedPage({Key? key}) : super(key: key);

  @override
  _PhotoFeedPageState createState() => _PhotoFeedPageState();
}

class _PhotoFeedPageState extends State<PhotoFeedPage> {

  List<Widget> getFeed(response) {
    List<Widget> children = [];

    for (var item in response) {
      print(item);

      children.add(
          Post(imageUrl: '$apiUrl/images?path=${item['image_url']}', likes: item['likes'])
      );
    }

    return children;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text(
            'akio.',
            style: Theme
                .of(context)
                .textTheme
                .headline1,
          ),
        ),
      ),
      body: FutureBuilder(
        future: getPosts(10),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return SingleChildScrollView(
              child: Column(
                  children: getFeed(snapshot.data)
              ),
            );
          } else if (snapshot.hasError) {
            return Text('${snapshot.error}');
          }

          return Container(
            alignment: Alignment.center,
            child: const CircularProgressIndicator(),
          );
        },),
    );
    // shrinkWrap:
  }
}
