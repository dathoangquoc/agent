from typing import Optional, List, Literal, Union, Dict

# From Litellm
class Message():
    content: Optional[str]
    role: Literal["assistant", "user", "system", "tool", "function"]
    # tool_calls: Optional[List[ChatCompletionMessageToolCall]]
    # function_call: Optional[FunctionCall]
    # audio: Optional[ChatCompletionAudioResponse] = None
    reasoning_content: Optional[str] = None
    # thinking_blocks: Optional[
    #     List[Union[ChatCompletionThinkingBlock, ChatCompletionRedactedThinkingBlock]]
    # ] = None
    provider_specific_fields: Optional[Dict[str, Any]] = Field(
        default=None, exclude=True
    )
    # annotations: Optional[List[ChatCompletionAnnotation]] = None

