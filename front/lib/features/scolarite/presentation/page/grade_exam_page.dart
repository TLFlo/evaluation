// ignore_for_file: unused_element

import 'package:flutter/material.dart';

import '../widgets/grade_exam_header.dart';
import '../widgets/grade_scale_field.dart';
import '../widgets/student_grade_card.dart';
import '../widgets/student_search_field.dart';

import 'exams_to_grade_page.dart';

class GradeExamPage extends StatefulWidget {
  final ExamToGrade exam;

  const GradeExamPage({super.key, required this.exam});

  @override
  State<GradeExamPage> createState() => _GradeExamPageState();
}

class _GradeExamPageState extends State<GradeExamPage> {
  final TextEditingController _matriculeController = TextEditingController();

  final TextEditingController _gradeController = TextEditingController();

  double? _gradeScale;

  ExamStudent? _selectedStudent;

  int _gradedCount = 0;

  final List<ExamStudent> _students = const [
    ExamStudent(
      matricule: '2024-001',
      nom: 'RAKOTO',
      prenom: 'Jean',
      present: true,
    ),
    ExamStudent(
      matricule: '2024-002',
      nom: 'RABE',
      prenom: 'Marie',
      present: true,
    ),
    ExamStudent(
      matricule: '2024-003',
      nom: 'RANDRIA',
      prenom: 'Paul',
      present: false,
    ),
    ExamStudent(
      matricule: '2024-004',
      nom: 'RAZAFI',
      prenom: 'Sarah',
      present: true,
    ),
  ];

  @override
  void dispose() {
    _matriculeController.dispose();
    _gradeController.dispose();
    super.dispose();
  }

  void _searchStudent() {
    final matricule = _matriculeController.text.trim();

    if (matricule.isEmpty) {
      return;
    }

    final student = _students.where(
      (student) => student.matricule == matricule,
    );

    setState(() {
      _selectedStudent = student.isNotEmpty ? student.first : null;
    });
  }

  void _validateGrade() {
    if (_selectedStudent == null) {
      return;
    }

    final grade = double.tryParse(_gradeController.text.replaceAll(',', '.'));

    if (grade == null || _gradeScale == null) {
      return;
    }

    if (grade < 0 || grade > _gradeScale!) {
      return;
    }

    setState(() {
      _gradedCount++;
      _gradeController.clear();
      _matriculeController.clear();
      _selectedStudent = null;
    });
  }

  void _publishGrades() {
    if (_gradedCount < widget.exam.presentStudents) {
      return;
    }

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text(
            'Publier les notes ?',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          content: Text(
            'Toutes les notes des ${widget.exam.presentStudents} '
            'étudiants présents ont été saisies.\n\n'
            'Une fois publiées, les notes seront disponibles pour les étudiants.',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Annuler'),
            ),

            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop();

                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Notes publiées avec succès.')),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Theme.of(context).colorScheme.primary,
                foregroundColor: Colors.white,
              ),
              child: const Text('Publier'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            GradeExamHeader(
              examName: widget.exam.name,
              professor: widget.exam.professor,
              session: widget.exam.session,
              onBack: () {
                Navigator.of(context).pop();
              },
            ),

            Expanded(
              child: ListView(
                padding: const EdgeInsets.fromLTRB(20, 20, 20, 30),
                children: [
                  GradeScaleField(
                    value: _gradeScale,
                    onChanged: (value) {
                      setState(() {
                        _gradeScale = value;
                      });
                    },
                  ),

                  const SizedBox(height: 20),

                  StudentSearchField(
                    controller: _matriculeController,
                    onSearch: _searchStudent,
                    gradedCount: _gradedCount,
                    totalCount: widget.exam.presentStudents,
                  ),

                  const SizedBox(height: 20),

                  if (_selectedStudent != null)
                    StudentGradeCard(
                      student: _selectedStudent!,
                      gradeController: _gradeController,
                      gradeScale: _gradeScale,
                      onValidate: _validateGrade,
                    ),

                  const SizedBox(height: 30),

                  SizedBox(
                    width: double.infinity,
                    height: 54,
                    child: ElevatedButton.icon(
                      onPressed: _gradedCount >= widget.exam.presentStudents
                          ? _publishGrades
                          : null,
                      icon: const Icon(Icons.publish_rounded),
                      label: const Text(
                        'Publier les notes',
                        style: TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Theme.of(context).colorScheme.primary,
                        foregroundColor: Colors.white,
                        disabledBackgroundColor: Colors.grey.shade200,
                        disabledForegroundColor: Colors.grey.shade500,
                        elevation: 0,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(14),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ExamStudent {
  final String matricule;
  final String nom;
  final String prenom;
  final bool present;

  const ExamStudent({
    required this.matricule,
    required this.nom,
    required this.prenom,
    required this.present,
  });
}
