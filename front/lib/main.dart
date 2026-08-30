import 'package:flutter/material.dart';
//import 'features/auth/presentation/pages/login_page.dart';
//import 'features/surveillance/presentation/pages/exam_room_page.dart';
//import 'features/surveillance/presentation/pages/presence_page.dart';
import 'features/scolarite/presentation/page/exams_to_grade_page.dart';
import 'core/theme/app_theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Scolarity',
      theme: AppTheme.lightTheme,
      
      home: const ExamsToGradePage(),
    );
  }
}
