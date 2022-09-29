import 'dart:convert';
import 'dart:html';
import 'package:flutter_uploader/flutter_uploader.dart';
import 'package:flask_app/function.dart';
import 'package:flutter/material.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);

  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  String url = '';
  String initialHost = 'http://192.168.0.106:5000/api?query=';
  var data;
  File? videoFile;
  String output = "some shit";
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("lip to text")),
      body: Center(
          child: Container(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // TextField(
            TextFormField(
              initialValue: 'http://192.168.0.106:5000/',
              onChanged: (value) {
                // url = 'http://127.0.0.1:5000/api?query=' + value.toString();
                url = initialHost + value.toString() + 'api?query=';
              },
            ),

            TextField(
              onChanged: (character) {
                url = initialHost + character.toString();
              },
            ),

            TextButton.icon(
              onPressed: () async {
                data = await fetchData(url);
                var decoded = jsonDecode(data);
                setState(() {
                  output = decoded['output'].toString();
                });
              },
              icon: Icon(Icons.upload_file),
              label: Text("Upload"),
            ),

            TextButton(
                onPressed: () async {
                  data = await fetchData(url);
                  var decoded = jsonDecode(data);
                  setState(() {
                    output = decoded['output'].toString();
                  });
                },
                child: Text('Read Lip', style: TextStyle(fontSize: 20))),

            Text(output, style: TextStyle(fontSize: 40))
          ],
        ),
      )),
    );
  }
}
