import 'package:flutter/material.dart';

import '../pages/surveillance_page.dart';

class ExamRoomCard extends StatelessWidget {
  final ExamRoom room;
  final VoidCallback onTap;

  const ExamRoomCard({super.key, required this.room, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(20),
      elevation: 2,
      shadowColor: primaryColor.withValues(alpha: 0.50),

      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Numéro de salle
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: primaryColor.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      room.roomNumber,
                      style: TextStyle(
                        color: primaryColor,
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                  ),

                  const Spacer(),

                  Icon(
                    Icons.arrow_forward_rounded,
                    size: 20,
                    color: Colors.grey.shade500,
                  ),
                ],
              ),

              const SizedBox(height: 18),

              // Examen
              Text(
                room.exam,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(
                  context,
                ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
              ),

              const Spacer(),

              // Horaire
              _RoomInfo(icon: Icons.access_time_rounded, text: room.schedule),

              const SizedBox(height: 8),

              // Classe
              _RoomInfo(icon: Icons.groups_outlined, text: room.className),
            ],
          ),
        ),
      ),
    );
  }
}

class _RoomInfo extends StatelessWidget {
  final IconData icon;
  final String text;

  const _RoomInfo({required this.icon, required this.text});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 17, color: Colors.grey.shade600),
        const SizedBox(width: 7),
        Expanded(
          child: Text(
            text,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: Theme.of(
              context,
            ).textTheme.bodySmall?.copyWith(color: Colors.grey.shade700),
          ),
        ),
      ],
    );
  }
}
