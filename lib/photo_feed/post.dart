import 'package:flutter/material.dart';

class Post extends StatefulWidget {
  final String imageUrl;

  const Post({
    Key? key,
    required this.imageUrl,
  }) : super(key: key);

  @override
  _PostState createState() => _PostState();
}

class _PostState extends State<Post> {
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
      margin: const EdgeInsets.all(15),
      padding: const EdgeInsets.only(top: 20),
      child: Column(
        children: [
          Image.network(widget.imageUrl),
          Container(
            margin: const EdgeInsets.only(
              top: 30,
              right: 20
            ),
            child: Row(
              textDirection: TextDirection.rtl,
              children: [
                Text(
                  '100',
                  style: Theme.of(context).textTheme.caption,
                ),
                ElevatedButton(
                  onPressed: () => print('pressed'),
                  style: ElevatedButton.styleFrom(
                    primary: Colors.transparent.withOpacity(0),
                    elevation: 0.0,
                  ),
                  child: const Icon(
                    Icons.favorite,
                    color: Colors.black,
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
