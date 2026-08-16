import 'package:flutter/material.dart';

class StudentSearchBar extends StatelessWidget {
  final TextEditingController controller;

  const StudentSearchBar({
    super.key,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    return TextField(
      controller: controller,
      decoration: InputDecoration(
        hintText: 'Rechercher un étudiant...',
        prefixIcon: Icon(
          Icons.search_rounded,
          color: primaryColor,
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
          borderSide: BorderSide(
            color: primaryColor.withValues(alpha: 0.5),
          ),
        ),
      ),
    );
  }
}