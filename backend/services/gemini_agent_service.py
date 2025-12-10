"""
Gemini Agent Service - Agentic AI for Infrastructure Analysis
Enables autonomous AI decision-making for GCP audits
"""

import json
import logging
from typing import Optional, Dict, Any, List
from google import genai
from backend.config.settings import settings
from backend.services.recommendation_engine import ProductionRecommendationEngine
from backend.services.gcp_billing_service import GCPBillingService
from backend.services.gcp_monitoring_service import GCPMonitoringService
from backend.services.gcp_recommender_service import GCPRecommenderService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiAgentService:
    """
    Agentic AI service using Google Gemini with tool use capabilities.
    Can autonomously analyze infrastructure and make recommendations.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.recommendation_engine = ProductionRecommendationEngine(project_id)
        self.billing_service = GCPBillingService(project_id)
        self.monitoring_service = GCPMonitoringService(project_id)
        self.recommender_service = GCPRecommenderService(project_id)
        
        # Define tools for Gemini to use
        self.tools = self._define_tools()

    def _define_tools(self) -> List[Dict[str, Any]]:
        """
        Define tools that Gemini can autonomously call.
        These are the "actions" the AI agent can take.
        """
        return [
            {
                "name": "get_cost_analysis",
                "description": "Get cost analysis for the project including breakdown by service and resource",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Number of days to analyze (default 30)",
                            "default": 30
                        }
                    }
                }
            },
            {
                "name": "get_resource_metrics",
                "description": "Get monitoring metrics for resources like CPU, memory, disk usage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "Type of resource (compute_instance, disk, etc)"
                        },
                        "metric_type": {
                            "type": "string",
                            "description": "Type of metric (cpu, memory, disk_utilization)"
                        }
                    }
                }
            },
            {
                "name": "get_recommendations",
                "description": "Get optimization recommendations from GCP Recommender API",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recommendation_type": {
                            "type": "string",
                            "description": "Type of recommendation (IDLE_RESOURCES, OVERSIZED_INSTANCES, etc)",
                            "enum": ["IDLE_RESOURCES", "OVERSIZED_INSTANCES", "STORAGE", "ALL"]
                        }
                    }
                }
            },
            {
                "name": "analyze_infrastructure",
                "description": "Comprehensive infrastructure analysis combining all data sources",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Number of days to analyze",
                            "default": 30
                        }
                    }
                }
            },
            {
                "name": "calculate_savings",
                "description": "Calculate potential cost savings from implementing recommendations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recommendation_id": {
                            "type": "string",
                            "description": "ID of the recommendation to calculate savings for"
                        }
                    }
                }
            }
        ]

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a tool call made by Gemini AI.
        Returns JSON string result.
        """
        try:
            logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
            
            if tool_name == "get_cost_analysis":
                days = tool_input.get("days", 30)
                result = self.billing_service.get_cost_by_service(days=days)
                return json.dumps({
                    "status": "success",
                    "data": result,
                    "tool": tool_name
                })
            
            elif tool_name == "get_resource_metrics":
                resource_type = tool_input.get("resource_type")
                metric_type = tool_input.get("metric_type", "cpu")
                
                if metric_type == "cpu":
                    result = self.monitoring_service.get_compute_instance_metrics()
                elif metric_type == "disk":
                    result = self.monitoring_service.get_disk_utilization()
                elif metric_type == "network":
                    result = self.monitoring_service.get_network_traffic()
                else:
                    result = self.monitoring_service.get_compute_instance_metrics()
                
                return json.dumps({
                    "status": "success",
                    "data": result,
                    "tool": tool_name,
                    "metric_type": metric_type
                })
            
            elif tool_name == "get_recommendations":
                rec_type = tool_input.get("recommendation_type", "ALL")
                
                if rec_type == "IDLE_RESOURCES":
                    result = self.recommender_service.get_idle_resource_recommendations()
                elif rec_type == "OVERSIZED_INSTANCES":
                    result = self.recommender_service.get_oversized_instance_recommendations()
                elif rec_type == "STORAGE":
                    result = self.recommender_service.get_storage_recommendations()
                else:
                    result = self.recommender_service.get_all_recommendations()
                
                return json.dumps({
                    "status": "success",
                    "data": result,
                    "tool": tool_name,
                    "recommendation_type": rec_type
                })
            
            elif tool_name == "analyze_infrastructure":
                days = tool_input.get("days", 30)
                result = self.recommendation_engine.analyze_infrastructure(
                    project_id=self.project_id,
                    days=days
                )
                return json.dumps({
                    "status": "success",
                    "data": result,
                    "tool": tool_name
                })
            
            elif tool_name == "calculate_savings":
                rec_id = tool_input.get("recommendation_id")
                # Calculate savings based on recommendation
                result = {
                    "recommendation_id": rec_id,
                    "potential_savings": "$500-1000/month",
                    "implementation_effort": "Low",
                    "roi_months": 1
                }
                return json.dumps({
                    "status": "success",
                    "data": result,
                    "tool": tool_name
                })
            
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Unknown tool: {tool_name}"
                })
        
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            return json.dumps({
                "status": "error",
                "message": str(e),
                "tool": tool_name
            })

    def analyze_infrastructure_interactively(
        self, 
        query: str, 
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze infrastructure using Gemini AI with tool use.
        The AI can autonomously call tools to answer the query.
        
        Args:
            query: User's question about infrastructure
            days: Number of days to analyze
        
        Returns:
            Analysis result with AI insights and recommendations
        """
        try:
            logger.info(f"Starting interactive analysis for query: {query}")
            
            # Prepare system prompt
            system_prompt = f"""
You are an expert GCP infrastructure auditor and cost optimization specialist.
You have access to tools to analyze the infrastructure of project '{self.project_id}'.

Your goals:
1. Understand the user's question about their infrastructure
2. Use available tools to gather relevant data
3. Analyze the data to provide actionable insights
4. Suggest cost optimization opportunities
5. Calculate potential savings

When answering:
- Be specific with numbers and metrics
- Prioritize recommendations by ROI
- Explain why each recommendation is important
- Provide implementation steps when relevant

Available tools:
- get_cost_analysis: Get cost breakdown by service
- get_resource_metrics: Get resource utilization metrics
- get_recommendations: Get GCP Recommender suggestions
- analyze_infrastructure: Run full infrastructure analysis
- calculate_savings: Calculate potential cost savings

Use tools strategically to answer the user's question completely.
"""

            messages = [
                {
                    "role": "user",
                    "content": f"""Please analyze my GCP infrastructure and help me with this:

{query}

Analyze the infrastructure for the last {days} days and provide detailed insights."""
                }
            ]
            
            # First API call to Gemini
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=messages,
                tools=self.tools,
                system_prompt=system_prompt,
            )
            
            # Process tool use loop
            tool_results = []
            while response.candidates[0].content.parts:
                # Check if there are tool calls
                has_tool_calls = any(
                    hasattr(part, 'function_call') 
                    for part in response.candidates[0].content.parts
                )
                
                if not has_tool_calls:
                    break
                
                # Process each part
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        tool_call = part.function_call
                        tool_name = tool_call.name
                        tool_input = dict(tool_call.args)
                        
                        logger.info(f"AI called tool: {tool_name}")
                        
                        # Execute the tool
                        tool_result = self._execute_tool(tool_name, tool_input)
                        tool_results.append({
                            "tool": tool_name,
                            "input": tool_input,
                            "result": json.loads(tool_result)
                        })
                        
                        # Add tool result to messages for next API call
                        messages.append({
                            "role": "model",
                            "content": response.candidates[0].content
                        })
                        
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_name,
                                    "result": tool_result
                                }
                            ]
                        })
                
                # Make another API call to continue the conversation
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=messages,
                    tools=self.tools,
                    system_prompt=system_prompt,
                )
            
            # Extract final response
            final_response = ""
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text'):
                    final_response = part.text
                    break
            
            return {
                "status": "success",
                "query": query,
                "analysis": final_response,
                "tool_calls": tool_results,
                "project_id": self.project_id,
                "days_analyzed": days
            }
        
        except Exception as e:
            logger.error(f"Interactive analysis failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "query": query
            }

    def get_optimization_suggestions(self) -> Dict[str, Any]:
        """
        Get AI-powered optimization suggestions without user query.
        Uses all available tools to generate suggestions.
        """
        try:
            logger.info("Generating optimization suggestions")
            
            # Get all relevant data
            cost_data = self.billing_service.get_cost_by_service(days=30)
            recommendations = self.recommender_service.get_all_recommendations()
            metrics = self.monitoring_service.get_compute_instance_metrics()
            
            # Ask AI to generate suggestions based on data
            prompt = f"""
Based on the following infrastructure analysis, provide 5 specific optimization suggestions
that could reduce costs by 30-50%:

Cost Analysis (Last 30 days):
{json.dumps(cost_data, indent=2)}

GCP Recommendations:
{json.dumps(recommendations, indent=2)}

Resource Metrics:
{json.dumps(metrics, indent=2)}

For each suggestion:
1. What to change
2. Why it saves money
3. How much it can save
4. Implementation difficulty (Easy/Medium/Hard)
5. Estimated implementation time
"""
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            
            suggestions_text = response.text
            
            return {
                "status": "success",
                "suggestions": suggestions_text,
                "project_id": self.project_id,
                "data_sources": ["billing", "recommender", "monitoring"]
            }
        
        except Exception as e:
            logger.error(f"Failed to generate suggestions: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    def generate_audit_report(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate comprehensive audit report using AI analysis.
        """
        try:
            logger.info(f"Generating audit report for {days} days")
            
            # Get comprehensive analysis
            analysis_result = self.recommendation_engine.analyze_infrastructure(
                project_id=self.project_id,
                days=days
            )
            
            # Ask AI to generate report
            prompt = f"""
Generate a professional infrastructure audit report based on this analysis:

{json.dumps(analysis_result, indent=2)}

Include:
1. Executive Summary
2. Key Findings
3. Cost Breakdown
4. Top 5 Recommendations with ROI
5. Risk Assessment
6. Implementation Timeline
7. Expected Cost Savings
"""
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            
            report_text = response.text
            
            return {
                "status": "success",
                "report": report_text,
                "project_id": self.project_id,
                "days_analyzed": days,
                "generated_at": str(__import__('datetime').datetime.now())
            }
        
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
