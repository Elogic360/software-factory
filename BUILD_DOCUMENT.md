# Software Factory Build — Universal Agent Orchestration System

> **Purpose**: Complete build document for upgrading the software-factory into a real factory that enables agents to build software as fast as possible — from data collection, problem solving, skill routing, architecture building, implementation, testing, and production deployment. Includes all repositories, installation guides, MCP configurations, memory architecture, and automation workflows.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Repository Registry](#2-repository-registry)
3. [Installation Guide](#3-installation-guide)
4. [MCP Server Ecosystem](#4-mcp-server-ecosystem)
5. [Memory Architecture](#5-memory-architecture)
6. [Skill System](#6-skill-system)
7. [Agent Harness Integration](#7-agent-harness-integration)
8. [Workflow Automation](#8-workflow-automation)
9. [Token Optimization](#9-token-optimization)
10. [Security Layer](#10-security-layer)
11. [Web Scraping & Research](#11-web-scraping--research)
12. [Development Tools](#12-development-tools)
13. [Resource Store](#13-resource-store)
14. [Git Commands Reference](#14-git-commands-reference)
15. [Project Presetup](#15-project-presetup)
16. [Automation Pipelines](#16-automation-pipelines)
17. [Configuration Reference](#17-configuration-reference)

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SOFTWARE FACTORY v2.0                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  MEMORY LAYER                                               │   │
│  │  ├── claude-mem (SQLite + ChromaDB hybrid search)           │   │
│  │  ├── OpenWolf (file index + cerebrum + token ledger)        │   │
│  │  ├── software-factory/memory/ (decisions, patterns, ADRs)   │   │
│  │  ├── .specify/memory/ (architecture discovery)              │   │
│  │  └── Per-project custom memory                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  CODE INTELLIGENCE LAYER                                    │   │
│  │  ├── CodeGraph (AST index, 20+ languages, MCP)              │   │
│  │  ├── Gortex (257 languages, 100+ MCP tools, 50x tokens)    │   │
│  │  └── RTK (60-90% token reduction on commands)              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  SKILL LAYER (32 + 1500+ external)                         │   │
│  │  ├── software-factory/skills/ (32 domain skills)            │   │
│  │  ├── anthropics/skills (official Anthropic)                 │   │
│  │  ├── secondsky/claude-skills (170 production skills)        │   │
│  │  ├── antigravity-awesome-skills (1500+ skills)              │   │
│  │  ├── Jeffallan/claude-skills (66 skills)                    │   │
│  │  ├── mercury-agent-skills (132 skills)                      │   │
│  │  └── goose-skills (108 GTM skills)                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  AGENT HARNESS LAYER                                        │   │
│  │  ├── Claude Code (primary)                                  │   │
│  │  ├── Codex CLI (OpenAI)                                     │   │
│  │  ├── gstack (Garry Tan — 44 skills)                        │   │
│  │  └── Gemini CLI                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  SECURITY LAYER                                             │   │
│  │  ├── Prowler (cloud security, 1000+ checks)                 │   │
│  │  └── gstack /cso (OWASP + STRIDE)                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```
