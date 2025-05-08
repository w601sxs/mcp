# AWS Web Application Starter Template for Code Assistants

A modern React starter template optimized for building customized web applications on AWS. This template provides a solid foundation with React, TypeScript, Vite, Tailwind CSS, and shadcn/ui components, integrated with AWS Amplify for authentication and backend services.

## Features

- **Modern Frontend Stack**
  - React 18 with TypeScript
  - Vite for fast development and optimized builds
  - Tailwind CSS v3 for utility-first styling
  - shadcn/ui components for a beautiful, accessible UI

- **AWS Integration**
  - AWS Amplify for Authentication (Cognito)
  - Pre-configured authentication flows
  - Ready for AWS service integration

- **Developer Experience**
  - Component-based architecture
  - Type safety with TypeScript
  - ESLint configured for code quality
  - Responsive layouts ready to go

## Project Structure

```
├── public/              # Static assets
├── src/
│   ├── assets/          # Project assets
│   ├── components/      # Reusable components
│   │   ├── ui/          # shadcn/ui components
│   │   ├── chat/        # Chat interface components
│   │   ├── tasks/       # Task management components
│   │   └── app-sidebar.tsx # Main application sidebar
│   ├── hooks/           # Custom React hooks
│   ├── layouts/         # Page layouts
│   │   ├── private-layout.tsx # Layout for authenticated users
│   │   └── public-layout.tsx  # Layout for unauthenticated users
│   ├── lib/             # Utility functions and libraries
│   ├── pages/           # Page components
│   │   ├── dashboard.tsx # Main dashboard page
│   │   ├── login.tsx     # Authentication page
│   │   ├── settings.tsx  # User settings page
│   │   └── not-found.tsx # 404 page
│   ├── routes/          # Application routing
│   ├── store/           # State management
│   ├── App.tsx          # Main application component
│   └── main.tsx         # Application entry point
├── amplify_outputs.json # AWS Amplify configuration
├── components.json      # shadcn/ui configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── vite.config.ts       # Vite configuration
```

## Getting Started

1. **Clone the repository**

```bash
git clone <repository-url>
cd <repository-name>
```

2. **Install dependencies**

```bash
npm install
```

3. **Start the development server**

```bash
npm run dev
```

4. **Build for production**

```bash
npm run build
```

## AWS Configuration

This template comes with a pre-configured AWS Amplify setup for authentication. 

## UI Components

This template uses [shadcn/ui](https://ui.shadcn.com/) components, which are styled with Tailwind CSS. These components are copy-pasted into your project, giving you complete control over your UI.

Available components include:
- Avatar
- Button
- Card
- Dialog
- Dropdown Menu
- Form
- Input
- Select
- Sidebar
- Table
- Tabs
- and many more

## Customization

This template is designed to be a starting point for your application. You can customize it to fit your specific needs:

- Add or remove components as needed
- Customize the theme in `tailwind.config.js`

## License

MIT
