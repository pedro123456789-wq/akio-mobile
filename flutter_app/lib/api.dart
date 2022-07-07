import 'package:dio/dio.dart';

// Android emulator localhost ip
const apiUrl = "http://10.0.2.2:8080"; // TODO: Set me to production url

// Does not need to be under provider or anything as it will not have any impact on UI state.
String? token;

void handleError(DioError e) {
  final response = e.response;
  if (response != null) {
    print("ERROR IN REQUEST: ");
    print(response.statusCode);
    print(response.data);
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
      return response;
    }else{
      return e.message;
    }
  }
}
