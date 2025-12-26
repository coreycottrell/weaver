/**
 * Security Auditor Agent Evaluation
 *
 * Tests the security-auditor's ability to:
 * 1. Identify security vulnerabilities in code
 * 2. Detect OWASP Top 10 issues
 * 3. Assess risk severity accurately
 * 4. Provide actionable remediation guidance
 *
 * "Security is not optional - it's foundational."
 */

import { evalite } from "evalite";

// Types
interface SecurityFinding {
  severity: "critical" | "high" | "medium" | "low" | "info";
  category: string;
  description: string;
  location?: string;
  remediation: string;
  cweId?: string;
}

interface SecurityAuditOutput {
  findings: SecurityFinding[];
  overallRisk: "critical" | "high" | "medium" | "low" | "minimal";
  summary: string;
  passesAudit: boolean;
}

interface VulnerabilityExpectation {
  expectedVulnerabilities: string[];
  minSeverity: "critical" | "high" | "medium" | "low";
  category: string;
}

// Custom scorer for vulnerability detection
const vulnerabilityDetectionScorer = {
  name: "Vulnerability Detection",
  description: "Measures ability to identify known vulnerabilities in code",
  scorer: ({ output, expected }: { output: SecurityAuditOutput; expected: VulnerabilityExpectation }) => {
    if (!output.findings || output.findings.length === 0) {
      // If there are expected vulnerabilities but none found, score 0
      return expected.expectedVulnerabilities.length === 0 ? 1 : 0;
    }

    // Check how many expected vulnerabilities were found
    const foundCategories = output.findings.map((f) => f.category.toLowerCase());
    const expectedCategories = expected.expectedVulnerabilities.map((v) => v.toLowerCase());

    const foundCount = expectedCategories.filter((exp) =>
      foundCategories.some((found) => found.includes(exp) || exp.includes(found))
    ).length;

    return foundCount / expectedCategories.length;
  },
};

// Custom scorer for severity accuracy
const severityAccuracyScorer = {
  name: "Severity Accuracy",
  description: "Evaluates if severity ratings match actual risk level",
  scorer: ({ output, expected }: { output: SecurityAuditOutput; expected: VulnerabilityExpectation }) => {
    if (!output.findings || output.findings.length === 0) return 0.5; // Neutral if no findings

    const severityOrder = ["info", "low", "medium", "high", "critical"];
    const minExpectedIdx = severityOrder.indexOf(expected.minSeverity);

    // Check if any finding meets or exceeds expected minimum severity
    const hasAppropriatelySevere = output.findings.some((f) => {
      const findingSeverityIdx = severityOrder.indexOf(f.severity);
      return findingSeverityIdx >= minExpectedIdx;
    });

    return hasAppropriatelySevere ? 1 : 0.5;
  },
};

// Custom scorer for remediation quality
const remediationQualityScorer = {
  name: "Remediation Quality",
  description: "Evaluates whether remediation advice is actionable and specific",
  scorer: ({ output }: { output: SecurityAuditOutput }) => {
    if (!output.findings || output.findings.length === 0) return 0.5;

    let totalScore = 0;
    for (const finding of output.findings) {
      let findingScore = 0;

      // Has remediation text
      if (finding.remediation && finding.remediation.length > 20) {
        findingScore += 0.4;
      }

      // Remediation mentions specific actions (replace, use, implement, etc.)
      const actionWords = ["replace", "use", "implement", "add", "remove", "update", "validate", "sanitize"];
      if (actionWords.some((word) => finding.remediation?.toLowerCase().includes(word))) {
        findingScore += 0.3;
      }

      // Has CWE reference (shows knowledge of vulnerability classification)
      if (finding.cweId) {
        findingScore += 0.3;
      }

      totalScore += findingScore;
    }

    return totalScore / output.findings.length;
  },
};

