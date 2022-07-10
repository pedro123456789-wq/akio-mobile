import 'dart:io';
import 'dart:convert';

import 'package:akio_mobile/alert_box.dart';
import 'package:akio_mobile/api.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../device_info.dart';

//Make snackbar look better
//Add separate snackbar class

class CreatePostDialog extends StatefulWidget {
  final String username;

  const CreatePostDialog({
    Key? key,
    required this.username,
  }) : super(key: key);

  @override
  _CreatePostDialogState createState() => _CreatePostDialogState();
}

class _CreatePostDialogState extends State<CreatePostDialog> {
  File? chosenFile;

  Future<File?> _getImage(bool isGallery) async {
    XFile? pickedFile = await ImagePicker().pickImage(
      source: isGallery ? ImageSource.gallery : ImageSource.camera,
      maxWidth: 1800,
      maxHeight: 1800,
    );

    if (pickedFile != null) {
      File imageFile = File(pickedFile.path);
      return imageFile;
    } else {
      return null;
    }
  }

  Widget showPostImage(BuildContext context) {
    //only show image selected by user and post button if user has selected image to post
    if (chosenFile != null) {
      return Container(
        margin: EdgeInsets.only(
          top: DeviceInfo.deviceHeight(context) * 0.03,
        ),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(5),
              height: DeviceInfo.deviceHeight(context) * 0.45,
              alignment: Alignment.center,
              child: Image.file(
                chosenFile!,
              ),
            ),
            Container(
              width: DeviceInfo.deviceWidth(context) * 0.6,
              child: ElevatedButton(
                onPressed: () => makePost(),
                child: const Text(
                  'Post',
                  style: TextStyle(
                    fontSize: 22.0,
                    color: Colors.black,
                  ),
                ),
              ),
            )
          ],
        ),
      );
    } else {
      return Container();
    }
  }

  void makePost() async {
    if (chosenFile != null) {
      final bytes = await chosenFile!.readAsBytes();
      String base64String = base64Encode(bytes);
      bool isSuccess = await createPost(widget.username, base64String, '');

      if (isSuccess) {
        //show pop up at bottom of screen
        ScaffoldMessenger.of(context).showSnackBar(const AlertBox(
          isSuccess: true,
          message: 'The image has been posted',
        ).build(context) // try to make this cleaner
            );
        //return to home page
        Navigator.pop(context, true);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const AlertBox(
            isSuccess: false,
            message: 'You need to select an image',
          ).build(context),
        );
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const AlertBox(
          isSuccess: false,
          message: 'Network error',
        ).build(context),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          title: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Create Post',
                style: Theme.of(context).textTheme.headline1,
              ),
              ElevatedButton(
                onPressed: () => Navigator.pop(context, true),
                child: const Icon(Icons.exit_to_app),
              )
            ],
          ),
        ),
        body: Container(
          margin: EdgeInsets.only(
            top: DeviceInfo.deviceHeight(context) * 0.08,
          ),
          child: Column(
            children: [
              const Text(
                'Select image',
                style: TextStyle(fontSize: 22.0, color: Colors.white),
              ),
              Container(
                margin: EdgeInsets.only(
                  top: DeviceInfo.deviceHeight(context) * 0.05,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton(
                      onPressed: () async {
                        File? file = await _getImage(true);

                        //prevents updating state pointlessly which improves performance
                        if (file != null) {
                          setState(
                            () {
                              chosenFile = file;
                            },
                          );
                        }
                      },
                      child: Icon(
                        Icons.add_photo_alternate,
                        size: DeviceInfo.deviceWidth(context) * 0.15,
                      ),
                    ),
                    ElevatedButton(
                      onPressed: () async {
                        File? file = await _getImage(false);

                        //prevents updating state pointlessly which improves performance
                        if (file != null) {
                          setState(
                            () {
                              chosenFile = file;
                            },
                          );
                        }
                      },
                      child: Icon(
                        Icons.camera_enhance_sharp,
                        size: DeviceInfo.deviceWidth(context) * 0.15,
                      ),
                    )
                  ],
                ),
              ),
              showPostImage(context),
            ],
          ),
        ),
      ),
    );
  }
}
