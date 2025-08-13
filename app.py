import streamlit as st
from researcher import (
    Researcher,
    create_user_database_path,
    validate_openai_api_key,
    validate_exa_api_key,
)


# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Initialize session state
def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""

    if "exa_api_key" not in st.session_state:
        st.session_state.exa_api_key = ""

    if "researcher" not in st.session_state:
        st.session_state.researcher = None

    if "research_agent" not in st.session_state:
        st.session_state.research_agent = None

    if "memory_agent" not in st.session_state:
        st.session_state.memory_agent = None

    if "research_messages" not in st.session_state:
        st.session_state.research_messages = []

    if "memory_messages" not in st.session_state:
        st.session_state.memory_messages = []


def show_login_form():
    """Display the login/setup form for new users."""
    st.markdown(
        '<h1 class="main-header">🔬 Research Agent with Memory</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Your intelligent research assistant that remembers everything</p>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### 👤 Welcome! Please enter your details to get started:")

    # Create two columns for better layout
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### User Information")
        username = st.text_input(
            "Your Name",
            placeholder="Enter your name (e.g., John Doe)",
            help="This will create a personalized database for your research sessions",
        )

        st.markdown("#### API Configuration")
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Your OpenAI API key is needed for AI-powered research. Get one at https://platform.openai.com/api-keys",
        )

        exa_api_key = st.text_input(
            "Exa API Key",
            type="password",
            placeholder="Your Exa API key",
            help="Your Exa API key is needed for web research. Get one at https://exa.ai",
        )

        # Validation and submit
        submit_button = st.button("🚀 Start My Research Journey", type="primary")

        if submit_button:
            # Validate inputs
            if not username.strip():
                st.error("❌ Please enter your name")
                return False

            if not openai_api_key.strip():
                st.error("❌ Please enter your OpenAI API key")
                return False

            if not exa_api_key.strip():
                st.error("❌ Please enter your Exa API key")
                return False

            if not validate_openai_api_key(openai_api_key):
                st.error(
                    "❌ Please enter a valid OpenAI API key (should start with 'sk-')"
                )
                return False

            if not validate_exa_api_key(exa_api_key):
                st.error("❌ Please enter a valid Exa API key")
                return False

            # Store in session state
            st.session_state.username = username.strip()
            st.session_state.openai_api_key = openai_api_key.strip()
            st.session_state.exa_api_key = exa_api_key.strip()

            # Initialize researcher with memory
            try:
                database_path = create_user_database_path(username.strip(), "streamlit")

                with st.spinner("Initializing Research Assistant with Memory..."):
                    st.session_state.researcher = Researcher(
                        database_path=database_path,
                        openai_api_key=openai_api_key.strip(),
                        exa_api_key=exa_api_key.strip(),
                    )
                    st.session_state.research_agent = (
                        st.session_state.researcher.get_research_agent()
                    )
                    st.session_state.memory_agent = (
                        st.session_state.researcher.get_memory_agent()
                    )

                st.session_state.authenticated = True
                st.success(f"✅ Welcome {username}! Your research assistant is ready.")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error initializing your research assistant: {str(e)}")
                return False

    with col2:
        st.markdown("#### 🔬 What you'll get:")
        st.markdown("""
        - **🧠 Advanced Memory**: AI that remembers and learns from your research sessions
        - **🔍 Real-time Research**: Comprehensive web research using Exa
        - **📊 Pattern Analysis**: Understand your research interests and topics
        - **🎯 Personalized Insights**: Get recommendations based on your research history
        - **📈 Research History**: Visual analytics and insights
        - **🔒 Privacy First**: Your data stays secure and private
        - **🌱 Knowledge Building**: Build upon previous research sessions
        """)

        st.markdown("#### 🔑 About Your API Keys:")
        st.markdown("""
        - Your API keys are used to power the AI and research features
        - They're stored securely in your session only
        - We don't store or share your API keys
        - **OpenAI**: Get your free key at [OpenAI Platform](https://platform.openai.com/api-keys)
        - **Exa**: Get your key at [Exa.ai](https://exa.ai)
        """)

        st.markdown("#### 📱 Multi-Device Access:")
        st.markdown("""
        - Use the same name to access your research from any device
        - Your research sessions are saved in a personal database
        - Consistent experience across all your sessions
        """)

    return False


