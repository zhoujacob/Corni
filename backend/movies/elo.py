def expected_score(rating_a, rating_b) -> float:
    """Calculate the expected score of movie A against movie B using the Elo formula."""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def update_elo(rating_a, rating_b, score_a, k=32):
    """Update the Elo rating of movie A after a comparison against movie B.

    Args:
        rating_a (float): Current rating of movie A.
        rating_b (float): Current rating of movie B.
        score_a (float): Actual score of movie A (1 = win, 0.5 = draw, 0 = loss).
        k (int): K-factor determining the sensitivity of rating changes.

    Returns:
        (new_a, new_b): The updated ratings for A and B.
    """
    e_a = expected_score(rating_a, rating_b)
    e_b = 1 - e_a
    new_a = rating_a + k * (score_a - e_a)
    new_b = rating_b + k * ((1 - score_a) - e_b)

    return new_a, new_b