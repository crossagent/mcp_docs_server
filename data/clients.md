This page provides an overview of applications that support the Model Context Protocol (MCP). Each client may support different MCP features, allowing for varying levels of integration with MCP servers.

## [​](#feature-support-matrix) Feature support matrix

| Client | [Resources](https://modelcontextprotocol.io/docs/concepts/resources) | [Prompts](https://modelcontextprotocol.io/docs/concepts/prompts) | [Tools](https://modelcontextprotocol.io/docs/concepts/tools) | [Sampling](https://modelcontextprotocol.io/docs/concepts/sampling) | Roots | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| [5ire](https://github.com/nanbingxyz/5ire) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools. |
| [Apify MCP Tester](https://apify.com/jiri.spilka/tester-mcp-client) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools |
| [BeeAI Framework](https://i-am-bee.github.io/beeai-framework) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools in agentic workflows. |
| [Claude Code](https://claude.ai/code) | ❌ | ✅ | ✅ | ❌ | ❌ | Supports prompts and tools |
| [Claude Desktop App](https://claude.ai/download) | ✅ | ✅ | ✅ | ❌ | ❌ | Supports tools, prompts, and resources. |
| [Cline](https://github.com/cline/cline) | ✅ | ❌ | ✅ | ❌ | ❌ | Supports tools and resources. |
| [Continue](https://github.com/continuedev/continue) | ✅ | ✅ | ✅ | ❌ | ❌ | Supports tools, prompts, and resources. |
| [Copilot-MCP](https://github.com/VikashLoomba/copilot-mcp) | ✅ | ❌ | ✅ | ❌ | ❌ | Supports tools and resources. |
| [Cursor](https://cursor.com) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools. |
| [Daydreams Agents](https://github.com/daydreamsai/daydreams) | ✅ | ✅ | ✅ | ❌ | ❌ | Support for drop in Servers to Daydreams agents |
| [Emacs Mcp](https://github.com/lizqwerscott/mcp.el) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools in Emacs. |
| [fast-agent](https://github.com/evalstate/fast-agent) | ✅ | ✅ | ✅ | ✅ | ✅ | Full multimodal MCP support, with end-to-end tests |
| [Genkit](https://github.com/firebase/genkit) | ⚠️ | ✅ | ✅ | ❌ | ❌ | Supports resource list and lookup through tools. |
| [GenAIScript](https://microsoft.github.io/genaiscript/reference/scripts/mcp-tools/) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools. |
| [Goose](https://block.github.io/goose/docs/goose-architecture/#interoperability-with-extensions) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools. |
| [LibreChat](https://github.com/danny-avila/LibreChat) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools for Agents |
| [mcp-agent](https://github.com/lastmile-ai/mcp-agent) | ❌ | ❌ | ✅ | ⚠️ | ❌ | Supports tools, server connection management, and agent workflows. |
| [Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools |
| [OpenSumi](https://github.com/opensumi/core) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools in OpenSumi |
| [oterm](https://github.com/ggozad/oterm) | ❌ | ✅ | ✅ | ❌ | ❌ | Supports tools and prompts. |
| [Roo Code](https://roocode.com) | ✅ | ❌ | ✅ | ❌ | ❌ | Supports tools and resources. |
| [Sourcegraph Cody](https://sourcegraph.com/cody) | ✅ | ❌ | ❌ | ❌ | ❌ | Supports resources through OpenCTX |
| [SpinAI](https://spinai.dev) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools for Typescript AI Agents |
| [Superinterface](https://superinterface.ai) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools |
| [TheiaAI/TheiaIDE](https://eclipsesource.com/blogs/2024/12/19/theia-ide-and-theia-ai-support-mcp/) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools for Agents in Theia AI and the AI-powered Theia IDE |
| [VS Code GitHub Copilot](https://code.visualstudio.com/) | ❌ | ❌ | ✅ | ❌ | ✅ | Supports dynamic tool/roots discovery, secure secret configuration, and explicit tool prompting |
| [Windsurf Editor](https://codeium.com/windsurf) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools with AI Flow for collaborative development. |
| [Witsy](https://github.com/nbonamy/witsy) | ❌ | ❌ | ✅ | ❌ | ❌ | Supports tools in Witsy. |
| [Zed](https://zed.dev) | ❌ | ✅ | ❌ | ❌ | ❌ | Prompts appear as slash commands |

## [​](#client-details) Client details

### [​](#5ire) 5ire

[5ire](https://github.com/nanbingxyz/5ire) is an open source cross-platform desktop AI assistant that supports tools through MCP servers.

**Key features:**

* Built-in MCP servers can be quickly enabled and disabled.
* Users can add more servers by modifying the configuration file.
* It is open-source and user-friendly, suitable for beginners.
* Future support for MCP will be continuously improved.

### [​](#apify-mcp-tester) Apify MCP Tester

[Apify MCP Tester](https://github.com/apify/tester-mcp-client) is an open-source client that connects to any MCP server using Server-Sent Events (SSE).
It is a standalone Apify Actor designed for testing MCP servers over SSE, with support for Authorization headers.
It uses plain JavaScript (old-school style) and is hosted on Apify, allowing you to run it without any setup.

**Key features:**

* Connects to any MCP server via SSE.
* Works with the [Apify MCP Server](https://apify.com/apify/actors-mcp-server) to interact with one or more Apify [Actors](https://apify.com/store).
* Dynamically utilizes tools based on context and user queries (if supported by the server).

### [​](#beeai-framework) BeeAI Framework

[BeeAI Framework](https://i-am-bee.github.io/beeai-framework) is an open-source framework for building, deploying, and serving powerful agentic workflows at scale. The framework includes the **MCP Tool**, a native feature that simplifies the integration of MCP servers into agentic workflows.

**Key features:**

* Seamlessly incorporate MCP tools into agentic workflows.
* Quickly instantiate framework-native tools from connected MCP client(s).
* Planned future support for agentic MCP capabilities.

**Learn more:**

* [Example of using MCP tools in agentic workflow](https://i-am-bee.github.io/beeai-framework/#/typescript/tools?id=using-the-mcptool-class)

### [​](#claude-code) Claude Code

Claude Code is an interactive agentic coding tool from Anthropic that helps you code faster through natural language commands. It supports MCP integration for prompts and tools, and also functions as an MCP server to integrate with other clients.

**Key features:**

* Tool and prompt support for MCP servers
* Offers its own tools through an MCP server for integrating with other MCP clients

### [​](#claude-desktop-app) Claude Desktop App

The Claude desktop application provides comprehensive support for MCP, enabling deep integration with local tools and data sources.

**Key features:**

* Full support for resources, allowing attachment of local files and data
* Support for prompt templates
* Tool integration for executing commands and scripts
* Local server connections for enhanced privacy and security

> ⓘ Note: The Claude.ai web application does not currently support MCP. MCP features are only available in the desktop application.

### [​](#cline) Cline

[Cline](https://github.com/cline/cline) is an autonomous coding agent in VS Code that edits files, runs commands, uses a browser, and more–with your permission at each step.

**Key features:**

* Create and add tools through natural language (e.g. “add a tool that searches the web”)
* Share custom MCP servers Cline creates with others via the `~/Documents/Cline/MCP` directory
* Displays configured MCP servers along with their tools, resources, and any error logs

### [​](#continue) Continue

[Continue](https://github.com/continuedev/continue) is an open-source AI code assistant, with built-in support for all MCP features.

**Key features**

* Type ”@” to mention MCP resources
* Prompt templates surface as slash commands
* Use both built-in and MCP tools directly in chat
* Supports VS Code and JetBrains IDEs, with any LLM

### [​](#copilot-mcp) Copilot-MCP

[Copilot-MCP](https://github.com/VikashLoomba/copilot-mcp) enables AI coding assistance via MCP.

**Key features:**

* Support for MCP tools and resources
* Integration with development workflows
* Extensible AI capabilities

### [​](#cursor) Cursor

[Cursor](https://docs.cursor.com/advanced/model-context-protocol) is an AI code editor.

**Key Features**:

* Support for MCP tools in Cursor Composer
* Support for both STDIO and SSE

### [​](#daydreams) Daydreams

[Daydreams](https://github.com/daydreamsai/daydreams) is a generative agent framework for executing anything onchain

**Key features:**

* Supports MCP Servers in config
* Exposes MCP Client

### [​](#emacs-mcp) Emacs Mcp

[Emacs Mcp](https://github.com/lizqwerscott/mcp.el) is an Emacs client designed to interface with MCP servers, enabling seamless connections and interactions. It provides MCP tool invocation support for AI plugins like [gptel](https://github.com/karthink/gptel) and [llm](https://github.com/ahyatt/llm), adhering to Emacs’ standard tool invocation format. This integration enhances the functionality of AI tools within the Emacs ecosystem.

**Key features:**

* Provides MCP tool support for Emacs.

### [​](#fast-agent) fast-agent

[fast-agent](https://github.com/evalstate/fast-agent) is a Python Agent framework, with simple declarative support for creating Agents and Workflows, with full multi-modal support for Anthropic and OpenAI models.

**Key features:**

* PDF and Image support, based on MCP Native types
* Interactive front-end to develop and diagnose Agent applications, including passthrough and playback simulators
* Built in support for “Building Effective Agents” workflows.
* Deploy Agents as MCP Servers

### [​](#genkit) Genkit

[Genkit](https://github.com/firebase/genkit) is a cross-language SDK for building and integrating GenAI features into applications. The [genkitx-mcp](https://github.com/firebase/genkit/tree/main/js/plugins/mcp) plugin enables consuming MCP servers as a client or creating MCP servers from Genkit tools and prompts.

**Key features:**

* Client support for tools and prompts (resources partially supported)
* Rich discovery with support in Genkit’s Dev UI playground
* Seamless interoperability with Genkit’s existing tools and prompts
* Works across a wide variety of GenAI models from top providers

### [​](#genaiscript) GenAIScript

Programmatically assemble prompts for LLMs using [GenAIScript](https://microsoft.github.io/genaiscript/) (in JavaScript). Orchestrate LLMs, tools, and data in JavaScript.

**Key features:**

* JavaScript toolbox to work with prompts
* Abstraction to make it easy and productive
* Seamless Visual Studio Code integration

### [​](#goose) Goose

[Goose](https://github.com/block/goose) is an open source AI agent that supercharges your software development by automating coding tasks.

**Key features:**

* Expose MCP functionality to Goose through tools.
* MCPs can be installed directly via the [extensions directory](https://block.github.io/goose/v1/extensions/), CLI, or UI.
* Goose allows you to extend its functionality by [building your own MCP servers](https://block.github.io/goose/docs/tutorials/custom-extensions).
* Includes built-in tools for development, web scraping, automation, memory, and integrations with JetBrains and Google Drive.

### [​](#librechat) LibreChat

[LibreChat](https://github.com/danny-avila/LibreChat) is an open-source, customizable AI chat UI that supports multiple AI providers, now including MCP integration.

**Key features:**

* Extend current tool ecosystem, including [Code Interpreter](https://www.librechat.ai/docs/features/code_interpreter) and Image generation tools, through MCP servers
* Add tools to customizable [Agents](https://www.librechat.ai/docs/features/agents), using a variety of LLMs from top providers
* Open-source and self-hostable, with secure multi-user support
* Future roadmap includes expanded MCP feature support

### [​](#mcp-agent) mcp-agent

[mcp-agent](https://github.com/lastmile-ai/mcp-agent) is a simple, composable framework to build agents using Model Context Protocol.

**Key features:**

* Automatic connection management of MCP servers.
* Expose tools from multiple servers to an LLM.
* Implements every pattern defined in [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents).
* Supports workflow pause/resume signals, such as waiting for human feedback.

### [​](#microsoft-copilot-studio) Microsoft Copilot Studio

[Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-mcp) is a robust SaaS platform designed for building custom AI-driven applications and intelligent agents, empowering developers to create, deploy, and manage sophisticated AI solutions.

**Key features:**

* Support for MCP tools
* Extend Copilot Studio agents with MCP servers
* Leveraging Microsoft unified, governed, and secure API management solutions

### [​](#opensumi) OpenSumi

[OpenSumi](https://github.com/opensumi/core) is a framework helps you quickly build AI Native IDE products.

**Key features:**

* Supports MCP tools in OpenSumi
* Supports built-in IDE MCP servers and custom MCP servers

### [​](#oterm) oterm

[oterm](https://github.com/ggozad/oterm) is a terminal client for Ollama allowing users to create chats/agents.

**Key features:**

* Support for multiple fully customizable chat sessions with Ollama connected with tools.
* Support for MCP tools.

### [​](#roo-code) Roo Code

[Roo Code](https://roocode.com) enables AI coding assistance via MCP.

**Key features:**

* Support for MCP tools and resources
* Integration with development workflows
* Extensible AI capabilities

### [​](#sourcegraph-cody) Sourcegraph Cody

[Cody](https://openctx.org/docs/providers/modelcontextprotocol) is Sourcegraph’s AI coding assistant, which implements MCP through OpenCTX.

**Key features:**

* Support for MCP resources
* Integration with Sourcegraph’s code intelligence
* Uses OpenCTX as an abstraction layer
* Future support planned for additional MCP features

### [​](#spinai) SpinAI

[SpinAI](https://spinai.dev) is an open-source TypeScript framework for building observable AI agents. The framework provides native MCP compatibility, allowing agents to seamlessly integrate with MCP servers and tools.

**Key features:**

* Built-in MCP compatibility for AI agents
* Open-source TypeScript framework
* Observable agent architecture
* Native support for MCP tools integration

### [​](#superinterface) Superinterface

[Superinterface](https://superinterface.ai) is AI infrastructure and a developer platform to build in-app AI assistants with support for MCP, interactive components, client-side function calling and more.

**Key features:**

* Use tools from MCP servers in assistants embedded via React components or script tags
* SSE transport support
* Use any AI model from any AI provider (OpenAI, Anthropic, Ollama, others)

### [​](#theiaai%2Ftheiaide) TheiaAI/TheiaIDE

[Theia AI](https://eclipsesource.com/blogs/2024/10/07/introducing-theia-ai/) is a framework for building AI-enhanced tools and IDEs. The [AI-powered Theia IDE](https://eclipsesource.com/blogs/2024/10/08/introducting-ai-theia-ide/) is an open and flexible development environment built on Theia AI.

**Key features:**

* **Tool Integration**: Theia AI enables AI agents, including those in the Theia IDE, to utilize MCP servers for seamless tool interaction.
* **Customizable Prompts**: The Theia IDE allows users to define and adapt prompts, dynamically integrating MCP servers for tailored workflows.
* **Custom agents**: The Theia IDE supports creating custom agents that leverage MCP capabilities, enabling users to design dedicated workflows on the fly.

Theia AI and Theia IDE’s MCP integration provide users with flexibility, making them powerful platforms for exploring and adapting MCP.

**Learn more:**

* [Theia IDE and Theia AI MCP Announcement](https://eclipsesource.com/blogs/2024/12/19/theia-ide-and-theia-ai-support-mcp/)
* [Download the AI-powered Theia IDE](https://theia-ide.org/)

### [​](#vs-code-github-copilot) VS Code GitHub Copilot

[VS Code](https://code.visualstudio.com/) integrates MCP with GitHub Copilot through [agent mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode), allowing direct interaction with MCP-provided tools within your agentic coding workflow. Configure servers in Claude Desktop, workspace or user settings, with guided MCP installation and secure handling of keys in input variables to avoid leaking hard-coded keys.

**Key features:**

* Support for stdio and server-sent events (SSE) transport
* Per-session selection of tools per agent session for optimal performance
* Easy server debugging with restart commands and output logging
* Tool calls with editable inputs and always-allow toggle
* Integration with existing VS Code extension system to register MCP servers from extensions

### [​](#windsurf-editor) Windsurf Editor

[Windsurf Editor](https://codeium.com/windsurf) is an agentic IDE that combines AI assistance with developer workflows. It features an innovative AI Flow system that enables both collaborative and independent AI interactions while maintaining developer control.

**Key features:**

* Revolutionary AI Flow paradigm for human-AI collaboration
* Intelligent code generation and understanding
* Rich development tools with multi-model support

### [​](#witsy) Witsy

[Witsy](https://github.com/nbonamy/witsy) is an AI desktop assistant, supoorting Anthropic models and MCP servers as LLM tools.

**Key features:**

* Multiple MCP servers support
* Tool integration for executing commands and scripts
* Local server connections for enhanced privacy and security
* Easy-install from Smithery.ai
* Open-source, available for macOS, Windows and Linux

### [​](#zed) Zed

[Zed](https://zed.dev/docs/assistant/model-context-protocol) is a high-performance code editor with built-in MCP support, focusing on prompt templates and tool integration.

**Key features:**

* Prompt templates surface as slash commands in the editor
* Tool integration for enhanced coding workflows
* Tight integration with editor features and workspace context
* Does not support MCP resources

## [​](#adding-mcp-support-to-your-application) Adding MCP support to your application

If you’ve added MCP support to your application, we encourage you to submit a pull request to add it to this list. MCP integration can provide your users with powerful contextual AI capabilities and make your application part of the growing MCP ecosystem.

Benefits of adding MCP support:

* Enable users to bring their own context and tools
* Join a growing ecosystem of interoperable AI applications
* Provide users with flexible integration options
* Support local-first AI workflows

To get started with implementing MCP in your application, check out our [Python](https://github.com/modelcontextprotocol/python-sdk) or [TypeScript SDK Documentation](https://github.com/modelcontextprotocol/typescript-sdk)

## [​](#updates-and-corrections) Updates and corrections

This list is maintained by the community. If you notice any inaccuracies or would like to update information about MCP support in your application, please submit a pull request or [open an issue in our documentation repository](https://github.com/modelcontextprotocol/modelcontextprotocol/issues).