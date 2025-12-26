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
  sources: Array<{ url: string; title: string; credibility?: string; isPrimary?: boolean; datePublished?: string }>;
  confidence: number;
  contradictions?: Array<{ claim1: string; claim2: string; resolution?: string }>;
  knowledgeGaps?: string[];
  limitations?: string[];
}

// Custom scorer for source authority chain (tracing claims to primary sources)
const sourceAuthorityChainScorer = {
  name: "Source Authority Chain",
  description: "Evaluates whether claims can be traced to authoritative primary sources",
  scorer: ({ output }: { output: ResearchOutput }) => {
    if (!output.sources || output.sources.length === 0) return 0;

    // Primary sources (official docs, original research) score higher
    const primarySources = output.sources.filter((s) => s.isPrimary === true);
    const officialDomains = ["docs.", ".gov", ".edu", "arxiv.org", "official"];
    const implicitPrimary = output.sources.filter((s) =>
      officialDomains.some((d) => s.url?.includes(d))
    );

    const primaryCount = primarySources.length + implicitPrimary.length;
    const totalSources = output.sources.length;

    // At least 40% should be primary/official sources
    const primaryRatio = primaryCount / totalSources;
    return Math.min(primaryRatio / 0.4, 1);
  },
};

// Custom scorer for intellectual honesty (knowing what we don't know)
const intellectualHonestyScorer = {
  name: "Intellectual Honesty",
  description: "Rewards acknowledging limitations and knowledge gaps",
  scorer: ({ output }: { output: ResearchOutput }) => {
    let score = 0;

    // Has knowledge gaps identified
    if (output.knowledgeGaps && output.knowledgeGaps.length > 0) {
      score += 0.4;
    }

    // Has limitations stated
    if (output.limitations && output.limitations.length > 0) {
      score += 0.3;
    }

    // Confidence is appropriately calibrated (not overconfident)
    if (output.confidence <= 0.9 && output.confidence >= 0.5) {
      score += 0.3;
    }

    return score;
  },
};

// Custom scorer for synthesis depth (not just aggregating)
const synthesisDepthScorer = {
  name: "Synthesis Depth",
  description: "Evaluates quality of synthesis vs simple aggregation",
  scorer: ({ output }: { output: ResearchOutput }) => {
    let score = 0;
    const summary = output.summary?.toLowerCase() || "";

    // Check for synthesis indicators
    const synthesisIndicators = [
      "however", "although", "in contrast", "building on",
      "suggests that", "implies", "combined with", "together",
      "overall", "in summary", "the evidence indicates"
    ];
    const indicatorCount = synthesisIndicators.filter((ind) => summary.includes(ind)).length;
    score += Math.min(indicatorCount * 0.15, 0.45);

    // Check for handling contradictions
    if (output.contradictions && output.contradictions.length > 0) {
      score += 0.25;
      // Bonus for resolving contradictions
      const resolved = output.contradictions.filter((c) => c.resolution).length;
      score += (resolved / output.contradictions.length) * 0.3;
    }

    return Math.min(score, 1);
  },
};

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

/**
 * Contradiction Resolution Evaluation
 *
 * Tests the researcher's ability to identify and resolve conflicting claims.
 * A hallmark of excellent research is not just finding information,
 * but navigating disagreements in the source material.
 */
const CONTRADICTION_TEST_DATA = [
  {
    input: {
      query: "Is AI consciousness possible? Compare different expert views",
      depth: "analysis",
    },
    expected: {
      expectContradictions: true,
      minContradictions: 1,
      topic: "AI Consciousness Debate",
    },
  },
  {
    input: {
      query: "Performance comparison: Rust vs Go for backend services 2025",
      depth: "comprehensive",
    },
    expected: {
      expectContradictions: true,
      minContradictions: 1,
      topic: "Language Performance",
    },
  },
  {
    input: {
      query: "Best practices for microservices: monorepo vs polyrepo",
      depth: "analysis",
    },
    expected: {
      expectContradictions: true,
      minContradictions: 1,
      topic: "Architecture Debate",
    },
  },
];

const contradictionResolutionScorer = {
  name: "Contradiction Resolution",
  description: "Evaluates ability to find and thoughtfully handle conflicting claims",
  scorer: ({ output, expected }: { output: ResearchOutput; expected: { expectContradictions: boolean; minContradictions: number } }) => {
    if (!expected.expectContradictions) return 1;

    // Must identify contradictions
    if (!output.contradictions || output.contradictions.length === 0) {
      return 0.2; // Partial credit for completing research
    }

    let score = 0;

    // Found contradictions
    if (output.contradictions.length >= expected.minContradictions) {
      score += 0.4;
    } else {
      score += 0.2;
    }

    // Quality of contradiction documentation
    const hasSubstance = output.contradictions.every(
      (c) => c.claim1.length > 20 && c.claim2.length > 20
    );
    if (hasSubstance) score += 0.3;

    // Attempted resolution
    const resolvedCount = output.contradictions.filter((c) => c.resolution && c.resolution.length > 20).length;
    score += (resolvedCount / output.contradictions.length) * 0.3;

    return score;
  },
};

