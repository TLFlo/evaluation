import 'package:flutter/material.dart';

import '../widgets/logo.dart';
import '../widgets/login_form.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(
              horizontal: 24,
              vertical: 32,
            ),
            child: ConstrainedBox(
              constraints: const BoxConstraints(
                maxWidth: 420,
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const AppLogo(),

                  const SizedBox(height: 38),

                  // Text(
                  //   'Bienvenue',
                  //   style: Theme.of(context)
                  //       .textTheme
                  //       .headlineMedium
                  //       ?.copyWith(
                  //         fontWeight: FontWeight.bold,
                  //       ),
                  // ),

                  const SizedBox(height: 8),

                  Text(
                    'Bienvenu votre appli de scolarité! Connectez-vous à votre compte',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),

                  const SizedBox(height: 35),

                  const LoginForm(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}