PROBLEM_WITH_EXPERIENCE_TEMPLATE = """Please solve the problem:
{problem}

When solving problems, you MUST first carefully read and understand the helpful instructions and experiences:
{experiences}"""


SINGLE_ROLLOUT_SUMMARY_TEMPLATE = """An agent system may be provided with some experiences, and then it produces the following trajectory to solve the given problem. Please summarize the trajectory step-by-step:

1. For each step, describe **what action is being taken**, and which experience has been used in this step.
2. Given the grading of this rollout and the correct answer, identify and explain any steps that **represent detours, errors, or backtracking**, highlighting why they might have occurred and what their impact was on the trajectory's progress. 
3. Maintain **all the core outcome of each step**, even if it was part of a flawed process.

<trajectory>
{trajectory}
</trajectory>

<evaluation>
{grade}
</evaluation>

<groundtruth>
{answer}
</groundtruth>

Only return the trajectory summary of each step, e.g.,
1. what happened in the first step and the core outcomes
2. what happened in the second step and the core outcomes
3. ..."""


SINGLE_QUERY_CRITIQUE_TEMPLATE = """An agent system is provided with a set of experiences and has tried to solve the problem multiple times with both successful and wrong solutions. Review these problem-solving attempt and extract generalizable experiences. Follow these steps:

1. Trajectory Analysis:
    - For successful steps: Identify key correct decisions and insights
    - For errors: Pinpoint where and why the reasoning went wrong
    - Note any important patterns or strategies used/missed
    - Review why some trajectories fail? Is there any existing experiences are missed, or experiences do not provide enough guidance?

2. Update Existing Experiences
    - Some trajectories may be correct and others may be wrong, you should ensure there are experiences can help to run correctly
    - You have two options: [modify, add]
        * modify: You can modify current experiences to make it helpful
        * add: You can introduce new experiences may need to be 
    - You can update at most {max_operations} clear, generalizable lessons for this case
    - Before updating each experience, you need to:
        * Specify when it would be most relevant
        * List key problem features that make this experience applicable
        * Identify similar problem patterns where this advice applies
    
3. Requirements for each experience that is modified or added.
    - Begin with general background with several words in the experience
    - Focus on strategic thinking patterns, not specific calculations
    - Emphasize decision points that could apply to similar problems

Please provide reasoning in details under the guidance of the above 3 steps.
After the step-by-step reasoning, you will finish by returning in this JSON format as follows:
```json
[
    {{
        "option": "modify",
        "experience": "the modified experience",
        "modified_from": "G17" # specify the ID of experience that is modified
    }},
    {{
        "option": "add",
        "experience": "the added experience",
    }},
    ...
]
```
Note that your updated experiences may not need to cover all two options. Only using one type of updates is also very good.

<problem> 
{problem}
</problem>

<trajectories>
{trajectories}
</trajectories>

<groundtruth>
{answer}
</groundtruth>

<experience>
{experiences}
</experience>"""


BATCH_EXPERIENCE_UPDATE_TEMPLATE = """An agent system is provided with a set of experiences and has tried to solve the problem multiple times. From the reflections, some suggestions on the existing experiences have been posed. Your task is to collect and think for the final experience revision plan. Each final experience must satisfy the following requirements.
1. It must be clear, generalizable lessons for this case, with no more than 32 words
2. Begin with general background with several words in the experience
3. Focus on strategic thinking patterns, not specific calculations
4. Emphasize decision points that could apply to similar problems
5. Avoid repeating saying similar experience in multiple different experiences

<existing_experiences> 
{experiences}
</existing_experiences>

<suggested_updates>
{updates}
</suggested_updates>

Please provide reasoning in each of the suggestions, and think for how to update existing experiences 
You have two update options: [modify, merge]
* modify: You can modify current experiences to make it helpful
* merge: You can merge some similar experiences into a more general forms to reduce duplication

After generating the step-by-step reasoning, you need to give the final experience revision details by returning in this JSON format as follows:
```json
[
    {{
        "option": "modify",
        "experience": "the modified experience",
        "modified_from": "C1" # specify the str ID of experience that is modified
    }},
    {{
        "option": "merge",
        "experience": "the merged experience",
        "merged_from": ["C1", "C3", "S4", ...] # specify the str IDs of experiences that is merged from, at least 2 IDs are needed
    }},
    ...
]
```

Your updated experiences may not need to cover all two options. Only using one type of updates is OK."""


SINGLE_ROLLOUT_SUMMARY_NO_GT_TEMPLATE = """An agent system may be provided with some experiences, and then it produces the following trajectory to solve the given problem. Please summarize the trajectory step-by-step:

1. For each step, describe **what action is being taken**, and which experience has been used in this step.
2. Given the grading of this rollout and the correct answer, identify and explain any steps that **represent detours, errors, or backtracking**, highlighting why they might have occurred and what their impact was on the trajectory's progress. 
3. Maintain **all the core outcome of each step**, even if it was part of a flawed process.

<trajectory>
{trajectory}
</trajectory>

Only return the trajectory summary of each step, e.g.,
1. what happened in the first step and the core outcomes
2. what happened in the second step and the core outcomes
3. ..."""


SINGLE_QUERY_CRITIQUE_NO_GT_TEMPLATE = """An agent system is provided with a set of experiences and has tried to solve the problem multiple times. Review these problem-solving attempt and extract generalizable experiences. Follow these steps:

1. Trajectory Analysis:
    - Identify key correct decisions and insights
    - Pinpoint where and why the reasoning went wrong
    - Note any important patterns or strategies used/missed
    - Review why some trajectories seems to fail? Is there any existing experiences are missed, or experiences do not provide enough guidance?

2. Update Existing Experiences
    - Ensure there are experiences can help to run correctly
    - You have two options: [modify, add]
        * modify: You can modify current experiences to make it helpful
        * add: You can introduce new experiences may need to be 
    - You can update at most {max_operations} clear, generalizable lessons for this case
    - Before updating each experience, you need to:
        * Specify when it would be most relevant
        * List key problem features that make this experience applicable
        * Identify similar problem patterns where this advice applies
    
3. Requirements for each experience that is modified or added.
    - Begin with general background with several words in the experience
    - Focus on strategic thinking patterns, not specific calculations
    - Emphasize decision points that could apply to similar problems

Please provide reasoning in details under the guidance of the above 3 steps.
After the step-by-step reasoning, you will finish by returning in this JSON format as follows:
```json
[
    {{
        "option": "modify",
        "experience": "the modified experience",
        "modified_from": "G17" # specify the ID of experience that is modified
    }},
    {{
        "option": "add",
        "experience": "the added experience",
    }},
    ...
]
```
Note that your updated experiences may not need to cover all two options. Only using one type of updates is also very good.

<problem> 
{problem}
</problem>

<trajectories>
{trajectories}
</trajectories>

<experience>
{experiences}
</experience>"""
