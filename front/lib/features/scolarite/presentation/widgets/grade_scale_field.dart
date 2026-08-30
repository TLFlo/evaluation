import 'package:flutter/material.dart';

class GradeScaleField extends StatelessWidget {
  final double? value;
  final ValueChanged<double?> onChanged;

  const GradeScaleField({
    super.key,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    return Row(
      children: [
        Text(
          'Note sur :',
          style: Theme.of(context)
              .textTheme
              .titleSmall
              ?.copyWith(
                fontWeight: FontWeight.w600,
              ),
        ),

        const SizedBox(width: 12),

        SizedBox(
          width: 90,
          child: TextFormField(
            keyboardType: const TextInputType.numberWithOptions(
              decimal: true,
            ),
            textAlign: TextAlign.center,
            decoration: InputDecoration(
              hintText: '20',
              filled: true,
              fillColor: primaryColor.withValues(alpha: 0.08),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide.none,
              ),
            ),
            onChanged: (text) {
              onChanged(double.tryParse(text));
            },
          ),
        ),
      ],
    );
  }
}