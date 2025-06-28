import json
from datetime import datetime
from typing import Dict, List, Optional

class SecurityPolicyGenerator:
    """Generates security policies based on compliance frameworks and industry requirements"""
    
    def __init__(self):
        self.frameworks = {
            'iso27001': {
                'name': 'ISO 27001',
                'description': 'Information Security Management System',
                'controls': [
                    'Information Security Policies',
                    'Organization of Information Security',
                    'Human Resource Security',
                    'Asset Management',
                    'Access Control',
                    'Cryptography',
                    'Physical and Environmental Security',
                    'Operations Security',
                    'Communications Security',
                    'System Acquisition, Development and Maintenance',
                    'Supplier Relationships',
                    'Information Security Incident Management',
                    'Information Security Aspects of Business Continuity Management',
                    'Compliance'
                ]
            },
            'iso42001': {
                'name': 'ISO 42001',
                'description': 'AI Management System',
                'controls': [
                    'AI Governance and Leadership',
                    'AI Risk Management',
                    'AI Policy and Objectives',
                    'AI System Development and Deployment',
                    'AI Data Management',
                    'AI Model Management',
                    'AI System Operations',
                    'AI Performance Monitoring',
                    'AI Incident Management',
                    'AI Compliance and Ethics',
                    'AI Human Resources',
                    'AI Supplier Management',
                    'AI Internal Audit',
                    'AI Management Review'
                ]
            },
            'nist_ai_rmf': {
                'name': 'NIST AI RMF',
                'description': 'NIST Artificial Intelligence Risk Management Framework',
                'controls': [
                    'Governance',
                    'Map',
                    'Measure',
                    'Manage',
                    'AI System Inventory and Documentation',
                    'AI Risk Assessment and Categorization',
                    'AI System Monitoring and Evaluation',
                    'AI Incident Response and Recovery',
                    'AI System Testing and Validation',
                    'AI Bias and Fairness Management',
                    'AI Transparency and Explainability',
                    'AI Data Quality and Integrity',
                    'AI Model Security and Privacy',
                    'AI System Lifecycle Management'
                ]
            },
            'nist_sp_800_53': {
                'name': 'NIST SP 800-53',
                'description': 'NIST Special Publication 800-53 - Security and Privacy Controls',
                'controls': [
                    'Access Control (AC)',
                    'Awareness and Training (AT)',
                    'Audit and Accountability (AU)',
                    'Assessment, Authorization, and Monitoring (CA)',
                    'Configuration Management (CM)',
                    'Contingency Planning (CP)',
                    'Identification and Authentication (IA)',
                    'Incident Response (IR)',
                    'Maintenance (MA)',
                    'Media Protection (MP)',
                    'Physical and Environmental Protection (PE)',
                    'Planning (PL)',
                    'Program Management (PM)',
                    'Personnel Security (PS)',
                    'Personal Data Processing and Privacy (PDP)',
                    'Risk Assessment (RA)',
                    'System and Communications Protection (SC)',
                    'System and Information Integrity (SI)',
                    'Supply Chain Risk Management (SR)'
                ]
            },
            'fedramp': {
                'name': 'FedRAMP',
                'description': 'Federal Risk and Authorization Management Program',
                'controls': [
                    'Access Control',
                    'Awareness and Training',
                    'Audit and Accountability',
                    'Assessment, Authorization, and Monitoring',
                    'Configuration Management',
                    'Contingency Planning',
                    'Identification and Authentication',
                    'Incident Response',
                    'Maintenance',
                    'Media Protection',
                    'Physical and Environmental Protection',
                    'Planning',
                    'Program Management',
                    'Personnel Security',
                    'Risk Assessment',
                    'System and Communications Protection',
                    'System and Information Integrity',
                    'Supply Chain Risk Management'
                ]
            },
            'cis': {
                'name': 'CIS Controls',
                'description': 'Center for Internet Security Critical Security Controls',
                'controls': [
                    'Inventory and Control of Enterprise Assets',
                    'Inventory and Control of Software Assets',
                    'Data Protection',
                    'Secure Configuration of Enterprise Assets and Software',
                    'Account Management',
                    'Access Control Management',
                    'Continuous Vulnerability Management',
                    'Audit Log Management',
                    'Email and Web Browser Protections',
                    'Malware Defenses',
                    'Data Recovery',
                    'Network Infrastructure Management',
                    'Network Monitoring and Defense',
                    'Security Awareness and Skills Training',
                    'Service Provider Management',
                    'Application Software Security',
                    'Incident Response Management',
                    'Penetration Testing'
                ]
            },
            'pci': {
                'name': 'PCI DSS',
                'description': 'Payment Card Industry Data Security Standard',
                'controls': [
                    'Build and Maintain a Secure Network and Systems',
                    'Protect Cardholder Data',
                    'Maintain a Vulnerability Management Program',
                    'Implement Strong Access Control Measures',
                    'Regularly Monitor and Test Networks',
                    'Maintain an Information Security Policy'
                ]
            },
            'soc2': {
                'name': 'SOC 2',
                'description': 'Service Organization Control 2',
                'controls': [
                    'Security',
                    'Availability',
                    'Processing Integrity',
                    'Confidentiality',
                    'Privacy'
                ]
            },
            'gdpr': {
                'name': 'GDPR',
                'description': 'General Data Protection Regulation',
                'controls': [
                    'Data Protection Principles',
                    'Lawful Basis for Processing',
                    'Data Subject Rights',
                    'Data Protection Impact Assessment',
                    'Data Breach Notification',
                    'Data Protection Officer',
                    'Cross-border Data Transfers',
                    'Accountability and Governance'
                ]
            },
            'nist_csf': {
                'name': 'NIST CSF',
                'description': 'NIST Cybersecurity Framework',
                'controls': [
                    'Identify',
                    'Protect',
                    'Detect',
                    'Respond',
                    'Recover',
                    'Asset Management',
                    'Business Environment',
                    'Governance',
                    'Risk Assessment',
                    'Risk Management Strategy',
                    'Supply Chain Risk Management',
                    'Identity Management and Access Control',
                    'Awareness and Training',
                    'Data Security',
                    'Information Protection Processes and Procedures',
                    'Maintenance',
                    'Protective Technology',
                    'Anomalies and Events',
                    'Security Continuous Monitoring',
                    'Detection Processes',
                    'Response Planning',
                    'Communications',
                    'Analysis',
                    'Mitigation',
                    'Improvements',
                    'Recovery Planning',
                    'Improvements',
                    'Communications'
                ]
            },
            'hitrust': {
                'name': 'HITRUST CSF',
                'description': 'HITRUST Common Security Framework',
                'controls': [
                    'Information Protection Program',
                    'Access Control',
                    'Human Resources Security',
                    'Risk Management',
                    'Security Policy',
                    'Organization of Information Security',
                    'Asset Management',
                    'Communications and Operations Management',
                    'Information Systems Acquisition, Development and Maintenance',
                    'Information Security Incident Management',
                    'Business Continuity Management',
                    'Compliance',
                    'Privacy Practices',
                    'Data Protection and Privacy',
                    'Technical Access Control',
                    'Physical Access Control',
                    'Security Awareness and Training',
                    'Configuration Management',
                    'Vulnerability Management',
                    'Network Protection',
                    'Transmission Protection',
                    'Password Management',
                    'Mobile Device Security',
                    'Secure Software Development',
                    'Data Backup and Recovery',
                    'Audit Logging and Monitoring',
                    'Third-party Security',
                    'Incident Response',
                    'Business Continuity',
                    'Privacy by Design'
                ]
            },
            'owasp': {
                'name': 'OWASP',
                'description': 'Open Web Application Security Project - Application Security Framework',
                'controls': [
                    'Injection Prevention',
                    'Broken Authentication',
                    'Sensitive Data Exposure',
                    'XML External Entities (XXE)',
                    'Broken Access Control',
                    'Security Misconfiguration',
                    'Cross-Site Scripting (XSS)',
                    'Insecure Deserialization',
                    'Using Components with Known Vulnerabilities',
                    'Insufficient Logging & Monitoring',
                    'Server-Side Request Forgery (SSRF)',
                    'Software and Data Integrity Failures',
                    'Security Logging Failures',
                    'Vulnerable and Outdated Components',
                    'Identification and Authentication Failures',
                    'Software and Data Integrity Failures',
                    'Security Headers',
                    'Input Validation',
                    'Output Encoding',
                    'Session Management'
                ]
            },
            'itil': {
                'name': 'ITIL',
                'description': 'Information Technology Infrastructure Library - IT Service Management',
                'controls': [
                    'Service Strategy',
                    'Service Design',
                    'Service Transition',
                    'Service Operation',
                    'Continual Service Improvement',
                    'Change Management',
                    'Incident Management',
                    'Problem Management',
                    'Release Management',
                    'Configuration Management',
                    'Service Level Management',
                    'Capacity Management',
                    'Availability Management',
                    'IT Service Continuity Management',
                    'Information Security Management',
                    'Supplier Management',
                    'Financial Management',
                    'Knowledge Management',
                    'Service Catalog Management',
                    'Request Fulfillment'
                ]
            },
            'csa': {
                'name': 'CSA',
                'description': 'Cloud Security Alliance - Cloud Security Framework',
                'controls': [
                    'Cloud Architecture',
                    'Identity and Access Management',
                    'Data Security and Privacy',
                    'Application Security',
                    'Infrastructure Security',
                    'Virtualization Security',
                    'Compliance and Audit',
                    'Incident Response',
                    'Business Continuity',
                    'Risk Management',
                    'Governance and Enterprise Risk Management',
                    'Legal and Electronic Discovery',
                    'Compliance and Audit Management',
                    'Information Management and Data Security',
                    'Interoperability and Portability',
                    'Traditional Security, Business Continuity, and Disaster Recovery',
                    'Data Center Operations',
                    'Incident Response, Notification, and Remediation',
                    'Application Security',
                    'Encryption and Key Management',
                    'Identity, Entitlement, and Access Management',
                    'Virtualization',
                    'Security as a Service'
                ]
            }
        }
        
        self.industry_requirements = {
            'Technology/Software': {
                'specific_controls': [
                    'Software Development Lifecycle Security',
                    'API Security',
                    'Cloud Security',
                    'DevOps Security',
                    'Third-party Component Management'
                ],
                'risks': [
                    'Code vulnerabilities',
                    'API abuse',
                    'Cloud misconfiguration',
                    'Supply chain attacks'
                ]
            },
            'Healthcare': {
                'specific_controls': [
                    'HIPAA Compliance',
                    'Patient Data Protection',
                    'Medical Device Security',
                    'Clinical System Security',
                    'Healthcare IoT Security'
                ],
                'risks': [
                    'Patient data breaches',
                    'Medical device vulnerabilities',
                    'Ransomware attacks',
                    'Compliance violations'
                ]
            },
            'Financial Services': {
                'specific_controls': [
                    'Financial Data Protection',
                    'Transaction Security',
                    'Regulatory Compliance',
                    'Fraud Detection',
                    'Anti-money Laundering'
                ],
                'risks': [
                    'Financial fraud',
                    'Regulatory penalties',
                    'Customer data breaches',
                    'System downtime'
                ]
            },
            'Manufacturing': {
                'specific_controls': [
                    'Industrial Control System Security',
                    'Supply Chain Security',
                    'Intellectual Property Protection',
                    'Operational Technology Security',
                    'Quality Management System Security'
                ],
                'risks': [
                    'Industrial espionage',
                    'Production disruption',
                    'Intellectual property theft',
                    'Safety incidents'
                ]
            },
            'Retail/E-commerce': {
                'specific_controls': [
                    'Payment Card Security',
                    'Customer Data Protection',
                    'E-commerce Platform Security',
                    'Inventory System Security',
                    'Point of Sale Security'
                ],
                'risks': [
                    'Payment card fraud',
                    'Customer data breaches',
                    'E-commerce attacks',
                    'Inventory theft'
                ]
            }
        }
    
    def generate_policy(self, organization_name: str, industry: List[str], framework: List[str], 
                       organization_size: str = '', additional_requirements: str = '', countries: Optional[List[str]] = None) -> str:
        """Generate a comprehensive security policy"""
        
        if countries is None:
            countries = []
            
        # Validate frameworks
        for fw in framework:
            if fw not in self.frameworks:
                raise ValueError(f"Unsupported framework: {fw}")
        
        # Get framework information for all selected frameworks
        framework_infos = [self.frameworks[fw] for fw in framework]
        
        # Get industry information for all selected industries
        industry_infos = {}
        for ind in industry:
            if ind in self.industry_requirements:
                industry_infos[ind] = self.industry_requirements[ind]
        
        # Generate policy content
        policy_content = self._generate_policy_header(organization_name, framework_infos, countries)
        policy_content += self._generate_executive_summary(organization_name, framework_infos, industry, countries)
        policy_content += self._generate_scope_and_objectives(framework_infos, industry, countries)
        policy_content += self._generate_roles_and_responsibilities(organization_size)
        policy_content += self._generate_risk_management(industry_infos)
        policy_content += self._generate_controls_section(framework_infos, industry_infos)
        policy_content += self._generate_data_sovereignty_section(countries)
        policy_content += self._generate_incident_management()
        policy_content += self._generate_compliance_and_monitoring(framework_infos, countries)
        policy_content += self._generate_additional_requirements(additional_requirements)
        policy_content += self._generate_policy_maintenance()
        
        return policy_content
    
    def _generate_policy_header(self, organization_name: str, framework_infos: List[Dict], countries: List[str]) -> str:
        """Generate the policy header section"""
        frameworks = ", ".join([fw['name'] for fw in framework_infos])
        return f"""# {organization_name} Security Policy
## Based on {frameworks}

**Document Version:** 1.0  
**Effective Date:** {datetime.now().strftime('%B %d, %Y')}  
**Last Reviewed:** {datetime.now().strftime('%B %d, %Y')}  
**Next Review Date:** {datetime.now().strftime('%B %d, %Y')}  
**Document Owner:** Chief Information Security Officer (CISO)  
**Approved By:** Executive Management

---

"""
    
    def _generate_executive_summary(self, organization_name: str, framework_infos: List[Dict], industry: List[str], countries: List[str]) -> str:
        """Generate the executive summary section"""
        frameworks = ", ".join([fw['name'] for fw in framework_infos])
        industries = ", ".join(industry)
        return f"""## Executive Summary

This security policy document establishes the framework for {organization_name}'s information security management system, aligned with {frameworks} standards. The policy is designed to protect the organization's information assets, ensure business continuity, and maintain stakeholder trust.

### Key Objectives:
- Protect the confidentiality, integrity, and availability of information assets
- Ensure compliance with {frameworks} requirements
- Establish clear roles and responsibilities for information security
- Implement risk-based security controls appropriate for {industries} industries
- Foster a culture of security awareness and continuous improvement

### Scope:
This policy applies to all employees, contractors, vendors, and third-party service providers who have access to {organization_name}'s information systems, data, or facilities.

### Country-Specific Considerations
- {", ".join([f"**{country}**: {self.industry_requirements[country]['description']}" for country in countries])}

---

"""
    
    def _generate_scope_and_objectives(self, framework_infos: List[Dict], industry: List[str], countries: List[str]) -> str:
        """Generate the scope and objectives section"""
        frameworks = ", ".join([fw['name'] for fw in framework_infos])
        industries = ", ".join(industry)
        
        # Generate industry-specific scope details
        industry_scope_details = self._generate_industry_scope_details(industry, countries)
        
        return f"""## Scope and Objectives

### Policy Scope
This security policy covers all aspects of information security within {frameworks} framework, including:

- Information assets and systems
- Physical and environmental security
- Human resource security
- Access control and authentication
- Incident management and response
- Business continuity and disaster recovery
- Compliance and audit requirements

### Policy Objectives
1. **Protection of Information Assets**: Ensure the confidentiality, integrity, and availability of all information assets
2. **Risk Management**: Implement a systematic approach to identify, assess, and mitigate security risks
3. **Compliance**: Maintain compliance with {frameworks} requirements and industry regulations
4. **Continuous Improvement**: Establish processes for ongoing policy review and enhancement
5. **Awareness and Training**: Promote security awareness and provide regular training to all personnel

### Industry-Specific Scope
This policy is tailored to address the unique security requirements of the following industries:

{industry_scope_details}

### Country-Specific Considerations
- {", ".join([f"**{country}**: {self.industry_requirements[country]['description']}" for country in countries])}

---
"""
    
    def _generate_industry_scope_details(self, industries: List[str], countries: List[str]) -> str:
        """Generate detailed industry-specific scope information"""
        industry_details = {
            'Technology/Software': {
                'scope': 'Software development, cloud services, and digital products',
                'key_areas': [
                    'Software Development Lifecycle (SDLC) security',
                    'API and web application security',
                    'Cloud infrastructure and services',
                    'DevOps and CI/CD pipeline security',
                    'Third-party component and dependency management',
                    'Intellectual property protection'
                ],
                'compliance': 'SOC 2, ISO 27001, OWASP guidelines'
            },
            'Healthcare': {
                'scope': 'Patient care, medical devices, and health information systems',
                'key_areas': [
                    'HIPAA compliance and patient data protection',
                    'Medical device security and safety',
                    'Clinical system and EHR security',
                    'Healthcare IoT and connected devices',
                    'Telemedicine and remote care security',
                    'Pharmaceutical data protection'
                ],
                'compliance': 'HIPAA, HITECH, FDA cybersecurity guidelines'
            },
            'Financial Services': {
                'scope': 'Banking, payment processing, and financial data management',
                'key_areas': [
                    'Payment card data protection (PCI DSS)',
                    'Financial transaction security',
                    'Anti-money laundering (AML) compliance',
                    'Fraud detection and prevention',
                    'Customer financial data protection',
                    'Regulatory reporting and compliance'
                ],
                'compliance': 'PCI DSS, GLBA, SOX, Basel III'
            },
            'Manufacturing': {
                'scope': 'Industrial processes, supply chain, and operational technology',
                'key_areas': [
                    'Industrial Control System (ICS) security',
                    'Supply chain and vendor security',
                    'Intellectual property and trade secrets',
                    'Operational Technology (OT) security',
                    'Quality management system security',
                    'Product lifecycle security'
                ],
                'compliance': 'ISO 27001, NIST Cybersecurity Framework, IEC 62443'
            },
            'Retail/E-commerce': {
                'scope': 'Customer transactions, inventory, and e-commerce platforms',
                'key_areas': [
                    'Payment card and transaction security',
                    'Customer data and privacy protection',
                    'E-commerce platform security',
                    'Point of Sale (POS) system security',
                    'Inventory and supply chain security',
                    'Customer loyalty and marketing data'
                ],
                'compliance': 'PCI DSS, GDPR, CCPA, state privacy laws'
            },
            'Education': {
                'scope': 'Student data, research, and educational technology',
                'key_areas': [
                    'Student and faculty data protection',
                    'Research data and intellectual property',
                    'Educational technology and LMS security',
                    'Distance learning and virtual classroom security',
                    'Library and research database access',
                    'FERPA compliance and student privacy'
                ],
                'compliance': 'FERPA, COPPA, state education privacy laws'
            },
            'Government': {
                'scope': 'Public services, citizen data, and government systems',
                'key_areas': [
                    'Citizen data and public records protection',
                    'Government system and infrastructure security',
                    'Classified and sensitive information handling',
                    'Inter-agency data sharing security',
                    'E-government and digital services security',
                    'National security and defense systems'
                ],
                'compliance': 'FISMA, NIST standards, state government regulations'
            },
            'Non-profit': {
                'scope': 'Donor data, program delivery, and volunteer management',
                'key_areas': [
                    'Donor and supporter data protection',
                    'Program and service delivery security',
                    'Volunteer and staff data management',
                    'Fundraising and financial data security',
                    'Grant and funding information protection',
                    'Community outreach and communication security'
                ],
                'compliance': 'State privacy laws, grant requirements, donor privacy'
            }
        }
        
        scope_text = ""
        for ind in industries:
            if ind in industry_details:
                details = industry_details[ind]
                scope_text += f"#### {ind}\n"
                scope_text += f"**Scope**: {details['scope']}\n\n"
                scope_text += "**Key Security Areas**:\n"
                for area in details['key_areas']:
                    scope_text += f"- {area}\n"
                scope_text += f"\n**Compliance Requirements**: {details['compliance']}\n\n"
            else:
                scope_text += f"#### {ind}\n"
                scope_text += "**Scope**: General business operations and information management\n\n"
                scope_text += "**Key Security Areas**:\n"
                scope_text += "- Information asset protection\n"
                scope_text += "- Access control and authentication\n"
                scope_text += "- Incident management and response\n"
                scope_text += "- Business continuity planning\n"
                scope_text += "- Regulatory compliance\n\n"
                scope_text += "**Compliance Requirements**: Applicable industry and regional regulations\n\n"
        
        return scope_text
    
    def _generate_roles_and_responsibilities(self, organization_size: str) -> str:
        """Generate the roles and responsibilities section"""
        size_specific = ""
        if "Small" in organization_size:
            size_specific = """
**Note for Small Organizations**: In smaller organizations, multiple roles may be combined. The CEO or a designated senior manager may assume the CISO role, while IT staff may handle multiple security functions."""
        elif "Medium" in organization_size:
            size_specific = """
**Note for Medium Organizations**: Consider establishing a dedicated security team or security committee to coordinate security activities across departments."""
        
        return f"""## Roles and Responsibilities

### Executive Management
- Approve and support the information security policy
- Allocate necessary resources for security initiatives
- Ensure security objectives align with business goals
- Review security performance and compliance reports

### Chief Information Security Officer (CISO)
- Develop and maintain the information security strategy
- Oversee implementation of security controls and procedures
- Monitor security metrics and compliance status
- Report security status to executive management
- Coordinate incident response activities

### IT Department
- Implement and maintain technical security controls
- Monitor systems for security threats and vulnerabilities
- Perform regular security assessments and audits
- Maintain security documentation and procedures
- Provide technical support for security initiatives

### Human Resources
- Conduct security background checks for new hires
- Include security responsibilities in job descriptions
- Coordinate security awareness training programs
- Manage disciplinary actions for security violations

### All Employees
- Follow security policies and procedures
- Report security incidents and suspicious activities
- Participate in security awareness training
- Protect organizational information and assets
- Use strong passwords and secure authentication methods{size_specific}

---

"""
    
    def _generate_risk_management(self, industry_infos: Dict) -> str:
        """Generate the risk management section"""
        industries = ", ".join(industry_infos.keys())
        risks = []
        for ind, info in industry_infos.items():
            risks.extend(info.get('risks', ['Data breaches', 'System downtime', 'Compliance violations']))
        
        return f"""## Risk Management

### Risk Assessment Process
1. **Asset Identification**: Identify and classify all information assets
2. **Threat Analysis**: Assess potential threats and vulnerabilities
3. **Risk Evaluation**: Determine likelihood and impact of identified risks
4. **Risk Treatment**: Select appropriate risk mitigation strategies
5. **Monitoring and Review**: Continuously monitor and review risk status

### Industry-Specific Risks
Based on the organization's industries, the following risks require special attention:
{chr(10).join([f"- {risk}" for risk in risks])}

### Risk Treatment Options
- **Risk Avoidance**: Eliminate the risk by avoiding the activity
- **Risk Reduction**: Implement controls to reduce likelihood or impact
- **Risk Transfer**: Transfer risk through insurance or contracts
- **Risk Acceptance**: Accept the risk when cost of mitigation exceeds potential loss

---

"""
    
    def _generate_controls_section(self, framework_infos: List[Dict], industry_infos: Dict) -> str:
        """Generate the security controls section"""
        controls = []
        for fw in framework_infos:
            controls.extend(fw.get('controls', []))
        
        industry_controls = industry_infos.get('specific_controls', [])
        
        controls_text = f"""## Security Controls

### {', '.join([fw['name'] for fw in framework_infos])} Controls
The following controls are implemented based on {', '.join([fw['name'] for fw in framework_infos])} requirements:

"""
        
        for i, control in enumerate(controls, 1):
            controls_text += f"{i}. **{control}**\n"
        
        if industry_controls:
            controls_text += f"\n### Industry-Specific Controls\nAdditional controls specific to the organization's industries:\n\n"
            for i, control in enumerate(industry_controls, 1):
                controls_text += f"{i}. **{control}**\n"
        
        controls_text += "\n### Control Implementation\nEach control area includes:\n- Detailed procedures and guidelines\n- Responsibility assignments\n- Performance metrics and monitoring\n- Regular review and update processes\n\n---\n"
        
        return controls_text
    
    def _generate_data_sovereignty_section(self, countries: List[str]) -> str:
        """Generate data sovereignty and privacy law compliance section"""
        if not countries:
            return ""
            
        # Define country-specific privacy laws and requirements
        country_laws = {
            'US': {
                'laws': ['CCPA', 'CPRA', 'COPPA', 'HIPAA', 'GLBA', 'SOX'],
                'requirements': [
                    'Data localization requirements for certain industries',
                    'Consumer privacy rights and opt-out mechanisms',
                    'Healthcare data protection under HIPAA',
                    'Financial data protection under GLBA',
                    'Children\'s online privacy protection under COPPA'
                ]
            },
            'EU': {
                'laws': ['GDPR', 'ePrivacy Directive', 'NIS Directive'],
                'requirements': [
                    'Right to be forgotten and data portability',
                    'Explicit consent for data processing',
                    'Data protection impact assessments (DPIAs)',
                    'Cross-border data transfer restrictions',
                    'Breach notification within 72 hours'
                ]
            },
            'CA': {
                'laws': ['PIPEDA', 'CASL', 'Provincial Privacy Laws'],
                'requirements': [
                    'Meaningful consent for data collection',
                    'Data residency requirements for government contracts',
                    'Anti-spam legislation compliance',
                    'Provincial privacy law variations'
                ]
            },
            'AU': {
                'laws': ['Privacy Act 1988', 'Notifiable Data Breaches Scheme'],
                'requirements': [
                    'Australian Privacy Principles (APPs)',
                    'Mandatory breach notification',
                    'Data localization for government data',
                    'Cross-border disclosure restrictions'
                ]
            },
            'UK': {
                'laws': ['UK GDPR', 'Data Protection Act 2018'],
                'requirements': [
                    'UK-specific data protection requirements',
                    'Adequacy decisions for international transfers',
                    'ICO enforcement and guidance compliance',
                    'Brexit-related data transfer considerations'
                ]
            }
        }
        
        section_content = "\n## Data Sovereignty and Privacy Law Compliance\n\n"
        section_content += "This section addresses data sovereignty requirements and privacy law compliance for the countries where the organization operates.\n\n"
        
        for country in countries:
            if country in country_laws:
                laws = country_laws[country]
                section_content += f"### {country} Compliance Requirements\n\n"
                section_content += f"**Applicable Laws:** {', '.join(laws['laws'])}\n\n"
                section_content += "**Key Requirements:**\n"
                for req in laws['requirements']:
                    section_content += f"- {req}\n"
                section_content += "\n"
            else:
                section_content += f"### {country} Compliance Requirements\n\n"
                section_content += "**Note:** This organization operates in jurisdictions with local privacy and data protection laws. "
                section_content += "Compliance with applicable local regulations is required.\n\n"
        
        section_content += "### Data Localization and Transfer Requirements\n\n"
        section_content += "- **Data Residency:** Ensure data is stored in compliance with local data residency requirements\n"
        section_content += "- **Cross-border Transfers:** Implement appropriate safeguards for international data transfers\n"
        section_content += "- **Local Representatives:** Appoint local representatives where required by law\n"
        section_content += "- **Regulatory Reporting:** Maintain records and reporting mechanisms for regulatory authorities\n\n"
        
        section_content += "### Implementation Guidelines\n\n"
        section_content += "1. **Data Mapping:** Maintain comprehensive data flow maps for all jurisdictions\n"
        section_content += "2. **Consent Management:** Implement country-specific consent mechanisms\n"
        section_content += "3. **Breach Response:** Establish jurisdiction-specific breach notification procedures\n"
        section_content += "4. **Audit Trails:** Maintain detailed audit trails for compliance verification\n"
        section_content += "5. **Training:** Provide country-specific privacy training to employees\n\n"
        
        section_content += "---\n"
        return section_content
    
    def _generate_incident_management(self) -> str:
        """Generate the incident management section"""
        return """## Incident Management

### Incident Response Process
1. **Detection and Reporting**: Identify and report security incidents immediately
2. **Assessment and Classification**: Assess severity and classify the incident
3. **Containment**: Take immediate action to contain the incident
4. **Investigation**: Conduct thorough investigation to determine root cause
5. **Eradication**: Remove the threat and restore affected systems
6. **Recovery**: Restore normal operations and verify system integrity
7. **Lessons Learned**: Document lessons learned and update procedures

### Incident Categories
- **Critical**: Immediate business impact, requires immediate response
- **High**: Significant business impact, requires response within 4 hours
- **Medium**: Moderate business impact, requires response within 24 hours
- **Low**: Minimal business impact, requires response within 72 hours

### Communication Plan
- Internal notification procedures
- External communication protocols
- Regulatory reporting requirements
- Customer notification procedures

---

"""
    
    def _generate_compliance_and_monitoring(self, framework_infos: List[Dict], countries: List[str]) -> str:
        """Generate the compliance and monitoring section"""
        frameworks = ", ".join([fw['name'] for fw in framework_infos])
        return f"""## Compliance and Monitoring

### Compliance Requirements
- Maintain compliance with {frameworks} requirements
- Regular internal audits and assessments
- External certification audits (as applicable)
- Regulatory compliance monitoring
- Industry-specific compliance requirements

### Monitoring and Metrics
- Security performance indicators
- Compliance status tracking
- Risk assessment updates
- Control effectiveness monitoring
- Incident trend analysis

### Audit and Review
- Annual policy review and updates
- Regular security assessments
- Third-party security audits
- Management review meetings
- Continuous improvement processes

### Country-Specific Considerations
- {", ".join([f"**{country}**: {self.industry_requirements[country]['description']}" for country in countries])}

---

"""
    
    def _generate_additional_requirements(self, additional_requirements: str) -> str:
        """Generate additional requirements section if provided"""
        if not additional_requirements.strip():
            return ""
        
        return f"""## Additional Requirements

### Custom Requirements
{additional_requirements}

---

"""
    
    def _generate_policy_maintenance(self) -> str:
        """Generate the policy maintenance section"""
        return """## Policy Maintenance

### Review and Update Process
This policy shall be reviewed and updated:
- Annually or when significant changes occur
- Following security incidents or breaches
- When new regulations or standards are implemented
- When organizational structure or processes change

### Version Control
- All policy changes must be documented
- Previous versions must be archived
- Changes must be approved by appropriate management
- All personnel must be notified of policy updates

### Training and Awareness
- New employees must receive policy training
- Annual refresher training for all personnel
- Regular security awareness campaigns
- Policy acknowledgment and acceptance procedures

---

## Document Approval

**Prepared By:** [Security Team]  
**Reviewed By:** [Legal/Compliance Team]  
**Approved By:** [Executive Management]  
**Date:** [Date of Approval]

---

*This document is confidential and intended for internal use only. Unauthorized distribution is prohibited.*
""" 