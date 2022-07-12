import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:nfc_manager/nfc_manager.dart';
import 'package:provider/provider.dart';

class ScanItemPage extends StatefulWidget {
  const ScanItemPage({Key? key}) : super(key: key);

  @override
  _ScanItemPageState createState() => _ScanItemPageState();
}


Future<void> processTag(NfcTag tag) async {
  Ndef? ndef = Ndef.from(tag);
  NdefMessage? data = await ndef?.read();

  if (data != null) {
    Utf8Decoder decode = const Utf8Decoder();
    var records = data.records;

    // String uuid = records[0];
    //
    // addItem(username, uuid);

    // for (var record in records) {
    //   var byteContent = record.payload;

    //   String stringContents = decode.convert(byteContent);

    //   print(stringContents);
    // }
  }
}


class _ScanItemPageState extends State<ScanItemPage> {
  bool? _nfcAvailable;

  @override
  void initState() {
    super.initState();
    startTagScan();
  }

  @override
  void dispose() {
    super.dispose();
    stopTagScan();
  }

  Future<void> startTagScan() async {
    _nfcAvailable = await NfcManager.instance.isAvailable();
    setState(() {
      _nfcAvailable = _nfcAvailable;
    });

    if (_nfcAvailable == true) {
      NfcManager.instance.startSession(
        onDiscovered: processTag
      );
    }
  }

  void stopTagScan() {
    if (_nfcAvailable == true) {
      NfcManager.instance.stopSession();
    }
  }

  Widget getBody() {
    return _nfcAvailable == null
        ? const CircularProgressIndicator()
        : (
        _nfcAvailable == true
            ? Column(
          children: [
            const CircularProgressIndicator(),
            const SizedBox(height: 50),
            Text("Please place your phone against an NFC tag.", style: Theme.of(context).textTheme.subtitle1,)
          ],
          mainAxisAlignment: MainAxisAlignment.center,
        )
            : Center(
          child: Padding(
            padding: const EdgeInsets.all(50),
            child: Text("Please enable NFC if you're on android. If you're on iOS, then your phone may not support tag scanning.", style: Theme.of(context).textTheme.subtitle1,)
          )
        )
    );
  }

  @override
  Widget build(BuildContext context) {
    return
        Scaffold(
        appBar: AppBar(
            backgroundColor: Colors.black,
            title: Center(
                child: Text(
                    'Scan clothing',
                    style: Theme.of(context).textTheme.headline1
                )
            )
        ),
        body: Center(
          child: getBody()
        )

    );
  }
}
