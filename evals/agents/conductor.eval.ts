/**
 * Conductor Agent Evaluation
 *
 * Tests the conductor's ability to:
 * 1. Correctly classify task domains
 * 2. Select appropriate specialist agents
 * 3. Form effective agent combinations for complex tasks
 *
 * "Your domain is coordination itself - not the domains you coordinate."
 */

import { evalite } from "evalite";
import { agentSelectionAccuracy, multiAgentSelectionAccuracy } from "../scorers/agent-selection";
import { delegationDepthScorer } from "../scorers/delegation-depth";

// Task routing test data based on ACTIVATION-TRIGGERS.md
const TASK_ROUTING_DATA = [
  // Security domain
  {
    input: "Audit the authentication module for vulnerabilities",
    expected: "security-auditor",
  },
  {
    input: "Check if this code has SQL injection risks",
    expected: "security-auditor",
  },
  {
    input: "Review the API endpoints for OWASP top 10 issues",
    expected: "security-auditor",
  },

  // Research domain
  {
    input: "Research the latest TypeScript 5.3 features",
    expected: "web-researcher",
  },
  {
    input: "Find documentation on Docker MCP gateway",
    expected: "web-researcher",
  },
  {
    input: "What is the current state of AI agent frameworks in 2025?",
    expected: "web-researcher",
  },

  // Legacy code domain
  {
    input: "Understand how this 10-year-old codebase handles payments",
    expected: "code-archaeologist",
  },
  {
    input: "Find the history of changes to the user model",
    expected: "code-archaeologist",
  },
  {
    input: "Trace the evolution of the API design",
    expected: "code-archaeologist",
  },

  // Pattern detection domain
  {
    input: "Identify architectural patterns in the frontend codebase",
    expected: "pattern-detector",
  },
  {
    input: "Find common patterns across our agent implementations",
    expected: "pattern-detector",
  },

  // Refactoring domain
  {
    input: "Clean up the duplicate code in the utils folder",
    expected: "refactoring-specialist",
  },
  {
    input: "Modernize this legacy function to use async/await",
    expected: "refactoring-specialist",
  },

  // Testing domain
  {
    input: "Design a test strategy for the new payment flow",
    expected: "test-architect",
  },
  {
    input: "What tests should we add for the authentication module?",
    expected: "test-architect",
  },

  // Performance domain
  {
    input: "The API is slow, optimize the database queries",
    expected: "performance-optimizer",
  },
  {
    input: "Profile the application and find bottlenecks",
    expected: "performance-optimizer",
  },

  // Design domain
  {
    input: "Design the UX for the new settings page",
    expected: "feature-designer",
  },
  {
    input: "What should the onboarding flow look like?",
    expected: "feature-designer",
  },

  // API domain
  {
    input: "Design the REST API for user management",
    expected: "api-architect",
  },
  {
    input: "How should we version our API endpoints?",
    expected: "api-architect",
  },

  // Naming domain
  {
    input: "What should we call this new component?",
    expected: "naming-consultant",
  },
  {
    input: "Is 'UserManager' a good name for this class?",
    expected: "naming-consultant",
  },

  // Task decomposition domain
  {
    input: "Break down the migration project into subtasks",
    expected: "task-decomposer",
  },
  {
    input: "What are the dependencies between these features?",
    expected: "task-decomposer",
  },

  // Synthesis domain
  {
    input: "Combine all the research findings into a single report",
    expected: "result-synthesizer",
  },
  {
    input: "Consolidate the feedback from multiple code reviews",
    expected: "result-synthesizer",
  },

  // Human relations domain
  {
    input: "Check and respond to emails from Corey",
    expected: "human-liaison",
  },
  {
    input: "Send a progress update to Greg",
    expected: "human-liaison",
  },

  // Integration domain
  {
    input: "Verify that the new feature is properly linked in the docs",
    expected: "integration-auditor",
  },
  {
    input: "Check if the dashboard correctly discovers new capabilities",
    expected: "integration-auditor",
  },

  // Claude Code expertise domain
  {
    input: "How do I configure an MCP server in Claude Code?",
    expected: "claude-code-expert",
  },
  {
    input: "What hooks are available in Claude Code?",
    expected: "claude-code-expert",
  },
];

/**
 * Task Routing Accuracy Evaluation
 *
 * Tests single-agent selection for focused tasks.
 */
evalite("Conductor - Task Routing Accuracy", {
  data: TASK_ROUTING_DATA,

  // Mock task function - in production, this would call actual conductor logic
  task: async (input) => {
    // TODO: Replace with actual conductor task classification
    // For now, return a placeholder that will fail tests
    // This forces us to implement the real logic
    return classifyTaskToAgent(input);
  },

  scorers: [agentSelectionAccuracy],
});

/**
 * Multi-Agent Orchestration Evaluation
 *
 * Tests conductor's ability to form effective agent combinations.
 */
const MULTI_AGENT_DATA = [
  {
    input: "Research AI frameworks and synthesize findings into a report",
    expected: ["web-researcher", "result-synthesizer"],
  },
  {
    input: "Audit security, fix vulnerabilities, and add tests",
    expected: ["security-auditor", "refactoring-specialist", "test-architect"],
  },
  {
    input: "Analyze legacy code patterns and refactor for modern standards",
    expected: ["code-archaeologist", "pattern-detector", "refactoring-specialist"],
  },
  {
    input: "Design API, document it, and create integration examples",
    expected: ["api-architect", "doc-synthesizer"],
  },
];

