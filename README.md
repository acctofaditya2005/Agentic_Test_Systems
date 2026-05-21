## The Application Under Test

The drum kit is a simple one-page web application with 7 interactive 
buttons (W, A, S, D, J, K, L). Each button plays a different drum sound 
when clicked or when the corresponding keyboard key is pressed.

This was chosen as the test subject because:
- It has real interactive UI elements (buttons, keyboard events)
- Simple enough to understand quickly
- Complex enough to demonstrate real testing challenges
- CSS selectors can break when classes change — perfect for self-healing demo

The application is served locally at http://localhost:8000 during testing.
# Drum Kit Agentic Test System

A self-healing AI agent that autonomously runs Playwright UI tests,
diagnoses failures, and fixes broken CSS selectors without human intervention.

## What It Does

- Runs automated Playwright tests on a drum kit web application
- Detects test failures and classifies them: script issue vs system bug
- Self-heals broken CSS selectors by reading the HTML source to verify
  the correct class name before making any fix
- Circuit breaker prevents infinite loops — stops after 3 retries and escalates
- Saves structured test results to JSON using Pydantic models

## Evolution of This Project

### V1 — Basic Agentic Test System
The first version was a simple agent that ran pytest and summarized 
pass/fail results in plain English using LangChain and Gemini.
No self-healing, no circuit breaker, no structured output.

### V2 — Self-Healing Agent (this project)
Applied to a real web application — a drum kit UI with 7 interactive buttons.
Added three key improvements:
1. Self-healing — agent fixes broken selectors automatically
2. Circuit breaker — prevents agent from looping infinitely
3. Context engineering — agent reads HTML before fixing to prevent hallucination

Key lesson: The agent initially hallucinated fixes (changed .drum-k to .drum 
instead of .k). Solved by giving the agent verified HTML context before acting.
