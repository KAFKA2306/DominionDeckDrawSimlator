from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass(frozen=True)
class GameConstants:
    TRANSPARENT_MIRROR_INITIAL_VALUE: int = 7
    TRANSPARENT_MIRROR_DIFFERENCE: int = 2
    SUBSCRIBE_COST: int = 2
    JOINWARS_INITIAL_COST: int = 36
    VICTORY_POINT_MULTIPLIER: int = 6
    MAX_ALLOWED_FINAL_COINS: int = 1560031
    MIN_ACCEPTABLE_VICTORY_POINTS: int = 0
    MAX_ACCEPTABLE_VICTORY_POINTS: int = 486
    HELD_COINS_OPTIONS: Tuple[int, ...] = (10, 20, 30, 50)
    MAX_TURNS: int = 20

@dataclass
class GameStrategy:
    transparent_mirror_count: int
    subscribe_count: int
    held_coins: int
    final_needed_coins: int
    victory_points: int
    turns_needed: int
    coins_after_growth: int
    tm_cost: int
    sub_cost: int

class JoinWarsOptimizer:
    def __init__(self, constants: GameConstants):
        self.constants = constants

    def calculate_final_needed_coins(self, tm_count: int, sub_count: int) -> Tuple[int, int, int]:
        tm_cost = tm_count * (self.constants.TRANSPARENT_MIRROR_INITIAL_VALUE * 2 + 
                             (tm_count - 1) * self.constants.TRANSPARENT_MIRROR_DIFFERENCE) // 2
        sub_cost = self.constants.SUBSCRIBE_COST * sub_count
        total_cost = tm_cost + sub_cost + self.constants.JOINWARS_INITIAL_COST
        return total_cost, tm_cost, sub_cost

    def calculate_victory_points(self, tm_count: int, sub_count: int) -> int:
        return self.constants.VICTORY_POINT_MULTIPLIER * tm_count * sub_count

    def calculate_turns_needed(self, final_needed_coins: int, held_coins: int) -> Tuple[int, int]:
        turns = 0
        coins = held_coins
        while coins < final_needed_coins and turns < self.constants.MAX_TURNS:
            new_coins = coins * 2
            coins = min(new_coins + held_coins, self.constants.MAX_ALLOWED_FINAL_COINS)
            turns += 1
            if coins >= final_needed_coins:
                break
        return turns if coins >= final_needed_coins else float('inf'), coins

    def is_valid_ratio(self, tm_count: int, sub_count: int) -> bool:
        ratio = tm_count / sub_count if sub_count != 0 else float('inf')
        return 1/3 <= ratio <= 3

    def generate_optimal_strategies(self, held_coins: int) -> List[GameStrategy]:
        strategies = []
        max_count = int(math.sqrt(self.constants.MAX_ALLOWED_FINAL_COINS / self.constants.TRANSPARENT_MIRROR_INITIAL_VALUE))

        for tm_count in range(1, max_count + 1):
            for sub_count in range(1, max_count + 1):
                if not self.is_valid_ratio(tm_count, sub_count):
                    continue

                final_needed_coins, tm_cost, sub_cost = self.calculate_final_needed_coins(tm_count, sub_count)
                
                if final_needed_coins <= self.constants.MAX_ALLOWED_FINAL_COINS:
                    victory_points = self.calculate_victory_points(tm_count, sub_count)
                    
                    if self.constants.MIN_ACCEPTABLE_VICTORY_POINTS <= victory_points <= self.constants.MAX_ACCEPTABLE_VICTORY_POINTS:
                        turns_needed, coins_after_growth = self.calculate_turns_needed(final_needed_coins, held_coins)
                        if turns_needed <= self.constants.MAX_TURNS:
                            strategies.append(GameStrategy(tm_count, sub_count, held_coins, final_needed_coins, 
                                                           victory_points, turns_needed, coins_after_growth, tm_cost, sub_cost))

        return strategies

