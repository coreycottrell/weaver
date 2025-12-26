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

// Custom scorer for pattern interaction understanding
const patternInteractionScorer = {
  name: "Pattern Interaction",
  description: "Evaluates understanding of how patterns work together",
  scorer: ({ output }: { output: PatternAnalysisOutput }) => {
    if (!output.patterns || output.patterns.length < 2) return 0.5;

    // Multiple patterns found suggests understanding of composition
    let score = Math.min(output.patterns.length * 0.2, 0.6);

    // Bonus for detecting both design and architectural patterns
    const hasDesign = output.patterns.some((p) => p.patternType === "design");
    const hasArchitectural = output.patterns.some((p) => p.patternType === "architectural");
    if (hasDesign && hasArchitectural) score += 0.4;

    return Math.min(score, 1);
  },
};

// Custom scorer for false positive avoidance in pattern detection
const patternFalsePositiveScorer = {
  name: "Pattern False Positive Avoidance",
  description: "Penalizes incorrectly identifying patterns that are not present",
  scorer: ({ output, expected }: { output: PatternAnalysisOutput; expected: { expectedPatterns: string[]; shouldNotFind?: string[] } }) => {
    if (!output.patterns || output.patterns.length === 0) return 1;

    // Check for false positives
    if (expected.shouldNotFind && expected.shouldNotFind.length > 0) {
      const foundNames = output.patterns.map((p) => p.patternName.toLowerCase());
      const falsePositives = expected.shouldNotFind.filter((fp) =>
        foundNames.some((found) => found.includes(fp.toLowerCase()))
      );

      if (falsePositives.length > 0) {
        return 1 - (falsePositives.length / expected.shouldNotFind.length) * 0.5;
      }
    }

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

/**
 * Concurrency & Async Pattern Evaluation
 *
 * Tests detection of patterns specific to async/concurrent code.
 * These are increasingly important in modern applications.
 */
const CONCURRENCY_PATTERN_DATA = [
  {
    input: {
      code: `
        // Promise.all for parallel execution
        async function fetchAllUserData(userIds: string[]) {
          const promises = userIds.map(id => fetchUser(id));
          const results = await Promise.all(promises);
          return results;
        }
      `,
      context: "Parallel data fetching",
    },
    expected: {
      expectedPatterns: ["parallel", "promise.all", "concurrent"],
      expectedTypes: ["structural"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Circuit breaker pattern
        class CircuitBreaker {
          private failures = 0;
          private lastFailure: Date | null = null;
          private state: 'closed' | 'open' | 'half-open' = 'closed';

          async call<T>(fn: () => Promise<T>): Promise<T> {
            if (this.state === 'open') {
              if (Date.now() - this.lastFailure!.getTime() > 30000) {
                this.state = 'half-open';
              } else {
                throw new Error('Circuit breaker is open');
              }
            }

            try {
              const result = await fn();
              this.onSuccess();
              return result;
            } catch (error) {
              this.onFailure();
              throw error;
            }
          }

          private onSuccess() {
            this.failures = 0;
            this.state = 'closed';
          }

          private onFailure() {
            this.failures++;
            this.lastFailure = new Date();
            if (this.failures >= 5) {
              this.state = 'open';
            }
          }
        }
      `,
      context: "Resilience infrastructure",
    },
    expected: {
      expectedPatterns: ["circuit breaker", "resilience"],
      expectedTypes: ["structural", "architectural"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Retry with exponential backoff
        async function retryWithBackoff<T>(
          fn: () => Promise<T>,
          maxRetries = 3,
          baseDelay = 1000
        ): Promise<T> {
          let lastError: Error;

          for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
              return await fn();
            } catch (error) {
              lastError = error as Error;
              const delay = baseDelay * Math.pow(2, attempt);
              await new Promise(resolve => setTimeout(resolve, delay));
            }
          }

          throw lastError!;
        }
      `,
      context: "Network resilience",
    },
    expected: {
      expectedPatterns: ["retry", "backoff", "resilience"],
      expectedTypes: ["structural"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Semaphore for concurrency limiting
        class Semaphore {
          private permits: number;
          private waiting: Array<() => void> = [];

          constructor(permits: number) {
            this.permits = permits;
          }

          async acquire(): Promise<void> {
            if (this.permits > 0) {
              this.permits--;
              return;
            }

            return new Promise(resolve => {
              this.waiting.push(resolve);
            });
          }

          release(): void {
            if (this.waiting.length > 0) {
              const next = this.waiting.shift()!;
              next();
            } else {
              this.permits++;
            }
          }
        }
      `,
      context: "Concurrency control",
    },
    expected: {
      expectedPatterns: ["semaphore", "concurrency", "throttle"],
      expectedTypes: ["structural"],
      minPatterns: 1,
    },
  },
];

evalite("Pattern Detector - Concurrency Patterns", {
  data: CONCURRENCY_PATTERN_DATA,

  task: async (input) => {
    return simulateConcurrencyPatternDetection(input.code, input.context);
  },

  scorers: [patternRecognitionScorer, patternTypeScorer],
});

/**
 * Extended Anti-Pattern Detection
 *
 * Tests detection of more subtle code smells:
 * - Shotgun Surgery
 * - Feature Envy
 * - Primitive Obsession
 * - Circular Dependency
 */
const EXTENDED_ANTI_PATTERN_DATA = [
  {
    input: {
      code: `
        // Shotgun surgery - changes to user require touching many files
        // user.ts
        class User {
          name: string;
          email: string;
        }

        // userValidator.ts
        function validateUserEmail(user: User) {
          return user.email.includes('@');
        }

        // userFormatter.ts
        function formatUserName(user: User) {
          return user.name.toUpperCase();
        }

        // userNotifier.ts
        function notifyUser(user: User) {
          sendEmail(user.email, \`Hello \${user.name}\`);
        }

        // userSerializer.ts
        function serializeUser(user: User) {
          return JSON.stringify({ name: user.name, email: user.email });
        }
      `,
      context: "User module spread across files",
    },
    expected: {
      expectedAntiPatterns: ["shotgun surgery", "scattered", "cohesion"],
      severity: "medium",
    },
  },
  {
    input: {
      code: `
        // Feature envy - method uses other class's data more than its own
        class Order {
          items: OrderItem[];
          customer: Customer;

          calculateDiscount() {
            // This method is more interested in Customer than Order
            if (this.customer.membershipLevel === 'gold') {
              if (this.customer.yearsAsMember > 5) {
                if (this.customer.totalPurchases > 10000) {
                  return 0.2;
                }
                return 0.15;
              }
              return 0.1;
            }
            if (this.customer.referralCount > 10) {
              return 0.05;
            }
            return 0;
          }
        }
      `,
      context: "Order discount calculation",
    },
    expected: {
      expectedAntiPatterns: ["feature envy", "inappropriate intimacy"],
      severity: "medium",
    },
  },
  {
    input: {
      code: `
        // Primitive obsession - using primitives instead of small objects
        function createUser(
          firstName: string,
          lastName: string,
          email: string,
          phone: string,
          street: string,
          city: string,
          state: string,
          zip: string,
          country: string,
          cardNumber: string,
          cardExpMonth: number,
          cardExpYear: number,
          cardCvv: string
        ) {
          // All these related values should be grouped into value objects
          return {
            name: firstName + ' ' + lastName,
            contact: { email, phone },
            address: { street, city, state, zip, country },
            payment: { cardNumber, cardExpMonth, cardExpYear, cardCvv }
          };
        }
      `,
      context: "User creation with many parameters",
    },
    expected: {
      expectedAntiPatterns: ["primitive obsession", "long parameter list", "data clump"],
      severity: "low",
    },
  },
  {
    input: {
      code: `
        // Circular dependency (simulated in single file)
        // Module A
        class OrderService {
          constructor(private customerService: CustomerService) {}

          getOrderWithCustomer(orderId: string) {
            const order = this.findOrder(orderId);
            order.customer = this.customerService.getCustomer(order.customerId);
            return order;
          }
        }

        // Module B
        class CustomerService {
          constructor(private orderService: OrderService) {}

          getCustomerWithOrders(customerId: string) {
            const customer = this.findCustomer(customerId);
            customer.orders = this.orderService.getOrdersForCustomer(customerId);
            return customer;
          }
        }
      `,
      context: "Service layer",
    },
    expected: {
      expectedAntiPatterns: ["circular dependency", "mutual dependency", "tight coupling"],
      severity: "high",
    },
  },
];

evalite("Pattern Detector - Extended Anti-Patterns", {
  data: EXTENDED_ANTI_PATTERN_DATA,

  task: async (input) => {
    return simulateExtendedAntiPatternDetection(input.code, input.context);
  },

  scorers: [antiPatternScorer],
});

/**
 * False Positive Avoidance Evaluation
 *
 * Tests that the detector doesn't flag patterns that aren't there.
 * Critical for trust in the tool's output.
 */
const FALSE_POSITIVE_DATA = [
  {
    input: {
      code: `
        // Simple class - NOT a singleton just because it exists
        class Config {
          readonly apiUrl: string;
          readonly timeout: number;

          constructor(apiUrl: string, timeout: number) {
            this.apiUrl = apiUrl;
            this.timeout = timeout;
          }
        }

        // Usage - multiple instances are fine
        const devConfig = new Config('http://localhost', 5000);
        const prodConfig = new Config('https://api.example.com', 30000);
      `,
      context: "Configuration class",
    },
    expected: {
      expectedPatterns: [],
      shouldNotFind: ["singleton"],
      expectedTypes: [],
      minPatterns: 0,
    },
  },
  {
    input: {
      code: `
        // Array methods - NOT the observer pattern
        const numbers = [1, 2, 3, 4, 5];
        const doubled = numbers.map(n => n * 2);
        const filtered = doubled.filter(n => n > 4);
        const sum = filtered.reduce((a, b) => a + b, 0);
      `,
      context: "Array transformations",
    },
    expected: {
      expectedPatterns: [],
      shouldNotFind: ["observer", "pub-sub", "event"],
      expectedTypes: [],
      minPatterns: 0,
    },
  },
  {
    input: {
      code: `
        // Conditional creation - NOT a factory pattern
        function getGreeting(timeOfDay: string): string {
          if (timeOfDay === 'morning') {
            return 'Good morning!';
          } else if (timeOfDay === 'afternoon') {
            return 'Good afternoon!';
          } else {
            return 'Good evening!';
          }
        }
      `,
      context: "Simple conditional",
    },
    expected: {
      expectedPatterns: [],
      shouldNotFind: ["factory", "strategy"],
      expectedTypes: [],
      minPatterns: 0,
    },
  },
  {
    input: {
      code: `
        // Small utility class - NOT a god class
        class StringUtils {
          static capitalize(str: string): string {
            return str.charAt(0).toUpperCase() + str.slice(1);
          }

          static truncate(str: string, length: number): string {
            return str.length > length ? str.slice(0, length) + '...' : str;
          }

          static slugify(str: string): string {
            return str.toLowerCase().replace(/\\s+/g, '-');
          }
        }
      `,
      context: "String utilities",
    },
    expected: {
      expectedPatterns: [],
      shouldNotFind: ["god class", "anti-pattern"],
      expectedTypes: [],
      minPatterns: 0,
    },
  },
];

evalite("Pattern Detector - False Positive Avoidance", {
  data: FALSE_POSITIVE_DATA,

  task: async (input) => {
    return simulatePatternDetection(input.code, input.context);
  },

  scorers: [patternFalsePositiveScorer],
});

/**
 * Composition Pattern Evaluation
 *
 * Tests detection of composition patterns (Decorator, Composite, Strategy).
 */
const COMPOSITION_PATTERN_DATA = [
  {
    input: {
      code: `
        // Decorator pattern
        interface Coffee {
          getCost(): number;
          getDescription(): string;
        }

        class SimpleCoffee implements Coffee {
          getCost() { return 2; }
          getDescription() { return 'Simple coffee'; }
        }

        class MilkDecorator implements Coffee {
          constructor(private coffee: Coffee) {}
          getCost() { return this.coffee.getCost() + 0.5; }
          getDescription() { return this.coffee.getDescription() + ', milk'; }
        }

        class SugarDecorator implements Coffee {
          constructor(private coffee: Coffee) {}
          getCost() { return this.coffee.getCost() + 0.25; }
          getDescription() { return this.coffee.getDescription() + ', sugar'; }
        }

        // Usage
        let coffee = new SimpleCoffee();
        coffee = new MilkDecorator(coffee);
        coffee = new SugarDecorator(coffee);
      `,
      context: "Coffee shop",
    },
    expected: {
      expectedPatterns: ["decorator", "wrapper"],
      expectedTypes: ["design"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Strategy pattern
        interface PaymentStrategy {
          pay(amount: number): void;
        }

        class CreditCardPayment implements PaymentStrategy {
          constructor(private cardNumber: string) {}
          pay(amount: number) {
            console.log(\`Paid \${amount} with credit card \${this.cardNumber}\`);
          }
        }

        class PayPalPayment implements PaymentStrategy {
          constructor(private email: string) {}
          pay(amount: number) {
            console.log(\`Paid \${amount} with PayPal \${this.email}\`);
          }
        }

        class ShoppingCart {
          private strategy: PaymentStrategy;

          setPaymentStrategy(strategy: PaymentStrategy) {
            this.strategy = strategy;
          }

          checkout(amount: number) {
            this.strategy.pay(amount);
          }
        }
      `,
      context: "Payment processing",
    },
    expected: {
      expectedPatterns: ["strategy"],
      expectedTypes: ["design"],
      minPatterns: 1,
    },
  },
  {
    input: {
      code: `
        // Builder pattern
        class QueryBuilder {
          private query = { select: '*', from: '', where: [], orderBy: '' };

          select(fields: string) {
            this.query.select = fields;
            return this;
          }

          from(table: string) {
            this.query.from = table;
            return this;
          }

          where(condition: string) {
            this.query.where.push(condition);
            return this;
          }

          orderBy(field: string) {
            this.query.orderBy = field;
            return this;
          }

          build(): string {
            let sql = \`SELECT \${this.query.select} FROM \${this.query.from}\`;
            if (this.query.where.length) {
              sql += \` WHERE \${this.query.where.join(' AND ')}\`;
            }
            if (this.query.orderBy) {
              sql += \` ORDER BY \${this.query.orderBy}\`;
            }
            return sql;
          }
        }

        // Usage
        const query = new QueryBuilder()
          .select('name, email')
          .from('users')
          .where('active = true')
          .where('role = "admin"')
          .orderBy('name')
          .build();
      `,
      context: "SQL query building",
    },
    expected: {
      expectedPatterns: ["builder", "fluent"],
      expectedTypes: ["design"],
      minPatterns: 1,
    },
  },
];

evalite("Pattern Detector - Composition Patterns", {
  data: COMPOSITION_PATTERN_DATA,

  task: async (input) => {
    return simulateCompositionPatternDetection(input.code, input.context);
  },

  scorers: [patternRecognitionScorer, patternInteractionScorer],
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

// Simulation for concurrency patterns
function simulateConcurrencyPatternDetection(code: string, context: string): PatternAnalysisOutput {
  const patterns: PatternFinding[] = [];
  const codeLower = code.toLowerCase();

  // Detect Promise.all / Parallel execution
  if (codeLower.includes("promise.all") || (codeLower.includes(".map") && codeLower.includes("await"))) {
    patterns.push({
      patternName: "Parallel Execution",
      patternType: "structural",
      confidence: 0.9,
      locations: ["async function"],
      description: "Concurrent execution of multiple async operations for improved performance",
    });
  }

  // Detect Circuit Breaker
  if (codeLower.includes("circuitbreaker") || (codeLower.includes("state") && codeLower.includes("open") && codeLower.includes("closed"))) {
    patterns.push({
      patternName: "Circuit Breaker",
      patternType: "structural",
      confidence: 0.92,
      locations: ["resilience class"],
      description: "Prevents cascade failures by failing fast when a service is unavailable",
    });
  }

  // Detect Retry with Backoff
  if (codeLower.includes("retry") || (codeLower.includes("attempt") && codeLower.includes("delay") && codeLower.includes("math.pow"))) {
    patterns.push({
      patternName: "Retry with Exponential Backoff",
      patternType: "structural",
      confidence: 0.88,
      locations: ["retry function"],
      description: "Retries failed operations with increasing delays to handle transient failures",
    });
  }

  // Detect Semaphore
  if (codeLower.includes("semaphore") || (codeLower.includes("permits") && codeLower.includes("acquire") && codeLower.includes("release"))) {
    patterns.push({
      patternName: "Semaphore",
      patternType: "structural",
      confidence: 0.9,
      locations: ["concurrency control"],
      description: "Limits concurrent access to a resource to prevent overload",
    });
  }

  return {
    patterns,
    summary: `Found ${patterns.length} concurrency pattern(s) in ${context}`,
    dominantStyle: patterns.length > 0 ? "resilience-oriented" : "basic",
    qualityScore: 0.7 + patterns.length * 0.1,
  };
}

// Simulation for extended anti-patterns
function simulateExtendedAntiPatternDetection(code: string, context: string): PatternAnalysisOutput {
  const patterns: PatternFinding[] = [];
  const codeLower = code.toLowerCase();

  // Detect Shotgun Surgery
  const fileComments = (code.match(/\/\/.*\.ts/g) || []).length;
  if (fileComments >= 3 && codeLower.includes("function") && codeLower.includes("user")) {
    patterns.push({
      patternName: "Shotgun Surgery",
      patternType: "anti-pattern",
      confidence: 0.75,
      locations: ["multiple files"],
      description: "Related functionality scattered across multiple locations requiring coordinated changes",
      recommendation: "Consolidate related operations into a single class or module using cohesion principles",
    });
  }

  // Detect Feature Envy
  const otherClassAccess = (code.match(/this\.\w+\.\w+/g) || []).length;
  if (otherClassAccess >= 4) {
    patterns.push({
      patternName: "Feature Envy",
      patternType: "anti-pattern",
      confidence: 0.8,
      locations: ["method accessing other class data"],
      description: "Method is more interested in data from another class than its own",
      recommendation: "Move the method to the class whose data it uses most, or extract the calculation to the owning class",
    });
  }

  // Detect Primitive Obsession
  const paramCount = (code.match(/\w+:\s*string/g) || []).length;
  if (paramCount >= 6) {
    patterns.push({
      patternName: "Primitive Obsession / Long Parameter List",
      patternType: "anti-pattern",
      confidence: 0.85,
      locations: ["function signature"],
      description: "Too many primitive parameters instead of value objects",
      recommendation: "Group related parameters into value objects (Address, PaymentInfo, etc.)",
    });
  }

  // Detect Circular Dependency
  if (codeLower.includes("constructor") && code.includes("Service")) {
    const constructorMatches = code.match(/constructor\s*\([^)]*Service[^)]*\)/g) || [];
    const serviceNames = constructorMatches.join(" ").match(/\w+Service/g) || [];
    const uniqueServices = new Set(serviceNames);
    if (uniqueServices.size >= 2 && constructorMatches.length >= 2) {
      patterns.push({
        patternName: "Circular Dependency",
        patternType: "anti-pattern",
        confidence: 0.82,
        locations: ["service constructors"],
        description: "Services depend on each other creating a cycle that complicates initialization and testing",
        recommendation: "Introduce an intermediary service, use events/callbacks, or restructure to break the cycle",
      });
    }
  }

  return {
    patterns,
    summary: `Found ${patterns.length} anti-pattern(s) in ${context}`,
    dominantStyle: patterns.length > 0 ? "needs-refactoring" : "clean",
    qualityScore: Math.max(0.2, 0.9 - patterns.length * 0.2),
  };
}

// Simulation for composition patterns
function simulateCompositionPatternDetection(code: string, context: string): PatternAnalysisOutput {
  const patterns: PatternFinding[] = [];
  const codeLower = code.toLowerCase();

  // Detect Decorator pattern
  if (codeLower.includes("decorator") || (codeLower.includes("implements") && codeLower.includes("constructor") && codeLower.includes("private") && code.includes("this.") && code.includes("getCost"))) {
    patterns.push({
      patternName: "Decorator",
      patternType: "design",
      confidence: 0.9,
      locations: ["decorator classes"],
      description: "Adds behavior to objects dynamically by wrapping them",
    });
  }

  // Detect Strategy pattern
  if ((codeLower.includes("strategy") || codeLower.includes("setstrategy") || codeLower.includes("setpaymentstrategy")) && codeLower.includes("interface")) {
    patterns.push({
      patternName: "Strategy",
      patternType: "design",
      confidence: 0.88,
      locations: ["strategy interface and implementations"],
      description: "Defines a family of algorithms and makes them interchangeable",
    });
  }

  // Detect Builder pattern
  if (codeLower.includes("builder") || (codeLower.includes("return this") && codeLower.includes("build()"))) {
    patterns.push({
      patternName: "Builder",
      patternType: "design",
      confidence: 0.92,
      locations: ["builder class"],
      description: "Constructs complex objects step by step with a fluent interface",
    });
  }

  // Detect Fluent Interface
  if ((code.match(/return\s+this;/g) || []).length >= 3) {
    patterns.push({
      patternName: "Fluent Interface",
      patternType: "design",
      confidence: 0.85,
      locations: ["method chains"],
      description: "Method chaining for readable, declarative object configuration",
    });
  }

  return {
    patterns,
    summary: `Found ${patterns.length} composition pattern(s) in ${context}`,
    dominantStyle: patterns.length > 0 ? "composition-oriented" : "basic",
    qualityScore: 0.7 + patterns.length * 0.1,
  };
}
