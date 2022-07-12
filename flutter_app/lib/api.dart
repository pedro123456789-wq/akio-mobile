import 'package:akio_mobile/state.dart';
import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// Android emulator localhost ip
const apiUrl = "http://10.0.2.2:8080"; // TODO: Set me to production url
// const apiUrl = "http://192.168.1.82:8080";

// Does not need to be under provider or anything as it will not have any impact on UI state.
// Needs to be moved to saved state/localstorage sort of thing so it saves between app reload
String? token;

void handleError(DioError e) {
  final response = e.response;
  if (response != null) {
    print("ERROR IN REQUEST: ");
    print(response.statusCode);
    print(response.data);
    return response.data['message'];
  } else {
    print("Assume some sort of network error.");
    // print(e.requestOptions);
    // print(e.message);
  }
  return;
}

Future<bool> login(String username, String password) async {
  var loginUrl = apiUrl + "/api/login";
  try {
    print("$username and $password");
    var response = await Dio()
        .post(loginUrl, data: {'username': username, 'password': password});
    // print(response.statusCode);
    // print(response.data);
    token = response.data['token'];

    return true;
  } on DioError catch (e) {
    handleError(e);
    return false;
  }
}

Future<bool> register(String username, String password) async {
  var registerUrl = apiUrl + "/api/sign-up";
  try {
    var response = await Dio()
        .post(registerUrl, data: {'username': username, 'password': password});
    print(response.data);
    return response.statusCode == 200;
  } on DioError catch (e) {
    handleError(e);
    return false;
  }
}

Future getPosts(BuildContext context, int postNumber) async {
  var postUrl = apiUrl + "/api/posts";

  try {
    Dio dio = Dio(
      BaseOptions(
        queryParameters: {
          'post_number': 10,
          'username': Provider.of<AppModel>(context, listen: false).username,
        },
      ),
    );

    var response = await dio.get(postUrl);
    return response.data['data'];
  } on DioError catch (e) {
    handleError(e);
    return [];
  }
}

Future<bool> postAction(
    BuildContext context, String postUuid, bool isLike) async {
  var likeUrl = apiUrl + "/api/posts";
  var username = Provider.of<AppModel>(context, listen: false).username;

  try {
    var response = await Dio().post(
      likeUrl,
      data: {
        'uuid': postUuid,
        'action': isLike ? 'LIKE' : 'UNLIKE',
        'username': username,
        'token': token
      },
    );
    return response.data['success'];
  } on DioError catch (e) {
    handleError(e);
    return false;
  }
}

Future<bool> createPost(
    String username, String imageData, String caption) async {
  var postUrl = apiUrl + "/api/user/posts";

  try {
    var response = await Dio().post(
      postUrl,
      data: {
        'username': username,
        'token': token,
        'image_data': imageData,
        'caption': caption
      },
    );

    return response.data['success'];
  } on DioError catch (e) {
    handleError(e);
    return false;
  }
}

Future getUserPosts(String username) async {
  var postUrl = apiUrl + "/api/user/posts";

  try {
    Dio dio = Dio(
      BaseOptions(
        queryParameters: {
          'token': token,
          'username': username,
        },
      ),
    );
    var response = await dio.get(postUrl);
    return response.data['data'];
  } on DioError catch (e) {
    handleError(e);
    return [];
  }
}

Future<bool> addItem(String username, String uuid) async {
  var url = apiUrl + "/api/user/clothing-items";

  try {
    var response = await Dio().post(url, data: {'username': username, 'token': token, 'uuid': uuid});

    print(response.statusCode);
    print(response.data);

    return true;  // Try block will fail if response is a 400, so we can assume success.
  } on DioError catch (e) {
    handleError(e);
    return false;
  }
}
