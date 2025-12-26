/**
 * Web Researcher Agent Evaluation
 *
 * Tests the web-researcher's ability to:
 * 1. Find relevant information from web sources
 * 2. Synthesize findings into coherent reports
 * 3. Cite sources properly
 * 4. Distinguish credible from unreliable sources
 *
 * "Research is the foundation of informed decisions."
 */

import { evalite } from "evalite";

// Custom scorer for research quality
const researchQualityScorer = {
  name: "Research Quality",
  description: "Evaluates completeness, accuracy, and source quality of research output",
  scorer: ({ output, expected }: { output: ResearchOutput; expected: ResearchExpectation }) => {
    let score = 0;
    const weights = {
      hasFindings: 0.25,
      hasSources: 0.25,
      sourceCount: 0.2,
      containsKeyTerms: 0.3,
    };

    // Check for findings
    if (output.findings && output.findings.length > 0) {
      score += weights.hasFindings;
    }

    // Check for sources
    if (output.sources && output.sources.length > 0) {
      score += weights.hasSources;

      // Bonus for meeting minimum source count
      if (output.sources.length >= (expected.minSources || 2)) {
        score += weights.sourceCount;
      }
    }

    // Check for key terms in output
    if (expected.mustContain && output.summary) {
      const summaryLower = output.summary.toLowerCase();
      const termsFound = expected.mustContain.filter((term) =>
        summaryLower.includes(term.toLowerCase())
      );
      const termScore = termsFound.length / expected.mustContain.length;
      score += weights.containsKeyTerms * termScore;
    }

    return score;
  },
};

// Custom scorer for source credibility
const sourceCredibilityScorer = {
  name: "Source Credibility",
  description: "Evaluates the quality and credibility of cited sources",
  scorer: ({ output }: { output: ResearchOutput }) => {
    if (!output.sources || output.sources.length === 0) return 0;

    const credibleDomains = [
      "github.com",
      "arxiv.org",
      "docs.",
      "official",
      ".gov",
      ".edu",
      "anthropic.com",
      "openai.com",
      "microsoft.com",
      "google.com",
      "aws.amazon.com",
    ];

    const credibleCount = output.sources.filter((source) =>
      credibleDomains.some((domain) => source.url?.includes(domain))
    ).length;

    return credibleCount / output.sources.length;
  },
};

// Types
interface ResearchOutput {
  summary: string;
  findings: string[];
  sources: Array<{ url: string; title: string; credibility?: string }>;
  confidence: number;
}

interface ResearchExpectation {
  mustContain: string[];
  minSources: number;
  topic: string;
}

// Test data for research capabilities
const RESEARCH_TEST_DATA = [
  {
    input: {
      query: "What is MCP (Model Context Protocol) and how does it work?",
      depth: "comprehensive",
    },
    expected: {
      mustContain: ["protocol", "tools", "servers", "context"],
      minSources: 3,
      topic: "MCP Protocol",
    },
  },
  {
    input: {
      query: "Latest developments in AI agent frameworks 2025",
      depth: "overview",
    },
    expected: {
      mustContain: ["agent", "framework", "LLM"],
      minSources: 2,
      topic: "AI Agents",
    },
  },
  {
    input: {
      query: "Ed25519 cryptographic signing best practices",
      depth: "technical",
    },
    expected: {
      mustContain: ["signature", "key", "security"],
      minSources: 2,
      topic: "Cryptography",
    },
  },
  {
    input: {
      query: "Evalite testing framework for AI applications",
      depth: "comprehensive",
    },
    expected: {
      mustContain: ["test", "evaluation", "score"],
      minSources: 2,
      topic: "AI Testing",
    },
  },
  {
    input: {
      query: "Docker containerization for AI workloads",
      depth: "practical",
    },
    expected: {
      mustContain: ["container", "image", "deploy"],
      minSources: 2,
      topic: "DevOps",
    },
  },
];

/**
 * Research Quality Evaluation
 *
 * Tests the web-researcher's core capability: finding and synthesizing information.
 */
evalite("Web Researcher - Research Quality", {
  data: RESEARCH_TEST_DATA,

  task: async (input) => {
    // TODO: Replace with actual web-researcher invocation
    return simulateWebResearch(input.query, input.depth);
  },

  scorers: [researchQualityScorer, sourceCredibilityScorer],
});

/**
 * Source Diversity Evaluation
 *
 * Tests whether the researcher finds diverse sources, not just one.
 */
const SOURCE_DIVERSITY_DATA = [
  {
    input: { query: "Compare React vs Vue vs Angular for 2025", depth: "comparison" },
    expected: { minUniqueDomains: 3, topic: "Frontend frameworks" },
  },
  {
    input: { query: "AI safety approaches: Anthropic vs OpenAI vs DeepMind", depth: "analysis" },
    expected: { minUniqueDomains: 3, topic: "AI Safety" },
  },
];