def main():
    constants = GameConstants()
    optimizer = JoinWarsOptimizer(constants)
    
    all_strategies = []

    for held_coins in constants.HELD_COINS_OPTIONS:
        strategies = optimizer.generate_optimal_strategies(held_coins)
        all_strategies.extend(strategies)

    # Group strategies by held_coins and turns_needed
    grouped_strategies = {}
    for strategy in all_strategies:
        key = (strategy.held_coins, strategy.turns_needed)
        if key not in grouped_strategies or strategy.victory_points > grouped_strategies[key].victory_points:
            grouped_strategies[key] = strategy

    # Sort strategies by held_coins and turns_needed
    sorted_strategies = sorted(grouped_strategies.values(), key=lambda s: (s.held_coins, s.turns_needed))

    # Prepare output
    output = "| Held Coins | Turns | VP | Final Coins | Growth Coins | TM | Sub | TM Cost | Sub Cost | JoinWars |\n"
    output += "|------------|-------|----|------------|--------------|----|-----|---------|----------|----------|\n"

    for strategy in sorted_strategies:
        output += f"| {strategy.held_coins:10d} | {strategy.turns_needed:5d} | {strategy.victory_points:3d} | "
        output += f"{strategy.final_needed_coins:10d} | {strategy.coins_after_growth:12d} | "
        output += f"{strategy.transparent_mirror_count:3d} | {strategy.subscribe_count:3d} | "
        output += f"{strategy.tm_cost:7d} | {strategy.sub_cost:8d} | {constants.JOINWARS_INITIAL_COST:8d} |\n"

    # Print to console
    print(output)

    # Write to file
    with open('joinwars_detailed_strategies.txt', 'w') as f:
        f.write(output)

if __name__ == "__main__":
    main()
    
    

import matplotlib.pyplot as plt

def calculate_growth_coins(initial_coins, max_turns):
    coins = [initial_coins]
    for _ in range(max_turns):
        new_coins = coins[-1] * 2
        total_coins = new_coins + initial_coins
        coins.append(min(total_coins, 1560031))  # 上限を1560031に設定
    return coins

def generate_growth_coin_chart(held_coins_options, max_turns):
    plt.figure(figsize=(12, 8))
    
    for held_coins in held_coins_options:
        growth_coins = calculate_growth_coins(held_coins, max_turns)
        plt.plot(range(max_turns + 1), growth_coins, marker='o', label=f'Initial: {held_coins}')
    
    plt.title('JoinWars Precise Growth Coin Chart')
    plt.xlabel('Turns')
    plt.ylabel('Coins')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')  # 対数スケールを使用
    plt.savefig('joinwars_precise_growth_coin_chart.png')
    plt.close()

def generate_growth_coin_text(held_coins_options, max_turns):
    output = "JoinWars Precise Growth Coin Table\n"
    output += "Turns | " + " | ".join([f"Initial: {coins}" for coins in held_coins_options]) + "\n"
    output += "-" * (7 + 11 * len(held_coins_options)) + "\n"

    for turn in range(max_turns + 1):
        output += f"{turn:5d} | "
        for held_coins in held_coins_options:
            growth_coins = calculate_growth_coins(held_coins, max_turns)
            output += f"{growth_coins[turn]:9d} | "
        output += "\n"

    return output

def main():
    held_coins_options = (0, 10,20,30,40,50,100, 200, 300)
    max_turns = 15

    # Generate and save chart
    generate_growth_coin_chart(held_coins_options, max_turns)
    print("JoinWars Precise Growth Coin Chart has been generated and saved as 'joinwars_precise_growth_coin_chart.png'")

    # Generate text output
    text_output = generate_growth_coin_text(held_coins_options, max_turns)

    # Print to console
    print("\n" + text_output)

    # Save to text file
    with open('joinwars_precise_growth_coin_table.txt', 'w') as f:
        f.write(text_output)
    print("JoinWars Precise Growth Coin Table has been saved as 'joinwars_precise_growth_coin_table.txt'")

if __name__ == "__main__":
    main()