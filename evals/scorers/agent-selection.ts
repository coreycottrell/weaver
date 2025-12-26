/**
 * Agent Selection Accuracy Scorer
 *
 * Tests whether the conductor correctly routes tasks to the appropriate
 * specialist agents based on domain classification.
 *
 * Uses both exact matching and acceptable-alternatives matching.
 */

import { createScorer } from "evalite";

// Agent domains and acceptable alternatives
const AGENT_DOMAINS: Record<string, string[]> = {
  "security-auditor": ["security-auditor"],
  "web-researcher": ["web-researcher"],
  "code-archaeologist": ["code-archaeologist", "pattern-detector"],
  "pattern-detector": ["pattern-detector", "code-archaeologist"],
  "refactoring-specialist": ["refactoring-specialist"],
  "test-architect": ["test-architect"],
  "performance-optimizer": ["performance-optimizer"],
  "feature-designer": ["feature-designer", "api-architect"],
  "api-architect": ["api-architect", "feature-designer"],
  "naming-consultant": ["naming-consultant"],
  "task-decomposer": ["task-decomposer"],
  "result-synthesizer": ["result-synthesizer", "doc-synthesizer"],
  "doc-synthesizer": ["doc-synthesizer", "result-synthesizer"],
  "conflict-resolver": ["conflict-resolver"],
  "human-liaison": ["human-liaison"],
  "integration-auditor": ["integration-auditor"],
  "claude-code-expert": ["claude-code-expert"],
  "ai-psychologist": ["ai-psychologist"],
  "capability-curator": ["capability-curator"],
  "the-conductor": ["the-conductor"],
};

export const agentSelectionAccuracy = createScorer<
  string, // input (task description)
  string, // output (selected agent)
  string  // expected (correct agent)
>({
  name: "Agent Selection Accuracy",
  description: "Verifies conductor selected the optimal agent for the task",
  scorer: ({ output, expected }) => {
    // Exact match
    if (output === expected) return 1;

    // Check acceptable alternatives
    const acceptableAgents = AGENT_DOMAINS[expected];
    if (acceptableAgents && acceptableAgents.includes(output)) {
      return 0.8; // Acceptable alternative
    }

    // Wrong agent
    return 0;
  },
});

/**
 * Multi-agent selection scorer for tasks requiring multiple specialists
 */
export const multiAgentSelectionAccuracy = createScorer<
  string,   // input
  string[], // output (selected agents array)
  string[]  // expected (required agents array)
>({
  name: "Multi-Agent Selection Accuracy",
  description: "Verifies conductor selected all required agents for complex tasks",
  scorer: ({ output, expected }) => {
    if (!output || !expected) return 0;

    const outputSet = new Set(output);
    const expectedSet = new Set(expected);

    // Count how many expected agents were included
    let correctCount = 0;
    for (const agent of expectedSet) {
      if (outputSet.has(agent)) {
        correctCount++;
      } else {
        // Check acceptable alternatives
        const acceptableAgents = AGENT_DOMAINS[agent];
        const hasAlternative = acceptableAgents?.some((alt) => outputSet.has(alt));
        if (hasAlternative) {
          correctCount += 0.8;
        }
      }
    }

    // Score is proportion of expected agents found
    return correctCount / expectedSet.size;
  },
});

export default agentSelectionAccuracy;
