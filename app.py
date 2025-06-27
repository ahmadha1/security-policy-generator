from flask import Flask, render_template, request, jsonify, send_file
from flask_wtf.csrf import CSRFProtect
import json
import os
from datetime import datetime
from policy_generator import SecurityPolicyGenerator
from claude_policy_generator import ClaudePolicyGenerator
from policy_database import PolicyDatabase
import ssl
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import ipaddress
import sys

# Set the correct template folder path
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
csrf = CSRFProtect(app)

# SSL Configuration
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = True

# Initialize the policy generators
policy_generator = SecurityPolicyGenerator()
claude_generator = None

# Initialize the policy database
policy_db = PolicyDatabase()

# Try to initialize Claude generator if API key is available
try:
    claude_generator = ClaudePolicyGenerator()
    print("Claude API integration enabled")
except ValueError as e:
    print(f"Claude API not available: {e}")
    print("Using standard policy generator only")

def markdown_to_pdf(markdown_content, filename):
    """Convert markdown content to PDF"""
    # Create PDF file path
    pdf_path = os.path.join('temp', filename.replace('.md', '.pdf'))
    os.makedirs('temp', exist_ok=True)
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Parse markdown content and convert to PDF elements
    story = []
    
    lines = markdown_content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('# '):
            # Main title
            title = line[2:]
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
        elif line.startswith('## '):
            # Section heading
            heading = line[3:]
            story.append(Paragraph(heading, heading_style))
            story.append(Spacer(1, 12))
            
        elif line.startswith('### '):
            # Subsection heading
            subheading = line[4:]
            story.append(Paragraph(subheading, styles['Heading3']))
            story.append(Spacer(1, 8))
            
        elif line.startswith('- '):
            # Bullet point
            bullet_text = line[2:]
            story.append(Paragraph(f"• {bullet_text}", normal_style))
            
        elif line.startswith('**') and line.endswith('**'):
            # Bold text
            bold_text = line[2:-2]
            story.append(Paragraph(f"<b>{bold_text}</b>", normal_style))
            
        elif line == '---':
            # Horizontal rule
            story.append(Spacer(1, 20))
            
        elif line and not line.startswith('```'):
            # Regular paragraph
            story.append(Paragraph(line, normal_style))
            
        i += 1
    
    # Build PDF
    doc.build(story)
    return pdf_path

@app.route('/')
def index():
    """Main page with the policy generator form"""
    return render_template('index.html')

@app.route('/database')
def database():
    """Database page to view saved policies and controls"""
    return render_template('database.html')