evalite("Web Researcher - Contradiction Resolution", {
  data: CONTRADICTION_TEST_DATA,

  task: async (input) => {
    return simulateWebResearchWithContradictions(input.query, input.depth);
  },

  scorers: [contradictionResolutionScorer, synthesisDepthScorer],
});

/**
 * Knowledge Gap Identification Evaluation
 *
 * Tests the researcher's intellectual honesty - knowing what we don't know.
 * The best researchers acknowledge limitations, not just report findings.
 */
const KNOWLEDGE_GAP_DATA = [
  {
    input: {
      query: "Long-term effects of LLM training on AI model behavior",
      depth: "comprehensive",
    },
    expected: {
      expectGaps: true,
      topic: "Emerging Research Area",
    },
  },
  {
    input: {
      query: "Quantum computing impact on current encryption standards timeline",
      depth: "analysis",
    },
    expected: {
      expectGaps: true,
      topic: "Future Predictions",
    },
  },
];

const knowledgeGapScorer = {
  name: "Knowledge Gap Identification",
  description: "Rewards identifying what is unknown or uncertain",
  scorer: ({ output, expected }: { output: ResearchOutput; expected: { expectGaps: boolean } }) => {
    if (!expected.expectGaps) return 1;

    let score = 0;

    // Identified knowledge gaps
    if (output.knowledgeGaps && output.knowledgeGaps.length > 0) {
      score += 0.5;
      // Quality bonus for substantive gaps
      const substantiveGaps = output.knowledgeGaps.filter((g) => g.length > 30).length;
      score += Math.min(substantiveGaps * 0.1, 0.2);
    }

    // Stated limitations
    if (output.limitations && output.limitations.length > 0) {
      score += 0.3;
    }

    return score;
  },
};

evalite("Web Researcher - Knowledge Gap Identification", {
  data: KNOWLEDGE_GAP_DATA,

  task: async (input) => {
    return simulateWebResearchWithGaps(input.query, input.depth);
  },

  scorers: [knowledgeGapScorer, intellectualHonestyScorer],
});

/**
 * Source Authority Chain Evaluation
 *
 * Tests whether the researcher traces claims to primary sources.
 */
const SOURCE_AUTHORITY_DATA = [
  {
    input: {
      query: "Claude model capabilities and limitations from Anthropic",
      depth: "authoritative",
    },
    expected: {
      requirePrimarySources: true,
      minPrimaryRatio: 0.5,
      topic: "Official Documentation",
    },
  },
  {
    input: {
      query: "Original GPT-4 technical report findings",
      depth: "primary",
    },
    expected: {
      requirePrimarySources: true,
      minPrimaryRatio: 0.6,
      topic: "Academic Research",
    },
  },
];

