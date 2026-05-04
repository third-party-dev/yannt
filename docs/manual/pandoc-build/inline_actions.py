#!/usr/bin/env python3

import os
import subprocess
import json
import json.decoder

fpath = "test.json"

# Intended for configuration.
COMMENT_START = "<!--"
COMMENT_END = "-->"
INLINE_ACTION = "INLINE_ACTION"
INLINE_ACTION_END = "INLINE_ACTION_END"

# Intended for runtime cache, DO NOT use as configuration.
INLINE_ACTION_START = f"{COMMENT_START} {INLINE_ACTION}:"
INLINE_ACTION_END_START = f"{COMMENT_START} {INLINE_ACTION_END}:"
END_TAG = COMMENT_END

class Part:
    def __repr__(self):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()

class TextPart(Part):
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return f"TextPart(len {len(self.data)})"
    def __str__(self):
        return self.data

class InlineAction(Part):
    def __init__(self, act_str, act_obj, end_str, end_obj, res_str):
        self.act_str = act_str
        self.act_obj = act_obj
        self.end_str = end_str
        self.end_obj = end_obj
        self.res_str = res_str

    def update(self):
        import hashlib

        res_parts = []

        # Enter requested folder as cwd
        old_path = os.getcwd()
        if "workdir" in self.act_obj:
            os.chdir(self.act_obj["workdir"])

        # Loop only added for jump on command failure.
        while True:

            # Apply header
            if "header" in self.act_obj:
                res_parts.append(self.act_obj["header"])
            
            # Run command
            if "cmd" in self.act_obj:
                if "shell" in self.act_obj:
                    result = subprocess.run(self.act_obj["cmd"], shell=True, executable=self.act_obj["shell"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    # ! Only allow successful commands to overwrite res_str.
                    if result.returncode == 0:
                        res_parts.append(result.stdout)
                    else:
                        res_parts = [self.res_str]
                        break
                else:
                    result = subprocess.run(self.act_obj["cmd"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    # ! Only allow successful commands to overwrite res_str.
                    if result.returncode == 0:
                        res_parts.append(result.stdout)
                    else:
                        res_parts = [self.res_str]
                        break

            # Apply footer
            if "footer" in self.act_obj:
                res_parts.append(self.act_obj["footer"])
            
            break
        
        # Revert folder change.
        os.chdir(old_path)

        # Update res string
        self.res_str = ''.join(res_parts)

        # Update end tag with digest of content.
        self.end_obj["md5"] = hashlib.md5(self.res_str.encode()).hexdigest()
        self.end_str = f"{INLINE_ACTION_END_START} {json.dumps(self.end_obj)} {END_TAG}"

    def __repr__(self):
        return f"InlineAction(act {len(self.act_str)} res {len(self.res_str)} end {len(self.end_str)})"
    def __str__(self):
        return ''.join([self.act_str, self.res_str, self.end_str])

def main():

    with open(fpath) as fobj:
        # Since this is for human written documentation, always assuming
        # we can fit everything in memory.
        data = fobj.read()
        #import hashlib
        #print(f"start hash {hashlib.md5(data.encode()).hexdigest()}")
        #print(f"{'-' * 50}\n{data}\n{'-' * 50}")

    decoder = json.JSONDecoder()

    file_parts = []
    pos = 0
    prev = 0
    while pos < len(data):

        # --------- INLINE_ACTION -----------

        # Find the next INLINE_ACTION.
        res = data[pos:].find(INLINE_ACTION_START)
        if res < 0:
            # No more INLINE_ACTIONs
            break
        pos += res
        act_start = pos

        # Record the file part before this INLINE_ACTION.
        if pos != prev:
            file_parts.append(TextPart(data[prev:pos]))
            prev = pos
        pos += len(INLINE_ACTION_START)

        # Find the next '{'
        res = data[pos:].find("{")
        # Note: There should only be whitespace between ':' and '{'.
        if res < 0 or len(data[pos:pos+res].strip()) > 0:
            # Something is wrong.
            LBRACKET = '{'
            raise Exception(f"Failed to find '{LBRACKET}' in INLINE_ACTION. pos {pos}")
        pos += res

        try:
            act_obj, end = decoder.raw_decode(data[pos:], 0)
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"Failed to decode JSON in INLINE_ACTION. pos {pos}: {e}")
        # This is the position after JSON.
        pos += end

        # Find the next '-->'
        res = data[pos:].find(END_TAG)
        if res < 0:
            # Something is wrong.
            raise Exception(f"Failed to find '-->' in INLINE_ACTION. pos {pos}")
        pos += res + len(END_TAG)
        act_end = pos

        # --------- INLINE_ACTION_END -----------

        # Find the next INLINE_ACTION_END.
        res = data[pos:].find(INLINE_ACTION_END_START)
        if res < 0:
            raise Exception(f"Failed to find required INLINE_ACTION_END. pos {pos}")
        end_start = pos + res
        pos += res + len(INLINE_ACTION_END_START)

        # Find the next '{'
        res = data[pos:].find("{")
        #breakpoint()
        # Note: There should only be whitespace between ':' and '{'.
        if res < 0 or len(data[pos:pos+res].strip()) > 0:
            # Something is wrong.
            LBRACKET = '{'
            raise Exception(f"Failed to find '{LBRACKET}' in INLINE_ACTION_END. pos {pos}")
        pos += res

        try:
            end_obj, end = decoder.raw_decode(data[pos:], 0)
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"Failed to decode JSON in INLINE_ACTION_END. pos {pos}: {e}")
        # This is the position after JSON.
        pos += end

        # Find the next '-->'
        res = data[pos:].find(END_TAG)
        if res < 0:
            # Something is wrong.
            raise Exception(f"Failed to find '-->' in INLINE_ACTION_END. pos {pos}")
        pos += res + len(END_TAG)
        end_end = pos

        # Record the inline action as a file part
        act_str = data[act_start:act_end]
        end_str = data[end_start:end_end]
        res_str = data[act_end:end_start]
        #breakpoint()
        file_parts.append(InlineAction(act_str, act_obj, end_str, end_obj, res_str))
        prev = pos

    if pos < len(data):
        file_parts.append(TextPart(data[pos:]))

    # for part in file_parts:
    #     print(f"{part}")

    # Run all the inline actions.
    for part in file_parts:
        if isinstance(part, InlineAction):
            part.update()

    rebuild = ''.join(str(part) for part in file_parts)
    ## import hashlib
    ## print(f"rebuild hash {hashlib.md5(rebuild.encode()).hexdigest()}")
    #print(f"{'-' * 50}\n{rebuild}\n{'-' * 50}")

    with open(fpath, "w") as fobj:
        fobj.write(rebuild)

main()

#breakpoint()