"""
Visualizations Module - Creates interactive Plotly charts for proposals
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st


def create_proposal_visualizations(proposals, lead_data):
    """
    Create comprehensive visualizations for the 3 mortgage proposals
    
    Args:
        proposals: List of proposal dictionaries
        lead_data: Dictionary with client information
    """
    
    st.subheader(f"📊 Proposal Comparison for {lead_data.get('name', 'Client')}")
    
    # Extract data for comparison
    proposal_names = []
    monthly_payments = []
    loan_amounts = []
    interest_rates = []
    aprs = []
    total_costs = []
    cash_amounts = []
    
    for proposal in proposals:
        # Use the first option from each proposal type for main comparison
        option = proposal["options"][0]
        
        proposal_names.append(proposal["type"])
        monthly_payments.append(option["monthly_payment"])
        loan_amounts.append(option["loan_amount"])
        interest_rates.append(option["interest_rate"])
        aprs.append(option["apr"])
        total_costs.append(option["loan_costs"])
        cash_amounts.append(option.get("cash_to_borrower", 0))
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Quick Comparison", 
        "💰 Monthly Payment Details", 
        "📈 Cost Breakdown",
        "📋 Full Details"
    ])
    
    with tab1:
        # Quick comparison chart
        st.markdown("### Side-by-Side Comparison")
        
        # Create comparison metrics
        col1, col2, col3 = st.columns(3)
        
        for idx, (col, proposal) in enumerate(zip([col1, col2, col3], proposals)):
            with col:
                option = proposal["options"][0]
                
                st.markdown(f"#### {proposal['type']}")
                st.metric(
                    "Monthly Payment", 
                    f"${option['monthly_payment']:,.2f}",
                    help="Principal + Interest payment"
                )
                st.metric(
                    "Interest Rate", 
                    f"{option['interest_rate']:.3f}%"
                )
                st.metric(
                    "Cash Out", 
                    f"${option.get('cash_to_borrower', 0):,}"
                )
                st.metric(
                    "Loan Costs", 
                    f"${option['loan_costs']:,}"
                )
                st.caption(proposal["description"])
        
        # Bar chart comparison
        fig = go.Figure(data=[
            go.Bar(
                name='Monthly Payment',
                x=proposal_names,
                y=monthly_payments,
                text=[f'${x:,.2f}' for x in monthly_payments],
                textposition='auto',
                marker_color='lightblue'
            )
        ])
        
        fig.update_layout(
            title="Monthly Payment Comparison",
            xaxis_title="Loan Type",
            yaxis_title="Monthly Payment ($)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Detailed payment breakdown
        st.markdown("### Monthly Payment Details")
        
        # Create subplots for each proposal showing all options
        for proposal in proposals:
            st.markdown(f"#### {proposal['type']}")
            
            if len(proposal["options"]) > 1:
                # Multiple options - show comparison
                option_names = [opt["name"] for opt in proposal["options"]]
                option_payments = [opt["monthly_payment"] for opt in proposal["options"]]
                option_rates = [opt["interest_rate"] for opt in proposal["options"]]
                
                fig = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=("Monthly Payment", "Interest Rate"),
                    specs=[[{"type": "bar"}, {"type": "bar"}]]
                )
                
                # Payment comparison
                fig.add_trace(
                    go.Bar(
                        x=option_names,
                        y=option_payments,
                        text=[f'${x:,.2f}' for x in option_payments],
                        textposition='auto',
                        marker_color='lightgreen',
                        name="Payment"
                    ),
                    row=1, col=1
                )
                
                # Rate comparison
                fig.add_trace(
                    go.Bar(
                        x=option_names,
                        y=option_rates,
                        text=[f'{x:.3f}%' for x in option_rates],
                        textposition='auto',
                        marker_color='lightcoral',
                        name="Rate"
                    ),
                    row=1, col=2
                )
                
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Single option - show details
                option = proposal["options"][0]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Monthly Payment", f"${option['monthly_payment']:,.2f}")
                with col2:
                    st.metric("Interest Rate", f"{option['interest_rate']:.3f}%")
                with col3:
                    st.metric("APR", f"{option['apr']:.3f}%")
            
            st.divider()
    
    with tab3:
        # Cost breakdown
        st.markdown("### Total Cost Analysis")
        
        # Pie chart of costs
        fig = go.Figure(data=[
            go.Bar(
                x=proposal_names,
                y=total_costs,
                text=[f'${x:,}' for x in total_costs],
                textposition='auto',
                marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']
            )
        ])
        
        fig.update_layout(
            title="Upfront Loan Costs Comparison",
            xaxis_title="Loan Type",
            yaxis_title="Loan Costs ($)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Interest rate vs APR comparison
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Interest Rate',
            x=proposal_names,
            y=interest_rates,
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='APR',
            x=proposal_names,
            y=aprs,
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            title="Interest Rate vs APR",
            xaxis_title="Loan Type",
            yaxis_title="Rate (%)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Full detailed tables
        st.markdown("### Complete Proposal Details")
        
        for proposal in proposals:
            st.markdown(f"#### {proposal['type']}")
            st.caption(proposal["description"])
            
            # Create a table for each option
            for option in proposal["options"]:
                st.markdown(f"**{option['name']}**")
                
                details = {
                    "Loan Amount": f"${option['loan_amount']:,}",
                    "Interest Rate": f"{option['interest_rate']:.3f}%",
                    "APR": f"{option['apr']:.3f}%",
                    "Term": option['term'],
                    "Monthly Payment": f"${option['monthly_payment']:,.2f}",
                    "Loan Costs": f"${option['loan_costs']:,}",
                    "Cash to Borrower": f"${option.get('cash_to_borrower', 0):,}"
                }
                
                if "note" in option:
                    details["Note"] = option["note"]
                
                # Display as a nice table
                col1, col2 = st.columns(2)
                items = list(details.items())
                mid = len(items) // 2
                
                with col1:
                    for key, value in items[:mid]:
                        st.text(f"{key}: {value}")
                
                with col2:
                    for key, value in items[mid:]:
                        st.text(f"{key}: {value}")
                
                st.markdown("---")
            
            st.divider()
    
    # Summary recommendation box
    st.info(f"""
    ### 💡 Next Steps
    
    Review the options above and let me know if you have any questions! Here's what we can do:
    
    1. **Adjust the numbers**: If you want to see different scenarios (more/less cash out, different loan amounts)
    2. **Compare in detail**: Look at the full breakdown in the tabs above
    3. **Move forward**: Once you've chosen an option, I can help you start the application process
    
    **Property Value**: ${lead_data.get('property_value', 0):,}
    **Current Balance**: ${lead_data.get('current_balance', 0):,}
    **Cash Out Requested**: ${lead_data.get('cash_out_amount', 0):,}
    """)


def create_summary_chart(proposals):
    """Create a summary radar chart comparing all proposals"""
    
    categories = ['Monthly Payment', 'Interest Rate', 'Loan Costs', 'APR']
    
    fig = go.Figure()
    
    for proposal in proposals:
        option = proposal["options"][0]
        
        # Normalize values for radar chart (scale 0-100)
        values = [
            100 - (option["monthly_payment"] / 3000 * 100),  # Lower is better
            100 - (option["interest_rate"] / 10 * 100),      # Lower is better
            100 - (option["loan_costs"] / 10000 * 100),      # Lower is better
            100 - (option["apr"] / 10 * 100)                 # Lower is better
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=proposal["type"]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Overall Comparison (Higher is Better)"
    )
    
    return fig
