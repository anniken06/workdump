class CommandGenerator:
    def generate_commands(template, replace_dict={}):
        commands = [template]
        for keyword, replacements in replace_dict.items():
            commands = [command.replace(str(keyword), str(replacement)) for command in commands for replacement in replacements]
        return commands

if __name__ == '__main__':
    test_template = "my command <OPT1> <OPT2>"
    test_replace_dict = {
        "<OPT1>": ["1", "2", 3],
        "<OPT2>" : [True, False],
    }
    print(CommandGenerator.generate_commands(test_template, test_replace_dict))
