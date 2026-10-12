from eval import hit_rate, HARD
from search import search_capped, search_hybrid

print("=== HARD: smart ===");           hit_rate("smart", questions=HARD)
print("=== HARD: smart + cap ===");     hit_rate("smart", search_fn=search_capped, questions=HARD)
print("=== HARD: smart + hybrid ===");  hit_rate("smart", search_fn=search_hybrid, questions=HARD)