import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:nfc_manager/nfc_manager.dart';

class ScanItemPage extends StatefulWidget {
  const ScanItemPage({Key? key}) : super(key: key);

  @override
  _ScanItemPageState createState() => _ScanItemPageState();
}

class _ScanItemPageState extends State<ScanItemPage> {
  bool nfcAvailable = false;

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
    nfcAvailable = await NfcManager.instance.isAvailable();

    if (nfcAvailable) {
      NfcManager.instance.startSession(
        onDiscovered: (NfcTag tag) async {
          // Do something with an NfcTag instance.
          Ndef? ndef = Ndef.from(tag);
          NdefMessage? data = await ndef?.read();
          if (data != null) {
            Utf8Decoder decode = const Utf8Decoder();
            var contents = data.records.last.payload;

            String stringContents = decode.convert(contents);

            print(stringContents);
          }
        },
      );
    }
  }

  void stopTagScan() {
    if (nfcAvailable) {
      NfcManager.instance.stopSession();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Center(
          child: Text(
            'Scan Item',
            style: Theme.of(context).textTheme.headline1,
          ),
        )
      ],
    );
  }
}
