# llm_router.py

from typing import Dict

# --------------------------------------
# 1. Model Profiles
# --------------------------------------
model_profiles: Dict[str, Dict] = {
    "gpt-4-turbo": {
        "modalities": ["text", "code", "image"],
        "strengths": ["complex reasoning", "multi-modal analysis", "coding"],
        "cost_per_1k_tokens": 0.01,
        "max_tokens": 128000
    },
    "claude-3-opus": {
        "modalities": ["text", "code", "image"],
        "strengths": ["long-form reasoning", "code understanding", "factual accuracy"],
        "cost_per_1k_tokens": 0.015,
        "max_tokens": 200000
    },
    "gemini-1.5-pro": {
        "modalities": ["text", "code", "image"],
        "strengths": ["multi-modal chat", "creative writing", "fast execution"],
        "cost_per_1k_tokens": 0.008,
        "max_tokens": 100000
    },
    "mistral-medium": {
        "modalities": ["text", "code"],
        "strengths": ["lightweight tasks", "low-latency", "cost efficiency"],
        "cost_per_1k_tokens": 0.003,
        "max_tokens": 32000
    }
}


# --------------------------------------
# 2. Query Classifier
# --------------------------------------
def classify_query(query: str, has_image: bool = False, tokens_estimate: int = 1000) -> str:
    query_lower = query.lower()

    if has_image:
        return "image_analysis"
    if "generate" in query_lower or "creative" in query_lower or "story" in query_lower:
        return "creative_writing"
    if "analyze" in query_lower or "debug" in query_lower or "explain" in query_lower or "code" in query_lower:
        return "complex_code"
    if tokens_estimate > 100000:
        return "long_context"
    if "quick" in query_lower or tokens_estimate < 1000:
        return "fast_low_cost"
    return "general_text"


# --------------------------------------
# 3. Model Selector
# --------------------------------------
def select_model(query_type: str) -> str:
    priority_map = {
        "image_analysis": ["gpt-4-turbo", "claude-3-opus", "gemini-1.5-pro"],
        "complex_code": ["claude-3-opus", "gpt-4-turbo", "gemini-1.5-pro"],
        "creative_writing": ["gemini-1.5-pro", "gpt-4-turbo"],
        "fast_low_cost": ["mistral-medium", "gemini-1.5-pro"],
        "long_context": ["claude-3-opus", "gpt-4-turbo"],
        "general_text": ["gemini-1.5-pro", "mistral-medium"]
    }

    for model in priority_map.get(query_type, []):
        return model  # Return first match
    return "gpt-4-turbo"  # Default fallback


# --------------------------------------
# 4. Router
# --------------------------------------
def route_query(user_query: str, has_image: bool = False, estimated_tokens: int = 1000) -> Dict:
    query_type = classify_query(user_query, has_image, estimated_tokens)
    selected_model = select_model(query_type)
    cost = model_profiles[selected_model]["cost_per_1k_tokens"] * estimated_tokens / 1000

    return {
        "query_type": query_type,
        "selected_model": selected_model,
        "estimated_cost_usd": round(cost, 4),
        "max_tokens_supported": model_profiles[selected_model]["max_tokens"],
        "modalities": model_profiles[selected_model]["modalities"],
        "strengths": model_profiles[selected_model]["strengths"]
    }


# --------------------------------------
# 5. Example Usage
# --------------------------------------
if __name__ == "__main__":
    example_queries = [
        ("Can you analyze this Python function and explain the bug?", False, 1500),
        ("Here's an image of a receipt. Summarize the total items.", True, 500),
        ("Write a short story about dragons and space travel", False, 3000),
        ("Quick answer: What is the capital of France?", False, 200),
        ("Give me a 150,000 token report about world history", False, 150000)
    ]

    for q, img, tokens in example_queries:
        result = route_query(q, has_image=img, estimated_tokens=tokens)
        print(f"\n📝 Query: {q}")
        print("📦 Routed to:", result["selected_model"])
        print("🧠 Type:", result["query_type"])
        print("💰 Cost: $", result["estimated_cost_usd"])
        print("📈 Max Tokens:", result["max_tokens_supported"])
        print("📷 Modalities:", result["modalities"])
        print("🚀 Strengths:", result["strengths"])
