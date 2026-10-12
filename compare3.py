from eval import hit_rate, HELD_OUT
from search import search_capped, search_hybrid

print("=== HELD-OUT: naive ===");              hit_rate("naive", questions=HELD_OUT)
print("=== HELD-OUT: smart ===");              hit_rate("smart", questions=HELD_OUT)
print("=== HELD-OUT: naive + cap ===");        hit_rate("naive", search_fn=search_capped, questions=HELD_OUT)
print("=== HELD-OUT: smart + cap ===");        hit_rate("smart", search_fn=search_capped, questions=HELD_OUT)
print("=== HELD-OUT: smart + hybrid ===");     hit_rate("smart", search_fn=search_hybrid, questions=HELD_OUT)