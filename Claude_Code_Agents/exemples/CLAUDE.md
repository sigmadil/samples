# Projet : exemple

## Commandes
- Installer : `npm install`
- Tests : `npm test` (à lancer avant de déclarer une tâche terminée)
- Lint : `npm run lint`

## Conventions
- TypeScript strict, pas de `any`.
- Un composant par fichier, nommé en PascalCase.
- Messages de commit au format Conventional Commits, en français.

## Pièges connus
- Ne jamais modifier `src/generated/` : le dossier est régénéré par `npm run codegen`.
- Les tests d'intégration exigent `DATABASE_URL` ; sinon, lancer `npm run test:unit`.
