import 'package:dio/dio.dart';

// Android emulator localhost ip
const apiUrl = "http://10.0.2.2:8080"; // TODO: Set me to production url

void login(String username, String password) async {
  var loginUrl = apiUrl + "/api/login";
  try {
    print("$username and $password");
    var response = await Dio()
        .post(loginUrl, data: {'username': username, 'password': password});
    print(response.statusCode);
    print(response.data);
  } on DioError catch (e) {
    final response = e.response;
    if (response != null) {
      print(response.statusCode);
      print(response.data);
    } else {
      print("Assume some sort of network error.");
      print(e.requestOptions);
      print(e.message);
    }
  }
}


Future getPosts(int postNumber) async {
  var postUrl = apiUrl + "/api/posts";
  
  try{
    Dio dio = Dio(BaseOptions(
      headers: {
        'post_number': 10
      }
    ));

    var response = await dio.get(postUrl);
    return response.data['data'];
  } on DioError catch (e) {
    final response = e.response;

    if (response != null){
      return response.data['message'];
    }else{
      return e.message;
    }
  }
}