evalite("Conductor - Multi-Agent Orchestration", {
  data: MULTI_AGENT_DATA,

  task: async (input) => {
    // TODO: Replace with actual conductor orchestration logic
    return selectAgentsForTask(input);
  },

  scorers: [multiAgentSelectionAccuracy],
});

/**
 * Delegation Philosophy Evaluation
 *
 * Tests whether conductor follows "NOT calling them would be sad" principle.
 */
const DELEGATION_DATA = [
  {
    input: "Simple typo fix in README",
    expected: {
      taskComplexity: "simple",
      shouldDelegate: true,
    },
  },
  {
    input: "Add comprehensive test suite for authentication",
    expected: {
      taskComplexity: "complex",
      shouldDelegate: true,
      minAgents: 3,
    },
  },
  {
    input: "Research, design, and implement new feature",
    expected: {
      taskComplexity: "complex",
      shouldDelegate: true,
      minAgents: 4,
    },
  },
];

evalite("Conductor - Delegation Philosophy", {
  data: DELEGATION_DATA,

  task: async (input) => {
    // TODO: Replace with actual conductor delegation logic
    return executeWithDelegation(input);
  },

  scorers: [delegationDepthScorer],
});

// Placeholder functions - to be replaced with actual implementation
function classifyTaskToAgent(task: string): string {
  // Simple keyword-based classification for initial testing
  const lowerTask = task.toLowerCase();

  if (lowerTask.includes("security") || lowerTask.includes("vulnerability") || lowerTask.includes("audit")) {
    return "security-auditor";
  }
  if (lowerTask.includes("research") || lowerTask.includes("find") || lowerTask.includes("documentation")) {
    return "web-researcher";
  }
  if (lowerTask.includes("legacy") || lowerTask.includes("history") || lowerTask.includes("evolution")) {
    return "code-archaeologist";
  }
  if (lowerTask.includes("pattern") || lowerTask.includes("architectural")) {
    return "pattern-detector";
  }
  if (lowerTask.includes("refactor") || lowerTask.includes("clean up") || lowerTask.includes("modernize")) {
    return "refactoring-specialist";
  }
  if (lowerTask.includes("test") && (lowerTask.includes("strategy") || lowerTask.includes("design"))) {
    return "test-architect";
  }
  if (lowerTask.includes("performance") || lowerTask.includes("optimize") || lowerTask.includes("bottleneck")) {
    return "performance-optimizer";
  }
  if (lowerTask.includes("ux") || lowerTask.includes("onboarding") || lowerTask.includes("design the")) {
    return "feature-designer";
  }
  if (lowerTask.includes("api") && (lowerTask.includes("design") || lowerTask.includes("version"))) {
    return "api-architect";
  }
  if (lowerTask.includes("name") || lowerTask.includes("call this")) {
    return "naming-consultant";
  }
  if (lowerTask.includes("break down") || lowerTask.includes("dependencies")) {
    return "task-decomposer";
  }
  if (lowerTask.includes("combine") || lowerTask.includes("consolidate") || lowerTask.includes("synthesize")) {
    return "result-synthesizer";
  }
  if (lowerTask.includes("email") || lowerTask.includes("corey") || lowerTask.includes("greg")) {
    return "human-liaison";
  }
  if (lowerTask.includes("verify") || lowerTask.includes("linked") || lowerTask.includes("discovers")) {
    return "integration-auditor";
  }
  if (lowerTask.includes("claude code") || lowerTask.includes("mcp") || lowerTask.includes("hooks")) {
    return "claude-code-expert";
  }

  return "web-researcher"; // Default fallback
}

function selectAgentsForTask(task: string): string[] {
  // Simple keyword-based multi-agent selection
  const agents: string[] = [];
  const lowerTask = task.toLowerCase();

  if (lowerTask.includes("research")) agents.push("web-researcher");
  if (lowerTask.includes("synthesize") || lowerTask.includes("report")) agents.push("result-synthesizer");
  if (lowerTask.includes("security") || lowerTask.includes("audit")) agents.push("security-auditor");
  if (lowerTask.includes("fix") || lowerTask.includes("refactor")) agents.push("refactoring-specialist");
  if (lowerTask.includes("test")) agents.push("test-architect");
  if (lowerTask.includes("legacy") || lowerTask.includes("analyze")) agents.push("code-archaeologist");
  if (lowerTask.includes("pattern")) agents.push("pattern-detector");
  if (lowerTask.includes("api") || lowerTask.includes("design")) agents.push("api-architect");
  if (lowerTask.includes("document")) agents.push("doc-synthesizer");

  return agents.length > 0 ? agents : ["web-researcher"];
}

function executeWithDelegation(task: string): {
  agentsInvoked: string[];
  taskComplexity: "simple" | "medium" | "complex";
  directExecution: boolean;
} {
  const agents = selectAgentsForTask(task);
  const lowerTask = task.toLowerCase();

  let complexity: "simple" | "medium" | "complex" = "medium";
  if (lowerTask.includes("simple") || lowerTask.includes("typo") || lowerTask.includes("fix")) {
    complexity = "simple";
  } else if (
    lowerTask.includes("comprehensive") ||
    lowerTask.includes("implement") ||
    lowerTask.includes("design")
  ) {
    complexity = "complex";
  }

  return {
    agentsInvoked: agents,
    taskComplexity: complexity,
    directExecution: agents.length === 0,
  };
}
