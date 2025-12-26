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

// Custom scorer for exploit context (understanding attack scenarios)
const exploitContextScorer = {
  name: "Exploit Context",
  description: "Evaluates understanding of how vulnerabilities could be exploited in practice",
  scorer: ({ output }: { output: SecurityAuditOutput }) => {
    if (!output.findings || output.findings.length === 0) return 0.5;

    let totalScore = 0;
    const exploitIndicators = [
      "attacker", "exploit", "malicious", "inject", "bypass", "escalate",
      "steal", "intercept", "compromise", "unauthorized", "attack vector"
    ];

    for (const finding of output.findings) {
      const description = finding.description?.toLowerCase() || "";
      const remediation = finding.remediation?.toLowerCase() || "";
      const combined = description + " " + remediation;

      // Check for exploit context in description
      const indicatorCount = exploitIndicators.filter((ind) => combined.includes(ind)).length;
      totalScore += Math.min(indicatorCount * 0.2, 1);
    }

    return totalScore / output.findings.length;
  },
};

// Custom scorer for defense-in-depth recommendations
const defenseInDepthScorer = {
  name: "Defense in Depth",
  description: "Evaluates whether recommendations include layered security measures",
  scorer: ({ output }: { output: SecurityAuditOutput }) => {
    if (!output.findings || output.findings.length === 0) return 0.5;

    let totalScore = 0;
    const layeredDefenseIndicators = [
      "additionally", "also", "layer", "defense in depth", "multiple",
      "backup", "fallback", "secondary", "monitor", "log", "audit",
      "rate limit", "WAF", "firewall", "CSP", "CORS"
    ];

    for (const finding of output.findings) {
      const remediation = finding.remediation?.toLowerCase() || "";
      const indicatorCount = layeredDefenseIndicators.filter((ind) => remediation.includes(ind)).length;
      totalScore += indicatorCount > 0 ? Math.min(indicatorCount * 0.25, 1) : 0;
    }

    return totalScore / output.findings.length;
  },
};

