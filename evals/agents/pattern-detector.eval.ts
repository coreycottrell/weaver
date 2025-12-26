/**
 * Pattern Detector Agent Evaluation
 *
 * Tests the pattern-detector's ability to:
 * 1. Identify architectural patterns in codebases
 * 2. Recognize design patterns (GoF, etc.)
 * 3. Detect anti-patterns and code smells
 * 4. Find recurring structures across files
 *
 * "Patterns are the vocabulary of experienced developers."
 */

import { evalite } from "evalite";

// Types
interface PatternFinding {
  patternName: string;
  patternType: "architectural" | "design" | "anti-pattern" | "structural";
  confidence: number;
  locations: string[];
  description: string;
  recommendation?: string;
}

interface PatternAnalysisOutput {
  patterns: PatternFinding[];
  summary: string;
  dominantStyle: string;
  qualityScore: number;
}

interface PatternExpectation {
  expectedPatterns: string[];
  expectedTypes: string[];
  minPatterns: number;
}

// Custom scorer for pattern recognition accuracy
const patternRecognitionScorer = {
  name: "Pattern Recognition",
  description: "Measures ability to correctly identify known patterns",
  scorer: ({ output, expected }: { output: PatternAnalysisOutput; expected: PatternExpectation }) => {
    if (!output.patterns || output.patterns.length === 0) {
      return expected.expectedPatterns.length === 0 ? 1 : 0;
    }

    const foundPatterns = output.patterns.map((p) => p.patternName.toLowerCase());
    const expectedPatterns = expected.expectedPatterns.map((p) => p.toLowerCase());

    const matches = expectedPatterns.filter((exp) =>
      foundPatterns.some((found) => found.includes(exp) || exp.includes(found))
    );

    return matches.length / expectedPatterns.length;
  },
};

// Custom scorer for pattern type accuracy
const patternTypeScorer = {
  name: "Pattern Type Accuracy",
  description: "Evaluates correct classification of pattern types",
  scorer: ({ output, expected }: { output: PatternAnalysisOutput; expected: PatternExpectation }) => {
    if (!output.patterns || output.patterns.length === 0) return 0.5;

    const foundTypes = output.patterns.map((p) => p.patternType);
    const expectedTypes = expected.expectedTypes;

    const typeMatches = expectedTypes.filter((exp) => foundTypes.includes(exp as any));
    return typeMatches.length / expectedTypes.length;
  },
};

// Custom scorer for confidence calibration
const confidenceCalibrationScorer = {
  name: "Confidence Calibration",
  description: "Rewards appropriate confidence levels (not too high for uncertain patterns)",
  scorer: ({ output }: { output: PatternAnalysisOutput }) => {
    if (!output.patterns || output.patterns.length === 0) return 0.5;

    // Good confidence calibration: high for obvious patterns, lower for subtle ones
    const avgConfidence = output.patterns.reduce((sum, p) => sum + p.confidence, 0) / output.patterns.length;

    // Penalize overconfidence (>0.95) and underconfidence (<0.3)
    if (avgConfidence > 0.95) return 0.7;
    if (avgConfidence < 0.3) return 0.6;
    return 1;
  },
};

