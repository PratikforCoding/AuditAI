"""
Cost Calculator - Infrastructure Cost Analysis & Projections
Calculates costs, trends, and ROI for infrastructure recommendations
"""


from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class CostBreakdown:
    """Cost breakdown data structure"""
    service: str
    cost: float
    percentage: float
    trend: str  # "up", "down", "stable"
    monthly_projection: float


@dataclass
class ROICalculation:
    """ROI calculation result"""
    recommendation_id: str
    monthly_savings: float
    annual_savings: float
    implementation_cost: float
    payback_months: float
    roi_percentage: float
    confidence: float


class CostCalculator:
    """
    Advanced cost calculation engine for infrastructure optimization.
    Calculates savings, ROI, projections, and cost trends.
    """
    
    def __init__(self):
        """Initialize cost calculator"""
        self.logger = logger
        
    # ========================================================================
    # Cost Analysis Methods
    # ========================================================================
    
    def calculate_cost_breakdown(
        self, 
        costs_by_service: List[Dict]
    ) -> List[CostBreakdown]:
        """
        Calculate cost breakdown with percentages and trends
        
        Args:
            costs_by_service: List of costs with service names
            
        Returns:
            List of CostBreakdown objects with analysis
        """
        try:
            total_cost = sum(item['total_cost'] for item in costs_by_service)
            
            if total_cost == 0:
                self.logger.warning("Total cost is zero")
                return []
            
            breakdowns = []
            for item in costs_by_service:
                service_name = item['service_name']
                cost = item['total_cost']
                percentage = (cost / total_cost) * 100
                
                # Determine trend (simple: compare to average)
                avg_cost = total_cost / len(costs_by_service)
                trend = "up" if cost > avg_cost * 1.1 else ("down" if cost < avg_cost * 0.9 else "stable")
                
                # Project to monthly
                monthly_projection = cost  # Already monthly from billing
                
                breakdown = CostBreakdown(
                    service=service_name,
                    cost=round(cost, 2),
                    percentage=round(percentage, 2),
                    trend=trend,
                    monthly_projection=round(monthly_projection, 2)
                )
                
                breakdowns.append(breakdown)
            
            # Sort by cost (highest first)
            breakdowns.sort(key=lambda x: x.cost, reverse=True)
            
            self.logger.info(f"Calculated breakdown for {len(breakdowns)} services")
            return breakdowns
        
        except Exception as e:
            self.logger.error(f"Error calculating cost breakdown: {e}")
            raise
    
    def calculate_monthly_projection(
        self,
        daily_costs: List[Dict],
        days: int = 30
    ) -> Dict[str, float]:
        """
        Project monthly cost from daily data
        
        Args:
            daily_costs: List of daily cost data
            days: Number of days in projection period
            
        Returns:
            {
                'current_month': float,
                'projected_month': float,
                'trend': str,
                'growth_rate': float
            }
        """
        try:
            if not daily_costs:
                return {
                    'current_month': 0.0,
                    'projected_month': 0.0,
                    'trend': 'stable',
                    'growth_rate': 0.0
                }
            
            # Get current and previous month totals
            current_month_cost = sum(item['cost'] for item in daily_costs)
            daily_average = current_month_cost / days if days > 0 else 0
            
            # Project for full month
            projected_month = daily_average * 30
            
            # Calculate growth rate (if we have trend data)
            growth_rate = 0.0
            if len(daily_costs) > 1:
                first_half = daily_costs[:len(daily_costs)//2]
                second_half = daily_costs[len(daily_costs)//2:]
                
                first_avg = sum(d['cost'] for d in first_half) / len(first_half) if first_half else 0
                second_avg = sum(d['cost'] for d in second_half) / len(second_half) if second_half else 0
                
                if first_avg > 0:
                    growth_rate = ((second_avg - first_avg) / first_avg) * 100
            
            # Determine trend
            if growth_rate > 5:
                trend = "up"
            elif growth_rate < -5:
                trend = "down"
            else:
                trend = "stable"
            
            result = {
                'current_month': round(current_month_cost, 2),
                'projected_month': round(projected_month, 2),
                'daily_average': round(daily_average, 2),
                'trend': trend,
                'growth_rate': round(growth_rate, 2),
                'projection_confidence': self._calculate_confidence(len(daily_costs))
            }
            
            self.logger.info(f"Monthly projection: ${result['projected_month']}/month (trend: {trend})")
            return result
        
        except Exception as e:
            self.logger.error(f"Error calculating monthly projection: {e}")
            raise
    
    def calculate_annual_projection(
        self,
        monthly_cost: float,
        growth_rate: float = 0.0
    ) -> Dict[str, float]:
        """
        Project annual cost with growth rate
        
        Args:
            monthly_cost: Current monthly cost in USD
            growth_rate: Monthly growth rate as percentage (e.g., 2.5 for 2.5% growth)
            
        Returns:
            {
                'annual_cost': float,
                'by_quarter': [float, float, float, float],
                'monthly_growth': float,
                'with_growth': float
            }
        """
        try:
            annual_cost = monthly_cost * 12
            
            # Calculate quarterly costs
            quarterly_costs = []
            running_cost = monthly_cost
            
            for quarter in range(4):
                quarter_cost = running_cost * 3
                quarterly_costs.append(round(quarter_cost, 2))
                
                # Apply growth for next quarter
                if growth_rate != 0:
                    growth_factor = (1 + (growth_rate / 100)) ** 3
                    running_cost = running_cost * growth_factor
            
            # Total with growth
            annual_with_growth = sum(quarterly_costs)
            
            result = {
                'annual_cost_no_growth': round(annual_cost, 2),
                'annual_cost_with_growth': round(annual_with_growth, 2),
                'monthly_average': round(monthly_cost, 2),
                'by_quarter': quarterly_costs,
                'monthly_growth_rate': growth_rate,
                'total_growth_dollars': round(annual_with_growth - annual_cost, 2)
            }
            
            self.logger.info(f"Annual projection: ${result['annual_cost_with_growth']} (with {growth_rate}% growth)")
            return result
        
        except Exception as e:
            self.logger.error(f"Error calculating annual projection: {e}")
            raise
    
    # ========================================================================
    # ROI & Savings Calculation Methods
    # ========================================================================
    
    def calculate_roi(
        self,
        recommendation_id: str,
        monthly_savings: float,
        implementation_cost: float = 0.0,
        confidence: float = 0.85
    ) -> ROICalculation:
        """
        Calculate ROI for a recommendation
        
        Args:
            recommendation_id: ID of the recommendation
            monthly_savings: Estimated monthly savings in USD
            implementation_cost: One-time implementation cost
            confidence: Confidence level (0-1)
            
        Returns:
            ROICalculation object with complete ROI metrics
        """
        try:
            annual_savings = monthly_savings * 12
            
            # Calculate payback period
            if monthly_savings > 0:
                payback_months = (implementation_cost / monthly_savings) if implementation_cost > 0 else 0
            else:
                payback_months = 0
            
            # Calculate ROI percentage
            if implementation_cost > 0:
                year_one_savings = annual_savings - implementation_cost
                roi_percentage = (year_one_savings / implementation_cost) * 100
            else:
                roi_percentage = 100.0  # 100% if no implementation cost
            
            roi = ROICalculation(
                recommendation_id=recommendation_id,
                monthly_savings=round(monthly_savings, 2),
                annual_savings=round(annual_savings, 2),
                implementation_cost=round(implementation_cost, 2),
                payback_months=round(payback_months, 1),
                roi_percentage=round(roi_percentage, 2),
                confidence=confidence
            )
            
            self.logger.info(
                f"ROI for {recommendation_id}: "
                f"${annual_savings}/year, "
                f"payback {payback_months} months, "
                f"ROI {roi_percentage}%"
            )
            
            return roi
        
        except Exception as e:
            self.logger.error(f"Error calculating ROI: {e}")
            raise
    
    def calculate_total_savings(
        self,
        recommendations: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate total savings from multiple recommendations
        
        Args:
            recommendations: List of recommendation dicts with savings
            
        Returns:
            {
                'monthly_total': float,
                'annual_total': float,
                'highest': float,
                'average': float,
                'confidence_weighted': float
            }
        """
        try:
            if not recommendations:
                return {
                    'monthly_total': 0.0,
                    'annual_total': 0.0,
                    'highest': 0.0,
                    'average': 0.0,
                    'confidence_weighted': 0.0
                }
            
            monthly_savings = []
            confidences = []
            
            for rec in recommendations:
                monthly = rec.get('monthly_savings', 0)
                confidence = rec.get('confidence', 0.85)
                
                monthly_savings.append(monthly)
                confidences.append(confidence)
            
            monthly_total = sum(monthly_savings)
            annual_total = monthly_total * 12
            
            # Weighted by confidence
            confidence_weighted = sum(
                s * c for s, c in zip(monthly_savings, confidences)
            )
            
            result = {
                'monthly_total': round(monthly_total, 2),
                'annual_total': round(annual_total, 2),
                'highest': round(max(monthly_savings), 2) if monthly_savings else 0.0,
                'average': round(monthly_total / len(monthly_savings), 2) if monthly_savings else 0.0,
                'confidence_weighted': round(confidence_weighted, 2),
                'recommendation_count': len(recommendations),
                'high_confidence_count': len([c for c in confidences if c >= 0.8])
            }
            
            self.logger.info(
                f"Total savings: ${result['monthly_total']}/month, "
                f"${result['annual_total']}/year from {result['recommendation_count']} recommendations"
            )
            
            return result
        
        except Exception as e:
            self.logger.error(f"Error calculating total savings: {e}")
            raise
    
    def calculate_payback_period(
        self,
        monthly_savings: float,
        upfront_cost: float,
        monthly_maintenance: float = 0.0
    ) -> float:
        """
        Calculate payback period in months
        
        Args:
            monthly_savings: Monthly savings amount
            upfront_cost: One-time upfront cost
            monthly_maintenance: Ongoing monthly cost
            
        Returns:
            Number of months to break even
        """
        try:
            if monthly_savings <= monthly_maintenance:
                self.logger.warning("Monthly savings not greater than maintenance costs")
                return float('inf')
            
            net_monthly_savings = monthly_savings - monthly_maintenance
            
            if net_monthly_savings <= 0:
                return float('inf')
            
            payback_months = upfront_cost / net_monthly_savings
            
            self.logger.info(f"Payback period: {payback_months:.1f} months")
            return round(payback_months, 1)
        
        except Exception as e:
            self.logger.error(f"Error calculating payback period: {e}")
            raise
    
    # ========================================================================
    # Trend Analysis Methods
    # ========================================================================
    
    def analyze_cost_trend(
        self,
        daily_costs: List[Dict],
        window_days: int = 7
    ) -> Dict[str, any]:
        """
        Analyze cost trends with moving average
        
        Args:
            daily_costs: List of daily costs with 'date' and 'cost'
            window_days: Moving average window
            
        Returns:
            {
                'trend': str,
                'trend_percentage': float,
                'moving_average': float,
                'forecast_30_days': float,
                'volatility': float
            }
        """
        try:
            if len(daily_costs) < window_days:
                self.logger.warning(f"Not enough data for {window_days}-day window")
                return {
                    'trend': 'insufficient_data',
                    'trend_percentage': 0.0,
                    'moving_average': 0.0,
                    'forecast_30_days': 0.0,
                    'volatility': 0.0
                }
            
            costs = [item['cost'] for item in daily_costs]
            
            # Calculate moving average
            moving_avg = []
            for i in range(len(costs) - window_days + 1):
                window = costs[i:i + window_days]
                moving_avg.append(sum(window) / window_days)
            
            # Determine trend
            if len(moving_avg) >= 2:
                first_avg = sum(moving_avg[:len(moving_avg)//2]) / (len(moving_avg)//2)
                last_avg = sum(moving_avg[len(moving_avg)//2:]) / (len(moving_avg) - len(moving_avg)//2)
                
                trend_percentage = ((last_avg - first_avg) / first_avg * 100) if first_avg > 0 else 0
                
                if trend_percentage > 5:
                    trend = "increasing"
                elif trend_percentage < -5:
                    trend = "decreasing"
                else:
                    trend = "stable"
            else:
                trend_percentage = 0.0
                trend = "unknown"
            
            # Calculate volatility (standard deviation)
            avg_cost = sum(costs) / len(costs) if costs else 0
            variance = sum((c - avg_cost) ** 2 for c in costs) / len(costs) if costs else 0
            volatility = (variance ** 0.5) / avg_cost * 100 if avg_cost > 0 else 0
            
            # Forecast 30 days
            current_avg = moving_avg[-1] if moving_avg else 0
            forecast_30 = current_avg * 30
            
            result = {
                'trend': trend,
                'trend_percentage': round(trend_percentage, 2),
                'moving_average': round(current_avg, 2),
                'forecast_30_days': round(forecast_30, 2),
                'volatility': round(volatility, 2),
                'confidence': self._calculate_confidence(len(daily_costs))
            }
            
            self.logger.info(f"Cost trend: {trend} ({trend_percentage:.1f}%)")
            return result
        
        except Exception as e:
            self.logger.error(f"Error analyzing cost trend: {e}")
            raise
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def _calculate_confidence(self, data_points: int) -> str:
        """
        Calculate confidence level based on data points
        
        Args:
            data_points: Number of data points available
            
        Returns:
            Confidence level: "low", "medium", or "high"
        """
        if data_points >= 30:
            return "high"
        elif data_points >= 14:
            return "medium"
        else:
            return "low"
    
    def prioritize_recommendations(
        self,
        recommendations: List[Dict]
    ) -> List[Dict]:
        """
        Prioritize recommendations by ROI and implementation difficulty
        
        Args:
            recommendations: List of recommendation dicts
            
        Returns:
            Sorted list prioritized by ROI (adjusted for difficulty)
        """
        try:
            scored_recs = []
            
            for rec in recommendations:
                monthly_savings = rec.get('monthly_savings', 0)
                difficulty_map = {'Easy': 3, 'Medium': 2, 'Hard': 1}
                difficulty = difficulty_map.get(rec.get('difficulty', 'Medium'), 2)
                confidence = rec.get('confidence', 0.85)
                
                # Score = (savings * difficulty * confidence) for prioritization
                score = monthly_savings * difficulty * confidence
                
                scored_recs.append({
                    **rec,
                    'priority_score': round(score, 2)
                })
            
            # Sort by priority score (highest first)
            scored_recs.sort(key=lambda x: x['priority_score'], reverse=True)
            
            self.logger.info(f"Prioritized {len(scored_recs)} recommendations")
            return scored_recs
        
        except Exception as e:
            self.logger.error(f"Error prioritizing recommendations: {e}")
            raise
    
    def estimate_implementation_time(
        self,
        difficulty: str,
        resource_count: int = 1
    ) -> Dict[str, int]:
        """
        Estimate implementation time based on difficulty
        
        Args:
            difficulty: Implementation difficulty (Easy/Medium/Hard)
            resource_count: Number of resources to modify
            
        Returns:
            {
                'hours': int,
                'business_days': int,
                'calendar_days': int
            }
        """
        try:
            time_estimates = {
                'Easy': {'hours': 1, 'per_resource': 0.5},
                'Medium': {'hours': 4, 'per_resource': 2},
                'Hard': {'hours': 16, 'per_resource': 8}
            }
            
            estimate = time_estimates.get(difficulty, time_estimates['Medium'])
            total_hours = estimate['hours'] + (estimate['per_resource'] * max(0, resource_count - 1))
            
            return {
                'hours': int(total_hours),
                'business_days': int((total_hours / 8) + 1),  # 8 hour workday + buffer
                'calendar_days': int((total_hours / 6) + 1)   # 6 hour work blocks
            }
        
        except Exception as e:
            self.logger.error(f"Error estimating implementation time: {e}")
            raise


# Usage examples:
# from backend.utils.cost_calculator import CostCalculator
#
# calculator = CostCalculator()
#
# # Calculate breakdown
# breakdown = calculator.calculate_cost_breakdown(costs_by_service)
#
# # Calculate ROI
# roi = calculator.calculate_roi(
#     recommendation_id="rec_123",
#     monthly_savings=500,
#     implementation_cost=2000
# )
#
# # Analyze trend
# trend = calculator.analyze_cost_trend(daily_costs)
#
# # Prioritize recommendations
# prioritized = calculator.prioritize_recommendations(recommendations)