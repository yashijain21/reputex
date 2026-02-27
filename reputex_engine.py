import math

class ReputeXEngine:
    @staticmethod
    def calculate_total_points(total_reviews, average_rating):
        return total_reviews * average_rating

    @staticmethod
    def get_approximate_distribution(total_reviews):
        # Default healthcare ORM distribution model
        return {
            5: round(total_reviews * 0.70),
            4: round(total_reviews * 0.15),
            3: round(total_reviews * 0.07),
            2: round(total_reviews * 0.04),
            1: round(total_reviews * 0.04)
        }

    @staticmethod
    def solve_for_additional_reviews(total_reviews, current_rating, target_rating, star_value=5.0):
        if target_rating >= star_value:
            return float('inf')  # Impossible to reach or exceeds possible star value
        
        # Formula: x = T(D - R) / (WSV - D)
        # We use round to avoid floating point precision issues before ceiling
        x = total_reviews * (target_rating - current_rating) / (star_value - target_rating)
        return max(0, math.ceil(round(x, 10)))

    @staticmethod
    def predict_time(required_reviews, velocity):
        if velocity <= 0:
            return float('inf')
        return required_reviews / velocity

    @staticmethod
    def calculate_adjusted_velocity(base_velocity, growth_factor):
        return base_velocity * growth_factor

    @staticmethod
    def simulate_negative_impact(total_reviews, current_rating, new_reviews_count, new_reviews_rating):
        total_points = total_reviews * current_rating
        added_points = new_reviews_count * new_reviews_rating
        new_total_reviews = total_reviews + new_reviews_count
        new_rating = (total_points + added_points) / new_total_reviews
        return new_rating

    @staticmethod
    def calculate_weighted_star_value(distribution_percentages):
        # distribution_percentages: {5: 0.8, 4: 0.15, 3: 0.05, ...}
        wsv = sum(star * prob for star, prob in distribution_percentages.items())
        return wsv

    @staticmethod
    def get_age_factor(age_months):
        if age_months <= 12:
            return 1
        elif age_months <= 36:
            return 1.2
        elif age_months <= 60:
            return 1.5
        else:
            return 2

    @staticmethod
    def calculate_difficulty_score(required_reviews, age_months):
        return required_reviews * ReputeXEngine.get_age_factor(age_months)

    @staticmethod
    def get_strategy_recommendation(required_reviews, months_needed, target_rating):
        if months_needed > 24:
            return f"Moving to {target_rating} is a long-term goal. Consider a more practical intermediate target."
        elif months_needed > 12:
            return f"Achieving {target_rating} is achievable in 1-2 years with consistent effort."
        else:
            return f"Moving to {target_rating} is achievable in less than 12 months."
