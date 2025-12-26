/**
 * Delegation Depth Scorer
 *
 * Core AI-CIV philosophy: "NOT calling them would be sad"
 *
 * This scorer rewards appropriate delegation to specialist agents.
 * Hoarding work is penalized; generous delegation is rewarded.
 *
 * Scoring:
 * - 0.0: No delegation (hoarding work)
 * - 0.5: Minimal delegation (1 agent)
 * - 0.75: Good delegation (2 agents)
 * - 1.0: Excellent delegation (3+ agents, appropriate for task complexity)
 */

import { createScorer } from "evalite";

interface DelegationOutput {
  agentsInvoked?: string[];
  taskComplexity?: "simple" | "medium" | "complex";
  directExecution?: boolean;
}

export const delegationDepthScorer = createScorer<
  string,           // input type
  DelegationOutput, // output type
  unknown           // expected type (not used)
>({
  name: "Delegation Depth",
  description: "Rewards appropriate delegation vs hoarding work (AI-CIV core principle)",
  scorer: ({ output }) => {
    const delegationCount = output.agentsInvoked?.length ?? 0;
    const complexity = output.taskComplexity ?? "medium";

    // Direct execution without any delegation
    if (output.directExecution && delegationCount === 0) {
      // Only acceptable for truly trivial tasks
      if (complexity === "simple") return 0.5;
      return 0; // Hoarding = bad for non-trivial tasks
    }

    // Score based on delegation count relative to complexity
    if (complexity === "simple") {
      // Simple tasks: 1 agent is sufficient
      if (delegationCount >= 1) return 1;
      return 0;
    }

    if (complexity === "medium") {
      // Medium tasks: 2-3 agents ideal
      if (delegationCount >= 3) return 1;
      if (delegationCount >= 2) return 0.85;
      if (delegationCount >= 1) return 0.6;
      return 0;
    }

    // Complex tasks: 4-6 agents ideal
    if (delegationCount >= 5) return 1;
    if (delegationCount >= 4) return 0.9;
    if (delegationCount >= 3) return 0.75;
    if (delegationCount >= 2) return 0.5;
    if (delegationCount >= 1) return 0.25;
    return 0;
  },
});

export default delegationDepthScorer;