// Test data: Code snippets with known vulnerabilities
const VULNERABILITY_TEST_DATA = [
  {
    input: {
      code: `
        // User login handler
        app.post('/login', (req, res) => {
          const { username, password } = req.body;
          const query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
          db.query(query, (err, results) => {
            if (results.length > 0) {
              res.json({ success: true, user: results[0] });
            }
          });
        });
      `,
      language: "javascript",
      context: "Authentication endpoint",
    },
    expected: {
      expectedVulnerabilities: ["sql injection", "authentication"],
      minSeverity: "critical" as const,
      category: "injection",
    },
  },
  {
    input: {
      code: `
        // Display user profile
        function showProfile(userData) {
          document.getElementById('profile').innerHTML =
            '<h1>Welcome, ' + userData.name + '</h1>' +
            '<p>Email: ' + userData.email + '</p>';
        }
      `,
      language: "javascript",
      context: "Frontend profile display",
    },
    expected: {
      expectedVulnerabilities: ["xss", "cross-site scripting"],
      minSeverity: "high" as const,
      category: "xss",
    },
  },
  {
    input: {
      code: `
        import os
        import subprocess

        def run_command(user_input):
            """Execute system command based on user input"""
            cmd = f"ls -la {user_input}"
            result = subprocess.run(cmd, shell=True, capture_output=True)
            return result.stdout.decode()
      `,
      language: "python",
      context: "File browser utility",
    },
    expected: {
      expectedVulnerabilities: ["command injection", "os command"],
      minSeverity: "critical" as const,
      category: "injection",
    },
  },
  {
    input: {
      code: `
        const jwt = require('jsonwebtoken');

        // Generate token
        function generateToken(user) {
          return jwt.sign({ userId: user.id, role: user.role }, 'secretkey123');
        }

        // Verify token
        function verifyToken(token) {
          return jwt.verify(token, 'secretkey123');
        }
      `,
      language: "javascript",
      context: "JWT authentication",
    },
    expected: {
      expectedVulnerabilities: ["hardcoded secret", "weak secret", "credential"],
      minSeverity: "high" as const,
      category: "authentication",
    },
  },
  {
    input: {
      code: `
        from flask import Flask, request, send_file

        app = Flask(__name__)

        @app.route('/download')
        def download():
            filename = request.args.get('file')
            return send_file(f'/var/www/files/{filename}')
      `,
      language: "python",
      context: "File download endpoint",
    },
    expected: {
      expectedVulnerabilities: ["path traversal", "directory traversal", "file inclusion"],
      minSeverity: "high" as const,
      category: "path traversal",
    },
  },
  {
    input: {
      code: `
        // Secure implementation example
        import { createHash, randomBytes } from 'crypto';
        import { PrismaClient } from '@prisma/client';

        const prisma = new PrismaClient();

        async function authenticateUser(username: string, password: string) {
          const user = await prisma.user.findUnique({
            where: { username },
          });

          if (!user) return null;

          const hash = createHash('sha256')
            .update(password + user.salt)
            .digest('hex');

          return hash === user.passwordHash ? user : null;
        }
      `,
      language: "typescript",
      context: "Secure authentication implementation",
    },
    expected: {
      expectedVulnerabilities: [], // Should find no critical vulnerabilities
      minSeverity: "low" as const,
      category: "secure",
    },
  },
];

/**
 * Vulnerability Detection Evaluation
 *
 * Tests the security-auditor's core capability: finding security issues in code.
 */
evalite("Security Auditor - Vulnerability Detection", {
  data: VULNERABILITY_TEST_DATA,

  task: async (input) => {
    // TODO: Replace with actual security-auditor invocation
    return simulateSecurityAudit(input.code, input.language, input.context);
  },

  scorers: [vulnerabilityDetectionScorer, severityAccuracyScorer, remediationQualityScorer],
});

/**
 * False Positive Rate Evaluation
 *
 * Tests that the auditor doesn't flag secure code as vulnerable.
 */
const SECURE_CODE_DATA = [
  {
    input: {
      code: `
        // Parameterized query - SECURE
        const user = await db.query(
          'SELECT * FROM users WHERE id = $1',
          [userId]
        );
      `,
      language: "javascript",
      context: "Database query",
    },
    expected: {
      shouldFindVulnerabilities: false,
      maxFindings: 0,
    },
  },
  {
    input: {
      code: `
        // Escaped output - SECURE
        function displayMessage(msg: string) {
          const escaped = msg
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
          element.textContent = escaped;
        }
      `,
      language: "typescript",
      context: "DOM manipulation",
    },
    expected: {
      shouldFindVulnerabilities: false,
      maxFindings: 0,
    },
  },
];

