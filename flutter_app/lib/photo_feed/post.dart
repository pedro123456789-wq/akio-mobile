import 'package:akio_mobile/api.dart';
import 'package:akio_mobile/device_info.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';


class Post extends StatefulWidget {
  final String imageUrl;
  final int likes;
  final bool hasLiked;
  final String uuid;
  final String poster;

  const Post(
      {Key? key,
      required this.imageUrl,
      required this.likes,
      required this.hasLiked,
      required this.uuid,
      required this.poster})
      : super(key: key);

  @override
  _PostState createState() => _PostState();
}

class _PostState extends State<Post> {
  int likes = 0;
  bool hasLiked = false;

  @override
  void initState() {
    super.initState();

    setState(() {
      likes = widget.likes;
      hasLiked = widget.hasLiked;
    });
  }

  Widget generateLikeButton(BuildContext context) {
    var username = Provider.of<AppModel>(context, listen: false).username;

    // if user is logged in return button since they can like the post
    // if user is not logged in just show icon since they cannot like posts

    if (username != null) {
      return ElevatedButton(
        onPressed: () async => {
          if (hasLiked == false)
            {
              await postAction(context, widget.uuid, true).then(
                (isSuccess) => {
                  if (isSuccess)
                    {
                      setState(
                        () => {
                          likes += 1,
                          hasLiked = true,
                        },
                      )
                    }
                  else
                    {
                      print("network error")
                      // TODO: Show error pop up
                    }
                },
              )
            }
          else
            {
              await postAction(context, widget.uuid, false).then(
                (isSuccess) => {
                  if (isSuccess)
                    {
                      setState(
                        () => {
                          likes -= 1,
                          hasLiked = false,
                        },
                      )
                    }
                  else
                    {print("network error")}
                },
              )
            }
        },
        style: ElevatedButton.styleFrom(
          primary: Colors.transparent.withOpacity(0),
          elevation: 0.0,
        ),
        child: Icon(
          Icons.favorite,
          color: hasLiked ? Colors.red : Colors.black,
        ),
      );
    } else {
      return Container(
        padding: const EdgeInsets.all(10),
        child: Icon(
          Icons.favorite,
          color: hasLiked ? Colors.red : Colors.black,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    var username = Provider.of<AppModel>(context, listen: false).username;

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(
          color: Colors.transparent,
        ),
        borderRadius: const BorderRadius.all(
          Radius.circular(5),
        ),
      ),
      margin: EdgeInsets.all(
        DeviceInfo.deviceWidth(context) * 0.05,
      ),
      padding: EdgeInsets.only(
        top: DeviceInfo.deviceHeight(context) * 0.02,
      ),
      child: Column(
        children: [
          Container(
            alignment: Alignment.topLeft,
            child: Container(
              margin: const EdgeInsets.only(left: 10),
              child: Text(
                widget.poster,
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ),
          ),
          Container(
            width: DeviceInfo.deviceWidth(context) * 0.9,
            height: DeviceInfo.deviceHeight(context) * 0.45,
            child: Image.network(
              widget.imageUrl,
            ),
          ),
          Container(
            margin: EdgeInsets.only(
              top: DeviceInfo.deviceHeight(context) * 0.01,
              right: DeviceInfo.deviceWidth(context) * 0.02,
            ),
            child: Row(
              textDirection: TextDirection.rtl,
              children: [
                Text(
                  likes.toString(),
                  style: Theme.of(context).textTheme.caption,
                ),
                generateLikeButton(context),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
