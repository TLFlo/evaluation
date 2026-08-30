import 'package:flutter/material.dart';

import '../widgets/presence/presence_header.dart';
import '../widgets/presence/camera_preview_placeholder.dart';
import '../widgets/presence/recognition_result_card.dart';

class PresencePage extends StatefulWidget {
  final String examName;
  final String className;
  final String roomNumber;

  const PresencePage({
    super.key,
    required this.examName,
    required this.className,
    required this.roomNumber,
  });

  @override
  State<PresencePage> createState() => _PresencePageState();
}

class _PresencePageState extends State<PresencePage> {
  // Pour le moment, on simule l'état de reconnaissance.
  bool isRecognized = false;

  void _simulateRecognition() {
    setState(() {
      isRecognized = true;
    });
  }

  void _resetRecognition() {
    setState(() {
      isRecognized = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            PresenceHeader(
              examName: widget.examName,
              className: widget.className,
              roomNumber: widget.roomNumber,
              onBack: () {
                Navigator.of(context).pop();
              },
            ),

            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.fromLTRB(
                  20,
                  20,
                  20,
                  30,
                ),
                child: Column(
                  children: [
                    CameraPreviewPlaceholder(
                      onTap: _simulateRecognition,
                    ),

                    const SizedBox(height: 24),

                    if (isRecognized)
                      RecognitionResultCard(
                        matricule: '2024-001',
                        nom: 'RAKOTO',
                        prenom: 'Jean',
                        isPresent: true,
                        onReset: _resetRecognition,
                      )
                    else
                      const _ScanningInstruction(),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ScanningInstruction extends StatelessWidget {
  const _ScanningInstruction();

  @override
  Widget build(BuildContext context) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    return Column(
      children: [
        Icon(
          Icons.face_retouching_natural_rounded,
          size: 42,
          color: primaryColor.withValues(alpha: 0.7),
        ),

        const SizedBox(height: 12),

        Text(
          'Positionnez le visage devant la caméra',
          textAlign: TextAlign.center,
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.w600,
              ),
        ),

        const SizedBox(height: 6),

        Text(
          'Le système identifiera automatiquement l’étudiant.',
          textAlign: TextAlign.center,
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: Colors.grey.shade600,
              ),
        ),
      ],
    );
  }
}