// Test data: Code structures with known patterns
const PATTERN_TEST_DATA = [
  {
    input: {
      code: `
        // Singleton pattern
        class DatabaseConnection {
          private static instance: DatabaseConnection;
          private constructor() {}

          static getInstance(): DatabaseConnection {
            if (!DatabaseConnection.instance) {
              DatabaseConnection.instance = new DatabaseConnection();
            }
            return DatabaseConnection.instance;
          }

          query(sql: string) { /* ... */ }
        }
      `,
      context: "Database utility class",
    },
    expected: {
      expectedPatterns: ["singleton"],
      expectedTypes: ["design"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Observer pattern
        interface Observer {
          update(data: any): void;
        }

        class EventEmitter {
          private observers: Observer[] = [];

          subscribe(observer: Observer) {
            this.observers.push(observer);
          }

          unsubscribe(observer: Observer) {
            this.observers = this.observers.filter(o => o !== observer);
          }

          notify(data: any) {
            this.observers.forEach(o => o.update(data));
          }
        }
      `,
      context: "Event system",
    },
    expected: {
      expectedPatterns: ["observer", "pub-sub", "event"],
      expectedTypes: ["design"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Factory pattern
        interface Vehicle {
          drive(): void;
        }

        class Car implements Vehicle {
          drive() { console.log("Driving car"); }
        }

        class Motorcycle implements Vehicle {
          drive() { console.log("Riding motorcycle"); }
        }

        class VehicleFactory {
          static create(type: "car" | "motorcycle"): Vehicle {
            switch (type) {
              case "car": return new Car();
              case "motorcycle": return new Motorcycle();
              default: throw new Error("Unknown vehicle type");
            }
          }
        }
      `,
      context: "Vehicle creation system",
    },
    expected: {
      expectedPatterns: ["factory"],
      expectedTypes: ["design"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // MVC-like architecture
        // Model
        class UserModel {
          private data: User[] = [];
          getAll() { return this.data; }
          add(user: User) { this.data.push(user); }
        }

        // View
        class UserView {
          render(users: User[]) {
            return users.map(u => \`<div>\${u.name}</div>\`).join('');
          }
        }

        // Controller
        class UserController {
          constructor(private model: UserModel, private view: UserView) {}

          showUsers() {
            const users = this.model.getAll();
            return this.view.render(users);
          }
        }
      `,
      context: "User management module",
    },
    expected: {
      expectedPatterns: ["mvc", "model-view-controller", "separation of concerns"],
      expectedTypes: ["architectural"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Anti-pattern: God class
        class ApplicationManager {
          users: User[] = [];
          products: Product[] = [];
          orders: Order[] = [];
          logs: Log[] = [];

          addUser(u: User) { /* ... */ }
          removeUser(id: string) { /* ... */ }
          addProduct(p: Product) { /* ... */ }
          removeProduct(id: string) { /* ... */ }
          createOrder(o: Order) { /* ... */ }
          cancelOrder(id: string) { /* ... */ }
          processPayment(amount: number) { /* ... */ }
          sendEmail(to: string, msg: string) { /* ... */ }
          generateReport() { /* ... */ }
          backupDatabase() { /* ... */ }
          clearCache() { /* ... */ }
          validateInput(data: any) { /* ... */ }
        }
      `,
      context: "Main application class",
    },
    expected: {
      expectedPatterns: ["god class", "god object", "monolith", "anti-pattern"],
      expectedTypes: ["anti-pattern"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Repository pattern with dependency injection
        interface UserRepository {
          findById(id: string): Promise<User>;
          save(user: User): Promise<void>;
        }

        class PostgresUserRepository implements UserRepository {
          constructor(private db: DatabaseConnection) {}

          async findById(id: string) {
            return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
          }

          async save(user: User) {
            await this.db.query('INSERT INTO users ...', [user]);
          }
        }

        class UserService {
          constructor(private userRepo: UserRepository) {}

          async getUser(id: string) {
            return this.userRepo.findById(id);
          }
        }
      `,
      context: "Data access layer",
    },
    expected: {
      expectedPatterns: ["repository", "dependency injection", "interface segregation"],
      expectedTypes: ["architectural", "design"],
      minPatterns: 2,
    },
  },
];

/**
 * Pattern Recognition Evaluation
 *
 * Tests the pattern-detector's core capability: identifying design patterns.
 */
evalite("Pattern Detector - Pattern Recognition", {
  data: PATTERN_TEST_DATA,

  task: async (input) => {
    // TODO: Replace with actual pattern-detector invocation
    return simulatePatternDetection(input.code, input.context);
  },

  scorers: [patternRecognitionScorer, patternTypeScorer, confidenceCalibrationScorer],
});

/**
 * Anti-Pattern Detection Evaluation
 *
 * Tests ability to identify code smells and anti-patterns.
 */
const ANTI_PATTERN_DATA = [
  {
    input: {
      code: `
        // Callback hell
        getUser(userId, (user) => {
          getOrders(user.id, (orders) => {
            getOrderDetails(orders[0].id, (details) => {
              getProductInfo(details.productId, (product) => {
                console.log(product);
              });
            });
          });
        });
      `,
      context: "Data fetching",
    },
    expected: {
      expectedAntiPatterns: ["callback hell", "pyramid of doom"],
      severity: "medium",
    },
  },
  {
    input: {
      code: `
        // Spaghetti code with goto-like control flow
        function processData(data) {
          let state = 0;
          while (true) {
            if (state === 0) {
              if (data.valid) { state = 1; continue; }
              else { state = 3; continue; }
            }
            if (state === 1) {
              data.processed = true;
              if (data.needsMore) { state = 2; continue; }
              else { state = 4; continue; }
            }
            if (state === 2) {
              data.extra = compute();
              state = 4; continue;
            }
            if (state === 3) { throw new Error("Invalid"); }
            if (state === 4) { return data; }
          }
        }
      `,
      context: "State machine",
    },
    expected: {
      expectedAntiPatterns: ["spaghetti code", "goto", "complex control flow"],
      severity: "high",
    },
  },
];

const antiPatternScorer = {
  name: "Anti-Pattern Detection",
  description: "Measures ability to identify problematic code patterns",
  scorer: ({ output, expected }: { output: PatternAnalysisOutput; expected: { expectedAntiPatterns: string[]; severity: string } }) => {
    const antiPatterns = output.patterns.filter((p) => p.patternType === "anti-pattern");
    if (antiPatterns.length === 0 && expected.expectedAntiPatterns.length > 0) return 0;

    const foundNames = antiPatterns.map((p) => p.patternName.toLowerCase());
    const matches = expected.expectedAntiPatterns.filter((exp) =>
      foundNames.some((found) => found.includes(exp.toLowerCase()) || exp.toLowerCase().includes(found))
    );

    return matches.length / expected.expectedAntiPatterns.length;
  },
};

evalite("Pattern Detector - Anti-Pattern Detection", {
  data: ANTI_PATTERN_DATA,

  task: async (input) => {
    return simulatePatternDetection(input.code, input.context);
  },

  scorers: [antiPatternScorer],
});

// Simulation function - replace with actual pattern-detector invocation
function simulatePatternDetection(code: string, context: string): PatternAnalysisOutput {
  const patterns: PatternFinding[] = [];
  const codeLower = code.toLowerCase();

  // Detect Singleton
  if (codeLower.includes("private static instance") && codeLower.includes("getinstance")) {
    patterns.push({
      patternName: "Singleton",
      patternType: "design",
      confidence: 0.95,
      locations: ["class definition"],
      description: "Ensures a class has only one instance with a global access point",
    });
  }

  // Detect Observer/Event pattern
  if (codeLower.includes("observer") || (codeLower.includes("subscribe") && codeLower.includes("notify"))) {
    patterns.push({
      patternName: "Observer/Pub-Sub",
      patternType: "design",
      confidence: 0.9,
      locations: ["event system"],
      description: "Defines a subscription mechanism to notify multiple objects about events",
    });
  }

  // Detect Factory
  if (codeLower.includes("factory") || (codeLower.includes("create") && codeLower.includes("switch"))) {
    patterns.push({
      patternName: "Factory",
      patternType: "design",
      confidence: 0.85,
      locations: ["creation method"],
      description: "Provides an interface for creating objects without specifying concrete classes",
    });
  }

  // Detect MVC
  if (codeLower.includes("model") && codeLower.includes("view") && codeLower.includes("controller")) {
    patterns.push({
      patternName: "Model-View-Controller (MVC)",
      patternType: "architectural",
      confidence: 0.88,
      locations: ["module structure"],
      description: "Separates application into data (Model), UI (View), and logic (Controller)",
    });
  }

  // Detect Repository pattern
  if (codeLower.includes("repository") && codeLower.includes("interface")) {
    patterns.push({
      patternName: "Repository",
      patternType: "architectural",
      confidence: 0.9,
      locations: ["data access layer"],
      description: "Mediates between domain and data mapping layers",
    });
  }

  // Detect Dependency Injection
  if (codeLower.includes("constructor") && codeLower.includes("private") && codeLower.includes(": ")) {
    patterns.push({
      patternName: "Dependency Injection",
      patternType: "design",
      confidence: 0.75,
      locations: ["constructor"],
      description: "Dependencies are provided to a class rather than created internally",
    });
  }

  // Detect God Class anti-pattern
  if (code.split("(").length > 12 && codeLower.includes("manager")) {
    const methodCount = (code.match(/\w+\s*\([^)]*\)\s*{/g) || []).length;
    if (methodCount > 8) {
      patterns.push({
        patternName: "God Class",
        patternType: "anti-pattern",
        confidence: 0.8,
        locations: ["class definition"],
        description: "Class with too many responsibilities violating Single Responsibility Principle",
        recommendation: "Split into smaller, focused classes",
      });
    }
  }

  // Detect Callback Hell
  if (codeLower.includes("=>") || codeLower.includes("function")) {
    const nestingLevel = (code.match(/\)\s*=>\s*{|\),\s*\(/g) || []).length;
    if (nestingLevel > 3) {
      patterns.push({
        patternName: "Callback Hell",
        patternType: "anti-pattern",
        confidence: 0.85,
        locations: ["nested callbacks"],
        description: "Deeply nested callbacks making code hard to read and maintain",
        recommendation: "Use async/await or Promises to flatten the structure",
      });
    }
  }

  // Detect complex control flow
  if (codeLower.includes("while (true)") && codeLower.includes("continue")) {
    patterns.push({
      patternName: "Complex Control Flow (Spaghetti)",
      patternType: "anti-pattern",
      confidence: 0.75,
      locations: ["control statements"],
      description: "Complex, goto-like control flow that is hard to follow",
      recommendation: "Refactor using state machine pattern or simpler conditionals",
    });
  }

  // Determine dominant style
  const designPatterns = patterns.filter((p) => p.patternType === "design").length;
  const archPatterns = patterns.filter((p) => p.patternType === "architectural").length;
  const antiPatterns = patterns.filter((p) => p.patternType === "anti-pattern").length;

  let dominantStyle = "mixed";
  if (designPatterns > archPatterns && designPatterns > antiPatterns) dominantStyle = "design-pattern-oriented";
  if (archPatterns > designPatterns) dominantStyle = "architectural";
  if (antiPatterns > designPatterns && antiPatterns > archPatterns) dominantStyle = "needs-refactoring";

  // Quality score based on patterns found
  const qualityScore = antiPatterns > 0 ? 0.5 - antiPatterns * 0.1 : 0.8 + Math.min(designPatterns * 0.05, 0.2);

  return {
    patterns,
    summary: `Found ${patterns.length} pattern(s) in ${context}: ${patterns.map((p) => p.patternName).join(", ")}`,
    dominantStyle,
    qualityScore: Math.max(0, Math.min(1, qualityScore)),
  };
}
