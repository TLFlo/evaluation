import 'package:flutter/material.dart';

import '../pages/exam_room_page.dart';

class PresenceFilterButton extends StatelessWidget {
  final PresenceFilter selectedFilter;
  final ValueChanged<PresenceFilter> onChanged;

  const PresenceFilterButton({
    super.key,
    required this.selectedFilter,
    required this.onChanged,
  });

  String get _label {
    switch (selectedFilter) {
      case PresenceFilter.all:
        return 'Tous';
      case PresenceFilter.present:
        return 'Présents';
      case PresenceFilter.absent:
        return 'Absents';
    }
  }

  @override
  Widget build(BuildContext context) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    return PopupMenuButton<PresenceFilter>(
      onSelected: onChanged,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
      ),
      itemBuilder: (context) => [
        const PopupMenuItem(
          value: PresenceFilter.all,
          child: Text('Tous les étudiants'),
        ),
        const PopupMenuItem(
          value: PresenceFilter.present,
          child: Text('Présents seulement'),
        ),
        const PopupMenuItem(
          value: PresenceFilter.absent,
          child: Text('Absents seulement'),
        ),
      ],
      child: Container(
        height: 56,
        padding: const EdgeInsets.symmetric(horizontal: 13),
        decoration: BoxDecoration(
          color: primaryColor.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(14),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.filter_list_rounded,
              color: primaryColor,
              size: 21,
            ),
            const SizedBox(width: 6),
            Text(
              _label,
              style: TextStyle(
                color: primaryColor,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}