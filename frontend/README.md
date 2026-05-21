# Frontend - Insurance Claims Workbench

Next.js 16 frontend application built with shadcn/ui components for the multi-agent insurance claims processing system.

## Features

- **Next.js 16** with App Router
- **React 19** with latest features
- **shadcn/ui** components for beautiful UI
- **Tailwind CSS v4** for styling
- **TypeScript** for type safety

## Local Development

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Troubleshooting

### React 19 Compatibility

The dependency set has been upgraded for React 19 and Next.js 16. Use the checked-in lockfile with `npm install`.

## Environment Variables

For local development, the frontend automatically connects to `http://localhost:8000` for the backend API.

In production (Azure Container Apps), it automatically detects and connects to the deployed backend.

## Adding shadcn/ui Components

```bash
npx shadcn@latest add button
npx shadcn@latest add button card dialog
```

## Deployment

This frontend deploys to Azure Container Apps alongside the FastAPI backend:

```bash
azd auth login
azd up
```

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
