"""
Gemini Client - Google Gemini AI API Integration
Handles AI model initialization and inference for infrastructure analysis
"""

import os
import logging
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class GeminiClient:
    """
    Client for interacting with Google Gemini AI API
    Provides methods for text generation and analysis using Gemini 2.5
    """

    def __init__(self):
        """
        Initialize Gemini Client with API credentials
        Uses GOOGLE_API_KEY from environment variables
        """
        try:
            # Get API key from settings
            api_key = settings.GOOGLE_API_KEY
            
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set")
            
            # Configure Gemini API
            genai.configure(api_key=api_key)
            
            # Initialize Gemini 2.5 Flash model
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            
            logger.info("Gemini Client initialized successfully with gemini-2.5-flash")
        
        except Exception as e:
            logger.error(f"Failed to initialize Gemini Client: {str(e)}")
            raise

    def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate text using Gemini AI
        
        Args:
            prompt: Input prompt for the model
            temperature: Creativity level (0.0 to 1.0)
        
        Returns:
            Generated text response
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                ),
            )
            
            logger.info("Text generation completed successfully")
            return response.text
        
        except Exception as e:
            logger.error(f"Failed to generate text: {str(e)}")
            return f"Error generating response: {str(e)}"

    def analyze_infrastructure(self, infrastructure_data: Dict[str, Any]) -> str:
        """
        Analyze infrastructure data using Gemini AI
        
        Args:
            infrastructure_data: Dictionary containing infrastructure details
        
        Returns:
            Analysis and recommendations
        """
        try:
            prompt = f"""
Analyze the following GCP infrastructure and provide recommendations:

{infrastructure_data}

Please provide:
1. Current state summary
2. Potential cost optimization opportunities
3. Security recommendations
4. Performance optimization suggestions
5. Implementation priority and estimated ROI

Format the response as a structured report.
"""
            
            return self.generate_text(prompt)
        
        except Exception as e:
            logger.error(f"Failed to analyze infrastructure: {str(e)}")
            return f"Error analyzing infrastructure: {str(e)}"

    def generate_optimization_suggestions(self, cost_data: Dict[str, Any]) -> str:
        """
        Generate cost optimization suggestions based on billing data
        
        Args:
            cost_data: Cost breakdown and resource utilization data
        
        Returns:
            Optimization suggestions
        """
        try:
            prompt = f"""
Based on the following GCP cost and resource data, provide 5 specific cost optimization suggestions:

{cost_data}

For each suggestion, provide:
- Action to take
- Expected monthly savings
- Implementation complexity (Low/Medium/High)
- Time to implement
- ROI timeline

Prioritize by impact and ease of implementation.
"""
            
            return self.generate_text(prompt, temperature=0.5)
        
        except Exception as e:
            logger.error(f"Failed to generate suggestions: {str(e)}")
            return f"Error generating suggestions: {str(e)}"

    def generate_security_recommendations(self, resources: List[Dict[str, Any]]) -> str:
        """
        Generate security recommendations for GCP resources
        
        Args:
            resources: List of GCP resources
        
        Returns:
            Security recommendations
        """
        try:
            prompt = f"""
Review the following GCP resources for security issues and provide recommendations:

{resources}

Identify:
1. Security misconfigurations
2. Best practice violations
3. Compliance risks
4. Access control issues
5. Data protection concerns

Provide actionable recommendations with severity levels (Critical/High/Medium/Low).
"""
            
            return self.generate_text(prompt, temperature=0.3)
        
        except Exception as e:
            logger.error(f"Failed to generate security recommendations: {str(e)}")
            return f"Error generating security recommendations: {str(e)}"

    def explain_recommendation(self, recommendation: str) -> str:
        """
        Provide detailed explanation for a recommendation
        
        Args:
            recommendation: The recommendation to explain
        
        Returns:
            Detailed explanation
        """
        try:
            prompt = f"""
Provide a detailed explanation for the following GCP optimization recommendation:

{recommendation}

Include:
1. Why this is important
2. Current impact/risk
3. Benefits of implementing
4. Implementation steps
5. Potential challenges
6. Success metrics
"""
            
            return self.generate_text(prompt)
        
        except Exception as e:
            logger.error(f"Failed to explain recommendation: {str(e)}")
            return f"Error explaining recommendation: {str(e)}"

    def generate_report(self, analysis_data: Dict[str, Any]) -> str:
        """
        Generate comprehensive infrastructure audit report
        
        Args:
            analysis_data: Complete analysis data including costs, metrics, recommendations
        
        Returns:
            Formatted audit report
        """
        try:
            prompt = f"""
Generate a professional infrastructure audit report based on the following analysis:

{analysis_data}

The report should include:
1. Executive Summary
2. Current Infrastructure Overview
3. Cost Analysis
   - Current spend breakdown
   - Trends and patterns
4. Key Findings
   - Top cost drivers
   - Inefficiencies identified
   - Risk areas
5. Recommendations
   - Quick wins (implement in <1 week)
   - Medium-term improvements (1-4 weeks)
   - Strategic initiatives (1-3 months)
6. Expected Impact
   - Cost savings estimate
   - Performance improvements
   - Risk reduction
7. Implementation Roadmap
8. Conclusion

Format as a professional report suitable for stakeholder presentation.
"""
            
            return self.generate_text(prompt, temperature=0.6)
        
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            return f"Error generating report: {str(e)}"

    def verify_connection(self) -> bool:
        """
        Verify that Gemini API connection is working
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = self.generate_text("Hello, test connection")
            is_valid = bool(response) and "Error" not in response
            
            if is_valid:
                logger.info("Gemini API connection verified successfully")
            else:
                logger.warning("Gemini API connection failed")
            
            return is_valid
        
        except Exception as e:
            logger.error(f"Gemini API connection verification failed: {str(e)}")
            return False


# For testing
if __name__ == "__main__":
    import sys
    
    try:
        client = GeminiClient()
        
        if client.verify_connection():
            print("✅ Gemini Client is ready!")
            print("✅ gemini-2.5-flash model loaded")
            print("✅ API connection verified")
        else:
            print("❌ Gemini API connection failed")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)