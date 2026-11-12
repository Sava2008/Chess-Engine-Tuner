from enum import Enum
from typing import Generator

SCALING_CONST: float = 0.0001
def get_sigmoid(x: int | float, k: float=SCALING_CONST) -> float:
    return 1 / (1 + 10 ** (-k * x / 400))


class GameResult(Enum):
    white_win = 1.0
    black_win = 0.0
    draw = 0.5
    
    def __sub__(self, second: int | float) -> None:
        return self.value - second
    
    
def get_mean_error(game_results: list[GameResult], pos_evals: list[int], k: float) -> float:
    """defines average evaluation error
    evals are measured in centipawns (100 cp = +1.00 eval advantage)"""
    squared_errors: float = 0.0
    pos_count: int = len(game_results)  # game results are parallel to game count
    for result, pos_eval in zip(game_results, pos_evals):
        squared_errors += (result - get_sigmoid(pos_eval, k)) ** 2
        
    return squared_errors / pos_count
   
   
def find_best_k(game_results: list[GameResult], pos_evals: list[int]) -> float:
    print("calculating best scaling constant...")
    texel_k_range: Generator[int] = (i * 0.001 for i in range(1, 2001))
    
    min_error: float
    current_k: float | None
    min_error, current_k = float("inf"), None
    
    for k in texel_k_range:
        current_error: float = get_mean_error(game_results, pos_evals, k)

        if current_error < min_error:
            min_error = current_error
            current_k = k
    return current_k


print(find_best_k([GameResult.draw, GameResult.white_win, GameResult.black_win], [-50, 500, -300]))