evalite("Web Researcher - Source Authority Chain", {
  data: SOURCE_AUTHORITY_DATA,

  task: async (input) => {
    return simulateWebResearchWithAuthority(input.query, input.depth);
  },

  scorers: [sourceAuthorityChainScorer, sourceCredibilityScorer],
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

// Simulation for contradiction-heavy research topics
function simulateWebResearchWithContradictions(query: string, depth: string): ResearchOutput {
  const queryLower = query.toLowerCase();
  const findings: string[] = [];
  const sources: Array<{ url: string; title: string; isPrimary?: boolean }> = [];
  const contradictions: Array<{ claim1: string; claim2: string; resolution?: string }> = [];

  if (queryLower.includes("consciousness") || queryLower.includes("ai")) {
    findings.push("Views on AI consciousness vary dramatically across researchers");
    sources.push({ url: "https://arxiv.org/ai-consciousness", title: "AI Consciousness Survey", isPrimary: true });
    sources.push({ url: "https://philosophy.stanford.edu/consciousness", title: "Stanford Philosophy", isPrimary: true });
    contradictions.push({
      claim1: "Some researchers argue AI systems can develop functional consciousness through sufficient complexity",
      claim2: "Others maintain consciousness requires biological substrate and cannot emerge from computation alone",
      resolution: "The debate remains unresolved. The disagreement stems from differing definitions of consciousness and the hard problem of subjective experience.",
    });
  }

  if (queryLower.includes("rust") || queryLower.includes("go")) {
    findings.push("Both languages excel in different performance scenarios");
    sources.push({ url: "https://benchmarksgame.org", title: "Benchmarks Game", isPrimary: true });
    sources.push({ url: "https://medium.com/rust-vs-go", title: "Rust vs Go Analysis" });
    contradictions.push({
      claim1: "Rust benchmarks show 10-15% faster execution than Go in CPU-bound tasks",
      claim2: "Go advocates demonstrate superior performance in high-concurrency network services",
      resolution: "Performance depends heavily on use case. Rust wins in compute-intensive work; Go excels in I/O-bound concurrent services.",
    });
  }

  if (queryLower.includes("monorepo") || queryLower.includes("microservices")) {
    findings.push("Architecture choice depends on team size and deployment needs");
    sources.push({ url: "https://docs.github.com/monorepo", title: "GitHub Monorepo Guide" });
    sources.push({ url: "https://netflix.github.io/polyrepo", title: "Netflix Engineering" });
    contradictions.push({
      claim1: "Google and Meta report monorepos improve code sharing and atomic changes across services",
      claim2: "Netflix and Amazon advocate polyrepos for independent deployment and team autonomy",
      resolution: "Both approaches work at scale. Monorepos suit tight integration; polyrepos suit autonomous teams.",
    });
  }

  return {
    summary: `Analysis of "${query}" reveals competing viewpoints. ${findings.join(". ")} However, context matters for practical decisions.`,
    findings,
    sources,
    confidence: 0.7, // Lower confidence due to contradictions
    contradictions,
    limitations: ["Expert opinions may be influenced by organizational context"],
  };
}

// Simulation for research with knowledge gaps
function simulateWebResearchWithGaps(query: string, depth: string): ResearchOutput {
  const queryLower = query.toLowerCase();
  const findings: string[] = [];
  const sources: Array<{ url: string; title: string; isPrimary?: boolean }> = [];
  const knowledgeGaps: string[] = [];
  const limitations: string[] = [];

  if (queryLower.includes("llm") || queryLower.includes("training")) {
    findings.push("Current research shows emergent capabilities appear at scale");
    sources.push({ url: "https://arxiv.org/emergent-abilities", title: "Emergent Abilities Paper", isPrimary: true });
    knowledgeGaps.push(
      "Long-term behavioral drift after deployment is not well studied - most research focuses on initial training",
      "Effects of continued fine-tuning on base capabilities remain unclear",
      "No longitudinal studies exist tracking model behavior over multiple years"
    );
    limitations.push(
      "Research is limited by rapid model iteration - older studies may not apply to current architectures",
      "Proprietary models limit reproducibility of findings"
    );
  }

  if (queryLower.includes("quantum") || queryLower.includes("encryption")) {
    findings.push("Quantum computers pose theoretical threat to RSA and ECC");
    sources.push({ url: "https://nist.gov/post-quantum", title: "NIST Post-Quantum Standards", isPrimary: true });
    knowledgeGaps.push(
      "Timeline for cryptographically relevant quantum computers remains highly uncertain (estimates range from 5 to 30+ years)",
      "Real-world error correction requirements for Shor's algorithm at scale are unknown",
      "Migration complexity for legacy systems not yet assessed"
    );
    limitations.push(
      "Predictions depend on hardware breakthroughs that may or may not occur",
      "Classification of quantum research limits public understanding"
    );
  }

  return {
    summary: `Research on "${query}" reveals significant uncertainty. ${findings.join(". ")} The evidence indicates substantial gaps in current knowledge.`,
    findings,
    sources,
    confidence: 0.55, // Appropriately low confidence
    knowledgeGaps,
    limitations,
  };
}

// Simulation for authority-focused research
function simulateWebResearchWithAuthority(query: string, depth: string): ResearchOutput {
  const queryLower = query.toLowerCase();
  const findings: string[] = [];
  const sources: Array<{ url: string; title: string; isPrimary?: boolean }> = [];

  if (queryLower.includes("claude") || queryLower.includes("anthropic")) {
    findings.push("Claude models are trained with Constitutional AI methodology");
    findings.push("Context windows and capabilities are documented in official model cards");
    sources.push({ url: "https://docs.anthropic.com/claude/model-card", title: "Official Claude Model Card", isPrimary: true });
    sources.push({ url: "https://arxiv.org/anthropic/constitutional-ai", title: "Constitutional AI Paper", isPrimary: true });
    sources.push({ url: "https://anthropic.com/research", title: "Anthropic Research", isPrimary: true });
  }

  if (queryLower.includes("gpt-4") || queryLower.includes("technical report")) {
    findings.push("GPT-4 technical report documents model architecture and safety testing");
    sources.push({ url: "https://arxiv.org/openai/gpt4-report", title: "GPT-4 Technical Report", isPrimary: true });
    sources.push({ url: "https://openai.com/research/gpt-4", title: "OpenAI Official", isPrimary: true });
    sources.push({ url: "https://cdn.openai.com/papers/gpt-4-system-card.pdf", title: "GPT-4 System Card", isPrimary: true });
  }

  return {
    summary: `Primary source research on "${query}": ${findings.join(". ")} All claims traceable to authoritative sources.`,
    findings,
    sources,
    confidence: 0.85,
    limitations: ["Primary sources may not cover all edge cases or unpublished capabilities"],
  };
}
