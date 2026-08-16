import 'package:flutter/material.dart';

import '../widgets/exam_room_header.dart';
import '../widgets/student_card.dart';
import '../widgets/student_search_bar.dart';
import '../widgets/presence_filter.dart';

enum PresenceFilter {
  all,
  present,
  absent,
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

class ExamRoomPage extends StatefulWidget {
  final String roomNumber;
  final String examName;
  final String className;

  const ExamRoomPage({
    super.key,
    required this.roomNumber,
    required this.examName,
    required this.className,
  });

  @override
  State<ExamRoomPage> createState() => _ExamRoomPageState();
}

class _ExamRoomPageState extends State<ExamRoomPage> {
  final TextEditingController _searchController = TextEditingController();

  PresenceFilter _selectedFilter = PresenceFilter.all;

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
      present: false,
    ),
    ExamStudent(
      matricule: '2024-003',
      nom: 'RANDRIA',
      prenom: 'Paul',
      present: true,
    ),
    ExamStudent(
      matricule: '2024-004',
      nom: 'RAZAFI',
      prenom: 'Sarah',
      present: true,
    ),
    ExamStudent(
      matricule: '2024-005',
      nom: 'ANDRIAM',
      prenom: 'Lucas',
      present: false,
    ),
    ExamStudent(
      matricule: '2024-006',
      nom: 'RANAIVO',
      prenom: 'Emma',
      present: true,
    ),
  ];

  List<ExamStudent> get _filteredStudents {
    final query = _searchController.text.trim().toLowerCase();

    return _students.where((student) {
      final matchesSearch =
          student.matricule.toLowerCase().contains(query) ||
          student.nom.toLowerCase().contains(query) ||
          student.prenom.toLowerCase().contains(query);

      final matchesFilter = switch (_selectedFilter) {
        PresenceFilter.all => true,
        PresenceFilter.present => student.present,
        PresenceFilter.absent => !student.present,
      };

      return matchesSearch && matchesFilter;
    }).toList();
  }

  @override
  void initState() {
    super.initState();

    _searchController.addListener(() {
      setState(() {});
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _changeFilter(PresenceFilter filter) {
    setState(() {
      _selectedFilter = filter;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            ExamRoomHeader(
              examName: widget.examName,
              className: widget.className,
              onBack: () => Navigator.of(context).pop(),
              onPresence: () {
                debugPrint('Pointage');
              },
            ),

            Padding(
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 12),
              child: Row(
                children: [
                  Expanded(
                    child: StudentSearchBar(
                      controller: _searchController,
                    ),
                  ),

                  const SizedBox(width: 10),

                  PresenceFilterButton(
                    selectedFilter: _selectedFilter,
                    onChanged: _changeFilter,
                  ),
                ],
              ),
            ),

            Expanded(
              child: _filteredStudents.isEmpty
                  ? const Center(
                      child: Text(
                        'Aucun étudiant trouvé',
                      ),
                    )
                  : ListView.separated(
                      padding: const EdgeInsets.fromLTRB(
                        20,
                        8,
                        20,
                        24,
                      ),
                      itemCount: _filteredStudents.length,
                      separatorBuilder: (_, _) => const SizedBox(height: 10),
                      itemBuilder: (context, index) {
                        final student = _filteredStudents[index];

                        return StudentCard(
                          student: student,
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}