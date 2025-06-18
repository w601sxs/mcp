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
								{ label: "AWS Documentation MCP Server", slug: "servers/aws-documentation-mcp-server" }
							]
						},
						{
							label: "🏗️ Infrastructure & Deployment",
							items: [
								{
									label: "Infrastructure as Code",
									items: [
										{ label: "AWS CDK MCP Server", slug: "servers/cdk-mcp-server" },
										{ label: "AWS Terraform MCP Server", slug: "servers/terraform-mcp-server" },
										{ label: "AWS CloudFormation MCP Server", slug: "servers/cfn-mcp-server" }
									]
								},
								{
									label: "Container Platforms",
									items: [
										{ label: "Amazon EKS MCP Server", slug: "servers/eks-mcp-server" },
										{ label: "Amazon ECS MCP Server", slug: "servers/ecs-mcp-server" },
										{ label: "Finch MCP Server", slug: "servers/finch-mcp-server" }
									]
								},
								{
									label: "Serverless & Functions",
									items: [
										{ label: "AWS Serverless MCP Server", slug: "servers/aws-serverless-mcp-server" },
										{ label: "AWS Lambda Tool MCP Server", slug: "servers/lambda-tool-mcp-server" }
									]
								},
								{
									label: "Support",
									items: [
										{ label: "AWS Support MCP Server", slug: "servers/aws-support-mcp-server" }
									]
								}
							]
						},
						{
							label: "🤖 AI & Machine Learning",
							items: [
								{ label: "Bedrock Knowledge Bases Retrieval MCP Server", slug: "servers/bedrock-kb-retrieval-mcp-server" },
								{ label: "Amazon Kendra Index MCP Server", slug: "servers/kendra-index-mcp-server" },
								{ label: "Amazon Q index MCP Server", slug: "servers/amazon-qindex-mcp-server" },
								{ label: "Amazon Nova Canvas MCP Server", slug: "servers/nova-canvas-mcp-server" },
								{ label: "Amazon Bedrock Data Automation MCP Server", slug: "servers/aws-bedrock-data-automation-mcp-server" }
							]
						},
						{
							label: "📊 Data & Analytics",
							items: [
								{
									label: "SQL & NoSQL Databases",
									items: [
										{ label: "Amazon DynamoDB MCP Server", slug: "servers/dynamodb-mcp-server" },
										{ label: "Amazon Aurora PostgreSQL MCP Server", slug: "servers/postgres-mcp-server" },
										{ label: "Amazon Aurora MySQL MCP Server", slug: "servers/mysql-mcp-server" },
										{ label: "Amazon Aurora DSQL MCP Server", slug: "servers/aurora-dsql-mcp-server" },
										{ label: "Amazon DocumentDB MCP Server", slug: "servers/documentdb-mcp-server" },
										{ label: "Amazon Neptune MCP Server", slug: "servers/amazon-neptune-mcp-server" },
										{ label: "Amazon Keyspaces MCP Server", slug: "servers/amazon-keyspaces-mcp-server" },
										{ label: "Amazon Timestream for InfluxDB MCP Server", slug: "servers/timestream-for-influxdb-mcp-server" }
									]
								},
								{
									label: "Caching & Performance",
									items: [
										{ label: "Amazon ElastiCache MCP Server", slug: "servers/elasticache-mcp-server" },
										{ label: "Amazon ElastiCache / MemoryDB for Valkey MCP Server", slug: "servers/valkey-mcp-server" },
										{ label: "Amazon ElastiCache for Memcached MCP Server", slug: "servers/memcached-mcp-server" }
									]
								}
							]
						},
						{
							label: "🛠️ Developer Tools & Support",
							items: [
								{ label: "Git Repo Research MCP Server", slug: "servers/git-repo-research-mcp-server" },
								{ label: "Code Doc Gen MCP Server", slug: "servers/code-doc-gen-mcp-server" },
								{ label: "AWS Diagram MCP Server", slug: "servers/aws-diagram-mcp-server" },
								{ label: "Frontend MCP Server", slug: "servers/frontend-mcp-server" },
								{ label: "Synthetic Data MCP Server", slug: "servers/syntheticdata-mcp-server" },
								{ label: "Core MCP Server", slug: "servers/core-mcp-server" }
							]
						},
						{
							label: "📡 Integration & Messaging",
							items: [
								{ label: "Amazon SNS / SQS MCP Server", slug: "servers/amazon-sns-sqs-mcp-server" },
								{ label: "Amazon MQ MCP Server", slug: "servers/amazon-mq-mcp-server" },
								{ label: "AWS Step Functions Tool MCP Server", slug: "servers/stepfunctions-tool-mcp-server" },
								{ label: "Amazon Location Service MCP Server", slug: "servers/aws-location-mcp-server" }
							]
						},
						{
							label: "💰 Cost & Operations",
							items: [
								{ label: "Cost Analysis MCP Server", slug: "servers/cost-analysis-mcp-server" },
								{ label: "AWS Cost Explorer MCP Server", slug: "servers/cost-explorer-mcp-server" },
								{ label: "Amazon CloudWatch Logs MCP Server", slug: "servers/cloudwatch-logs-mcp-server" },
								{ label: "AWS Managed Prometheus MCP Server", slug: "servers/prometheus-mcp-server" }
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
								{
									label: "Core Development Workflow",
									items: [
										{ label: "Core MCP Server", slug: "servers/core-mcp-server" },
										{ label: "AWS Documentation MCP Server", slug: "servers/aws-documentation-mcp-server" },
										{ label: "Git Repo Research MCP Server", slug: "servers/git-repo-research-mcp-server" }
									]
								},
								{
									label: "Infrastructure as Code",
									items: [
										{ label: "AWS CDK MCP Server", slug: "servers/cdk-mcp-server" },
										{ label: "AWS Terraform MCP Server", slug: "servers/terraform-mcp-server" },
										{ label: "AWS CloudFormation MCP Server", slug: "servers/cfn-mcp-server" }
									]
								},
								{
									label: "Application Development",
									items: [
										{ label: "Frontend MCP Server", slug: "servers/frontend-mcp-server" },
										{ label: "AWS Diagram MCP Server", slug: "servers/aws-diagram-mcp-server" },
										{ label: "Code Doc Gen MCP Server", slug: "servers/code-doc-gen-mcp-server" }
									]
								},
								{
									label: "Container & Serverless Development",
									items: [
										{ label: "Amazon EKS MCP Server", slug: "servers/eks-mcp-server" },
										{ label: "Amazon ECS MCP Server", slug: "servers/ecs-mcp-server" },
										{ label: "Finch MCP Server", slug: "servers/finch-mcp-server" },
										{ label: "AWS Serverless MCP Server", slug: "servers/aws-serverless-mcp-server" }
									]
								},
								{
									label: "Testing & Data",
									items: [
										{ label: "Synthetic Data MCP Server", slug: "servers/syntheticdata-mcp-server" }
									]
								}
							]
						},
						{
							label: "💬 Conversational Assistants",
							items: [
								{
									label: "Knowledge & Search",
									items: [
										{ label: "Bedrock Knowledge Bases Retrieval MCP Server", slug: "servers/bedrock-kb-retrieval-mcp-server" },
										{ label: "Amazon Kendra Index MCP Server", slug: "servers/kendra-index-mcp-server" },
										{ label: "Amazon Q index MCP Server", slug: "servers/amazon-qindex-mcp-server" },
										{ label: "AWS Documentation MCP Server", slug: "servers/aws-documentation-mcp-server" }
									]
								},
								{
									label: "Content Processing & Generation",
									items: [
										{ label: "Amazon Nova Canvas MCP Server", slug: "servers/nova-canvas-mcp-server" },
										{ label: "Amazon Bedrock Data Automation MCP Server", slug: "servers/aws-bedrock-data-automation-mcp-server" }
									]
								},
								{
									label: "Business Services",
									items: [
										{ label: "Amazon Location Service MCP Server", slug: "servers/aws-location-mcp-server" },
										{ label: "Cost Analysis MCP Server", slug: "servers/cost-analysis-mcp-server" },
										{ label: "AWS Cost Explorer MCP Server", slug: "servers/cost-explorer-mcp-server" }
									]
								}
							]
						},
						{
							label: "🤖 Autonomous Background Agents",
							items: [
								{
									label: "Data Operations & ETL",
									items: [
										{ label: "Amazon DynamoDB MCP Server", slug: "servers/dynamodb-mcp-server" },
										{ label: "Amazon Aurora PostgreSQL MCP Server", slug: "servers/postgres-mcp-server" },
										{ label: "Amazon Aurora MySQL MCP Server", slug: "servers/mysql-mcp-server" },
										{ label: "Amazon Aurora DSQL MCP Server", slug: "servers/aurora-dsql-mcp-server" },
										{ label: "Amazon DocumentDB MCP Server", slug: "servers/documentdb-mcp-server" },
										{ label: "Amazon Neptune MCP Server", slug: "servers/amazon-neptune-mcp-server" },
										{ label: "Amazon Keyspaces MCP Server", slug: "servers/amazon-keyspaces-mcp-server" },
										{ label: "Amazon Timestream for InfluxDB MCP Server", slug: "servers/timestream-for-influxdb-mcp-server" }
									]
								},
								{
									label: "Caching & Performance",
									items: [
										{ label: "Amazon ElastiCache / MemoryDB for Valkey MCP Server", slug: "servers/valkey-mcp-server" },
										{ label: "Amazon ElastiCache for Memcached MCP Server", slug: "servers/memcached-mcp-server" }
									]
								},
								{
									label: "Workflow & Integration",
									items: [
										{ label: "AWS Lambda Tool MCP Server", slug: "servers/lambda-tool-mcp-server" },
										{ label: "AWS Step Functions Tool MCP Server", slug: "servers/stepfunctions-tool-mcp-server" },
										{ label: "Amazon SNS / SQS MCP Server", slug: "servers/amazon-sns-sqs-mcp-server" },
										{ label: "Amazon MQ MCP Server", slug: "servers/amazon-mq-mcp-server" }
									]
								},
								{
									label: "Operations & Monitoring",
									items: [
										{ label: "Amazon CloudWatch Logs MCP Server", slug: "servers/cloudwatch-logs-mcp-server" },
										{ label: "AWS Cost Explorer MCP Server", slug: "servers/cost-explorer-mcp-server" },
										{ label: "AWS Managed Prometheus MCP Server", slug: "servers/prometheus-mcp-server" }
									]
								}
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
