import os, subprocess, json
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from models import TestResult, TestReport

def save_structured_report(test_output: str, ai_diagnosis: str):
    lines = test_output.split("\n")
    results = []
    
    for line in lines:
        if "PASSED" in line:
            test_name = line.split("::")[1].split(" ")[0]
            results.append(TestResult(
                test_name=test_name,
                passed=True
            ))
        elif "FAILED" in line:
            test_name = line.split("::")[1].split(" ")[0]
            results.append(TestResult(
                test_name=test_name,
                passed=False,
                error=line
            ))
    
    report = TestReport(
        total_tests=len(results),
        passed=len([r for r in results if r.passed]),
        failed=len([r for r in results if not r.passed]),
        results=results,
        ai_diagnosis=ai_diagnosis
    )
    
    # save to JSON
    with open("test_report.json", "w") as f:
        f.write(report.model_dump_json(indent=2))
    
    return report


llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    google_api_key = os.environ["GOOGLE_API_KEY"]
)

@tool
def run_test(test_file:str) -> str:
    "Run the drum kit Playwright test suite"
    result = subprocess.run(['py', '-m','pytest', test_file, '-v'], capture_output = True, text = True)
    return f"{result.stdout}{result.stderr}"

@tool
def fix_selector(old_selector : str, new_selector : str) -> str:
    "Fix a brokwn CSS selector in the test file"
    with open("drum_kit_tester/test_drum_kit.py", 'r', encoding = 'utf-8') as file:
        content = file.read()
    updated = content.replace(old_selector, new_selector)

    with open("drum_kit_tester/test_drum_kit.py", 'w', encoding = 'utf-8') as file:
        file.write(updated)
    return (f"Fixed selector from '{old_selector}' to '{new_selector}'")

@tool
def read_html() -> str:
    """Read the drum kit HTML to find correct CSS selectors.
    Use this before fixing any selector."""
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    start = content.find("<body>")
    end = content.find("</body>") + 7
    return content[start:end]

def run_agent():
    llm_with_tools = llm.bind_tools([run_test, fix_selector, read_html])
    retry_count = {}
    MAX_RETRIES = 3
    test_output = ""

    response = llm_with_tools.invoke(
        "Run the drum kit tests at drum_kit_tester/test_drum_kit.py. "
        "If any tests fail due to a broken selector, first call read_html "
        "to find the correct class name, then fix the selector and rerun. "
        "Tell me which tests passed, which failed, and what was fixed."
    )
    while response.tool_calls:
        for tool_call in response.tool_calls:
            name = tool_call['name']

            retry_count[name] = retry_count.get(name, 0) + 1
            if retry_count[name] > MAX_RETRIES:
                print(f"Circut breaker triggered from {name} - escalating")
                return
            
            print(f"Agent calling:{name}")
            if name == "run_test":
                result = run_test.invoke(tool_call['args'])
                test_output = result 
            elif name == "fix_selector":
                result = fix_selector.invoke(tool_call['args'])
            elif name == "read_html":
                result = read_html.invoke(tool_call['args'])
            else:
                result = f"Unknown tool: {name}"
            print(f"Result: {result[:200]}")

        response = llm_with_tools.invoke(
            f"Tool result: {result} \n\n"
            "Continue - fix any remaining issues and give final diagnosis."
        )
    print(f"\nFinal diagnosis:\n{response.content}")
    save_structured_report(test_output, response.content)

def main():
    print("Starting Drum Kit Agentic Tester...")
    run_agent()
    

if __name__ == "__main__":
    main()