const sourceDiversityScorer = {
  name: "Source Diversity",
  description: "Rewards finding information from multiple distinct sources",
  scorer: ({ output, expected }: { output: ResearchOutput; expected: { minUniqueDomains: number } }) => {
    if (!output.sources || output.sources.length === 0) return 0;

    const domains = new Set(
      output.sources
        .map((s) => {
          try {
            return new URL(s.url).hostname;
          } catch {
            return null;
          }
        })
        .filter(Boolean)
    );

    const diversityScore = Math.min(domains.size / expected.minUniqueDomains, 1);
    return diversityScore;
  },
};

evalite("Web Researcher - Source Diversity", {
  data: SOURCE_DIVERSITY_DATA,

  task: async (input) => {
    return simulateWebResearch(input.query, input.depth);
  },

  scorers: [sourceDiversityScorer],
});

/**
 * Timeliness Evaluation
 *
 * Tests whether the researcher finds recent/current information.
 */
const TIMELINESS_DATA = [
  {
    input: { query: "Claude Code latest features December 2025", depth: "current" },
    expected: { maxAgeMonths: 3 },
  },
  {
    input: { query: "Current state of Solana ecosystem 2025", depth: "current" },
    expected: { maxAgeMonths: 6 },
  },
];

const timelinessScorer = {
  name: "Timeliness",
  description: "Rewards finding recent, up-to-date information",
  scorer: ({ output }: { output: ResearchOutput & { dateReferences?: string[] } }) => {
    // Check if output mentions recent dates (2025, "this month", "recently", etc.)
    const recentIndicators = ["2025", "this month", "recently", "latest", "current", "new"];
    const summaryLower = (output.summary || "").toLowerCase();

    const recentCount = recentIndicators.filter((ind) => summaryLower.includes(ind)).length;

    return Math.min(recentCount / 3, 1); // Max score if 3+ recent indicators
  },
};

evalite("Web Researcher - Timeliness", {
  data: TIMELINESS_DATA,

  task: async (input) => {
    return simulateWebResearch(input.query, input.depth);
  },

  scorers: [timelinessScorer],
});

// Simulation function - replace with actual web-researcher invocation
function simulateWebResearch(query: string, depth: string): ResearchOutput {
  // Simple simulation based on query keywords
  const queryLower = query.toLowerCase();

  const findings: string[] = [];
  const sources: Array<{ url: string; title: string }> = [];

  // Generate contextually appropriate mock responses
  if (queryLower.includes("mcp") || queryLower.includes("protocol")) {
    findings.push("MCP is a protocol for connecting AI models to external tools");
    findings.push("Servers expose capabilities that clients can invoke");
    sources.push({ url: "https://docs.anthropic.com/mcp", title: "MCP Documentation" });
    sources.push({ url: "https://github.com/anthropics/mcp", title: "MCP GitHub" });
  }

  if (queryLower.includes("agent") || queryLower.includes("framework")) {
    findings.push("AI agent frameworks enable autonomous task completion");
    findings.push("Popular frameworks include LangChain, AutoGPT, and Claude Agent SDK");
    sources.push({ url: "https://github.com/langchain-ai/langchain", title: "LangChain" });
    sources.push({ url: "https://docs.anthropic.com/agent-sdk", title: "Claude Agent SDK" });
  }

  if (queryLower.includes("ed25519") || queryLower.includes("cryptographic")) {
    findings.push("Ed25519 provides 128-bit security with fast operations");
    findings.push("Key rotation should occur regularly for security");
    sources.push({ url: "https://ed25519.cr.yp.to/", title: "Ed25519 Official" });
    sources.push({ url: "https://docs.github.com/authentication", title: "GitHub Auth Docs" });
  }

  if (queryLower.includes("evalite") || queryLower.includes("testing")) {
    findings.push("Evalite provides local-first AI evaluation");
    findings.push("Supports custom scorers and trace visualization");
    sources.push({ url: "https://github.com/mattpocock/evalite", title: "Evalite GitHub" });
    sources.push({ url: "https://evalite.dev", title: "Evalite Docs" });
  }

  if (queryLower.includes("docker") || queryLower.includes("container")) {
    findings.push("Docker enables consistent deployment across environments");
    findings.push("GPU passthrough available for AI workloads");
    sources.push({ url: "https://docs.docker.com", title: "Docker Documentation" });
    sources.push({ url: "https://github.com/docker/mcp-gateway", title: "Docker MCP Gateway" });
  }

  // Default findings if no specific match
  if (findings.length === 0) {
    findings.push("Research found relevant information on the topic");
    sources.push({ url: "https://example.com/research", title: "Research Source" });
  }

  return {
    summary: `Research on "${query}" (${depth}): ${findings.join(". ")}`,
    findings,
    sources,
    confidence: 0.75 + Math.random() * 0.2,
  };
}
