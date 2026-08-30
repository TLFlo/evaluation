import 'package:flutter/material.dart';

class CameraPreviewPlaceholder extends StatelessWidget {
  final VoidCallback onTap;

  const CameraPreviewPlaceholder({
    super.key,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: double.infinity,
        height: 420,
        decoration: BoxDecoration(
          color: Colors.black,
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.10),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Stack(
          alignment: Alignment.center,
          children: [
            Icon(
              Icons.camera_alt_rounded,
              size: 55,
              color: Colors.white.withValues(alpha: 0.7),
            ),

            // Cadre de détection du visage
            Container(
              width: 210,
              height: 270,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(110),
                border: Border.all(
                  color: primaryColor.withValues(alpha: 0.8),
                  width: 2,
                ),
              ),
            ),

            Positioned(
              bottom: 20,
              child: Text(
                'Appuyez pour simuler une reconnaissance',
                style: TextStyle(
                  color: Colors.white.withValues(alpha: 0.8),
                  fontSize: 12,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}