@app.route('/generate_policy', methods=['POST'])
@csrf.exempt
def generate_policy():
    """Generate security policy based on form data"""
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug logging
        
        # Extract form data
        organization_name = data.get('organization_name', '')
        industry = data.get('industry', [])
        framework = data.get('framework', [])
        organization_size = data.get('organization_size', '')
        additional_requirements = data.get('additional_requirements', '')
        
        print(f"Extracted data - org: {organization_name}, industry: {industry}, framework: {framework}")  # Debug logging
        
        # Validate required fields
        if not organization_name or not industry or not framework:
            error_msg = 'Please fill in all required fields: Organization Name, Industry, and Framework'
            print(f"Validation failed: {error_msg}")  # Debug logging
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # Ensure industry and framework are lists
        if not isinstance(industry, list):
            industry = [industry] if industry else []
        if not isinstance(framework, list):
            framework = [framework] if framework else []
        
        print(f"Processed data - industry: {industry}, framework: {framework}")  # Debug logging
        
        # Use Claude generator if available, otherwise fall back to standard generator
        if claude_generator:
            print("Using Claude for policy generation...")
            policy_content = claude_generator.generate_policy(
                organization_name=organization_name,
                industry=industry,
                framework=framework,
                organization_size=organization_size,
                additional_requirements=additional_requirements
            )
        else:
            print("Using standard policy generator...")
            policy_content = policy_generator.generate_policy(
                organization_name=organization_name,
                industry=industry,
                framework=framework,
                organization_size=organization_size,
                additional_requirements=additional_requirements
            )
        
        print(f"Policy generated successfully, length: {len(policy_content)}")  # Debug logging
        
        # Create filename for download
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        framework_str = "_".join(framework) if isinstance(framework, list) else framework
        filename = f"{organization_name.replace(' ', '_')}_{framework_str}_{timestamp}.md"
        
        # Save policy to database
        try:
            policy_db.save_organization(
                name=organization_name,
                industry=industry,
                framework=framework,
                organization_size=organization_size
            )
            policy_db.save_policy(
                organization_name=organization_name,
                policy_content=policy_content,
                filename=filename,
                generator_type='claude' if claude_generator else 'standard'
            )
            print(f"Policy saved to database for organization: {organization_name}")
        except Exception as e:
            print(f"Warning: Could not save policy to database: {e}")
        
        return jsonify({
            'success': True,
            'policy_content': policy_content,
            'filename': filename,
            'organization_name': organization_name,
            'framework': framework,
            'generated_at': datetime.now().isoformat(),
            'generator_type': 'claude' if claude_generator else 'standard'
        })
        
    except Exception as e:
        print(f"Error in generate_policy: {str(e)}")  # Debug logging
        import traceback
        traceback.print_exc()  # Print full stack trace
        return jsonify({
            'success': False,
            'error': f'Error generating policy: {str(e)}'
        }), 500

@app.route('/download_policy', methods=['POST'])
@csrf.exempt
def download_policy():
    """Download the generated policy as a markdown file"""
    try:
        data = request.get_json()
        policy_content = data.get('policy_content', '')
        filename = data.get('filename', 'security_policy.md')
        
        # Create the file in a temporary location
        file_path = os.path.join('temp', filename)
        os.makedirs('temp', exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(policy_content)
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/markdown'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error downloading policy: {str(e)}'
        }), 500

@app.route('/download_pdf', methods=['POST'])
@csrf.exempt
def download_pdf():
    """Download the generated policy as a PDF file"""
    try:
        data = request.get_json()
        policy_content = data.get('policy_content', '')
        filename = data.get('filename', 'security_policy.md')
        
        # Convert markdown to PDF
        pdf_path = markdown_to_pdf(policy_content, filename)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=filename.replace('.md', '.pdf'),
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error generating PDF: {str(e)}'
        }), 500

