import 'package:akio_mobile/api.dart';
import 'package:akio_mobile/device_info.dart';
import 'package:flutter/material.dart';

class Post extends StatefulWidget {
  final String imageUrl;
  final int likes;
  final bool hasLiked;
  final String uuid;

  const Post(
      {Key? key,
      required this.imageUrl,
      required this.likes,
      required this.hasLiked,
      required this.uuid})
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

  @override
  Widget build(BuildContext context) {
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
        top: DeviceInfo.deviceHeight(context) * 0.05,
      ),
      child: Column(
        children: [
          Image.network(
            widget.imageUrl,
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
                ElevatedButton(
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
                              {
                                print("network error")
                              }
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
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