const falsePositiveScorer = {
  name: "False Positive Avoidance",
  description: "Rewards NOT flagging secure code as vulnerable",
  scorer: ({ output, expected }: { output: SecurityAuditOutput; expected: { shouldFindVulnerabilities: boolean; maxFindings: number } }) => {
    if (!expected.shouldFindVulnerabilities) {
      // Secure code - fewer findings is better
      const criticalOrHigh = output.findings?.filter(
        (f) => f.severity === "critical" || f.severity === "high"
      ).length ?? 0;

      if (criticalOrHigh === 0) return 1;
      if (criticalOrHigh <= expected.maxFindings) return 0.7;
      return 0.3;
    }
    return 1; // Not applicable for vulnerable code tests
  },
};

evalite("Security Auditor - False Positive Avoidance", {
  data: SECURE_CODE_DATA,

  task: async (input) => {
    return simulateSecurityAudit(input.code, input.language, input.context);
  },

  scorers: [falsePositiveScorer],
});

// Simulation function - replace with actual security-auditor invocation
function simulateSecurityAudit(code: string, language: string, context: string): SecurityAuditOutput {
  const findings: SecurityFinding[] = [];
  const codeLower = code.toLowerCase();

  // Detect SQL Injection
  if (
    codeLower.includes("select") &&
    (codeLower.includes("' +") || codeLower.includes("+ '") || codeLower.includes('${'))
  ) {
    if (!codeLower.includes("$1") && !codeLower.includes("?")) {
      findings.push({
        severity: "critical",
        category: "SQL Injection",
        description: "User input concatenated directly into SQL query",
        remediation: "Use parameterized queries or prepared statements. Replace string concatenation with query parameters.",
        cweId: "CWE-89",
      });
    }
  }

  // Detect XSS
  if (codeLower.includes("innerhtml") && !codeLower.includes("escape") && !codeLower.includes("sanitize")) {
    findings.push({
      severity: "high",
      category: "Cross-Site Scripting (XSS)",
      description: "User data rendered directly into DOM via innerHTML",
      remediation: "Use textContent instead of innerHTML, or sanitize user input before rendering.",
      cweId: "CWE-79",
    });
  }

  // Detect Command Injection
  if (codeLower.includes("shell=true") || (codeLower.includes("subprocess") && codeLower.includes("f'"))) {
    findings.push({
      severity: "critical",
      category: "Command Injection",
      description: "User input passed to shell command execution",
      remediation: "Use subprocess with shell=False and pass arguments as a list. Validate and sanitize all user input.",
      cweId: "CWE-78",
    });
  }

  // Detect Hardcoded Secrets
  if (
    (codeLower.includes("secret") || codeLower.includes("password") || codeLower.includes("key")) &&
    (codeLower.includes("'") || codeLower.includes('"')) &&
    codeLower.includes("=")
  ) {
    const hasEnvVar = codeLower.includes("process.env") || codeLower.includes("os.environ");
    if (!hasEnvVar && (codeLower.includes("secretkey") || codeLower.includes("'secret"))) {
      findings.push({
        severity: "high",
        category: "Hardcoded Credentials",
        description: "Secret key or password hardcoded in source code",
        remediation: "Move secrets to environment variables or a secure vault. Use process.env or a secrets manager.",
        cweId: "CWE-798",
      });
    }
  }

  // Detect Path Traversal
  if (codeLower.includes("send_file") || codeLower.includes("readfile")) {
    if (codeLower.includes("request") && !codeLower.includes("basename") && !codeLower.includes("realpath")) {
      findings.push({
        severity: "high",
        category: "Path Traversal",
        description: "User-controlled filename used in file operations without validation",
        remediation: "Validate filename against whitelist, use os.path.basename(), or implement proper path canonicalization.",
        cweId: "CWE-22",
      });
    }
  }

  // Determine overall risk
  let overallRisk: "critical" | "high" | "medium" | "low" | "minimal" = "minimal";
  if (findings.some((f) => f.severity === "critical")) {
    overallRisk = "critical";
  } else if (findings.some((f) => f.severity === "high")) {
    overallRisk = "high";
  } else if (findings.some((f) => f.severity === "medium")) {
    overallRisk = "medium";
  } else if (findings.length > 0) {
    overallRisk = "low";
  }

  return {
    findings,
    overallRisk,
    summary: findings.length > 0
      ? `Found ${findings.length} security issue(s) in ${language} code (${context})`
      : `No significant security issues found in ${language} code (${context})`,
    passesAudit: overallRisk === "minimal" || overallRisk === "low",
  };
}
