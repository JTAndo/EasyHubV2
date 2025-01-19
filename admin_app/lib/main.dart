import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EasyHub Admin App',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const UserRegistrationPage(),
    );
  }
}

class UserRegistrationPage extends StatefulWidget {
  const UserRegistrationPage({Key? key}) : super(key: key);

  @override
  _UserRegistrationPageState createState() => _UserRegistrationPageState();
}

class _UserRegistrationPageState extends State<UserRegistrationPage> {
  final _formKey = GlobalKey<FormState>();
  String _name = '';
  String _email = '';
  String _role = 'Admin';
  bool _remoteAccess = false;
  bool _videoCall = false;
  bool _voiceCall = false;
  bool _manageUsers = false;

void _submitForm() async {
  if (_formKey.currentState?.validate() ?? false) {
    _formKey.currentState?.save();
    final response = await http.post(
      Uri.parse('http://localhost:7071/api/registerUser'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': _name,
        'email': _email,
        'role': _role,
        'permissions': {
          'remote_access': _remoteAccess,
          'video_call': _videoCall,
          'voice_call': _voiceCall,
          'manage_users': _manageUsers,
        },
      }),
    );

    if (response.statusCode == 201) {
      // Success
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('User registered successfully!')),
      );
    } else {
      // Error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${response.body}')),
      );
    }
  }
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('User Registration'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: 'Name'),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Enter a name' : null,
                onSaved: (value) => _name = value ?? '',
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Email'),
                validator: (value) => value == null || !value.contains('@')
                    ? 'Enter a valid email'
                    : null,
                onSaved: (value) => _email = value ?? '',
              ),
              DropdownButtonFormField<String>(
                value: _role,
                items: const [
                  DropdownMenuItem(value: 'Admin', child: Text('Admin')),
                  DropdownMenuItem(value: 'Non-Admin', child: Text('Non-Admin')),
                ],
                onChanged: (value) => setState(() => _role = value!),
                decoration: const InputDecoration(labelText: 'Role'),
              ),
              SwitchListTile(
                title: const Text('Remote Access'),
                value: _remoteAccess,
                onChanged: (value) => setState(() => _remoteAccess = value),
              ),
              SwitchListTile(
                title: const Text('Video Call'),
                value: _videoCall,
                onChanged: (value) => setState(() => _videoCall = value),
              ),
              SwitchListTile(
                title: const Text('Voice Call'),
                value: _voiceCall,
                onChanged: (value) => setState(() => _voiceCall = value),
              ),
              SwitchListTile(
                title: const Text('Manage Users'),
                value: _manageUsers,
                onChanged: (value) => setState(() => _manageUsers = value),
              ),
              ElevatedButton(
                onPressed: _submitForm,
                child: const Text('Submit'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
