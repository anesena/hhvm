#!/usr/bin/env python3

"""
 Takes LSP commands and communicates them with the LSP server.

 This script is useful for testing the LSP server: you can feed in a payload and
 confirm that the responses are correct.

 The LSP spec can be found here:
 https://github.com/Microsoft/language-server-protocol/blob/master/protocol.md

 The input files must contain an array of json-rpc
 commands to send to the language server.

 Commands that you expect a response from the server
 should include an "id" field.  The field should be
 a unique integer per command.  The server will
 send responses with the "id" passed in, and this
 tool will use them to line up sent/response pairs.

 Commands that are notificatins where you don't
 expect a server response should not contain an
 "id" field.  See textDocument/didOpen for an
 example of this.

 Inside a command body, you can run a python function on the argument
 to cause the string output of that function to be replaced at run-time.
 For example, for a URI, you can use

   >>> file_uri('sample.php')

 which would generate something like

   file:///home/chrishahn/test/sample.php

 you can also use

   >>> read_file('sample.php')

 read_file() will read the contents of 'sample.php' and
 insert them.  This is useful in conjunction with the
 textDocument/didOpen command.

 Suggested command-line usage:

    python talk.py filename.txt
"""
import json
import fileinput
from lspcommand import LspCommandProcessor


def main():
    with LspCommandProcessor.create() as lsp_proc:
        json = lsp_proc.parse_commands(read_commands())
        t = lsp_proc.communicate(json)
        print_transcript(lsp_proc, t)


def print_transcript(lsp_proc, t):
    for id, package in t.items():
        print(f"Sent [id={id}]:\n")
        print(json.dumps(package["sent"], indent=2))

        if lsp_proc.is_request_id(id):
            print("\nReceived:\n")
            print(json.dumps(package["received"], indent=2))

        print('-' * 80)


# this will read command data from stdin or
# an arbitrary list of files
def read_commands():
    command_lines = []
    for line in fileinput.input():
        command_lines.append(line)
    return '\n'.join(command_lines)

if __name__ == "__main__":
    main()