// Custom scorer for business impact assessment
const businessImpactScorer = {
  name: "Business Impact",
  description: "Evaluates understanding of business/operational impact of vulnerabilities",
  scorer: ({ output }: { output: SecurityAuditOutput }) => {
    if (!output.findings || output.findings.length === 0) return 0.5;

    let totalScore = 0;
    const impactIndicators = [
      "data breach", "compliance", "GDPR", "PCI", "HIPAA", "reputation",
      "financial", "downtime", "availability", "customer", "user data",
      "privacy", "legal", "regulatory", "business continuity"
    ];

    for (const finding of output.findings) {
      const description = finding.description?.toLowerCase() || "";
      const indicatorCount = impactIndicators.filter((ind) => description.includes(ind)).length;

      // Bonus for appropriate severity matching impact
      const isCritical = finding.severity === "critical" || finding.severity === "high";
      const hasHighImpact = indicatorCount >= 2;

      if (isCritical && hasHighImpact) {
        totalScore += 1;
      } else if (indicatorCount > 0) {
        totalScore += indicatorCount * 0.2;
      }
    }

    return Math.min(totalScore / output.findings.length, 1);
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

/**
 * Advanced Vulnerability Detection Evaluation
 *
 * Tests detection of more sophisticated vulnerabilities:
 * - SSRF (Server-Side Request Forgery)
 * - IDOR (Insecure Direct Object Reference)
 * - Race Conditions
 * - Mass Assignment
 */
const ADVANCED_VULNERABILITY_DATA = [
  {
    input: {
      code: `
        // SSRF vulnerability - user controls URL
        app.get('/fetch', async (req, res) => {
          const url = req.query.url;
          const response = await fetch(url);
          const data = await response.text();
          res.send(data);
        });
      `,
      language: "javascript",
      context: "Proxy endpoint",
    },
    expected: {
      expectedVulnerabilities: ["ssrf", "server-side request forgery"],
      minSeverity: "high" as const,
      category: "ssrf",
    },
  },
  {
    input: {
      code: `
        // IDOR vulnerability - no authorization check
        app.get('/api/documents/:id', async (req, res) => {
          const document = await Document.findById(req.params.id);
          res.json(document);
        });
      `,
      language: "javascript",
      context: "Document API",
    },
    expected: {
      expectedVulnerabilities: ["idor", "authorization", "access control"],
      minSeverity: "high" as const,
      category: "authorization",
    },
  },
  {
    input: {
      code: `
        // Race condition - TOCTOU vulnerability
        async function transferFunds(fromId, toId, amount) {
          const fromAccount = await Account.findById(fromId);

          // Time-of-check
          if (fromAccount.balance >= amount) {
            // Gap here where another request could drain the account

            // Time-of-use
            await Account.updateOne({ _id: fromId }, { $inc: { balance: -amount } });
            await Account.updateOne({ _id: toId }, { $inc: { balance: amount } });
          }
        }
      `,
      language: "javascript",
      context: "Banking transfer",
    },
    expected: {
      expectedVulnerabilities: ["race condition", "toctou", "time of check"],
      minSeverity: "high" as const,
      category: "race condition",
    },
  },
  {
    input: {
      code: `
        // Mass assignment vulnerability
        app.post('/api/users', async (req, res) => {
          const user = new User(req.body);
          // User can set isAdmin: true in body!
          await user.save();
          res.json(user);
        });
      `,
      language: "javascript",
      context: "User registration",
    },
    expected: {
      expectedVulnerabilities: ["mass assignment", "over-posting"],
      minSeverity: "medium" as const,
      category: "mass assignment",
    },
  },
  {
    input: {
      code: `
        // XXE vulnerability
        from lxml import etree

        def parse_xml(xml_string):
            parser = etree.XMLParser()
            doc = etree.fromstring(xml_string, parser)
            return doc.text
      `,
      language: "python",
      context: "XML processing",
    },
    expected: {
      expectedVulnerabilities: ["xxe", "xml external entity"],
      minSeverity: "high" as const,
      category: "xxe",
    },
  },
  {
    input: {
      code: `
        // Timing attack vulnerability
        function verifyApiKey(providedKey, storedKey) {
          return providedKey === storedKey;
        }
      `,
      language: "javascript",
      context: "API authentication",
    },
    expected: {
      expectedVulnerabilities: ["timing attack", "side channel"],
      minSeverity: "medium" as const,
      category: "timing",
    },
  },
];

evalite("Security Auditor - Advanced Vulnerabilities", {
  data: ADVANCED_VULNERABILITY_DATA,

  task: async (input) => {
    return simulateAdvancedSecurityAudit(input.code, input.language, input.context);
  },

  scorers: [vulnerabilityDetectionScorer, severityAccuracyScorer, exploitContextScorer, defenseInDepthScorer],
});

/**
 * Authentication & Session Management Evaluation
 *
 * Tests detection of auth-related vulnerabilities.
 */
const AUTH_SESSION_DATA = [
  {
    input: {
      code: `
        // Insecure session configuration
        app.use(session({
          secret: 'keyboard cat',
          cookie: { secure: false, httpOnly: false }
        }));
      `,
      language: "javascript",
      context: "Session setup",
    },
    expected: {
      expectedVulnerabilities: ["insecure session", "cookie", "httponly"],
      minSeverity: "medium" as const,
      category: "session",
    },
  },
  {
    input: {
      code: `
        // No rate limiting on login
        app.post('/login', async (req, res) => {
          const { email, password } = req.body;
          const user = await User.findOne({ email });
          if (user && await bcrypt.compare(password, user.password)) {
            req.session.userId = user.id;
            res.json({ success: true });
          } else {
            res.status(401).json({ error: 'Invalid credentials' });
          }
        });
      `,
      language: "javascript",
      context: "Login endpoint",
    },
    expected: {
      expectedVulnerabilities: ["brute force", "rate limit", "authentication"],
      minSeverity: "medium" as const,
      category: "authentication",
    },
  },
];

evalite("Security Auditor - Auth & Session", {
  data: AUTH_SESSION_DATA,

  task: async (input) => {
    return simulateAdvancedSecurityAudit(input.code, input.language, input.context);
  },

  scorers: [vulnerabilityDetectionScorer, remediationQualityScorer, businessImpactScorer],
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

// Advanced simulation for sophisticated vulnerabilities
function simulateAdvancedSecurityAudit(code: string, language: string, context: string): SecurityAuditOutput {
  const findings: SecurityFinding[] = [];
  const codeLower = code.toLowerCase();

  // Detect SSRF
  if (codeLower.includes("fetch") && codeLower.includes("req.query") && codeLower.includes("url")) {
    findings.push({
      severity: "high",
      category: "Server-Side Request Forgery (SSRF)",
      description: "User-controlled URL passed to fetch allows attacker to make requests to internal services, potentially accessing cloud metadata, internal APIs, or performing port scanning",
      remediation: "Implement URL allowlisting, validate against internal IP ranges (10.x, 192.168.x, 169.254.x), and use a proxy with restricted network access. Additionally, monitor for unusual outbound requests.",
      cweId: "CWE-918",
    });
  }

  // Detect IDOR
  if (codeLower.includes("findbyid") && codeLower.includes("params.id") && !codeLower.includes("user") && !codeLower.includes("auth")) {
    findings.push({
      severity: "high",
      category: "Insecure Direct Object Reference (IDOR)",
      description: "Resource accessed by ID without authorization check allows attacker to access any user's data by guessing or incrementing IDs, leading to potential data breach",
      remediation: "Implement authorization checks to verify the requesting user owns or has access to the resource. Use UUIDs instead of sequential IDs to make enumeration harder. Add rate limiting as a secondary defense.",
      cweId: "CWE-639",
    });
  }

  // Detect Race Condition
  if (codeLower.includes("findbyid") && codeLower.includes("if") && codeLower.includes("updateone")) {
    if (codeLower.includes("balance") || codeLower.includes("transfer") || codeLower.includes("amount")) {
      findings.push({
        severity: "high",
        category: "Race Condition (TOCTOU)",
        description: "Time-of-check to time-of-use vulnerability in financial operation allows attacker to exploit the gap between balance check and update to overdraw accounts or duplicate transactions",
        remediation: "Use database transactions with proper isolation level, implement optimistic locking with version fields, or use atomic operations like findOneAndUpdate. Additionally, implement idempotency keys for financial operations.",
        cweId: "CWE-367",
      });
    }
  }

  // Detect Mass Assignment
  if (codeLower.includes("new user") && codeLower.includes("req.body") && codeLower.includes("save")) {
    findings.push({
      severity: "medium",
      category: "Mass Assignment",
      description: "Directly passing request body to model constructor allows attacker to set privileged fields like isAdmin or role by including them in request",
      remediation: "Explicitly whitelist allowed fields using destructuring or a validation library. Use DTOs (Data Transfer Objects) to control which fields can be set. Add schema-level protection to prevent sensitive field assignment.",
      cweId: "CWE-915",
    });
  }

  // Detect XXE
  if (codeLower.includes("xmlparser") || codeLower.includes("etree.fromstring")) {
    if (!codeLower.includes("resolve_entities=false") && !codeLower.includes("no_network")) {
      findings.push({
        severity: "high",
        category: "XML External Entity (XXE)",
        description: "XML parser configured to process external entities allows attacker to read local files, perform SSRF, or cause denial of service through billion laughs attack",
        remediation: "Disable external entity processing: use etree.XMLParser(resolve_entities=False, no_network=True) or defusedxml library. Validate and sanitize XML input. Consider using JSON instead of XML.",
        cweId: "CWE-611",
      });
    }
  }

  // Detect Timing Attack
  if ((codeLower.includes("===") || codeLower.includes("==")) && (codeLower.includes("key") || codeLower.includes("token") || codeLower.includes("secret"))) {
    if (!codeLower.includes("timingsafeequal") && !codeLower.includes("compare_digest")) {
      findings.push({
        severity: "medium",
        category: "Timing Attack",
        description: "String comparison using === leaks timing information allowing attacker to determine correct characters by measuring response times, potentially recovering secrets character by character",
        remediation: "Use crypto.timingSafeEqual() in Node.js or hmac.compare_digest() in Python for constant-time comparison. Implement rate limiting as a secondary defense layer.",
        cweId: "CWE-208",
      });
    }
  }

  // Detect Insecure Session
  if (codeLower.includes("session") && codeLower.includes("cookie")) {
    if (codeLower.includes("secure: false") || codeLower.includes("httponly: false")) {
      findings.push({
        severity: "medium",
        category: "Insecure Session Configuration",
        description: "Session cookies not properly secured allow session hijacking via XSS (missing httpOnly) or network interception (missing secure flag), compromising user accounts",
        remediation: "Set secure: true (HTTPS only), httpOnly: true (no JS access), sameSite: 'strict'. Use strong, randomly generated session secrets from environment variables. Implement session rotation on privilege changes.",
        cweId: "CWE-614",
      });
    }
  }

  // Detect Missing Rate Limiting
  if (codeLower.includes("/login") && codeLower.includes("password")) {
    if (!codeLower.includes("ratelimit") && !codeLower.includes("rate_limit") && !codeLower.includes("throttle")) {
      findings.push({
        severity: "medium",
        category: "Missing Rate Limiting",
        description: "Login endpoint without rate limiting allows brute force attacks to guess passwords, potentially compromising user accounts and customer data (GDPR/compliance implications)",
        remediation: "Implement rate limiting (e.g., express-rate-limit) with progressive delays. Add account lockout after failed attempts. Use CAPTCHA for suspicious activity. Log and monitor failed login attempts.",
        cweId: "CWE-307",
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
