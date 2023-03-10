import os
import logging
import openai

KEY = os.getenv('OPENAI_API_KEY')

if KEY is None:
    logging.error('Can not find API key; please set the "OPENAI_API_KEY" environment variable and restart.')
    breakpoint()

openai.api_key = KEY
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def writecode(prompt, lang='Python', max_tokens=1024, best_of=3, save=None):
    """
    Generates code from a text prompt using OpenAI's Codex model.

    Args:
        prompt: A string containing the text prompt with the instructions for Codex.
        lang: The language to generate code in. The default is Python.
        max_tokens: An optional integer specifying the maximum number of output tokens.
        best_of: An optional integer specifying the number of completions to generate server-side and return the "best" (the one with the highest log probability per token). The default is 3.
        save: An optional string specifying the name of the output file to save the code snippet to.

    Returns:
        A string containing the generated code. If the `save` parameter is specified, the code will also be saved to the specified file.
    """

    prompt = "# We're going to generate code in " + lang + " using the following details (stop after generating the " + lang + " code): " + prompt
    prompt += '\n# The generated code:\n<|endoftext|>'

    print(prompt)

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt='-*-*-\n' + prompt,
        stop='-*-*-\n',
        temperature=0,
        max_tokens=int(max_tokens),
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        best_of=best_of
    )

    output = response['choices'][0]['text']

    # search for excess code at the end
    if '# The generated code:' in output:
        logging.info('removing excess at the end of the output...')
        output = output[:output.find('# The generated code:')]

    if save is not None:
        with open(save, 'w') as f:
            f.write(output)

    return output


def explaincode(prompt, max_tokens=30, best_of=3, save=None):
    """
    Explains a snippet of code using OpenAI's Codex model.

    Args:
        prompt: A string containing the text prompt with the instructions for Codex.
        max_tokens: An optional integer specifying the maximum number of output tokens.
        best_of: An optional integer specifying the number of completions to generate server-side and return the "best" (the one with the highest log probability per token). The default is 3.
        save: An optional string specifying the name of the output file to save the code snippet to.

    Returns:
        A string containing the generated code. If the `save` parameter is specified, the code will also be saved to the specified file.
    """
    prompt = """Python:
import pyspedas
pyspedas.mms.fgm(trange=['2015-10-1', '2015-10-16'])
Explanation:
- Imports PySPEDAS
- Loads MMS Fluxgate Magnetometer data for October 1, 2015 until October 16, 2015
------
Python:
""" + prompt + """
Explanation:
"""

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=int(max_tokens),
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        best_of=best_of
    )

    output = response['choices'][0]['text']

    # search for excess code at the end
    if '------' in output:
        logging.info('removing excess at the end of the output...')
        output = output[:output.find('------')]

    if save is not None:
        with open(save, 'w') as f:
            f.write(output)

    return output
