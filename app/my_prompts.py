# file_map = """
# You will be given a single section from a text. This will be enclosed in triple backticks.
# Please provide a cohesive summary of the following section excerpt, focusing on the key points and main ideas, while maintaining clarity and conciseness.

# '''{text}'''

# FULL SUMMARY:
# """


# file_combine = """
# Read all the provided summaries from a larger document. They will be enclosed in triple backticks. 
# Determine what the overall document is about and summarize it with this information in mind.
# Synthesize the info into a well-formatted easy-to-read synopsis, structured like an essay that summarizes them cohesively. 
# Do not simply reword the provided text. Do not copy the structure from the provided text.
# Avoid repetition. Connect all the ideas together.
# Preceding the synopsis, write a short, bullet form list of key takeaways.
# Format in HTML. Text should be divided into paragraphs. Paragraphs should be indented. 

# '''{text}'''


# """

file_map = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Please provide a cohesive summary of the following section excerpt, focusing on the key points and main ideas, while maintaining clarity and conciseness.

'''{text}'''

FULL SUMMARY:
"""


file_combine = """
Read all the provided summaries from a larger document. They will be enclosed in triple backticks. 
Determine what the overall document is about and summarize it page by page with this information in mind.
Show page number and its summary and format it nicely. Summary must inlucde all pages from document.

'''{text}'''


"""