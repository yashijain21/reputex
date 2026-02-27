from reputex_engine import ReputeXEngine
import math

def test_module_1_total_points():
    T = 320
    R = 4.4
    points = ReputeXEngine.calculate_total_points(T, R)
    assert points == 1408

def test_module_2_target_simulation():
    T = 320
    R = 4.4
    D = 4.9
    x = ReputeXEngine.solve_for_additional_reviews(T, R, D)
    assert x == 1600

def test_module_3_time_prediction():
    T = 320
    A = 24
    V = T / A # 13.333
    x = 1600
    M = ReputeXEngine.predict_time(x, V)
    assert math.isclose(M, 120, rel_tol=1e-5)

def test_module_3_advanced_velocity():
    V = 13.3
    G = 20 / 13 # 1.538...
    V_new = ReputeXEngine.calculate_adjusted_velocity(V, G)
    assert math.isclose(V_new, 20.4615, rel_tol=1e-3)

def test_module_4_negative_impact():
    T = 320
    R = 4.4
    new_reviews = 10
    new_rating = 1
    new_avg = ReputeXEngine.simulate_negative_impact(T, R, new_reviews, new_rating)
    # (1408 + 10) / 330 = 1418 / 330 = 4.2969...
    assert math.isclose(new_avg, 4.2969, rel_tol=1e-4)

def test_module_5_manual_star_strategy():
    T = 320
    R = 4.4
    D = 4.9
    # Strategy: 80% 5, 15% 4, 5% 3
    dist = {5: 0.8, 4: 0.15, 3: 0.05}
    WSV = ReputeXEngine.calculate_weighted_star_value(dist)
    # 5*0.8 + 4*0.15 + 3*0.05 = 4.0 + 0.6 + 0.15 = 4.75
    assert WSV == 4.75
    
    # x = 320(4.9 - 4.4) / (4.75 - 4.9)
    # x = 320(0.5) / (-0.15) = 160 / -0.15 = -1066.6...
    # Since WSV < D, it's impossible to reach.
    x = ReputeXEngine.solve_for_additional_reviews(T, R, D, star_value=WSV)
    assert x == float('inf') 
    
    # Try reachable target
    D_reachable = 4.6
    # x = 320(4.6 - 4.4) / (4.75 - 4.6) = 320(0.2) / 0.15 = 64 / 0.15 = 426.66... -> 427
    x_reachable = ReputeXEngine.solve_for_additional_reviews(T, R, D_reachable, star_value=WSV)
    assert x_reachable == 427

def test_module_6_age_intelligence():
    # 5+ years -> age factor 2
    x = 100
    age_months = 72
    difficulty = ReputeXEngine.calculate_difficulty_score(x, age_months)
    assert difficulty == 200
