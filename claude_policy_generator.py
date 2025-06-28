import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
import time

class ClaudePolicyGenerator:
    """Enhanced policy generator using Claude's API for sophisticated policy generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('CLAUDE_API_KEY')
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-5-sonnet-20241022"
        
        if not self.api_key:
            raise ValueError("Claude API key is required. Set CLAUDE_API_KEY environment variable or pass api_key parameter.")
    
    def generate_policy(self, organization_name: str, industry: List[str], framework: List[str], 
                       organization_size: str = '', additional_requirements: str = '', countries: Optional[List[str]] = None) -> str:
        """Generate a comprehensive security policy using Claude"""
        
        if countries is None:
            countries = []
            
        # Build the prompt with country-specific considerations
        prompt = f"""Generate a comprehensive security policy for {organization_name} that addresses the following requirements:

**Organization Details:**
- Name: {organization_name}
- Industry: {', '.join(industry)}
- Compliance Frameworks: {', '.join(framework)}
- Organization Size: {organization_size}
- Operating Countries: {', '.join(countries) if countries else 'Not specified'}

**Additional Requirements:**
{additional_requirements if additional_requirements else 'None specified'}

**Country-Specific Considerations:**
"""
        
        # Add country-specific privacy law information
        if countries:
            country_laws = {
                'US': 'CCPA, CPRA, COPPA, HIPAA, GLBA, SOX',
                'EU': 'GDPR, ePrivacy Directive, NIS Directive',
                'CA': 'PIPEDA, CASL, Provincial Privacy Laws',
                'AU': 'Privacy Act 1988, Notifiable Data Breaches Scheme',
                'UK': 'UK GDPR, Data Protection Act 2018',
                'JP': 'APPI, Act on the Protection of Personal Information',
                'SG': 'PDPA, Personal Data Protection Act',
                'BR': 'LGPD, Lei Geral de Proteção de Dados',
                'IN': 'DPDP Act, Digital Personal Data Protection Act',
                'ZA': 'POPIA, Protection of Personal Information Act'
            }
            
            for country in countries:
                if country in country_laws:
                    prompt += f"- {country}: Must comply with {country_laws[country]}\n"
                else:
                    prompt += f"- {country}: Must comply with local privacy and data protection laws\n"
        else:
            prompt += "- No specific countries specified\n"
        
        prompt += f"""

**Requirements:**
1. Create a comprehensive security policy that addresses all selected frameworks: {', '.join(framework)}
2. Include industry-specific controls for: {', '.join(industry)}
3. Address data sovereignty and privacy law compliance for operating countries
4. Include data localization and cross-border transfer requirements
5. Provide clear roles and responsibilities
6. Include incident management procedures
7. Address compliance monitoring and audit requirements
8. Make the policy practical and implementable for {organization_size} organizations

**Format:**
- Use Markdown formatting
- Include clear section headers
- Provide specific, actionable controls
- Include compliance checklists where appropriate
- Address both technical and procedural aspects

