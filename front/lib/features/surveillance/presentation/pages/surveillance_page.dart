import 'package:flutter/material.dart';

import '../widgets/exam_room_card.dart';
import '../widgets/room_search_bar.dart';
import '../widgets/surveillance_header.dart';

class SurveillancePage extends StatefulWidget {
  const SurveillancePage({super.key});

  @override
  State<SurveillancePage> createState() => _SurveillancePageState();
}

class _SurveillancePageState extends State<SurveillancePage> {
  final TextEditingController _searchController = TextEditingController();

  final List<ExamRoom> _rooms = const [
    ExamRoom(
      roomNumber: 'A101',
      exam: 'Algèbre linéaire',
      schedule: '08:00 - 10:00',
      className: 'M1 GID',
    ),
    ExamRoom(
      roomNumber: 'A102',
      exam: 'Analyse numérique',
      schedule: '08:00 - 10:00',
      className: 'M1 GID',
    ),
    ExamRoom(
      roomNumber: 'B201',
      exam: 'Bases de données',
      schedule: '10:30 - 12:30',
      className: 'M1 GID',
    ),
    ExamRoom(
      roomNumber: 'B202',
      exam: 'Big Data',
      schedule: '10:30 - 12:30',
      className: 'M2 GID',
    ),
    ExamRoom(
      roomNumber: 'C301',
      exam: 'Programmation avancée',
      schedule: '14:00 - 16:00',
      className: 'M2 GID',
    ),
    ExamRoom(
      roomNumber: 'C302',
      exam: 'Intelligence artificielle',
      schedule: '14:00 - 16:00',
      className: 'M2 GID',
    ),
  ];

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: null,
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(20, 20, 20, 0),
                child: Column(
                  children: [
                    const SurveillanceHeader(),

                    const SizedBox(height: 24),

                    RoomSearchBar(
                      controller: _searchController,
                    ),

                    const SizedBox(height: 28),

                    Row(
                      children: [
                        Text(
                          'Mes salles',
                          style: Theme.of(context)
                              .textTheme
                              .titleLarge
                              ?.copyWith(
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                        const Spacer(),
                        Text(
                          '${_rooms.length} salles',
                          style:
                              Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    color: Colors.grey.shade600,
                                  ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 16),
                  ],
                ),
              ),
            ),

            SliverPadding(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 24),
              sliver: SliverGrid(
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    final room = _rooms[index];

                    return ExamRoomCard(
                      room: room,
                      onTap: () {
                        // Navigation vers la surveillance de cette salle.
                        debugPrint(
                          'Salle sélectionnée : ${room.roomNumber}',
                        );
                      },
                    );
                  },
                  childCount: _rooms.length,
                ),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 14,
                  mainAxisSpacing: 14,
                  childAspectRatio: 0.82,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ExamRoom {
  final String roomNumber;
  final String exam;
  final String schedule;
  final String className;

  const ExamRoom({
    required this.roomNumber,
    required this.exam,
    required this.schedule,
    required this.className,
  });
}