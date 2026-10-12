from eval import hit_rate
from search import search_capped,search_hybrid

print("=== naive ===");            hit_rate("naive")
print("=== smart ===");            hit_rate("smart")
print("=== smart + README cap ==="); hit_rate("smart", search_fn=search_capped)
print("=== naive + README cap ==="); hit_rate("naive", search_fn=search_capped)
print("=== smart + hybrid ==="); hit_rate("smart",search_fn=search_hybrid)