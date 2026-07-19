from langchain_core.tools import tool
from app.llm.model import llm
from app.prompts.reply_prompt import REPLY_PROMPT

@tool
def reply_tool(comment: str) -> str:
    """
    Generate a professional reply to a social media comment.
    """
    print("\nReply Tool Executed\n")
    prompt = REPLY_PROMPT.format(comment=comment)
    response = llm.invoke(prompt)
    reply = response.content

    return f""" Reply Generated Successfully

Reply:
{reply}
"""

@tool
def analyze_comment_tool(comment: str) -> str:
    """
    Analyze a social media comment and provide insights
    about sentiment, category, and risk level.
    """

    print("\nAnalyze Comment Tool Executed\n")

    analysis_prompt = f"""
Analyze this social media comment.

Comment:
{comment}

Return:

Sentiment:
Category:
Risk Level:

Possible categories:
- Complaint
- Question
- Positive Feedback
- Spam
- Hate Speech
- Abuse
- Other

Do not decide the action.
Only provide analysis.
"""

    response = llm.invoke(analysis_prompt)

    return response.content

@tool
def delete_tool(comment: str) -> str:
    """
    Delete a harmful comment.
    """
    print("\nDelete Tool Executed\n")

    return "Comment deleted successfully."


@tool
def hide_tool(comment: str) -> str:
    """
    Hide a comment from public view.
    """
    print("\nHide Tool Executed\n")

    return "Comment hidden successfully."


@tool
def escalate_tool(comment: str) -> str:
    """
    Escalate the comment to a human moderator.
    """
    print("\nEscalate Tool Executed\n")

    return "Escalated to a human moderator."


@tool
def ignore_tool() -> str:
    """
    Ignore the comment when no action is required.
    """
    print("\nIgnore Tool Executed\n")

    return "No action taken."