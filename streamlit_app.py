import streamlit as st
import json
import re
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.agent.agent import agent


# Page Configuration
st.set_page_config(
    page_title="CommentAnalyzer AI Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.title("🤖Customer Support AI Agent")
    st.caption("Autonomous AI Customer Support & Moderation")
    st.divider()

    st.markdown("### System Status")
    st.success("🟢 System Online & Connected")

    st.divider()
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.rerun()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_input" not in st.session_state:
    st.session_state.query_input = ""

# ---------------------------------------------------------
# Header & Quick Samples
# ---------------------------------------------------------
st.title("Smart Customer Support & Moderation AI Agent")
st.write("Enter comments, customer complaints, or product availability questions below.")

st.markdown("##### Sample Inputs")
c1, c2, c3, c4 = st.columns(4)

if c1.button("📱 Check iPhone 15", use_container_width=True):
    st.session_state.query_input = "is iPhone 15 available?"

if c2.button("📦 Order Damaged", use_container_width=True):
    st.session_state.query_input = "my order arrived damaged"

if c3.button("🔍 Product ID 101", use_container_width=True):
    st.session_state.query_input = "check product id 101"

if c4.button("⚠️ Spam Moderation", use_container_width=True):
    st.session_state.query_input = "Buy cheap followers now at spam-link.com!"

# Input Form
with st.form(key="inquiry_form", clear_on_submit=False):
    user_query = st.text_area(
        "Customer Inquiry or Comment",
        value=st.session_state.query_input,
        placeholder="e.g., Is iPhone 15 available? or My order arrived damaged...",
        height=100
    )
    submitted = st.form_submit_button("Run Agent", type="primary", use_container_width=True)


# Helper Functions to parse results
def parse_json_safely(text):

    if isinstance(text, list):
        text = text[0].get("text", "")

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:
        return json.loads(match.group())

    return {
        "status": "error",
        "message": "Invalid JSON response"
    }


def render_product_card(product_data, message=None):
    st.subheader("📦 Product Information")
    if message:
        st.info(message)
    
    col_a, col_b, col_c = st.columns(3)
    
    name = product_data.get("name", "N/A")
    price = product_data.get("price", "N/A")
    if isinstance(price, dict):
        currency = price.get("currency", "")
        amount = price.get("amount", "")
        price_str = f"{currency} {amount}"
    else:
        currency = product_data.get("currency", "PKR")
        price_str = f"{currency} {price}"
        
    stock = product_data.get("stock_quantity", product_data.get("stock", "N/A"))
    availability = product_data.get("availability", "Unknown")

    with col_a:
        st.metric(label="Product Name", value=str(name))
    with col_b:
        st.metric(label="Price", value=str(price_str))
    with col_c:
        st.metric(label="Stock & Availability", value=f"{stock} units ({availability})")

    st.markdown("---")
    
    desc = product_data.get("description", "")
    if desc:
        st.markdown(f"**Description:** {desc}")

    url = product_data.get("product_url", "")
    if url:
        st.link_button("🌐 Open Product Link", url)


def render_moderation_card(analysis_data, action_taken, reply_text):
    st.subheader("🛡️ Social Media Moderation & Support Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    category = analysis_data.get("category", "N/A")
    sentiment = analysis_data.get("sentiment", "N/A")
    risk_level = analysis_data.get("risk_level", "N/A")
    
    with col1:
        st.metric(label="Category / Intent", value=str(category))
    with col2:
        st.metric(label="Sentiment", value=str(sentiment))
    with col3:
        st.metric(label="Risk Level", value=str(risk_level))
    with col4:
        st.metric(label="Action Taken", value=str(action_taken).upper())

    st.markdown("---")
    if reply_text:
        st.markdown("#### Generated Customer Reply")
        st.success(reply_text)


# Agent Execution
if submitted and user_query.strip():
    st.markdown("---")
    st.subheader("Agent Workflow & Response")

    status_box = st.status("Initializing Agent...", expanded=True)
    status_box.write("📥 **Step 1: User Input Received**")
    
    step2_done = False
    step3_done = False
    step4_done = False

    tool_calls = []
    tool_results = {}
    final_response_text = ""

    try:
        for chunk in agent.stream({"messages": [HumanMessage(content=user_query)]}):
            for node_name, data in chunk.items():
                if "messages" in data:
                    for msg in data["messages"]:
                        if isinstance(msg, AIMessage):
                            if not step2_done:
                                status_box.write("🧠 **Step 2: Intent Classification & Reasoning**")
                                step2_done = True
                            
                            if msg.tool_calls:
                                if not step3_done:
                                    status_box.write("🔧 **Step 3: Tool Selection**")
                                    step3_done = True
                                for tool in msg.tool_calls:
                                    tool_name = tool.get("name", "tool")
                                    tool_calls.append(tool_name)
                                    status_box.write(f"⚙️ Executing `{tool_name}`...")

                            if msg.content:
                                final_response_text = msg.content

                        elif isinstance(msg, ToolMessage):
                            if not step4_done:
                                status_box.write("📊 **Step 4: Database Search / Comment Analysis**")
                                step4_done = True
                            
                            parsed_tool_res = parse_json_safely(msg.content)
                            tool_results[msg.name] = parsed_tool_res if parsed_tool_res else msg.content

        status_box.write("✅ **Step 5: Final Response Generated**")
        status_box.update(label="Workflow Complete", state="complete", expanded=False)

    except Exception as e:
        status_box.update(label=f"Execution Failed: {str(e)}", state="error", expanded=True)
        st.error(f"Error during agent execution: {e}")

    # Render Results Section
    st.markdown("### Agent Output")

    # 1. Product Query Result Check
    product_data = None
    if "product_search_tool" in tool_results:
        p_res = tool_results["product_search_tool"]
        if isinstance(p_res, dict):
            if p_res.get("status") == "success" and "product" in p_res:
                product_data = p_res["product"]

    final_json = parse_json_safely(final_response_text)
    if not product_data and final_json and isinstance(final_json, dict):
        resp = final_json.get("response", {})
        if "product_details" in resp:
            product_data = resp["product_details"]

    if product_data:
        message = None
        if final_json and isinstance(final_json, dict):
            message = final_json.get("response", {}).get("message")
        render_product_card(product_data, message=message)

    # 2. Moderation & Support Check
    elif "analyze_comment_tool" in tool_results:
        analysis_data = tool_results.get("analyze_comment_tool", {})
        if not isinstance(analysis_data, dict):
            analysis_data = {}
        
        action_taken = "Analyzed"
        reply_text = ""
        
        if "reply_tool" in tool_results:
            action_taken = "Reply Generated"
            r_tool = tool_results["reply_tool"]
            if isinstance(r_tool, dict):
                reply_text = r_tool.get("reply", "")
            elif isinstance(r_tool, str):
                reply_text = r_tool
        elif "delete_tool" in tool_results:
            action_taken = "Comment Deleted"
        elif "hide_tool" in tool_results:
            action_taken = "Comment Hidden"
        elif "escalate_tool" in tool_results:
            action_taken = "Escalated to Human Moderator"
        elif "ignore_tool" in tool_results:
            action_taken = "Ignored (No Action Required)"

        if not reply_text and final_response_text:
            if "Reply:" in final_response_text:
                reply_text = final_response_text.split("Reply:")[-1].strip()
            elif not final_json:
                reply_text = final_response_text

        render_moderation_card(analysis_data, action_taken, reply_text)

    # 3. Generic Text Response Fallback
    else:
        if final_json:
            st.json(final_json)
        elif final_response_text:
            st.info(final_response_text)
        else:
            st.warning("No response generated.")
