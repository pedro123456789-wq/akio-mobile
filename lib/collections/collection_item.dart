import 'package:flutter/material.dart';

class CollectionItem extends StatelessWidget {
  final int copies;

  const CollectionItem({
    Key? key,
    required this.copies,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
      ),
      height: 400,
      child: Column(
        children: [
          Text(
            '1 / $copies',
            style: Theme.of(context).textTheme.caption,
          )
        ],
      ),
    );
  }
}