Please generate a comprehensive, professional security policy that meets these requirements."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error generating policy with Claude: {e}")
            # Fallback to standard generator
            from policy_generator import SecurityPolicyGenerator
            standard_generator = SecurityPolicyGenerator()
            return standard_generator.generate_policy(
                organization_name=organization_name,
                industry=industry,
                framework=framework,
                organization_size=organization_size,
                additional_requirements=additional_requirements,
                countries=countries
            )
    
    def generate_controls(self, policy_content: str, framework: List[str], industry: List[str]) -> str:
        """Generate specific controls and implementation guidance based on the policy"""
        
        prompt = self._create_controls_prompt(policy_content, framework, industry)
        controls_content = self._call_claude_api(prompt)
        
        return controls_content
    
    def generate_implementation_guide(self, policy_content: str, controls_content: str, 
                                    organization_size: str) -> str:
        """Generate a practical implementation guide"""
        
        prompt = self._create_implementation_prompt(policy_content, controls_content, organization_size)
        implementation_guide = self._call_claude_api(prompt)
        
        return implementation_guide
    
    def _create_policy_prompt(self, organization_name: str, industry: List[str], 
                            framework: List[str], organization_size: str, 
                            additional_requirements: str) -> str:
        """Create a comprehensive prompt for policy generation"""
        
        frameworks_text = ", ".join(framework)
        industries_text = ", ".join(industry)
        
        prompt = f"""You are an expert cybersecurity consultant and policy writer. Generate a comprehensive, professional security policy document for {organization_name}.

ORGANIZATION DETAILS:
- Name: {organization_name}
- Industry: {industries_text}
- Compliance Framework(s): {frameworks_text}
- Organization Size: {organization_size}
- Additional Requirements: {additional_requirements}

REQUIREMENTS:
1. Create a complete security policy document in Markdown format
2. Structure it professionally with clear sections and subsections
3. Include all necessary components for {frameworks_text} compliance
4. Tailor the content specifically for {industries_text} industry requirements
5. Make it practical and implementable for {organization_size} organizations
6. Include specific controls, procedures, and responsibilities
7. Add industry-specific considerations and best practices
8. Include risk management, incident response, and compliance monitoring sections
9. Make it comprehensive but readable for both technical and non-technical stakeholders

DOCUMENT STRUCTURE:
- Executive Summary
- Policy Scope and Objectives
- Roles and Responsibilities
- Risk Management Framework
- Security Controls and Procedures
- Incident Management and Response
- Compliance and Monitoring
- Policy Maintenance and Review
- Appendices (if needed)

FORMAT:
- Use proper Markdown formatting
- Include headers, subheaders, bullet points, and numbered lists
- Add tables where appropriate
- Use bold and italic text for emphasis
- Include practical examples and checklists
- Make it ready for immediate use in an organization

Generate a complete, professional security policy document that can be immediately implemented by {organization_name}."""

        return prompt
    
    def _create_controls_prompt(self, policy_content: str, framework: List[str], 
                               industry: List[str]) -> str:
        """Create a prompt for generating specific controls"""
        
        frameworks_text = ", ".join(framework)
        industries_text = ", ".join(industry)
        
        prompt = f"""Based on the following security policy, generate a detailed controls implementation guide.

POLICY CONTEXT:
{policy_content[:2000]}... (truncated for brevity)

COMPLIANCE FRAMEWORKS: {frameworks_text}
INDUSTRIES: {industries_text}

REQUIREMENTS:
1. Generate specific, actionable security controls
2. Include technical implementation details
3. Provide configuration examples where applicable
4. Include monitoring and validation procedures
5. Add risk assessment criteria
6. Include compliance mapping to {frameworks_text}
7. Provide industry-specific controls for {industries_text}
8. Include both preventive and detective controls
9. Add metrics and KPIs for each control
10. Include testing and validation procedures

CONTROLS STRUCTURE:
- Access Control
- Data Protection
- Network Security
- Application Security
- Physical Security
- Incident Response
- Business Continuity
- Compliance Monitoring

For each control, provide:
- Control objective
- Implementation steps
- Configuration examples
- Monitoring procedures
- Testing methods
- Compliance evidence
- Risk level and impact

Generate a comprehensive controls implementation guide that can be used to operationalize the security policy."""

        return prompt
    
    def _create_implementation_prompt(self, policy_content: str, controls_content: str, 
                                    organization_size: str) -> str:
        """Create a prompt for generating implementation guidance"""
        
        prompt = f"""Create a practical implementation guide for deploying the security policy and controls.

POLICY SUMMARY:
{policy_content[:1000]}... (truncated)

CONTROLS SUMMARY:
{controls_content[:1000]}... (truncated)

ORGANIZATION SIZE: {organization_size}

REQUIREMENTS:
1. Create a step-by-step implementation roadmap
2. Include timeline and milestones
3. Provide resource requirements (people, tools, budget)
4. Include change management considerations
5. Add training and awareness programs
6. Include stakeholder engagement strategies
7. Provide risk mitigation during implementation
8. Include success metrics and KPIs
9. Add troubleshooting and support procedures
10. Include maintenance and continuous improvement plans

IMPLEMENTATION PHASES:
- Phase 1: Foundation and Planning
- Phase 2: Core Controls Implementation
- Phase 3: Advanced Controls and Monitoring
- Phase 4: Optimization and Continuous Improvement

For each phase, include:
- Objectives and deliverables
- Timeline and dependencies
- Resource requirements
- Risk considerations
- Success criteria
- Next steps

Generate a practical implementation guide that provides clear direction for deploying the security program."""

        return prompt
    
    def _call_claude_api(self, prompt: str) -> str:
        """Make API call to Claude"""
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result['content'][0]['text']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Claude API: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected response format from Claude API: {str(e)}")
    
    def generate_complete_security_package(self, organization_name: str, industry: List[str], 
                                         framework: List[str], organization_size: str = '', 
                                         additional_requirements: str = '') -> Dict[str, str | List[str]]:
        """Generate a complete security package including policy, controls, and implementation guide"""
        
        print("Generating security policy...")
        policy_content = self.generate_policy(
            organization_name, industry, framework, organization_size, additional_requirements
        )
        
        print("Generating security controls...")
        controls_content = self.generate_controls(policy_content, framework, industry)
        
        print("Generating implementation guide...")
        implementation_guide = self.generate_implementation_guide(
            policy_content, controls_content, organization_size
        )
        
        return {
            'policy': policy_content,
            'controls': controls_content,
            'implementation_guide': implementation_guide,
            'generated_at': datetime.now().isoformat(),
            'organization_name': organization_name,
            'framework': framework,
            'industry': industry
        } 