import 'package:flutter/material.dart';

class StudentSearchField extends StatelessWidget {
  final TextEditingController controller;
  final VoidCallback onSearch;

  final int gradedCount;
  final int totalCount;

  const StudentSearchField({
    super.key,
    required this.controller,
    required this.onSearch,
    required this.gradedCount,
    required this.totalCount,
  });

  @override
  Widget build(BuildContext context) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    return Row(
      children: [
        Expanded(
          child: TextField(
            controller: controller,
            textInputAction: TextInputAction.search,
            onSubmitted: (_) => onSearch(),
            decoration: InputDecoration(
              hintText: 'Saisir le matricule...',
              prefixIcon: Icon(Icons.badge_outlined, color: primaryColor),
              suffixIcon: IconButton(
                onPressed: onSearch,
                icon: Icon(Icons.search_rounded, color: primaryColor),
              ),
              filled: true,
              fillColor: primaryColor.withValues(alpha: 0.08),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(14),
                borderSide: BorderSide.none,
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(14),
                borderSide: BorderSide.none,
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(14),
                borderSide: BorderSide(color: primaryColor, width: 1.5),
              ),
            ),
          ),
        ),

        const SizedBox(width: 12),

        Text(
          '$gradedCount / $totalCount',
          style: TextStyle(
            color: primaryColor,
            fontSize: 15,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }
}
