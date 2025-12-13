"""
Gemini Client with Rate Limit Handling and Fallback
FIXED: Handles quota exceeded errors gracefully
Provides fallback analysis when Gemini is unavailable
"""

import os
import logging
import time
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class GeminiClientWithFallback:
    """
    Enhanced Gemini Client with rate limit handling and fallback analysis
    When Gemini quota is exceeded, provides rule-based analysis
    """

    def __init__(self):
        """Initialize Gemini Client with API credentials"""
        try:
            api_key = settings.GOOGLE_API_KEY
            
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set")
            
            # Configure Gemini API
            genai.configure(api_key=api_key)
            
            # Use stable model (gemini-2.5-flash-thinking-exp has better quota)
            # Or fallback to gemini-pro if flash is unavailable
            try:
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("✅ Gemini Client initialized with gemini-2.5-flash")
            except:
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("✅ Gemini Client initialized with gemini-pro (fallback)")
            
            self.rate_limit_retry_after = 0  # Timestamp when we can retry
            self.quota_exceeded = False
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini Client: {str(e)}")
            raise

    def generate_text(
        self, 
        prompt: str, 
        temperature: float = 0.7,
        use_fallback_on_error: bool = True
    ) -> str:
        """
        Generate text using Gemini AI with rate limit handling
        
        Args:
            prompt: Input prompt for the model
            temperature: Creativity level (0.0 to 1.0)
            use_fallback_on_error: If True, use rule-based fallback when Gemini fails
        
        Returns:
            Generated text response or fallback analysis
        """
        # Check if we're still in rate limit cooldown
        if self.quota_exceeded and time.time() < self.rate_limit_retry_after:
            remaining = int(self.rate_limit_retry_after - time.time())
            logger.warning(f"⚠️ Still in rate limit cooldown. {remaining}s remaining.")
            
            if use_fallback_on_error:
                return self._generate_fallback_analysis(prompt)
            else:
                return f"Rate limit exceeded. Please wait {remaining} seconds and try again."
        
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
            
            # Reset rate limit flags on success
            self.quota_exceeded = False
            self.rate_limit_retry_after = 0
            
            logger.info("✅ Text generation completed successfully")
            return response.text
        
        except google_exceptions.ResourceExhausted as e:
            # Rate limit exceeded - extract retry_after from error
            logger.error(f"❌ Gemini rate limit exceeded: {str(e)}")
            
            # Try to extract retry delay from error message
            retry_after = self._extract_retry_delay(str(e))
            self.rate_limit_retry_after = time.time() + retry_after
            self.quota_exceeded = True
            
            logger.warning(f"⚠️ Rate limit hit. Using fallback analysis. Retry in {retry_after}s")
            
            if use_fallback_on_error:
                return self._generate_fallback_analysis(prompt)
            else:
                return f"Error: Rate limit exceeded. Please wait {retry_after} seconds."
        
        except Exception as e:
            logger.error(f"❌ Failed to generate text: {str(e)}")
            
            if use_fallback_on_error:
                return self._generate_fallback_analysis(prompt)
            else:
                return f"Error generating response: {str(e)}"

    def _extract_retry_delay(self, error_message: str) -> int:
        """Extract retry delay from error message"""
        try:
            # Error message contains "Please retry in 54.283833036s"
            import re
            match = re.search(r'retry in (\d+(?:\.\d+)?)', error_message)
            if match:
                return int(float(match.group(1))) + 5  # Add 5s buffer
            return 60  # Default 60s
        except:
            return 60

    def _generate_fallback_analysis(self, prompt: str) -> str:
        """
        Generate rule-based analysis when Gemini is unavailable
        Provides basic but helpful recommendations
        """
        logger.info("🔄 Using fallback rule-based analysis")
        
        # Extract intent from prompt
        prompt_lower = prompt.lower()
        
        if "cost" in prompt_lower and "reduce" in prompt_lower:
            return self._fallback_cost_reduction()
        elif "security" in prompt_lower:
            return self._fallback_security_recommendations()
        elif "performance" in prompt_lower or "optimize" in prompt_lower:
            return self._fallback_performance_recommendations()
        else:
            return self._fallback_general_analysis()

    def _fallback_cost_reduction(self) -> str:
        """Fallback cost reduction recommendations"""
        return """
**Cost Reduction Recommendations (Rule-Based Analysis)**

⚠️ *Note: AI analysis temporarily unavailable due to rate limits. Showing rule-based recommendations.*

**Top 5 Cost Optimization Strategies:**

1. **Identify Idle Resources** (Potential 15-25% savings)
   - Review Compute instances with <5% CPU utilization for 7+ days
   - Stop or delete test/dev instances not in use
   - Action: Run `gcloud compute instances list` and check usage metrics

2. **Right-Size VM Instances** (Potential 10-20% savings)
   - Look for over-provisioned VMs using <30% of allocated resources
   - Downgrade machine types (e.g., n1-standard-4 → n1-standard-2)
   - Action: Review Cloud Monitoring dashboards for past 30 days

3. **Enable Committed Use Discounts** (Potential 30-40% savings)
   - For stable workloads, commit to 1-year or 3-year terms
   - Significant discounts on Compute Engine and GKE
   - Action: Billing → Committed Use Discounts

4. **Implement Storage Lifecycle Policies** (Potential 5-15% savings)
   - Move infrequently accessed data to Coldline/Archive storage
   - Delete old snapshots and backups
   - Action: Storage → Lifecycle Management

5. **Optimize Network Egress** (Potential 5-10% savings)
   - Use Cloud CDN to reduce egress costs
   - Keep traffic within same region when possible
   - Action: Review Network Intelligence Center

**Implementation Priority:**
- Week 1: Identify and stop idle resources (quick wins)
- Week 2-3: Right-size VMs and commit to CUDs
- Month 1-3: Optimize storage and network architecture

**Next Steps:**
1. Run cost analysis: `gcloud billing accounts list`
2. Review recommendations: GCP Console → Recommender
3. Set up budget alerts to monitor costs

*For AI-powered personalized analysis, please retry in a few minutes when rate limits reset.*
"""

    def _fallback_security_recommendations(self) -> str:
        """Fallback security recommendations"""
        return """
**Security Recommendations (Rule-Based Analysis)**

⚠️ *Note: AI analysis temporarily unavailable. Showing standard security checks.*

**Critical Security Actions:**

1. **Enable VPC Service Controls**
   - Protect sensitive data from unauthorized access
   - Create security perimeters around resources

2. **Implement Least Privilege IAM**
   - Review and remove excessive permissions
   - Use service accounts with minimal scopes

3. **Enable Cloud Armor**
   - DDoS protection for public-facing services
   - Web Application Firewall (WAF) rules

4. **Configure Security Command Center**
   - Continuous security monitoring
   - Vulnerability scanning and threat detection

5. **Enable Cloud Audit Logs**
   - Track all admin activity
   - Essential for compliance

**Check These Now:**
- Binary Authorization for GKE
- Encryption at rest and in transit
- VPC firewall rules review
- Secret Manager for credentials

*For detailed, personalized security analysis, please retry when rate limits reset.*
"""

    def _fallback_performance_recommendations(self) -> str:
        """Fallback performance recommendations"""
        return """
**Performance Optimization Recommendations (Rule-Based Analysis)**

⚠️ *Note: Showing standard performance best practices.*

**Quick Performance Wins:**

1. **Enable Cloud CDN**
   - Cache static content closer to users
   - Reduce latency by 50-80%

2. **Use Premium Network Tier**
   - Better performance and reliability
   - Lower latency for global traffic

3. **Implement Autoscaling**
   - Automatically adjust capacity
   - Handle traffic spikes efficiently

4. **Optimize Database Queries**
   - Add indexes for frequently accessed data
   - Use Cloud SQL query insights

5. **Use Cloud Load Balancing**
   - Distribute traffic across instances
   - Automatic health checks

*For AI-powered performance analysis, please retry when rate limits reset.*
"""

    def _fallback_general_analysis(self) -> str:
        """Fallback general infrastructure analysis"""
        return """
**Infrastructure Analysis (Rule-Based)**

⚠️ *Note: AI analysis temporarily unavailable. Showing general recommendations.*

**Standard GCP Best Practices:**

**Cost:**
- Review idle resources weekly
- Enable committed use discounts for stable workloads
- Set up budget alerts

**Security:**
- Enable Cloud Security Command Center
- Review IAM permissions monthly
- Use VPC Service Controls

**Reliability:**
- Implement multi-region redundancy
- Set up monitoring and alerting
- Regular disaster recovery tests

**Performance:**
- Use Cloud CDN for static content
- Enable autoscaling where applicable
- Optimize database queries

**Next Steps:**
1. Visit GCP Recommender for personalized suggestions
2. Review Security Command Center findings
3. Check Billing reports for cost anomalies

*For detailed AI-powered analysis tailored to your infrastructure, please retry in a few minutes.*
"""

    def analyze_infrastructure(self, infrastructure_data: Dict[str, Any]) -> str:
        """Analyze infrastructure with fallback support"""
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
        return self.generate_text(prompt, use_fallback_on_error=True)

    def verify_connection(self) -> bool:
        """Verify that Gemini API connection is working"""
        try:
            response = self.generate_text(
                "Hello, test connection", 
                use_fallback_on_error=False
            )
            is_valid = bool(response) and "Error" not in response
            
            if is_valid:
                logger.info("✅ Gemini API connection verified successfully")
            else:
                logger.warning("⚠️ Gemini API connection failed")
            
            return is_valid
        
        except Exception as e:
            logger.error(f"❌ Gemini API connection verification failed: {str(e)}")
            return False


# For testing
if __name__ == "__main__":
    import sys
    
    try:
        client = GeminiClientWithFallback()
        
        print("Testing Gemini Client with Fallback...")
        
        # Test 1: Normal query (may hit rate limit)
        response = client.generate_text(
            "What are the top 3 ways to reduce GCP costs?",
            use_fallback_on_error=True
        )
        print("\n📝 Response:")
        print(response)
        
        print("\n✅ Client is working (with fallback support)!")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)