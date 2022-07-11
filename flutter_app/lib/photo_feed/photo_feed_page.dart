import 'package:akio_mobile/device_info.dart';
import 'package:akio_mobile/photo_feed/post.dart';
import 'package:flutter/material.dart';
import 'package:akio_mobile/api.dart';
import 'package:provider/provider.dart';

import '../state.dart';
import 'create_post_dialog.dart';


//TO add in the future:
//Comments, Post captions


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
        Post(
          imageUrl: '$apiUrl/images?path=${item['image_url']}',
          likes: item['likes'],
          hasLiked: item['has_liked'],
          uuid: item['uuid'],
          poster: item['poster'],
        ),
      );
    }

    return children;
  }

  Widget getPostButton(BuildContext context, String? username) {
    //only show post button if user is logged in
    if (username != null) {
      return Container(
        margin: EdgeInsets.only(top: DeviceInfo.deviceHeight(context) * 0.01),
        child: ElevatedButton(
          onPressed: () {
            showDialog(
              context: context,
              builder: (BuildContext context) {
                return CreatePostDialog(username: username);
              },
            );
          },
          child: const Icon(Icons.add),
        ),
      );
    } else {
      return Container();
    }
  }

  @override
  Widget build(BuildContext context) {
    String? username = Provider.of<AppModel>(context, listen: false).username;

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
        future: getPosts(context, 10),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return Column(
              children: [
                Container(
                  height: DeviceInfo.deviceHeight(context) * 0.7,
                  child: SingleChildScrollView(
                    child: Column(children: getFeed(snapshot.data)),
                  ),
                ),
                getPostButton(context, username)
              ],
            );
          } else if (snapshot.hasError) {
            return Text('${snapshot.error}');
          }

          return Container(
            alignment: Alignment.center,
            child: const CircularProgressIndicator(),
          );
        },
      ),
    );
    // shrinkWrap:
  }
}
