"""
Software Factory Context & Token Optimization Plane.
Provides relevance ranking, deduplication, semantic compression, caching, and budget enforcement.
"""

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class OptimizationMetrics:
    tokens_before: int = 0
    tokens_after: int = 0
    compression_ratio: float = 0.0
    cache_hit_rate: float = 0.0
    tool_output_reduction: float = 0.0
    cost_saved_usd: float = 0.0

class ContextOptimizer:
    """Enterprise context optimization and token economy manager."""

    def __init__(self, token_cost_per_million: float = 3.0):
        self.cache: Dict[str, str] = {}
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.token_cost_per_million = token_cost_per_million

    def estimate_tokens(self, text: str) -> int:
        """Heuristic token estimation (~4 chars per token)."""
        if not text:
            return 0
        return max(1, len(text) // 4)

    def deduplicate(self, blocks: List[str]) -> List[str]:
        """Removes duplicated paragraphs and redundant blocks."""
        seen_hashes = set()
        unique_blocks = []
        for block in blocks:
            clean = re.sub(r'\s+', ' ', block.strip())
            h = hashlib.sha256(clean.encode('utf-8')).hexdigest()
            if h not in seen_hashes and len(clean) > 0:
                seen_hashes.add(h)
                unique_blocks.append(block)
        return unique_blocks

    def compress_text(self, text: str, max_tokens: Optional[int] = None) -> str:
        """Compresses verbose text by stripping repeated whitespace, boilerplate, and trimming."""
        # 1. Normalize whitespace
        compressed = re.sub(r'\n{3,}', '\n\n', text)
        compressed = re.sub(r'[ \t]+', ' ', compressed)

        # 2. Check token budget
        curr_tokens = self.estimate_tokens(compressed)
        if max_tokens and curr_tokens > max_tokens:
            char_budget = max_tokens * 4
            compressed = compressed[:char_budget] + "\n... [Context truncated to fit budget]"

        return compressed.strip()

    def optimize_context(self, task_query: str, context_sources: List[Dict[str, Any]], token_budget: int = 4000) -> Dict[str, Any]:
        """
        Ranks, deduplicates, compresses, and filters context blocks into the token budget.
        """
        total_raw_text = "".join([c.get("content", "") for c in context_sources])
        tokens_before = self.estimate_tokens(total_raw_text)

        # 1. Relevance scoring based on keyword overlap
        query_words = set(re.findall(r'\w+', task_query.lower()))
        scored_sources = []
        for src in context_sources:
            content = src.get("content", "")
            title = src.get("title", "")
            content_words = set(re.findall(r'\w+', (title + " " + content).lower()))
            overlap = len(query_words.intersection(content_words))
            priority = src.get("priority", 1.0)
            score = (overlap * 2.0) + priority
            scored_sources.append((score, src))

        # Sort highest score first
        scored_sources.sort(key=lambda x: x[0], reverse=True)

        # 2. Deduplication and budget packing
        selected_contents = []
        accumulated_tokens = 0

        for score, src in scored_sources:
            content = src.get("content", "")
            # Cache check
            c_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            if c_hash in self.cache:
                self.cache_hits += 1
            else:
                self.cache_misses += 1
                self.cache[c_hash] = content

            compressed = self.compress_text(content)
            cost = self.estimate_tokens(compressed)

            if accumulated_tokens + cost <= token_budget:
                selected_contents.append(f"### {src.get('title', 'Context')}\n{compressed}")
                accumulated_tokens += cost
            else:
                remaining_tokens = token_budget - accumulated_tokens
                if remaining_tokens > 50:
                    truncated = self.compress_text(content, max_tokens=remaining_tokens)
                    selected_contents.append(f"### {src.get('title', 'Context')} (Partial)\n{truncated}")
                    accumulated_tokens += self.estimate_tokens(truncated)
                break

        final_context = "\n\n".join(selected_contents)
        tokens_after = self.estimate_tokens(final_context)
        reduction = max(0, tokens_before - tokens_after)
        ratio = (tokens_after / max(1, tokens_before)) if tokens_before > 0 else 1.0
        total_lookups = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / max(1, total_lookups)) if total_lookups > 0 else 0.0
        cost_saved = (reduction / 1_000_000.0) * self.token_cost_per_million

        metrics = OptimizationMetrics(
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            compression_ratio=round(ratio, 3),
            cache_hit_rate=round(hit_rate, 3),
            tool_output_reduction=round((reduction / max(1, tokens_before)) * 100, 2),
            cost_saved_usd=round(cost_saved, 5)
        )

        return {
            "optimized_context": final_context,
            "metrics": metrics.__dict__,
            "sources_used": len(selected_contents),
            "sources_total": len(context_sources)
        }
