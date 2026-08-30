import 'package:flutter/material.dart';
import 'package:front/features/scolarite/presentation/page/grade_exam_page.dart';

import '../widgets/exam_to_grade_card.dart';


class ExamToGrade {
  final String id;
  final String name;
  final String professor;
  final String session;
  final int presentStudents;
  final int totalStudents;

  const ExamToGrade({
    required this.id,
    required this.name,
    required this.professor,
    required this.session,
    required this.presentStudents,
    required this.totalStudents,
  });
}

class ExamsToGradePage extends StatelessWidget {
  const ExamsToGradePage({super.key});

  static const List<ExamToGrade> exams = [
    ExamToGrade(
      id: 'exam-001',
      name: 'Algèbre linéaire',
      professor: 'Mme Rasoanaivo',
      session: 'Normale',
      presentStudents: 3,
      totalStudents: 38,
    ),
    ExamToGrade(
      id: 'exam-002',
      name: 'Analyse numérique',
      professor: 'M. Rakoto',
      session: 'Rattrapage',
      presentStudents: 24,
      totalStudents: 27,
    ),
    ExamToGrade(
      id: 'exam-003',
      name: 'Bases de données',
      professor: 'Mme Andria',
      session: 'Normale',
      presentStudents: 32,
      totalStudents: 32,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: const Text(
          'Examens à noter',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: ListView.separated(
        padding: const EdgeInsets.all(20),
        itemCount: exams.length,
        separatorBuilder: (_, _) => const SizedBox(height: 12),
        itemBuilder: (context, index) {
          final exam = exams[index];

          return ExamToGradeCard(
            exam: exam,
            onTap: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => GradeExamPage(
                    exam: exam,
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}