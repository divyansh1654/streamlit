import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd
import pickle
import plotly.express as px
import matplotlib.pyplot as plt;
import plotly.graph_objects as go;

# Configure APIs
genai.configure(api_key="AIzaSyBmIy8l0WOVZieQd3kKi-lRVdiBZXsBaP4")
API_KEY = "055e038fb8dedd03881fe188368a9c3d"

# Teams and cities
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Ahmedabad', 'Pune', 'Mohali', 'Bengaluru']

# Streamlit app configuration
st.set_page_config(page_title="CrickWin Pro", page_icon="🏏", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .header {
        font-size: 2.5em;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 20px;
        padding: 15px;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8E8E 100%);
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    .subheader {
        font-size: 1.5em;
        color: #FFFFFF;
        background: linear-gradient(135deg, #1F77B4 0%, #4FA8FF 100%);
        padding: 10px 15px;
        border-radius: 8px;
        margin-top: 25px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .metric-box {
        background: linear-gradient(145deg, #FFFFFF 0%, #F0F2F6 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border: 1px solid #E0E0E0;
    }
    .metric-box h3 {
        color: #333333;
        margin-top: 0;
        font-size: 1.2em;
    }
    .metric-box p {
        color: #666666;
        margin-bottom: 0;
    }
    .team-card {
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    .team-card h3 {
        color: #333333;
        margin: 0;
    }
    .team-card:hover {
        transform: translateY(-3px);
    }
    .batting-team {
        background: linear-gradient(135deg, #FFE4E1 0%, #FFC9C9 100%);
        border-left: 6px solid #FF4B4B;
    }
    .bowling-team {
        background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%);
        border-left: 6px solid #1F77B4;
    }
    .bar-chart-header {
    font-size: 1.2em;
    color: #333;
    margin-bottom: 10px;
    }
    .bar-chart-container {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8E8E 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 1em;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    body {
        background-color: #F8F9FA;
    }
    .ai-analysis {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1F77B4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: 20px;
        color: #333333;
    }
    .analysis-point {
        background: #F8F9FA;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #1F77B4;
    }
    .analysis-point h4 {
        margin-top: 0;
        color: #1F77B4;
    }
    .highlight-box {
        background: linear-gradient(135deg, #FFF9C4 0%, #FFEE58 100%);
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #FFC107;
    }
    .tactical-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #4CAF50;
    }
    .win-probability {
        font-size: 1.2em;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .dashboard-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .dashboard-card h3 {
        transition: all 0.3s ease;
    }
    .dashboard-card:hover h3 {
        text-decoration: underline;
    }
    .winning-team {
        background: linear-gradient(135deg, #E8F5E9 0%, #A5D6A7 100%);
        color: #2E7D32;
    }
    .losing-team {
        background: linear-gradient(135deg, #FFEBEE 0%, #EF9A9A 100%);
        color: #C62828;
    }
            .weather-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .weather-metric {
        display: flex;
        align-items: center;
        margin: 15px 0;
        padding: 15px;
        border-radius: 10px;
        background: rgba(255,255,255,0.9);
    }
    .weather-gauge {
        background: #f0f2f6;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    .wind-compass {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        position: relative;
        background: conic-gradient(from 0deg, #4CAF50 0%, #FFC107 50%, #F44336 100%);
        margin: 0 auto;
    }
    .wind-needle {
        position: absolute;
        width: 2px;
        height: 50%;
        background: #1A237E;
        left: 50%;
        bottom: 50%;
        transform-origin: bottom;
    }
    .analysis-point, .tactical-box, .highlight-box, .ai-analysis {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border-left: 4px solid;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.analysis-point:hover, .tactical-box:hover, .highlight-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

/* Section-Specific Styling */
.analysis-point {
    background: linear-gradient(95deg, #f8f9fa 0%, #ffffff 100%);
    border-left-color: #4e73df;
}

.analysis-point h4 {
    color: #2c3e50;
    font-size: 1.25rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.tactical-box {
    background: linear-gradient(95deg, #fff3cd 0%, #fff8e6 100%);
    border-left-color: #ffc107;
    border-style: dashed;
}

.highlight-box {
    background: linear-gradient(95deg, #d1ecf1 0%, #e8f7fa 100%);
    border-left-color: #17a2b8;
}

/* Content Styling */
.analysis-point ul {
    padding-left: 1.5rem;
    margin: 0;
}

.analysis-point li {
    margin-bottom: 0.5rem;
    position: relative;
    padding-left: 1.5rem;
    line-height: 1.6;
}

.analysis-point li:before {
    content: "•";
    position: absolute;
    left: 0;
    color: #4e73df;
    font-weight: bold;
}

/* Tactical Recommendations Enhancements */
.tactical-box h4 {
    color: #856404;
    font-size: 1.25rem;
    margin-bottom: 1rem;
}

.tactical-box ul {
    padding-left: 1.5rem;
}

.tactical-box li {
    margin-bottom: 0.75rem;
    padding-left: 1rem;
    border-left: 2px solid #ffc107;
}

# /* Weather Section Styling */
# .highlight-box h4 {
#     color: #0c5460;
#     font-size: 1.25rem;
#     margin-bottom: 1rem;
#     display: flex;
#     align-items: center;
#     gap: 0.5rem;
# }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<div class="header">🏏 CrickWin Pro: Advanced IPL Analytics</div>', unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.header("Match Parameters")
    batting_team = st.selectbox('Batting Team', sorted(teams))
    bowling_team = st.selectbox('Bowling Team', sorted(teams))
    selected_city = st.selectbox('Venue', sorted(cities))
    
    st.header("Match Situation")
    target = st.number_input('Target Score', min_value=0, step=1)
    score = st.number_input('Current Score', min_value=0, step=1)
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=20.0, step=0.1)
    wickets = st.number_input('Wickets Lost', min_value=0, max_value=10, step=1)
    
    predict_btn = st.button("Predict Probability", use_container_width=True)

# Function to get weather data
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'temp': data['main']['temp'],
                'wind': data['wind']['speed'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'icon': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            }
    except Exception as e:
        st.error(f"Weather API error: {str(e)}")
    return None

def get_gemini_prediction(batting_team, bowling_team, city, target, score, overs, wickets, weather_data=None):
    prompt = f"""
    You are an expert cricket analyst specializing in IPL match predictions. 
    Analyze this match situation and predict the exact win probability percentage for both teams:
    
    Match Details:
    - Batting Team: {batting_team}
    - Bowling Team: {bowling_team}
    - Venue: {city}
    - Target: {target}
    - Current Score: {score}/{wickets} in {overs} overs
    - Required Run Rate: {(target - score) / (20 - overs):.2f} (if overs < 20)
    
    Weather Conditions: {weather_data['description'] if weather_data else 'Not available'}
    
    Consider all relevant factors including:
    - Team strengths and recent performance
    - Venue statistics and pitch conditions
    - Current match situation (runs required, wickets in hand, overs remaining)
    - Weather impact if available
    
    Provide your response in this exact JSON format with no other text:
    {{
        "batting_team_win_probability": x.xx,
        "bowling_team_win_probability": x.xx,
        "confidence": "high/medium/low"
    }}
    
    The probabilities should sum to 100. Be precise in your calculations.
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Extract JSON from the response
        response_text = response.text
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        
        import json
        prediction = json.loads(json_str)
        return prediction
        
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None

# Main content layout
col1, col2 = st.columns([1, 1])

with col1:
    # Weather Section (always visible)
    st.markdown('<div class="subheader">🌦️ Venue Conditions</div>', unsafe_allow_html=True)
    weather_data = get_weather(selected_city)
    
    if weather_data:
        weather_col1, weather_col2 = st.columns([1, 3])
        with weather_col1:
            st.image(weather_data['icon'], width=80)
        with weather_col2:
            st.markdown(f"""
            **{selected_city} Weather Conditions**  
            🌡️ Temperature: {weather_data['temp']}°C  
            💨 Wind: {weather_data['wind']} m/s  
            💧 Humidity: {weather_data['humidity']}%  
            ☁️ Conditions: {weather_data['description'].title()}
            """)
        
        # Pitch Conditions Analysis
        st.markdown('<div class="subheader">📊 Pitch Conditions Analysis</div>', unsafe_allow_html=True)
        
        humidity = weather_data['humidity']
        wind_speed = weather_data['wind']
        temp = weather_data['temp']
        desc = weather_data['description'].lower()
        
        if humidity < 30:
            st.write("Low humidity; dry pitch may favor fast bowlers and provide extra bounce.")
        elif 30 <= humidity <= 60:
            st.write("Moderate humidity; pitch conditions are balanced, benefiting both batsmen and bowlers.")
            if wind_speed > 10:
                st.write("High wind speed may assist swing bowlers.")
        else:
            st.write("High humidity; conditions might aid seam movement for bowlers.")
        
        if temp > 30:
            st.write("Hot weather; pitch could become dry, favoring batsmen with hard-hitting.")
        elif 20 <= temp <= 30:
            st.write("Pleasant weather; pitch likely to remain favorable for batting.")
        else:
            st.write("Cool weather; the pitch might hold moisture, aiding bowlers.")

        if "rain" in desc:
            st.write("Rain may affect the pitch, possibly making it softer and more conducive to swing bowling.")
        elif "cloud" in desc:
            st.write("Overcast conditions may assist seamers and spinners, making the pitch unpredictable.")
    else:
        st.warning("Could not fetch weather data")

with col2:
    # Team Comparison Section (always visible)
    st.markdown('<div class="subheader">🏟️ Team Matchup</div>', unsafe_allow_html=True)
    
    team_col1, team_col2 = st.columns(2)
    with team_col1:
        st.markdown(f'<div class="team-card batting-team"><h3>Batting: {batting_team}</h3></div>', 
                   unsafe_allow_html=True)
    with team_col2:
        st.markdown(f'<div class="team-card bowling-team"><h3>Bowling: {bowling_team}</h3></div>', 
                   unsafe_allow_html=True)
    
    # Add Looker Studio Dashboard Link
    st.markdown(
        """
        <a href="https://lookerstudio.google.com/reporting/40219022-30a3-45d5-8e57-0ec95f2b2e61" target="_blank" style="text-decoration: none;">
            <div class="dashboard-card" style='
                background: linear-gradient(135deg, #4285F4 0%, #34A853 100%);
                border-radius: 12px;
                padding: 15px;
                margin-top: 20px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
                cursor: pointer;
            '>
                <div style='display: flex; align-items: center; justify-content: center;'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" style='margin-right: 10px;'>
                        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/>
                        <path d="M7 12h2v5H7zm4-7h2v12h-2zm4 4h2v8h-2z"/>
                    </svg>
                    <h3 style='color: white; margin: 0;'>Advanced Analytics Dashboard</h3>
                </div>
                <p style='color: rgba(255,255,255,0.8); margin: 8px 0 0 0; font-size: 14px;'>
                    Click to view detailed team analytics
                </p>
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )

# Prediction results
if predict_btn:
    if overs < 0 or target < 0 or score < 0 or wickets < 0:
        st.error('Score, Target, and Wickets must be non-negative.')
    elif overs > 20:
        st.error('Overs cannot exceed 20.')
    else:
        # Calculate match metrics
        crr = score / overs if overs > 0 else 0
        balls_left = 120 - (overs * 6)
        runs_left = target - score
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
        
        # Get prediction from Gemini
    with st.spinner("Analyzing match situation"):
            prediction = get_gemini_prediction(
                batting_team, bowling_team, selected_city, 
                target, score, overs, wickets, weather_data
            )

            if prediction:
                batting_prob = prediction['batting_team_win_probability'] / 100
                bowling_prob = prediction['bowling_team_win_probability'] / 100
                confidence = prediction['confidence']
                
                # Display results with enhanced visuals
                st.markdown('<div class="subheader">🎯 Win Probability Prediction</div>', unsafe_allow_html=True)
                
                # Determine winning and losing probabilities
                if batting_prob > bowling_prob:
                    winning_prob = batting_prob
                    winning_team = batting_team
                    losing_prob = bowling_prob
                    losing_team = bowling_team
                else:
                    winning_prob = bowling_prob
                    winning_team = bowling_team
                    losing_prob = batting_prob
                    losing_team = batting_team
                
                # Create DataFrame for bar chart
                prob_data = pd.DataFrame({
                    'Team': [winning_team, losing_team],
                    'Probability': [winning_prob, losing_prob],
                    'Color': ['#4CAF50', '#F44336']  # Green for winner, red for loser
                })
            
                # Create horizontal bar chart
                fig = px.bar(
                    prob_data,
                    x='Probability',
                    y='Team',
                    color='Team',
                    color_discrete_map={
                        winning_team: '#4CAF50',
                        losing_team: '#F44336'
                    },
                    orientation='h',
                    text='Probability',
                    title=f"Win Probability: {winning_team} vs {losing_team} (Confidence: {confidence})",
                    height=300
                )
            
                # Customize bar chart appearance
                fig.update_traces(
                    texttemplate='%{x:.1%}',
                    textposition='outside',
                    marker_line_color='white',
                    marker_line_width=1.5,
                    opacity=0.8
                )
            
                fig.update_layout(
                    xaxis=dict(
                        title='Win Probability',
                        tickformat='.0%',
                        range=[0, 1]  # Fixed 0-100% scale
                    ),
                    yaxis=dict(title=None),
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=20, r=20, t=60, b=20)
                )
            
                st.plotly_chart(fig, use_container_width=True)
            
                # Metrics display with winning/losing distinction
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown(f'<div class="win-probability winning-team">'
                            f'🏆 {winning_team}<br>'
                            f'<span style="font-size:28px;">{round(winning_prob * 100, 1)}%</span>'
                            '</div>', unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f'<div class="win-probability losing-team">'
                            f'😞 {losing_team}<br>'
                            f'<span style="font-size:28px;">{round(losing_prob * 100, 1)}%</span>'
                            '</div>', unsafe_allow_html=True)
            
            # Run progression chart
            st.markdown('<div class="subheader">📈 Run Progression</div>', unsafe_allow_html=True)
            projected_runs = score + (crr * (20 - overs))
            required_runs = target

            # Create figure with proper data points
            fig = go.Figure()

            # Main progression line (from start to current position)
            fig.add_trace(go.Scatter(
                x=[0, overs],
                y=[0, score],
                mode='lines+markers',
                name='Runs Scored',
                line=dict(color='#2196F3', width=3),
                marker=dict(size=8)
            ))

            # Projected runs line (dotted)
            fig.add_trace(go.Scatter(
                x=[overs, 20],
                y=[score, projected_runs],
                mode='lines+markers',
                name='Current Rate Projection',
                line=dict(color='#4CAF50', width=2, dash='dot'),
                marker=dict(size=6, symbol='diamond')
            ))

            # Required rate line (if needed)
            if runs_left > 0:
                fig.add_trace(go.Scatter(
                    x=[overs, 20],
                    y=[score, required_runs],
                    mode='lines+markers',
                    name='Required Rate',
                    line=dict(color='#F44336', width=2, dash='dash'),
                    marker=dict(size=6, symbol='x')
                ))

            # Target line (if already achieved)
            if score >= target:
                fig.add_hline(y=target, line_dash="dot", 
                            line_color="purple", 
                            annotation_text="Target Achieved",
                            annotation_position="bottom right")

            # Update layout
            fig.update_layout(
                title='Run Progression vs Required Rate',
                xaxis=dict(
                    title='Overs',
                    range=[0, 20],
                    dtick=2,
                    gridcolor='rgba(224, 224, 224, 0.5)',
                    showline=True,
                    linecolor='#E0E0E0'
                ),
                yaxis=dict(
                    title='Runs',
                    range=[0, max(projected_runs, required_runs, target)*1.1],
                    gridcolor='rgba(224, 224, 224, 0.5)',
                    showline=True,
                    linecolor='#E0E0E0'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(l=50, r=50, t=80, b=50),
                hovermode="x unified"
            )

            # Custom CSS to ensure proper display
            st.markdown("""
            <style>
                .js-plotly-plot .plotly .main-svg {
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                .js-plotly-plot .plotly .gridlayer .xgrid, 
                .js-plotly-plot .plotly .gridlayer .ygrid {
                    stroke-dasharray: 2px;
                }
            </style>
            """, unsafe_allow_html=True)

            st.plotly_chart(fig, use_container_width=True)
            
            # AI-generated match analysis
            st.markdown('<div class="subheader">🔍 AI Match Analysis</div>', unsafe_allow_html=True)
            
            analysis_prompt = f"""
            Analyze this IPL match situation between {batting_team} (batting) and {bowling_team} (bowling):
            
            Match Situation:
            - Target: {target}
            - Current: {score}/{wickets} in {overs} overs
            - Required Rate: {rrr:.2f} vs Current Rate: {crr:.2f}
            - Balls Left: {balls_left}
            - Win Probability: {batting_team} {round(batting_prob*100, 2)}% vs {bowling_team} {round(bowling_prob*100, 2)}%
            - Prediction Confidence: {confidence}
            
            Venue: {selected_city}
            Weather: {weather_data['description'] if weather_data else 'Data not available'}
            
            Provide a detailed analysis covering:
            1. Current match situation assessment
            2. Key factors influencing the probabilities
            3. Tactical recommendations for both teams
            4. How weather and pitch conditions might affect the outcome with time vs weather temp, humidity and wind speed analysis and pitch factors. 
                Format this section as:
                - Time vs Temperature: [time intervals and temp values]
                - Time vs Humidity: [time intervals and humidity%]
                - Time vs Wind Speed: [time intervals and wind speed km/h]
                - Pitch Condition Evolution: [time intervals and pitch descriptions]
                
            Format the response with clear sections and bullet points.
            Keep the analysis professional and cricket-focused.
            """
            
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(analysis_prompt)
                
                # Process the AI response to create better visual structure
                analysis_text = response.text
                
        
                # Split into sections if possible
                sections = analysis_text.split('\n\n')
                
                for section in sections:
                    content = section.replace("1. ", "").replace("2. ", "").replace("3. ", "").replace("4. ", "")
                    content = content.replace("Current Match Situation:", "").replace("Key Factors:", "").replace("Tactical Recommendations:", "").replace("Weather Impact:", "")
                    
                    if 'Current Match Situation' in section:
                        st.markdown(f'''
                        <div class="analysis-point">
                            <h4>📌 Current Match Situation</h4>
                            <div class="content">
                                {content.replace("•", "<span class='bullet'>•</span>")}
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                    elif 'Key Factors' in section:
                        st.markdown(f'''
                        <div class="analysis-point">
                            <h4>🔑 Key Factors Influencing Outcome</h4>
                            <div class="content">
                                {content.replace("•", "<span class='bullet'>•</span>")}
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                    elif 'Tactical Recommendations' in section:
                        st.markdown(f'''
                        <div class="tactical-box">
                            <h4>🎯 Tactical Recommendations</h4>
                            <div class="content">
                                {content.replace("•", "<span class='bullet'>•</span>")}
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                    elif 'Weather Impact' in section:
                        st.markdown(f'''
                        <div class="highlight-box">
                            <h4>🌦️ Weather & Pitch Impact</h4>
                            <div class="content">
                                {content.replace("•", "<span class='bullet'>•</span>")}
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                    else:
                        st.markdown(f'<div class="ai-analysis">{section}</div>', unsafe_allow_html=True)
                            
            except Exception as e:
                    st.error(f"Couldn't generate analysis: {str(e)}")
            
else:
    # Show before prediction is made
    st.info("Configure match parameters and click 'Predict Probability' to see detailed analysis")

# Add some space at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)

