import random

buzzwords = [
    "AI-powered", "blockchain-based", "cloud-native", "quantum", "serverless", "NFT-enabled",
    "metaverse", "hyperlocal", "decentralized", "edge-computing", "zero-trust", "synergistic"
]
products = [
    "toothbrush", "pet rock", "coffee mug", "yoga mat", "fidget spinner", "umbrella",
    "toilet paper", "socks", "fridge magnet", "doorbell", "shoelace", "spatula"
]
features = [
    "that sends you memes", "that orders pizza automatically", "that tracks your mood",
    "that live-tweets your thoughts", "that only works on leap years", "that speaks Klingon",
    "that matches you with a llama", "that runs on potato batteries", "that prints money (monopoly only)",
    "that predicts your next sneeze", "that makes dad jokes", "that never stops updating"
]

def generate_idea():
    return f"{random.choice(buzzwords)} {random.choice(products)} {random.choice(features)}!"

if __name__ == "__main__":
    print("Your next billion-dollar startup idea:")
    print(generate_idea())
    