@app.route('/convert_to_pdf', methods=['POST'])
@csrf.exempt
def convert_to_pdf():
    """Convert any content to PDF for download"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        filename = data.get('filename', 'document.pdf')
        
        # Convert content to PDF
        pdf_path = markdown_to_pdf(content, filename)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error generating PDF: {str(e)}'
        }), 500

@app.route('/api/frameworks')
def get_frameworks():
    """Get available compliance frameworks"""
    frameworks = [
        {'id': 'iso27001', 'name': 'ISO 27001', 'description': 'Information Security Management System'},
        {'id': 'iso42001', 'name': 'ISO 42001', 'description': 'AI Management System'},
        {'id': 'nist_ai_rmf', 'name': 'NIST AI RMF', 'description': 'NIST Artificial Intelligence Risk Management Framework'},
        {'id': 'nist_sp_800_53', 'name': 'NIST SP 800-53', 'description': 'NIST Special Publication 800-53 - Security and Privacy Controls'},
        {'id': 'nist_csf', 'name': 'NIST CSF', 'description': 'NIST Cybersecurity Framework'},
        {'id': 'hitrust', 'name': 'HITRUST CSF', 'description': 'HITRUST Common Security Framework'},
        {'id': 'fedramp', 'name': 'FedRAMP', 'description': 'Federal Risk and Authorization Management Program'},
        {'id': 'cis', 'name': 'CIS Controls', 'description': 'Center for Internet Security Critical Security Controls'},
        {'id': 'pci', 'name': 'PCI DSS', 'description': 'Payment Card Industry Data Security Standard'},
        {'id': 'soc2', 'name': 'SOC 2', 'description': 'Service Organization Control 2'},
        {'id': 'gdpr', 'name': 'GDPR', 'description': 'General Data Protection Regulation'},
        {'id': 'owasp', 'name': 'OWASP', 'description': 'Open Web Application Security Project - Application Security Framework'},
        {'id': 'itil', 'name': 'ITIL', 'description': 'Information Technology Infrastructure Library - IT Service Management'},
        {'id': 'csa', 'name': 'CSA', 'description': 'Cloud Security Alliance - Cloud Security Framework'}
    ]
    return jsonify(frameworks)

@app.route('/api/industries')
def get_industries():
    """Get available industries"""
    industries = [
        'Technology/Software',
        'Healthcare',
        'Financial Services',
        'Manufacturing',
        'Retail/E-commerce',
        'Education',
        'Government',
        'Non-profit',
        'Consulting',
        'Real Estate',
        'Transportation',
        'Energy',
        'Media/Entertainment',
        'Legal Services',
        'Other'
    ]
    return jsonify(industries)

@app.route('/api/organization_sizes')
def get_organization_sizes():
    """Get organization size options"""
    sizes = [
        'Small (1-50 employees)',
        'Medium (51-500 employees)',
        'Large (501-5000 employees)',
        'Enterprise (5000+ employees)'
    ]
    return jsonify(sizes)

@app.route('/generate_controls', methods=['POST'])
@csrf.exempt
def generate_controls():
    """Generate security controls using Claude"""
    try:
        if not claude_generator:
            return jsonify({
                'success': False,
                'error': 'Claude API is not available. Please set CLAUDE_API_KEY environment variable.'
            }), 400
        
        data = request.get_json()
        policy_content = data.get('policy_content', '')
        framework = data.get('framework', [])
        industry = data.get('industry', [])
        
        if not policy_content or not framework or not industry:
            return jsonify({
                'success': False,
                'error': 'Policy content, framework, and industry are required'
            }), 400
        
        print("Generating controls using Claude...")
        controls_content = claude_generator.generate_controls(policy_content, framework, industry)
        
        return jsonify({
            'success': True,
            'controls_content': controls_content,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in generate_controls: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error generating controls: {str(e)}'
        }), 500

@app.route('/generate_implementation_guide', methods=['POST'])
@csrf.exempt
def generate_implementation_guide():
    """Generate implementation guide using Claude"""
    try:
        if not claude_generator:
            return jsonify({
                'success': False,
                'error': 'Claude API is not available. Please set CLAUDE_API_KEY environment variable.'
            }), 400
        
        data = request.get_json()
        policy_content = data.get('policy_content', '')
        controls_content = data.get('controls_content', '')
        organization_size = data.get('organization_size', '')
        
        if not policy_content or not controls_content:
            return jsonify({
                'success': False,
                'error': 'Policy content and controls content are required'
            }), 400
        
        print("Generating implementation guide using Claude...")
        implementation_guide = claude_generator.generate_implementation_guide(
            policy_content, controls_content, organization_size
        )
        
        return jsonify({
            'success': True,
            'implementation_guide': implementation_guide,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in generate_implementation_guide: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error generating implementation guide: {str(e)}'
        }), 500

@app.route('/generate_complete_package', methods=['POST'])
@csrf.exempt
def generate_complete_package():
    """Generate complete security package (policy, controls, implementation guide) using Claude"""
    try:
        if not claude_generator:
            return jsonify({
                'success': False,
                'error': 'Claude API is not available. Please set CLAUDE_API_KEY environment variable.'
            }), 400
        
        data = request.get_json()
        organization_name = data.get('organization_name', '')
        industry = data.get('industry', [])
        framework = data.get('framework', [])
        organization_size = data.get('organization_size', '')
        additional_requirements = data.get('additional_requirements', '')
        
        if not organization_name or not industry or not framework:
            return jsonify({
                'success': False,
                'error': 'Organization name, industry, and framework are required'
            }), 400
        
        print("Generating complete security package using Claude...")
        package = claude_generator.generate_complete_security_package(
            organization_name=organization_name,
            industry=industry,
            framework=framework,
            organization_size=organization_size,
            additional_requirements=additional_requirements
        )
        
        # Create filenames for download
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        framework_str = "_".join(framework) if isinstance(framework, list) else framework
        base_filename = f"{organization_name.replace(' ', '_')}_{framework_str}_{timestamp}"
        
        return jsonify({
            'success': True,
            'package': package,
            'filenames': {
                'policy': f"{base_filename}_policy.md",
                'controls': f"{base_filename}_controls.md",
                'implementation': f"{base_filename}_implementation.md"
            },
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in generate_complete_package: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error generating complete package: {str(e)}'
        }), 500

@app.route('/api/organizations')
def get_organizations():
    """Get all organizations from database"""
    try:
        organizations = policy_db.get_organizations()
        return jsonify({
            'success': True,
            'organizations': organizations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching organizations: {str(e)}'
        }), 500

@app.route('/api/organizations/<organization_name>/policies')
def get_organization_policies(organization_name):
    """Get all policies for a specific organization"""
    try:
        policies = policy_db.get_organization_policies(organization_name)
        return jsonify({
            'success': True,
            'policies': policies
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching policies: {str(e)}'
        }), 500

@app.route('/api/organizations/<organization_name>/controls')
def get_organization_controls(organization_name):
    """Get all controls for a specific organization"""
    try:
        controls = policy_db.get_organization_controls(organization_name)
        return jsonify({
            'success': True,
            'controls': controls
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching controls: {str(e)}'
        }), 500

@app.route('/api/organizations/<organization_name>/guides')
def get_organization_guides(organization_name):
    """Get all implementation guides for a specific organization"""
    try:
        guides = policy_db.get_organization_guides(organization_name)
        return jsonify({
            'success': True,
            'guides': guides
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching guides: {str(e)}'
        }), 500

@app.route('/save_controls', methods=['POST'])
@csrf.exempt
def save_controls():
    """Save generated controls to database"""
    try:
        data = request.get_json()
        organization_name = data.get('organization_name', '')
        controls_content = data.get('controls_content', '')
        filename = data.get('filename', '')
        
        if not organization_name or not controls_content:
            return jsonify({
                'success': False,
                'error': 'Organization name and controls content are required'
            }), 400
        
        success = policy_db.save_controls(organization_name, controls_content, filename)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Controls saved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save controls'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error saving controls: {str(e)}'
        }), 500

@app.route('/save_implementation_guide', methods=['POST'])
@csrf.exempt
def save_implementation_guide():
    """Save generated implementation guide to database"""
    try:
        data = request.get_json()
        organization_name = data.get('organization_name', '')
        guide_content = data.get('guide_content', '')
        filename = data.get('filename', '')
        
        if not organization_name or not guide_content:
            return jsonify({
                'success': False,
                'error': 'Organization name and guide content are required'
            }), 400
        
        success = policy_db.save_implementation_guide(organization_name, guide_content, filename)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Implementation guide saved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save implementation guide'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error saving implementation guide: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Configure for HTTPS with SSL certificates
    ssl_context = None
    
    # Check if SSL certificates exist
    cert_file = 'ssl/cert.pem'
    key_file = 'ssl/key.pem'
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_context = (cert_file, key_file)
        print("SSL certificates found. Running with HTTPS...")
    else:
        print("SSL certificates not found.")
        print("To enable HTTPS, run: python generate_ssl_cert.py")
        print("Running without HTTPS...")
    
    # Run the app with HTTPS if SSL context is available
    if ssl_context:
        app.run(
            debug=True, 
            host='0.0.0.0', 
            port=5014,
            ssl_context=ssl_context
        )
    else:
        app.run(
            debug=True, 
            host='0.0.0.0', 
            port=5014
        ) 