# Machine Learning Knowledge Academy — Web

A lightweight Next.js App Router website for the Markdown-first ML question bank. This app lives in its own directory so existing Python projects, notebooks, exports, and Streamlit apps at repository root remain untouched.

## Requirements

- Node.js 20.9+ (use a current LTS release supported by Next.js)
- npm
- Git

## Run locally

From the repository root:

```bash
cd academy-web
npm install
npm run dev
```

Open http://localhost:3000.

The `predev` and `prebuild` scripts parse `../knowledge-bank/foundations/ml-foundations-001-050.md` and regenerate `src/data/questions.json`. Edit the Markdown source, not the generated JSON.

## Checks

```bash
npm run build:questions
npm run typecheck
npm run lint
npm run build
```

## Deploy to Vercel

1. Import `abhishekpandaOfficial/machine-learning-algorithms` into Vercel.
2. Set **Root Directory** to `academy-web`.
3. Use the detected Next.js framework and npm install/build commands.
4. Confirm the build command is `npm run build`.
5. Deploy to the Vercel preview URL first.
6. After verifying routes and existing domain behavior, attach the desired domain in Vercel's project settings and follow the DNS instructions it provides.

Do not change the repository's root Python requirements or replace the existing root README as part of this website deployment.

## Content flow

`knowledge-bank/foundations/ml-foundations-001-050.md` → build parser → `src/data/questions.json` → searchable and expandable question cards.

Markdown remains portable to GitHub, VS Code, Jupyter/Colab reference workflows, and future publishing systems. The website is a presentation layer over the same source content.
