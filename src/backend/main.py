import pprint
import env
from agent.graph import app

for s in app.stream(
    {
        "messages": [
            ("user", "Research AI agents and write a brief report about them.")
        ],
    },
    {"recursion_limit": 150},
    subgraphs = True
):
    # Detailed tracing of each stream output
    print(s)
    print("---")