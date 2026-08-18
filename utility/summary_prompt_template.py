from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import PromptTemplate


def load_summary_generation_prompt_value(chat: str, previous_summary: str = "") -> PromptValue:
    template = PromptTemplate(
        input_variables=["chat", "previous_summary"],
        template="""
            You are responsible for maintaining a compact rolling summary of an ongoing
            conversation.
            
            You are given two inputs:
            
            - chat: the conversation so far.
            - previous_summary: the summary generated from an earlier portion of the
              conversation. It may be empty.
            
            Generate a single compact and meaningful summary that preserves the important
            information required to maintain continuity in future conversation.
            
            Rules:
            
            1. The summary MUST be grounded exclusively in `chat` and `previous_summary`.
               Do not introduce any information that is not present in either input.
            
            2. Preserve substantial and conversation-relevant information, including:
               - user goals and intentions,
               - important decisions and conclusions,
               - requirements and constraints,
               - established preferences,
               - important facts provided by the user,
               - ongoing tasks, projects, or problems,
               - relevant technical details,
               - unresolved issues or questions.
            
            3. Remove unnecessary information such as:
               - greetings and pleasantries,
               - repetitive discussion,
               - irrelevant conversational details,
               - unnecessary explanations,
               - superseded intermediate discussion.
            
            4. When `previous_summary` is provided, merge it with the new information
               from `chat`. Do NOT simply append the new conversation to the previous
               summary.
            
            5. If `chat` contains information that corrects or supersedes information in
               `previous_summary`, preserve the latest information and discard the
               outdated information.
            
            6. Keep the summary compact and information-dense. Preserve important
               substance without turning the summary into a transcript.
            
            7. Do not speculate, infer unstated information, or use external knowledge.
            
            8. Do not mention the summarization process, the previous summary, or these
               instructions in the resulting summary.
            
            Return ONLY the resulting summary.
            
            CHAT:
            {chat}
            
            PREVIOUS SUMMARY:
            {previous_summary}
            """
    )

    return template.invoke({
        "chat": chat,
        "previous_summary": previous_summary
    })
