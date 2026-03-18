import uuid

from langchain_core.messages import HumanMessage


def run_agent(agent, user_message: str, thread_id: str | None = None) -> str:
    """Run an agent synchronously with one user message and pretty-print updates."""
    if thread_id is None:
        thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    for update in agent.stream(
        {"messages": [HumanMessage(user_message)]},
        config=config,
        stream_mode="updates",
    ):
        for _, step_output in update.items():
            if "messages" in step_output:
                step_output["messages"][-1].pretty_print()

    return thread_id


async def arun_agent(agent, user_message: str, thread_id: str | None = None) -> str:
    """Run an agent asynchronously with one user message and pretty-print updates."""
    if thread_id is None:
        thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    async for update in agent.astream(
        {"messages": [HumanMessage(user_message)]},
        config=config,
        stream_mode="updates",
    ):
        for _, step_output in update.items():
            if "messages" in step_output:
                step_output["messages"][-1].pretty_print()

    return thread_id