def show_user_info():
    """Display current user info in sidebar."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 Current User")
        st.markdown(f"**Name:** {st.session_state.username}")
        st.markdown(
            f"**Database:** `{create_user_database_path(st.session_state.username, 'streamlit')}`"
        )

        if st.button("🚪 Logout", help="Clear session and return to login"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def show_main_app():
    """Show the main application interface for authenticated users."""
    st.title("🔬 Research Agent with Persistent Memory")
    st.markdown("### AI Research Assistant that Remembers Everything")

    # Show user info in sidebar
    show_user_info()

    # Sidebar with navigation and info
    with st.sidebar:
        st.header("Navigation")
        tab_choice = st.radio(
            "Choose Mode:", ["🔬 Research Chat", "🧠 Memory Chat"], key="tab_choice"
        )

        st.header("About This Demo")
        st.markdown(
            f"""
        This demo showcases:
        - **Research Agent**: Uses Exa for real-time web research
        - **Memori Integration**: Remembers all research sessions
        - **Memory Chat**: Query your research history
        - **User:** {st.session_state.username}

        The research agent can:
        - 🔍 Conduct comprehensive research using Exa
        - 🧠 Remember all previous research 
        - 📚 Build upon past research
        - 💾 Store findings for future reference
        """
        )

        st.header("Research History")
        if st.button("🗑️ Clear All Memory", type="secondary"):
            import sqlite3

            db_path = create_user_database_path(st.session_state.username, "streamlit")
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                # Drop all tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                for table in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
                conn.commit()
                conn.close()
                st.success("Research memory cleared!")
            except Exception as e:
                st.error(f"Error clearing memory: {e}")

    # Research Chat Tab
    if tab_choice == "🔬 Research Chat":
        st.header("🔬 Research Agent")
        st.markdown(
            "*Ask me to research any topic and I'll create comprehensive reports while remembering everything!*"
        )

        # Display research chat messages
        for message in st.session_state.research_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Research chat input
        if research_prompt := st.chat_input("What would you like me to research?"):
            st.session_state.research_messages.append(
                {"role": "user", "content": research_prompt}
            )
            with st.chat_message("user"):
                st.markdown(research_prompt)
            with st.chat_message("assistant"):
                with st.spinner("🔍 Conducting research and searching memory..."):
                    try:
                        response = st.session_state.researcher.run_agent_with_memory(
                            st.session_state.research_agent, research_prompt
                        )
                        st.markdown(response.content)
                        st.session_state.research_messages.append(
                            {"role": "assistant", "content": response.content}
                        )
                    except Exception as e:
                        error_message = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_message)
                        st.session_state.research_messages.append(
                            {"role": "assistant", "content": error_message}
                        )

        # Research example prompts
        if not st.session_state.research_messages:
            st.markdown("### 🔬 Example Research Topics:")
            col1, col2 = st.columns(2)

            def set_research_chat_input(prompt):
                st.session_state.research_chat_quick_input = prompt

            with col1:
                if st.button("🧠 Brain-Computer Interfaces"):
                    set_research_chat_input(
                        "Research the latest developments in brain-computer interfaces"
                    )
                if st.button("🔋 Solid-State Batteries"):
                    set_research_chat_input(
                        "Analyze the current state of solid-state batteries"
                    )

            with col2:
                if st.button("🧬 CRISPR Gene Editing"):
                    set_research_chat_input(
                        "Research recent breakthroughs in CRISPR gene editing"
                    )
                if st.button("🚗 Autonomous Vehicles"):
                    set_research_chat_input(
                        "Investigate the development of autonomous vehicles"
                    )

            # If a quick action was selected, simulate chat input
            if st.session_state.get("research_chat_quick_input"):
                quick_prompt = st.session_state.pop("research_chat_quick_input")
                st.session_state.research_messages.append(
                    {"role": "user", "content": quick_prompt}
                )
                with st.chat_message("user"):
                    st.markdown(quick_prompt)
                with st.chat_message("assistant"):
                    with st.spinner("🔍 Conducting research and searching memory..."):
                        try:
                            response = (
                                st.session_state.researcher.run_agent_with_memory(
                                    st.session_state.research_agent, quick_prompt
                                )
                            )
                            st.markdown(response.content)
                            st.session_state.research_messages.append(
                                {"role": "assistant", "content": response.content}
                            )
                        except Exception as e:
                            error_message = f"Sorry, I encountered an error: {str(e)}"
                            st.error(error_message)
                            st.session_state.research_messages.append(
                                {"role": "assistant", "content": error_message}
                            )

    # Memory Chat Tab
    elif tab_choice == "🧠 Memory Chat":
        st.header("🧠 Research Memory Assistant")
        st.markdown(
            "*Ask me about your previous research sessions and I'll help you recall everything!*"
        )

        # Display memory chat messages
        for message in st.session_state.memory_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Memory chat input
        if memory_prompt := st.chat_input(
            "What would you like to know about your research history?"
        ):
            st.session_state.memory_messages.append(
                {"role": "user", "content": memory_prompt}
            )
            with st.chat_message("user"):
                st.markdown(memory_prompt)
            with st.chat_message("assistant"):
                with st.spinner("🧠 Searching through your research history..."):
                    try:
                        response = st.session_state.memory_agent.run(memory_prompt)
                        st.markdown(response.content)
                        st.session_state.memory_messages.append(
                            {"role": "assistant", "content": response.content}
                        )
                    except Exception as e:
                        error_message = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_message)
                        st.session_state.memory_messages.append(
                            {"role": "assistant", "content": error_message}
                        )

        # Memory example prompts
        if not st.session_state.memory_messages:
            st.markdown("### 🧠 Example Memory Queries:")
            col1, col2 = st.columns(2)

            def set_memory_chat_input(prompt):
                st.session_state.memory_chat_quick_input = prompt

            with col1:
                if st.button("📋 What were my last research topics?"):
                    set_memory_chat_input("What were my last research topics?")
                if st.button("🔍 Show my research on AI"):
                    set_memory_chat_input(
                        "Show me all my previous research related to artificial intelligence"
                    )

            with col2:
                if st.button("📊 Summarize my research history"):
                    set_memory_chat_input(
                        "Can you summarize my research history and main findings?"
                    )
                if st.button("🧬 Find my biotech research"):
                    set_memory_chat_input(
                        "Find all my research related to biotechnology and gene editing"
                    )

            # If a quick action was selected, simulate chat input
            if st.session_state.get("memory_chat_quick_input"):
                quick_prompt = st.session_state.pop("memory_chat_quick_input")
                st.session_state.memory_messages.append(
                    {"role": "user", "content": quick_prompt}
                )
                with st.chat_message("user"):
                    st.markdown(quick_prompt)
                with st.chat_message("assistant"):
                    with st.spinner("🧠 Searching through your research history..."):
                        try:
                            response = st.session_state.memory_agent.run(quick_prompt)
                            st.markdown(response.content)
                            st.session_state.memory_messages.append(
                                {"role": "assistant", "content": response.content}
                            )
                        except Exception as e:
                            error_message = f"Sorry, I encountered an error: {str(e)}"
                            st.error(error_message)
                            st.session_state.memory_messages.append(
                                {"role": "assistant", "content": error_message}
                            )


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Research Agent with Memory", page_icon="🔬", layout="wide"
    )

    initialize_session_state()

    # Check if user is authenticated
    if not st.session_state.authenticated:
        show_login_form()
        return

    # Show main application for authenticated users
    show_main_app()


if __name__ == "__main__":
    main()
