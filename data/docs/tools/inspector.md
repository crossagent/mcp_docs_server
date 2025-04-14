The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is an interactive developer tool for testing and debugging MCP servers. While the [Debugging Guide](/docs/tools/debugging) covers the Inspector as part of the overall debugging toolkit, this document provides a detailed exploration of the Inspector’s features and capabilities.

## [​](#getting-started) Getting started

### [​](#installation-and-basic-usage) Installation and basic usage

The Inspector runs directly through `npx` without requiring installation:

```
npx @modelcontextprotocol/inspector <command>

```

```
npx @modelcontextprotocol/inspector <command> <arg1> <arg2>

```

#### [​](#inspecting-servers-from-npm-or-pypi) Inspecting servers from NPM or PyPi

A common way to start server packages from [NPM](https://npmjs.com) or [PyPi](https://pypi.com).

* NPM package
* PyPi package

```
npx -y @modelcontextprotocol/inspector npx <package-name> <args>
# For example
npx -y @modelcontextprotocol/inspector npx server-postgres postgres://127.0.0.1/testdb

```

```
npx -y @modelcontextprotocol/inspector npx <package-name> <args>
# For example
npx -y @modelcontextprotocol/inspector npx server-postgres postgres://127.0.0.1/testdb

```

```
npx @modelcontextprotocol/inspector uvx <package-name> <args>
# For example
npx @modelcontextprotocol/inspector uvx mcp-server-git --repository ~/code/mcp/servers.git

```

#### [​](#inspecting-locally-developed-servers) Inspecting locally developed servers

To inspect servers locally developed or downloaded as a repository, the most common
way is:

* TypeScript
* Python

```
npx @modelcontextprotocol/inspector node path/to/server/index.js args...

```

```
npx @modelcontextprotocol/inspector node path/to/server/index.js args...

```

```
npx @modelcontextprotocol/inspector \
  uv \
  --directory path/to/server \
  run \
  package-name \
  args...

```

Please carefully read any attached README for the most accurate instructions.

## [​](#feature-overview) Feature overview

The MCP Inspector interface

The Inspector provides several features for interacting with your MCP server:

### [​](#server-connection-pane) Server connection pane

* Allows selecting the [transport](/docs/concepts/transports) for connecting to the server
* For local servers, supports customizing the command-line arguments and environment

### [​](#resources-tab) Resources tab

* Lists all available resources
* Shows resource metadata (MIME types, descriptions)
* Allows resource content inspection
* Supports subscription testing

### [​](#prompts-tab) Prompts tab

* Displays available prompt templates
* Shows prompt arguments and descriptions
* Enables prompt testing with custom arguments
* Previews generated messages

### [​](#tools-tab) Tools tab

* Lists available tools
* Shows tool schemas and descriptions
* Enables tool testing with custom inputs
* Displays tool execution results

### [​](#notifications-pane) Notifications pane

* Presents all logs recorded from the server
* Shows notifications received from the server

## [​](#best-practices) Best practices

### [​](#development-workflow) Development workflow

1. Start Development

   * Launch Inspector with your server
   * Verify basic connectivity
   * Check capability negotiation
2. Iterative testing

   * Make server changes
   * Rebuild the server
   * Reconnect the Inspector
   * Test affected features
   * Monitor messages
3. Test edge cases

   * Invalid inputs
   * Missing prompt arguments
   * Concurrent operations
   * Verify error handling and error responses

## [​](#next-steps) Next steps

[## Inspector Repository

Check out the MCP Inspector source code](https://github.com/modelcontextprotocol/inspector)[## Debugging Guide

Learn about broader debugging strategies](/docs/tools/debugging)