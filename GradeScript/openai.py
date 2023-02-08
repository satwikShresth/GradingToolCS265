import openai

openai.api_key = "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"  # Replace with your OpenAI API key

def fix_code(code: str) -> str:
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Fix the following code and leave remarks for mistakes:\n" + code,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

code = "#include <stdio.h>\n#include <string.h>\n\n#define MAX_LENGTH 100\n\nint main() {\n    char message[MAX_LENGTH];\n    int i, length;\n\n    printf(\"Enter a message: \");\n    for (i = 0; i < MAX_LENGTH - 1 && (message[i] = getchar()) != '\\n'; i++);\n    length = i;\n\n    printf(\"Reversal is: \");\n    for (i = 0; i < length; i++) {\n        putchar(message[i]);\n    }\n    putchar('\\n');\n\n    return 0;\n}"
fixed_code = fix_code(code)
print(fixed_code)


