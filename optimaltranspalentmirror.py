from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass(frozen=True)
class GameConstants:
    # Initial cost and growth rate for Transparent Mirror
    TRANSPARENT_MIRROR_INITIAL_VALUE: int = 7
    TRANSPARENT_MIRROR_DIFFERENCE: int = 2
    
    # Cost per Subscribe
    SUBSCRIBE_COST: int = 2
    
    # Initial cost for joining the game
    JOINWARS_INITIAL_COST: int = 36
    
    # Multiplier for calculating victory points
    VICTORY_POINT_MULTIPLIER: int = 6
    
    # Maximum allowed coins in the game
    MAX_ALLOWED_FINAL_COINS: int = 1560031
    
    # Range of acceptable victory points
    MIN_ACCEPTABLE_VICTORY_POINTS: int = 96
    MAX_ACCEPTABLE_VICTORY_POINTS: int = 486
    
    # Possible initial held coins values
    HELD_COINS_OPTIONS: Tuple[int, ...] = (10, 20, 30, 50)

@dataclass
class GameStrategy:
    transparent_mirror_count: int
    subscribe_count: int
    held_coins: int
    final_needed_coins: int
    victory_points: int
    turns_needed: int

class JoinWarsOptimizer:
    def __init__(self, constants: GameConstants):
        self.constants = constants

    def calculate_final_needed_coins(self, tm_count: int, sub_count: int) -> int:
        """
        Calculate the final number of coins needed for a given strategy.
        
        :param tm_count: Number of Transparent Mirrors
        :param sub_count: Number of Subscribes
        :return: Total coins needed
        """
        # Calculate cost for Transparent Mirrors
        tm_cost = tm_count * (self.constants.TRANSPARENT_MIRROR_INITIAL_VALUE * 2 + 
                             (tm_count - 1) * self.constants.TRANSPARENT_MIRROR_DIFFERENCE) // 2
        # Calculate cost for Subscribes
        sub_cost = self.constants.SUBSCRIBE_COST * sub_count
        # Return total cost including initial game cost
        return tm_cost + sub_cost + self.constants.JOINWARS_INITIAL_COST

    def calculate_victory_points(self, tm_count: int, sub_count: int) -> int:
        """
        Calculate the victory points for a given strategy.
        
        :param tm_count: Number of Transparent Mirrors
        :param sub_count: Number of Subscribes
        :return: Total victory points
        """
        return self.constants.VICTORY_POINT_MULTIPLIER * tm_count * sub_count

    def calculate_turns_needed(self, final_needed_coins: int, held_coins: int) -> int:
        """
        Calculate the number of turns needed to reach the final coin amount.
        
        :param final_needed_coins: The target number of coins
        :param held_coins: Initial number of coins held
        :return: Number of turns needed
        """
        turns = 0
        coins = held_coins
        while coins < final_needed_coins:
            coins = min(coins * 2, self.constants.MAX_ALLOWED_FINAL_COINS)
            turns += 1
            if coins >= final_needed_coins:
                break
        return turns

    def generate_balanced_strategies(self, held_coins: int) -> List[GameStrategy]:
        """
        Generate a list of balanced strategies for a given number of held coins.
        
        :param held_coins: Initial number of coins held
        :return: List of viable game strategies
        """
        strategies = []
        min_count = int(math.sqrt(self.constants.MIN_ACCEPTABLE_VICTORY_POINTS / self.constants.VICTORY_POINT_MULTIPLIER))
        max_count = int(math.sqrt(self.constants.MAX_ACCEPTABLE_VICTORY_POINTS / self.constants.VICTORY_POINT_MULTIPLIER))
        
        for base_count in range(min_count, max_count + 1): # この制約は無用かつ有害であり、制約なしにするか、最適アルゴリズムを別途作成するのが望ましい。
            # Generate strategies with balanced TM and Sub counts
            for tm_count, sub_count in [(base_count, base_count), (base_count + 1, base_count), (base_count, base_count + 1)]:
                victory_points = self.calculate_victory_points(tm_count, sub_count)
                if self.constants.MIN_ACCEPTABLE_VICTORY_POINTS <= victory_points <= self.constants.MAX_ACCEPTABLE_VICTORY_POINTS:
                    final_needed_coins = self.calculate_final_needed_coins(tm_count, sub_count)
                    
                    if final_needed_coins > self.constants.MAX_ALLOWED_FINAL_COINS:
                        continue
                    
                    turns_needed = self.calculate_turns_needed(final_needed_coins, held_coins)
                    strategies.append(GameStrategy(tm_count, sub_count, held_coins, final_needed_coins, victory_points, turns_needed))
        
        return strategies

def main():
    # Initialize game constants and optimizer
    constants = GameConstants()
    optimizer = JoinWarsOptimizer(constants)
    
    all_strategies = []

    # Generate strategies for each held coins option
    for held_coins in constants.HELD_COINS_OPTIONS:
        strategies = optimizer.generate_balanced_strategies(held_coins)
        all_strategies.extend(strategies)

    # Sort strategies based on held coins, turns needed, and victory points
    sorted_strategies = sorted(
        all_strategies,
        key=lambda s: (s.held_coins, s.turns_needed, s.victory_points)
    )

    # Print the header for the results table
    print("| Held Coins | Turns Needed | Actual VP | Transparent Mirror | Subscribe | Final Needed Coins |")
    print("|------------|--------------|-----------|---------------------|-----------|---------------------|")

    # Print each strategy in the sorted order
    for strategy in sorted_strategies:
        print(f"| {strategy.held_coins:10d} | {strategy.turns_needed:12d} | {strategy.victory_points:9d} | "
              f"{strategy.transparent_mirror_count:19d} | {strategy.subscribe_count:9d} | "
              f"{strategy.final_needed_coins:19d} |")

    print("|------------|--------------|-----------|---------------------|-----------|---------------------|")

if __name__ == "__main__":
    main()
