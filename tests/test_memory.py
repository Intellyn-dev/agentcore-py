from agentcore.memory import AgentMemory


def test_add_and_retrieve():
    mem = AgentMemory(max_messages=5)
    mem.add_message("user", "Hello")
    mem.add_message("assistant", "Hi there")
    history = mem.get_history()
    assert len(history) == 2
    assert history[0].role == "user"


def test_get_last_n():
    mem = AgentMemory(max_messages=10)
    for i in range(5):
        mem.add_message("user", f"msg {i}")
    last2 = mem.get_history(last_n=2)
    assert len(last2) == 2
    assert last2[-1].content == "msg 4"


def test_to_langchain_format():
    mem = AgentMemory()
    mem.add_message("user", "Question?")
    lc = mem.to_langchain_messages()
    assert lc[0] == {"role": "user", "content": "Question?"}
