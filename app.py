import asyncio
import streamlit as st
from agents.intent_classifier import classify_intent
from agents.theory import create_theory
from agents.examples import create_examples
from agents.python_code import create_python_code
from agents.consolidater import (
    consolidate_tutorial,
    TheorySection,
    ExamplesSection,
    PythonCodeSection,
)

# Configure Streamlit page
st.set_page_config(
    page_title="Data Science Tutorial Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """Main Streamlit app function."""

    # App title
    st.title("🧠 Data Science Tutorial Generator")
    st.markdown("---")

    # Sidebar configuration
    with st.sidebar:
        st.header("ℹ️ App Information")
        st.info("""
        This app generates comprehensive data science tutorials using AI agents that work concurrently to create:
        
        - **Theory**: Detailed explanations of concepts
        - **Examples**: Real-world applications  
        - **Python Code**: Practical implementations
        
        The agents work together to consolidate everything into a complete tutorial.
        """)

        st.markdown("---")

        # Clear button
        if st.button("🗑️ Clear Session", type="secondary", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Main content area
    st.subheader("Enter a Data Science Concept")

    # Initialize concept in session state if not exists
    if "concept" not in st.session_state:
        st.session_state.concept = ""

    # Text input for concept
    concept = st.text_input(
        "What would you like to learn about?",
        value=st.session_state.concept,
        placeholder="e.g., Linear Regression, Random Forest, K-Means Clustering...",
        help="Enter any data science concept you'd like to generate a tutorial for",
        key="concept_input",
    )

    # Update session state with current value
    st.session_state.concept = concept

    # Generate button
    generate_button = st.button(
        "🚀 Generate Tutorial", type="primary", use_container_width=True
    )

    # Process the concept when button is clicked
    if generate_button and concept:
        # Initialize progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Run the async tutorial generation
        asyncio.run(generate_tutorial(concept, progress_bar, status_text))

    elif generate_button and not concept:
        st.error("⚠️ Please enter a concept to generate a tutorial.")


async def generate_tutorial(concept, progress_bar, status_text):
    """Generate tutorial content using async agents."""

    try:
        # Step 1: Intent classification
        status_text.text("🔍 Checking if concept is within data science scope...")
        progress_bar.progress(10)

        with st.spinner("Classifying intent..."):
            intent_result = await classify_intent(concept)

        if not intent_result.in_scope:
            progress_bar.progress(100)
            st.error("❌ Concept Out of Scope")
            st.warning(f"The concept '{concept}' is not within the data science scope.")
            st.info(f"**Reason:** {intent_result.reason}")
            st.info(f"**Confidence:** {intent_result.confidence:.2f}")
            return

        # Show success for intent classification
        st.success(
            f"✅ Concept is within scope! (Confidence: {intent_result.confidence:.2f})"
        )
        st.info(f"**Reason:** {intent_result.reason}")

        progress_bar.progress(25)

        # Step 2: Generate content concurrently
        status_text.text(
            "🛠️ Generating tutorial content (Theory, Examples, Python Code)..."
        )

        with st.spinner("Running AI agents concurrently..."):
            # Run all three agents concurrently
            theory_task = create_theory(concept)
            examples_task = create_examples(concept)
            python_code_task = create_python_code(concept)

            theory_result, examples_result, python_code_result = await asyncio.gather(
                theory_task, examples_task, python_code_task
            )

        st.success("✅ All content sections generated successfully!")
        progress_bar.progress(75)

        # Step 3: Consolidate the outputs
        status_text.text("🔄 Consolidating tutorial sections...")

        with st.spinner("Consolidating tutorial..."):
            # Prepare sections for consolidator
            theory_section = TheorySection(
                title=theory_result.title, body=theory_result.body
            )

            examples_section = ExamplesSection(
                title=examples_result.title, examples=examples_result.examples
            )

            python_code_section = PythonCodeSection(
                title=python_code_result.title, code=python_code_result.code
            )

            # Consolidate into final tutorial
            consolidated_result = await consolidate_tutorial(
                concept=concept,
                theory_section=theory_section,
                examples_section=examples_section,
                python_code_section=python_code_section,
            )

        st.success("✅ Tutorial consolidated successfully!")
        progress_bar.progress(100)
        status_text.text("✨ Tutorial generation completed!")

        # Step 4: Display tutorial content
        st.markdown("---")
        st.header("📚 Generated Tutorial")

        # Tutorial title and summary
        st.subheader(consolidated_result.title)
        st.info(f"**Summary:** {consolidated_result.summary}")

        # Full tutorial content
        st.markdown("### 📖 Complete Tutorial")
        st.markdown(consolidated_result.tutorial_content)

        # Download button for the tutorial
        st.download_button(
            label="📥 Download Tutorial",
            data=f"# {consolidated_result.title}\n\n**Summary:** {consolidated_result.summary}\n\n{consolidated_result.tutorial_content}",
            file_name=f"{concept.replace(' ', '_').lower()}_tutorial.md",
            mime="text/markdown",
        )

    except Exception as e:
        progress_bar.progress(0)
        status_text.text("")
        st.error(f"❌ Error during tutorial generation: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
