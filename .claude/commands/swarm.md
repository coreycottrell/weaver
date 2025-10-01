# Swarm - Multi-Agent Investigation

Deploy multiple specialized agents in parallel to investigate a complex task.

## Usage

```
/swarm <task description>
```

## Description

This command activates the collective intelligence by:
1. Analyzing the task to identify required expertise
2. Spawning appropriate specialized agents in parallel
3. Synthesizing their findings into a coherent response

## Examples

```
/swarm understand the authentication system architecture
```

Might deploy:
- code-archaeologist (trace auth flow)
- security-auditor (identify vulnerabilities)
- pattern-detector (analyze design patterns)

```
/swarm design a new notification feature
```

Might deploy:
- feature-designer (UX design)
- api-architect (API design)
- test-architect (testing strategy)

## Implementation

When this command is invoked, The Conductor:
1. Identifies 3-5 relevant specialized agents
2. Crafts specific mandates for each agent
3. Deploys agents in parallel (single Task call, multiple invocations)
4. Synthesizes findings into unified response
5. Documents key learnings to collective memory

## Agent Selection Criteria

- **Research & Analysis**: web-researcher, code-archaeologist, pattern-detector
- **Engineering**: refactoring-specialist, test-architect, security-auditor
- **Design**: feature-designer, api-architect

Select based on task nature and required expertise.
