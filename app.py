import streamlit as st
import requests


def get_backend_url(role):
    """
    Maps user roles to specific FastAPI backend endpoints.
    For C-Level, the frontend will send the *selected sub-role* (e.g., 'finance'),
    so the backend will receive '/query' with the actual sub-role.
    """
    # Note: The backend expects specific individual roles like 'finance', 'engineering', etc.
    # The 'C-Level Executives' string itself is not sent to the backend for a query.
    return "http://127.0.0.1:8000/query" # All queries go to the same /query endpoint on backend


# Page configuration for the Streamlit application
st.set_page_config(
    page_title="FinSolve Technologies",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded for C-Level by default
)


# ---- Custom CSS for styling the entire application ----
# This block defines the visual theme, including fonts, colors, gradients,
# button styles, card designs, and responsiveness.
st.markdown("""
<style>
    /* Global settings for body and font */
    body {
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #e0e0e0; /* Light grey text */
        background-color: #0a0f0a; /* Dark background */
    }
    
    /* This CSS will only apply when st.sidebar is actively rendered by Streamlit */
    .stSidebar {
        background: linear-gradient(180deg, #0a0f0a 0%, #0d1f0d 100%); /* Dark to slightly lighter dark gradient */
        position: fixed; /* Make it fixed on scroll */
        right: 0; /* Align to the right edge */
        left: auto !important; /* Override default left alignment */
        width: 300px; /* Set a fixed width for the sidebar */
        height: 100vh; /* Make it full viewport height */
        overflow-y: auto; /* Enable scrolling if content overflows */
        padding-top: 20px; /* Adjust padding if needed */
        box-shadow: -5px 0 15px rgba(0, 0, 0, 0.3); /* Shadow on the left side to give depth */
        z-index: 999; /* Ensure it stays on top of other content */
    }
            
    .main {
        margin-right: 0; /* No right margin for now, as sidebar is expanded on some pages */
        margin-left: 0 !important; /* Ensure no left margin from default sidebar */
        max-width: 100% !important; /* Use full width */
    }

    .main .block-container {
        background: #0a0f0a; /* Changed to solid dark background */
        padding: 2rem;
        border-radius: 1rem;
        max-width: 100% !important; /* Ensure full width usage */
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #10b981; /* Bright green for headers */
        font-weight: 600;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #059669 0%, #10b981 100%); /* Green gradient button */
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 20px;
        font-weight: 500;
        transition: all 0.3s ease; /* Smooth transition for hover effects */
        box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3); /* Subtle shadow */
    }
    .stButton > button:hover {
        transform: translateY(-2px); /* Lift button on hover */
        box-shadow: 0 6px 15px rgba(16, 185, 129, 0.4); /* Enhanced shadow on hover */
    }
    
    /* User Input (text area) styling */
    .stTextArea > div > div {
        background-color: #0d1f0d;
        color: #e0e0e0;
        border: 1px solid #333;
        border-radius: 10px;
    }
    .stTextArea > div > div:focus-within {
        border-color: #059669; /* Green border on focus */
    }
    
    /* Hide default Streamlit branding and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* New CSS for sticky header in chat room */
    .sticky-header-container {
        position: sticky;
        top: 0;
        background: #0a0f0a; /* Solid background to prevent content showing through */
        z-index: 100; /* Ensure it stays above chat messages */
        padding-top: 1rem;
        padding-bottom: 1rem;
        margin-bottom: 1rem; /* Add some space below the header */
        border-bottom: 1px solid #333; /* Optional: a subtle separator */
        width: 100%; /* Ensure it spans full width */
        left: 0; /* Align to left edge */
        box-sizing: border-box; /* Include padding/border in the element's total width and height */
    }""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'role' not in st.session_state:
    st.session_state.role = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
# New session state variable to track the previously selected *primary* role
if "previous_primary_role" not in st.session_state:
    st.session_state.previous_primary_role = None


def render_role_cards():
    """
    Renders interactive cards for different user roles on the home screen.
    Each card displays an icon, title, and a button to select that role.
    Includes custom CSS for visual effects and responsiveness.
    """
    
    # Additional CSS specifically for role cards to provide interactive effects
    st.markdown("""
    <style>
        .roles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); /* Responsive grid */
            gap: 1.3rem;
            padding: 2rem 0;
            margin-top: 2rem;
        }
        
        .role-card {
            background: linear-gradient(145deg, #0d1f0d, #1a4d1a); /* Gradient background */
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.4s ease; /* Smooth transitions for hover effects */
            border: 2px solid transparent; /* Transparent border, becomes green on hover */
            box-shadow: 0 8px 45px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            height: 150px; /* Fixed height for consistent card size */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .role-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #059669, #10b981, #34d399); /* Top border gradient */
            transform: scaleX(0); /* Hidden by default */
            transition: transform 0.4s ease; /* Animation for top border */
        }
        
        .role-card:hover {
            transform: translateY(-25px); /* Lift card on hover */
            border-color: #059669; /* Green border on hover */
            box-shadow: 0 20px 50px rgba(5, 150, 105, 0.5); /* Enhanced shadow on hover */
            z-index: 10;
        }
        
        .role-card:hover::before {
            transform: scaleX(1); /* Show top border on hover */
        }
        
        .role-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
            filter: drop-shadow(0 4px 8px rgba(16, 185, 129, 0.3)); /* Icon shadow */
        }
        
        .role-title {
            color: #10b981;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .role-button {
            background: linear-gradient(45deg, #059669, #10b981);
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            width: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .role-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent); /* Shimmer effect */
            transition: left 0.5s;
        }
        
        .role-button:hover::before {
            left: 100%; /* Move shimmer across button */
        }
        
        .role-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(5, 150, 105, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Data for each role card
    roles_data = [
        {
            'role': 'C-Level Executives',
            'icon': '🏆',
            'title': 'C-Level Employee Management'
        },
        {
            'role': 'Finance Team',
            'icon': '💰',
            'title': 'Financial Department'
        },
        {
            'role': 'Marketing Team',
            'icon': '📈',
            'title': 'Marketing Team'
        },
        {
            'role': 'HR Team',
            'icon': '👥',
            'title': 'Human Resources Department'
        },
        {
            'role': 'Engineering Department',
            'icon': '⚙️',
            'title': 'Engineering Department'
        },
        {
            'role': 'General', # Consistent with backend role name
            'icon': '👤',
            'title': 'General Department Employee'
        }
    ]
    
    # Create columns for a responsive grid layout
    cols = st.columns(3) # Display 3 cards per row on wider screens
    
    for i, role_data in enumerate(roles_data):
        with cols[i % 3]: # Distribute cards evenly across columns
            # Render the role card HTML structure
            st.markdown(f"""
            <div class="role-card" style="text-align: center; padding: 2rem; background: linear-gradient(145deg, #0d1f0d, #1a4d1a); 
                        border-radius: 15px; margin: 1rem 0; height: 200px; display: flex; flex-direction: column; 
                        justify-content: center; align-items: center; transition: all 0.4s ease; border: 2px solid transparent;
                        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);"
                   onmouseover="this.style.transform='translateY(-10px)'; this.style.borderColor='#059669'; this.style.boxShadow='0 15px 40px rgba(5, 150, 105, 0.4)';"
                   onmouseout="this.style.transform='translateY(0px)'; this.style.borderColor='transparent'; this.style.box-shadow='0 8px 25px rgba(0, 0, 0, 0.3)';">
                    <div style="font-size: 3rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 8px rgba(16, 185, 129, 0.3));">
                        {role_data['icon']}
                    </div>
                    <h3 style="color: #10b981; font-size: 1.3rem; margin-bottom: 1.5rem; text-transform: uppercase; 
                                font-weight: 700; letter-spacing: 1px;">
                        {role_data['title']}
                    </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Button to select the role
            if st.button(f"Access {role_data['title']}", key=f"role_{i}", help=f"Login as {role_data['role']}"):
                st.session_state.role = role_data['role']
                # When a primary role is selected from the home screen, reset previous_primary_role
                st.session_state.previous_primary_role = st.session_state.role
                # Clear c_level_sub_role_display if it exists and we're not entering C-Level
                if "c_level_sub_role_display" in st.session_state and st.session_state.role != "C-Level Executives":
                    del st.session_state.c_level_sub_role_display
                st.rerun() # Rerun the app to switch to the chat room


def get_ai_response(prompt, role_for_backend):
    """
    Sends a query to the backend AI endpoint with the specified role and retrieves the AI's response.
    The `role_for_backend` parameter should be the actual lowercase role string (e.g., "finance", "general")
    that the backend expects.
    """
    url = get_backend_url(role_for_backend) # All queries go to the same /query endpoint

    payload = {
        "role": role_for_backend, # This is the role string like "finance", "general" etc.
        "query": prompt
    }

    try:
        response = requests.post(url, json=payload, timeout=60) # Send POST request with JSON payload
        if response.status_code == 200:
            return response.json().get("response", "No response from backend.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error contacting backend: {e}"


def render_home_screen():
    """
    Renders the main landing page of the application, including the company branding
    and an introductory section.
    """
    st.markdown("""
    <style>
        /* Header bar for company logo and name */
        .header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            position: relative;
        }

        /* Styling for the logo icon */
        .logo-icon {
            font-size: 4.5rem;
            position: absolute;
            left: 10rem;
            top: 1rem;
            align-self: center;
            color: #00f5d4; /* Teal color for the icon */
        }

        /* Styling for the company name */
        .company-name {
            font-size: 5.5rem;
            font-weight: bold;
            color: #ffffff;
            margin: 0 auto;
            text-align: center;
            width: 100%;
            font-family: 'Poppins', sans-serif, 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Styling for the company tagline */
        .company-tagline {
            text-align: center;
            color: #00f5d4;
            font-size: 1.5rem;
            margin-top: -10px;
            font-style: italic;
        }

        /* Main heading on the home screen */
        .main-heading {
            text-align: center;
            font-size: 2.8rem;
            color: #00f5d4;
            margin: 2rem 0 1.5rem 0;
        }

        /* Container for introductory text and image */
        .intro-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 3rem;
            padding: 2rem;
            flex-wrap: wrap; /* Allows wrapping on smaller screens */
        }

        /* Styling for introductory text */
        .intro-text {
            flex: 1;
            max-width: 600px;
            color: #ddd;
            font-size: 1.3rem;
            line-height: 1.6;
            text-align: left;
        }

        /* Styling for introductory image container */
        .intro-image {
            flex: 1;
            max-width: 400px;
            align-self: right;
        }
                
        .intro-image:hover {
        transform: translateY(-10px); /* Lift button on hover */
        box-shadow: 0 6px 15px rgba(16, 185, 129, 0.4); /* Enhanced shadow on hover */
        }

        /* Styling for the intro image */
        .intro-image img {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 0 95px rgba(0, 245, 212, 0.15); /* Subtle teal shadow */
        }

        /* Section title for role selection */
        .section-title {
            text-align: center;
            color: #fff;
            font-size: 3.5rem;
            margin-top: 2rem;
        }
    </style>

    <div class="header-bar">
        <div class="logo-icon">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAyE0D894-Jl4_o_ZM02H9Vy4RoIyo8C4gLw&s" alt="Finsolve Logo" style="height: 80px;" />
        </div>
        <div class="company-name">Finsolve</div>
    </div>
    <div class="company-tagline">---&nbsp; Be the financial fit</div>

    <h2 class="main-heading">Strategic Finance For Sustainable<br>Business Expansion</h2>

    <div class="intro-container">
        <div class="intro-text">
            <p>FinSolve Technologies is a leading FinTech company providing innovative financial solutions and services to individuals, businesses, and enterprises.</p>
            <p>
                Our AI-driven internal chatbot is built to empower teams across departments by delivering
                accurate, role-specific insights in real-time. Whether you're from Finance, Marketing, HR, or Engineering —
                FinSolve ensures that the data you need is always at your fingertips.
            </p>
            <p>
                Skip the delays, break the silos. With cutting-edge retrieval-augmented generation (RAG) technology,
                this platform transforms the way employees interact with organizational data — securely, intelligently, and instantly.
            </p>
        </div>
        <div class="intro-image">
            <img src="https://images.jdmagicbox.com/comp/kolkata/j7/033pxx33.xx33.210424102113.l7j7/catalogue/finsolve-solutions-haridevpur-kolkata-income-tax-consultants-4w8tf5a6ho-250.jpg" alt="FinSolve Intro Image" />
        </div>
    </div>

    <div class="roles-section"><h2 id="choose-your-role-section" class="section-title">Choose Your Role</h2></div>
    """, unsafe_allow_html=True)


def get_role_icon(role):
    """Returns an emoji icon for the given role."""
    icons = {
        'C-Level Executives': '🏆',
        'Finance Team': '�',
        'Marketing Team': '📈',
        'HR Team': '👥',
        'Engineering Department': '⚙️',
        'General': '👤' # Using 'General' as the role key
    }
    return icons.get(role, '👤') # Default to a generic user icon

def get_role_description(role):
    """Returns a brief description for the given role."""
    desc = {
        'C-Level Executives': "Strategic insights and executive decision support across all departments.",
        'Finance Team': "Financial analysis, reporting, and compliance assistance.",
        'Marketing Team': "Marketing analytics and campaign optimization.",
        'HR Team': "Human resources management and employee engagement.",
        'Engineering Department': "Technical support and project management.",
        'General': "General queries and support for all employees." # Using 'General' as the role key
    }
    return desc.get(role, "")

def render_chat_room():
    """
    Renders the chat interface for the selected role.
    Allows users to switch roles and interact with the AI assistant.
    Includes special handling for C-Level executives with a sub-department dropdown.
    """
    current_primary_role = st.session_state.role

    # Check if the primary role has changed to clear chat history, but persist for C-Level sub-role changes
    if st.session_state.previous_primary_role is None:
        # First time entering chat, set previous_primary_role
        st.session_state.previous_primary_role = current_primary_role
    elif current_primary_role != st.session_state.previous_primary_role:
        # If the primary role *has* changed (e.g., Finance to HR, or HR to C-Level)
        st.session_state.messages = [] # Clear history
        # If transitioning *into* C-Level, initialize its sub-role dropdown
        if current_primary_role == "C-Level Executives":
            st.session_state.c_level_sub_role_display = "Finance Team" 
        # Clear c_level_sub_role_display if transitioning *out of* C-Level
        elif "c_level_sub_role_display" in st.session_state:
            del st.session_state.c_level_sub_role_display
        st.session_state.previous_primary_role = current_primary_role # Update previous role
        st.rerun() # Rerun to apply changes

    # Define roles for display and their backend mapping
    roles_for_backend_map = {
        "Finance Team": "finance",
        "Marketing Team": "marketing",
        "HR Team": "hr",
        "Engineering Department": "engineering",
        "General": "general"
    }
    
    # These are the display names for the dropdown, C-Level uses these to select
    c_level_sub_roles_display = [
        "Finance Team", "Marketing Team", "HR Team", 
        "Engineering Department", "General"
    ]

    actual_backend_role_to_send = "" # This will be the lowercase role string sent to backend
    display_role_for_header = current_primary_role # Default header display is the primary role

    # --- Conditional rendering of controls (sidebar for C-Level, main content for others) ---
    if current_primary_role == "C-Level Executives":
        with st.sidebar:
            # C-Level sub-role dropdown
            if "c_level_sub_role_display" not in st.session_state:
                st.session_state.c_level_sub_role_display = c_level_sub_roles_display[0] # Default to Finance

            selected_sub_role_display = st.selectbox(
                "View Department Data:", 
                c_level_sub_roles_display, 
                index=c_level_sub_roles_display.index(st.session_state.c_level_sub_role_display),
                key="c_level_sub_role_selector_fixed" # Unique key for fixed element
            )
            
            # If the selected sub-role changes, update session state and rerun
            # IMPORTANT: We do NOT clear chat history here, only on primary role change
            if selected_sub_role_display != st.session_state.c_level_sub_role_display:
                st.session_state.c_level_sub_role_display = selected_sub_role_display
                st.rerun() # Rerun to update the AI Assistant header for the selected sub-role

            # The actual role sent to backend is the lowercase mapping of the selected sub-role
            actual_backend_role_to_send = roles_for_backend_map[st.session_state.c_level_sub_role_display]
            # The header should reflect the *selected sub-department* for C-Level
            display_role_for_header = st.session_state.c_level_sub_role_display 
            
    # --- Main chat content area ---
    # Create the sticky header container
    st.markdown('<div class="sticky-header-container">', unsafe_allow_html=True)
    
    # Layout for chat header and the back button inside the sticky container
    # Reordered columns for button on left and heading on right
    chat_header_cols = st.columns([2, 8]) 

    with chat_header_cols[0]:
        # Back to Home button (always in the main chat area)
        if st.button("← Back to Home", key="back_to_home_main_area_common"): # Common key for all roles
            st.session_state.role = None # Clear the selected primary role
            st.session_state.messages = [] # Clear all chat messages
            st.rerun()
            # Also clear the C-Level specific sub-role if it exists
            if "c_level_sub_role_display" in st.session_state:
                del st.session_state.c_level_sub_role_display
            
    with chat_header_cols[1]:
        header_role_name = display_role_for_header
        header_role_icon = get_role_icon(header_role_name) 
        header_role_description = get_role_description(header_role_name)

        # Display the AI Assistant header
        st.markdown(
            f"<div class='chat-header'><h1>{header_role_icon} {header_role_name} AI Assistant</h1>"
            f"<p>{header_role_description}</p></div>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True) # Close the sticky header container
    
    st.divider() # Visual separator after the top controls and header

    # Determine the actual backend role to send for non-C-Level cases
    if current_primary_role != "C-Level Executives":
        actual_backend_role_to_send = roles_for_backend_map[current_primary_role]
        # display_role_for_header is already set correctly above for non-C-Level

    # Display an initial greeting message from the assistant if no messages exist
    # The greeting adapts to the C-Level selected sub-role or the current primary role
    if not st.session_state.messages and st.session_state.role:
        st.session_state.messages.append({
            'role': 'assistant',
            'content': f"Hello! I'm your {display_role_for_header} AI Assistant. How can I help you today?"
        })

    # Display all chat messages in chronological order
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    # Input field for user queries
    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            with st.spinner('Thinking...'): # Show a spinner while waiting for AI response
                # Pass the dynamically determined backend role (e.g., "finance", "general")
                resp = get_ai_response(prompt, actual_backend_role_to_send)
                st.markdown(resp)
        st.session_state.messages.append({'role': 'assistant', 'content': resp})

# Main application flow based on session state
if __name__ == "__main__":
    if st.session_state.role is None:
        # If no role is selected, display the home screen and role selection cards
        render_home_screen()
        render_role_cards()
    else:
        # If a role is selected, display the chat room
        render_chat_room()

