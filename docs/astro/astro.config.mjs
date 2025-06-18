import starlight from "@astrojs/starlight";
import tailwindcss from "@tailwindcss/vite";
// @ts-check
import { defineConfig } from "astro/config";

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: "AWS MCP Servers",
			customCss: ["./src/styles/global.css"],
			social: [
				{
					icon: "github",
					label: "GitHub",
					href: "https://github.com/awslabs/mcp",
				},
			],
			sidebar: [
				{
					label: "Guide",
					items: [
						{ label: "Get Started", slug: "index" },
						{ label: "Samples", slug: "samples"},
						{ label: "Contributing", slug: "contributing/contributing"},
						{ label: "Disclaimer", slug: "contributing/disclaimer"},
					],
				},
				{
					label: "Browse by What You're Building",
					items: [
						{ 
							label: "📚 Real-time access to official AWS documentation",
							items: [
								{ label: "Documentation", slug: "building/aws-documentation" }
							]
							
						},
						{ 
							label: "🏗️ Infrastructure & Deployment", 
							items: [
								{ label: "Infrastructure as Code", slug: "building/infrastructure-as-code" },
								{ label: "Container Platforms", slug: "building/container-platforms" },
								{ label: "Serverless & Functions", slug: "building/serverless-functions" },
								{ label: "Support", slug: "building/support" }
							]
						},
						{ 
							label: "🤖 AI & Machine Learning",
							items: [
								{ label: "AI & ML", slug: "building/ai-machine-learning" }
							]
							
						},
						{ 
							label: "📊 Data & Analytics", 
							items: [
								{ label: "SQL & NoSQL Databases", slug: "building/sql-nosql-databases" },
								{ label: "Search & Analytics", slug: "building/search-analytics" },
								{ label: "Caching & Performance", slug: "building/caching-performance" }
							]
						},
						{ 
							label: "🛠️ Developer Tools & Support",
							items: [
								{ label: "Developer Tools", slug: "building/developer-tools" }
							]
						},
						{ 
							label: "📡 Integration & Messaging",
							items: [
								{ label: "Integration & Messaging", slug: "building/integration-messaging" }
							]
						},
						{ 
							label: "💰 Cost & Operations",
							items: [
								{ label: "Cost & Monitoring", slug: "building/cost-operations" }
							]
						},
					],
				},
				{
					label: "Browse by How You're Working",
					items: [
						{ 
							label: "👨‍💻 Vibe Coding & Development", 
							items: [
								{ label: "Core Development Workflow", slug: "workflows/core-development-workflow" },
								{ label: "Infrastructure as Code", slug: "workflows/infrastructure-as-code" },
								{ label: "Application Development", slug: "workflows/application-development" },
								{ label: "Container & Serverless Development", slug: "workflows/container-serverless-development" },
								{ label: "Testing & Data", slug: "workflows/testing-data" }
							]
						},
						{ 
							label: "💬 Conversational Assistants",
							items: [
								{ label: "Knowledge & Search", slug: "workflows/knowledge-search" },
								{ label: "Content Processing & Generation", slug: "workflows/content-processing-generation" },
								{ label: "Business Services", slug: "workflows/business-services" }
							]
						},
						{ 
							label: "🤖 Autonomous Background Agents", 
							items: [
								{ label: "Data Operations & ETL", slug: "workflows/data-operations-etl" },
								{ label: "Caching & Performance", slug: "workflows/caching-performance" },
								{ label: "Workflow & Integration", slug: "workflows/workflow-integration" },
								{ label: "Operations & Monitoring", slug: "workflows/operations-monitoring" }
							]
						}
					],
				},
			],
		}),
	],
	vite: {
		plugins: [tailwindcss()],
	},
});
