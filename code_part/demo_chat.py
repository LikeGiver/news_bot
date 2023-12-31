import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from llama_index.vector_stores import VectorStoreQuery

from vector_store import get_vector_store, get_embed_model
from client import get_client
from conversation import postprocess_text, preprocess_text, Conversation, Role

from llama_index.schema import NodeWithScore
from typing import Optional

MAX_LENGTH = 8192
RETRIEVAL_PROMPT = "根据用户问题检索到相关信息如下，你可以使用这些信息，可以直接忽略\n"
vector_store = get_vector_store()

client = get_client()

# Append a conversation into history, while show it in a new markdown block
def append_conversation(
    conversation: Conversation,
    history: list[Conversation],
    placeholder: DeltaGenerator | None=None,
    show = True
) -> None:
    history.append(conversation)
    if show:
        conversation.show(placeholder)

def main(top_p: float, temperature: float, system_prompt: str, prompt_text: str):
    placeholder = st.empty()
    with placeholder.container():
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        history: list[Conversation] = st.session_state.chat_history
        history_tmp = history.copy()

        for conversation in history:
            conversation.show()

    if prompt_text:
        print("=== prompt_text:")
        print(prompt_text)

        prompt_text = prompt_text.strip()
        # append_conversation(Conversation(Role.USER, prompt_text), history)

        ###########Define the retrieval part###########
        embed_model = get_embed_model()
        query_mode = "default"
        query_embedding = embed_model.get_query_embedding(prompt_text)

        vector_store_query = VectorStoreQuery(
            query_embedding=query_embedding, similarity_top_k=5, mode=query_mode
        )

        query_embedding2 = embed_model.get_query_embedding(history)

        # vector_store_query2 = VectorStoreQuery(
        #     query_embedding=query_embedding2, similarity_top_k=2, mode=query_mode
        # )


        query_result = vector_store.query(vector_store_query)

        # query_result2 = vector_store.query(vector_store_query2)

        nodes_with_scores = []
        for index, node in enumerate(query_result.nodes):
            score: Optional[float] = None
            if query_result.similarities is not None:
                score = query_result.similarities[index]
            nodes_with_scores.append(NodeWithScore(node=node, score=score))

        # for index, node in enumerate(query_result2.nodes):
        #     score: Optional[float] = None
        #     if query_result.similarities is not None:
        #         score = query_result.similarities[index]
        #     nodes_with_scores.append(NodeWithScore(node=node, score=score))

        for nodes_with_score in nodes_with_scores:
            if nodes_with_score.score >= 0.75:
                print("=== retrieved_text:")
                print(nodes_with_score.text)
                print("=== score:")
                print(nodes_with_score.score)
                print("=== retrieved_text metadata:")
                print(nodes_with_score.metadata)
                append_conversation(Conversation(Role.TOOL, RETRIEVAL_PROMPT + "\n### data retrived \n" + nodes_with_score.text + "\n### data retrived end \n"), history_tmp, show=False)
        ##########END retrieval###########
        append_conversation(Conversation(Role.USER, prompt_text), history_tmp, show=False)
        append_conversation(Conversation(Role.USER, prompt_text), history)

        input_text = preprocess_text(
            system_prompt,
            tools=None,
            history=history_tmp,
        )
        # print("=== Input:")
        # print(input_text)
        # print("=== History:")
        # print(history_tmp)

        placeholder = st.empty()
        message_placeholder = placeholder.chat_message(name="assistant", avatar="assistant")
        markdown_placeholder = message_placeholder.empty()

        output_text = ''
        for response in client.generate_stream(
            system_prompt,
            tools=None, 
            history=history_tmp,
            do_sample=True,
            max_length=MAX_LENGTH,
            temperature=temperature,
            top_p=top_p,
            stop_sequences=[str(Role.USER)],
        ):
            token = response.token
            if response.token.special:
                print("=== Output:")
                print(output_text)

                match token.text.strip():
                    case '<|user|>':
                        break
                    case _:
                        st.error(f'Unexpected special token: {token.text.strip()}')
                        break
            output_text += response.token.text
            markdown_placeholder.markdown(postprocess_text(output_text + '▌'))
        
        append_conversation(Conversation(
            Role.ASSISTANT,
            postprocess_text(output_text),
        ), history, markdown_placeholder)