"""
PDF Generator - Creates professional PDF proposals
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime


class ProposalPDFGenerator:
    """Generate PDF proposals for mortgage options"""
    
    def __init__(self, lead_data, proposals):
        """
        Initialize PDF generator
        
        Args:
            lead_data: Dictionary with client information
            proposals: List of proposal dictionaries
        """
        self.lead_data = lead_data
        self.proposals = proposals
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#003366'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        self.normal_style = self.styles['Normal']
    
    def generate_pdf(self):
        """Generate PDF and return as bytes"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add header
        elements.extend(self._create_header())
        elements.append(Spacer(1, 0.2*inch))
        
        # Add client information
        elements.extend(self._create_client_info())
        elements.append(Spacer(1, 0.3*inch))
        
        # Add each proposal
        for i, proposal in enumerate(self.proposals):
            elements.extend(self._create_proposal_section(proposal, i+1))
            if i < len(self.proposals) - 1:
                elements.append(Spacer(1, 0.3*inch))
        
        # Add footer
        elements.append(Spacer(1, 0.5*inch))
        elements.extend(self._create_footer())
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _create_header(self):
        """Create PDF header"""
        elements = []
        
        # Company name and logo placeholder
        title = Paragraph("West Capital Lending", self.title_style)
        elements.append(title)
        
        # Broker info
        broker_info = Paragraph(
            "<b>Phil Gustin</b> | Broker Associate<br/>"
            "(949) 209-0989 | www.philthemortgagepro.com<br/>"
            "NMLS 1629148 | DRE 02036208 | NMLS 1566096",
            ParagraphStyle('BrokerInfo', parent=self.normal_style, alignment=TA_CENTER, fontSize=10)
        )
        elements.append(broker_info)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Proposal title
        proposal_title = Paragraph(
            f"Mortgage Proposal Options",
            ParagraphStyle('ProposalTitle', parent=self.heading_style, fontSize=18, alignment=TA_CENTER)
        )
        elements.append(proposal_title)
        
        # Date
        date_text = Paragraph(
            f"Prepared: {datetime.now().strftime('%B %d, %Y')}",
            ParagraphStyle('Date', parent=self.normal_style, alignment=TA_CENTER, fontSize=10, textColor=colors.grey)
        )
        elements.append(date_text)
        
        return elements
    
    def _create_client_info(self):
        """Create client information section"""
        elements = []
        
        heading = Paragraph("Client Information", self.heading_style)
        elements.append(heading)
        
        # Client data table
        data = [
            ['Client Name:', self.lead_data.get('name', 'N/A')],
            ['Property Value:', f"${self.lead_data.get('property_value', 0):,}"],
            ['Current Mortgage Balance:', f"${self.lead_data.get('current_balance', 0):,}"],
            ['Desired Cash Out:', f"${self.lead_data.get('cash_out_amount', 0):,}"],
            ['Veteran Status:', self.lead_data.get('is_veteran', 'N/A').upper()],
        ]
        
        table = Table(data, colWidths=[2.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F4F8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_proposal_section(self, proposal, number):
        """Create a proposal section"""
        elements = []
        
        # Proposal heading
        heading = Paragraph(
            f"Option {number}: {proposal['type']}",
            self.heading_style
        )
        elements.append(heading)
        
        # Description
        desc = Paragraph(proposal['description'], self.normal_style)
        elements.append(desc)
        elements.append(Spacer(1, 0.2*inch))
        
        # Options table
        for option in proposal['options']:
            option_data = [
                ['', option['name']],
                ['Loan Amount:', f"${option['loan_amount']:,}"],
                ['Interest Rate:', f"{option['interest_rate']:.3f}%"],
                ['APR:', f"{option['apr']:.3f}%"],
                ['Term:', option['term']],
                ['Monthly Payment:', f"${option['monthly_payment']:,.2f}"],
                ['Loan Costs:', f"${option['loan_costs']:,}"],
                ['Cash to Borrower:', f"${option.get('cash_to_borrower', 0):,}"],
            ]
            
            # Add note if present
            if 'note' in option:
                option_data.append(['Note:', option['note']])
            
            table = Table(option_data, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#E8F4F8')),
                ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('SPAN', (0, 0), (1, 0)),
            ]))
            
            elements.append(table)
            
            # Space between options
            if len(proposal['options']) > 1 and option != proposal['options'][-1]:
                elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def _create_footer(self):
        """Create PDF footer"""
        elements = []
        
        # Disclaimer
        disclaimer_text = """
        <b>Important Disclosure:</b><br/>
        This is an estimate only and not a commitment to lend. Rates, terms, and conditions are subject to change 
        without notice. All loans subject to credit approval and property appraisal. Additional conditions may apply. 
        This is not a credit decision or a commitment to lend. Licensed by the Department of Financial Protection and Innovation 
        under the California Residential Mortgage Lending Act.
        """
        
        disclaimer = Paragraph(
            disclaimer_text,
            ParagraphStyle('Disclaimer', parent=self.normal_style, fontSize=8, textColor=colors.grey, alignment=TA_LEFT)
        )
        elements.append(disclaimer)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Contact info
        contact = Paragraph(
            "<b>Questions?</b> Contact Phil Gustin at (949) 209-0989 or visit www.philthemortgagepro.com",
            ParagraphStyle('Contact', parent=self.normal_style, fontSize=9, alignment=TA_CENTER)
        )
        elements.append(contact)
        
        return elements


def generate_proposal_pdf(lead_data, proposals):
    """
    Generate a PDF proposal
    
    Args:
        lead_data: Dictionary with client information
        proposals: List of proposal dictionaries
        
    Returns:
        PDF as bytes
    """
    generator = ProposalPDFGenerator(lead_data, proposals)
    return generator.generate_pdf()
