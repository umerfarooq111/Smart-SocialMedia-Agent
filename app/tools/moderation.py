from langchain_core.tools import tool


@tool
def reply_tool(comment: str) -> str:
    """
    Reply professionally to a customer.
    """
    print("\nReply Tool Executed\n")

    return (
        "Reply posted successfully. "
        "The customer received a professional response."
    )


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