import 'package:flutter/material.dart';

class SurveillanceHeader extends StatelessWidget {
  const SurveillanceHeader({super.key});

  @override
  Widget build(BuildContext context) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    return Row(
      children: [
        // Logo
        Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: primaryColor,
            borderRadius: BorderRadius.circular(14),
          ),
          child: Image.asset(
            'assets/images/logo_eni.png',
            width: 30,
            height: 30,
            fit: BoxFit.contain,
          ),
        ),

        const Spacer(),

        // Profil
        _HeaderIconButton(
          icon: Icons.person_outline_rounded,
          iconColor: primaryColor,

          onPressed: () {
            debugPrint('Profil');
          },
        ),

        const SizedBox(width: 8),

        // Notifications
        Stack(
          children: [
            _HeaderIconButton(
              icon: Icons.notifications_none_rounded,

              iconColor: primaryColor,

              onPressed: () {
                debugPrint('Notifications');
              },
            ),

            Positioned(
              top: 6,
              right: 6,
              child: Container(
                width: 8,
                height: 8,
                decoration: BoxDecoration(
                  color: Colors.red,
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white, width: 1.5),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }
}

class _HeaderIconButton extends StatelessWidget {
  final IconData icon;
  final Color iconColor;

  final VoidCallback onPressed;

  const _HeaderIconButton({
    required this.icon,
    required this.iconColor,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,

      borderRadius: BorderRadius.circular(14),
      child: InkWell(
        onTap: onPressed,
        borderRadius: BorderRadius.circular(14),
        child: SizedBox(width: 48, height: 48, child: Icon(icon, size: 28, color: iconColor,)),
      ),
    );
  }
}
