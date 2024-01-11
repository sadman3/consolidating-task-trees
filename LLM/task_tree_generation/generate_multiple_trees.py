import openai
import os
import json
import ast
openai.api_key = "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"

# This can be changed to gpt-4
GPT_MODEL = "gpt-3.5-turbo-16k"


def call_api(query="", id=""):
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are generating task tree for a robot from natural language instructions. A task tree is a list of functional unit where each functional unit is a json object. Each functional unit has input nodes, motion node and output nodes indicating the pre condition, action and its effect respectively.\nThe following items are available in the kitchen:\nwhole onion\nwhole carrot\nwhole strawberry\nWhen you generate functional units, you must start with this state if the state of the object is not mentioned in the instruction. "
            },
            {
                "role": "user",
                "content": "Put onion on the cutting board."
            },
            {
                "role": "assistant",
                "content": "[{'input_nodes': [{'label': 'onion', 'states': ['unpeeled', 'whole'], 'ingredients': [], 'container': None}, {'label': 'cuttingboard', 'states': ['empty'], 'ingredients': [], 'container': None}], 'motion_node': 'pick-and-place', 'output_nodes': [{'label': 'onion', 'states': ['unpeeled', 'whole'], 'ingredients': [], 'container': 'cuttingboard'}]}]"
            },
            {
                "role": "user",
                "content": "slice a carrot"
            },
            {
                "role": "assistant",
                "content": "[{'input_nodes': [{'label': 'carrot', 'states': ['whole'], 'ingredients': [], 'container': None}, {'label': 'cuttingboard', 'states': ['empty'], 'ingredients': [], 'container': None}], 'motion_node': 'pick-and-place', 'output_nodes': [{'label': 'carrot', 'states': ['whole'], 'ingredients': [], 'container': 'cuttingboard'}]}, {'input_nodes': [{'label': 'carrot', 'states': ['whole'], 'ingredients': [], 'container': 'cuttingboard'}, {'label': 'knife', 'states': ['sharp'], 'ingredients': [], 'container': None}], 'motion_node': 'slice', 'output_nodes': [{'label': 'carrot', 'states': ['sliced'], 'ingredients': [], 'container': 'cuttingboard'}]}]"
            },
            {
                "role": "user",
                "content": "Chop a peeled onion"
            },
            {
                "role": "assistant",
                "content": "[{'input_nodes': [{'label': 'onion', 'states': ['peeled', 'whole'], 'ingredients': [], 'container': 'cuttingboard'}, {'label': 'knife', 'states': [], 'ingredients': [], 'container': None}], 'motion_node': 'chop', 'output_nodes': [{'label': 'onion', 'states': ['chopped'], 'ingredients': [], 'container': 'cuttingboard'}]}]"
            },
            {
                "role": "user",
                "content": "Heat the skillet on the stove.\nPour butter from bowl to skillet.\nHeat to melt the butter."
            },
            {
                "role": "assistant",
                "content": "[{'input_nodes': [{'label': 'skillet', 'states': ['empty'], 'ingredients': [], 'container': None}, {'label': 'stove', 'states': ['on'], 'ingredients': [], 'container': None}], 'motion_node': 'heat', 'output_nodes': [{'label': 'skillet', 'states': ['heated'], 'ingredients': [], 'container': 'stove'}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['butter'], 'container': None}, {'label': 'butter', 'states': ['cubed'], 'ingredients': [], 'container': 'bowl'}, {'label': 'skillet', 'states': ['heated'], 'ingredients': [], 'container': 'stove'}], 'motion_node': 'pour', 'output_nodes': [{'label': 'butter', 'states': ['cubed'], 'ingredients': [], 'container': 'skillet'}, {'label': 'skillet', 'states': [], 'ingredients': ['butter'], 'container': 'stove'}]}, {'input_nodes': [{'label': 'stove', 'states': ['on'], 'ingredients': [], 'container': 'skillet'}, {'label': 'butter', 'states': ['cubed'], 'ingredients': [], 'container': 'skillet'}, {'label': 'skillet', 'states': [], 'ingredients': ['butter'], 'container': 'stove'}], 'motion_node': 'heat', 'output_nodes': [{'label': 'butter', 'states': ['melted'], 'ingredients': [], 'container': 'skillet'}, {'label': 'skillet', 'states': [], 'ingredients': ['butter'], 'container': 'stove'}]}]"
            },
            {
                "role": "user",
                "content": "put baked matzo on an empty plate.\nbreak matzo and put into a bowl of water.\nsoak matzo in the water.\ndrain the water.\ncrack an egg to the bowl of matzo.\ngrind salt to the bowl.\nmix everything with a spoon.\nadd vegetable oil to a cooking pan on stove.\nadd the matzo mixture to the cooking pan and spread with a spoon.\nflip partly cooked matzo brei and cook again.\\nserve matzo brei in a plate."
            },
            {
                "role": "assistant",
                "content": "[{'input_nodes': [{'label': 'matzo', 'states': ['baked'], 'ingredients': [], 'container': None}, {'label': 'plate', 'states': ['empty'], 'ingredients': [], 'container': None}], 'motion_node': 'pick-and-place', 'output_nodes': [{'label': 'plate', 'states': [], 'ingredients': ['matzo'], 'container': None}, {'label': 'matzo', 'states': ['baked'], 'ingredients': [], 'container': 'plate'}]}, {'input_nodes': [{'label': 'plate', 'states': [], 'ingredients': ['matzo'], 'container': None}, {'label': 'matzo', 'states': ['baked'], 'ingredients': [], 'container': 'plate'}], 'motion_node': 'break', 'output_nodes': [{'label': 'matzo', 'states': ['broken'], 'ingredients': [], 'container': None}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['water'], 'container': None}, {'label': 'matzo', 'states': ['broken'], 'ingredients': [], 'container': None}], 'motion_node': 'pick-and-place', 'output_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['water', 'matzo'], 'container': None}, {'label': 'matzo', 'states': ['broken'], 'ingredients': [], 'container': 'bowl'}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['water', 'matzo'], 'container': None}, {'label': 'water', 'states': [], 'ingredients': [], 'container': 'bowl'}, {'label': 'matzo', 'states': ['broken'], 'ingredients': [], 'container': 'bowl'}], 'motion_node': 'press', 'output_nodes': [{'label': 'matzo', 'states': ['soaked'], 'ingredients': [], 'container': 'bowl'}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['water', 'matzo'], 'container': None}, {'label': 'matzo', 'states': ['soaked'], 'ingredients': [], 'container': 'bowl'}, {'label': 'water', 'states': [], 'ingredients': [], 'container': 'bowl'}], 'motion_node': 'drain', 'output_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['matzo'], 'container': None}, {'label': 'matzo', 'states': ['mashed'], 'ingredients': [], 'container': 'bowl'}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['matzo'], 'container': None}, {'label': 'egg', 'states': ['uncracked'], 'ingredients': [], 'container': None}], 'motion_node': 'crack', 'output_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['matzo', 'eggwhiteandyolk'], 'container': None}, {'label': 'eggwhiteandyolk', 'states': [], 'ingredients': [], 'container': 'bowl'}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['matzo', 'eggwhiteandyolk'], 'container': None}, {'label': 'grinder', 'states': [], 'ingredients': ['salt'], 'container': None}, {'label': 'salt', 'states': [], 'ingredients': [], 'container': 'grinder'}], 'motion_node': 'grind', 'output_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['matzo', 'eggwhiteandyolk', 'salt'], 'container': None}, {'label': 'salt', 'states': ['granulated'], 'ingredients': [], 'container': 'bowl'}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['matzo', 'eggwhiteandyolk', 'salt'], 'container': None}, {'label': 'matzo', 'states': ['mashed'], 'ingredients': [], 'container': 'bowl'}, {'label': 'salt', 'states': ['granulated'], 'ingredients': [], 'container': 'bowl'}, {'label': 'spoon', 'states': [], 'ingredients': [], 'container': None}, {'label': 'eggwhiteandyolk', 'states': [], 'ingredients': [], 'container': 'bowl'}], 'motion_node': 'mix', 'output_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['matzomixture'], 'container': None}, {'label': 'matzomixture', 'states': [], 'ingredients': ['matzo', 'eggwhiteandyolk', 'salt'], 'container': 'bowl'}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['vegetableoil'], 'container': None}, {'label': 'vegetableoil', 'states': [], 'ingredients': [], 'container': 'bowl'}, {'label': 'cookingpan', 'states': ['heated'], 'ingredients': [], 'container': 'stove'}], 'motion_node': 'pour', 'output_nodes': [{'label': 'cookingpan', 'states': [], 'ingredients': ['vegetableoil'], 'container': 'stove'}, {'label': 'vegetableoil', 'states': [], 'ingredients': [], 'container': 'pan'}]}, {'input_nodes': [{'label': 'bowl', 'states': [], 'ingredients': ['matzomixture'], 'container': None}, {'label': 'matzomixture', 'states': [], 'ingredients': ['matzo', 'eggwhiteandyolk', 'salt'], 'container': 'bowl'}, {'label': 'cookingpan', 'states': [], 'ingredients': ['vegetableoil'], 'container': 'stove'}, {'label': 'spoon', 'states': [], 'ingredients': [], 'container': None}], 'motion_node': 'scrape', 'output_nodes': [{'label': 'cookingpan', 'states': [], 'ingredients': ['matzomixture'], 'container': 'stove'}, {'label': 'matzomixture', 'states': [], 'ingredients': ['matzo', 'eggwhiteandyolk', 'salt'], 'container': 'pan'}, {'label': 'bowl', 'states': [], 'ingredients': [], 'container': None}]}, {'input_nodes': [{'label': 'cookingpan', 'states': [], 'ingredients': ['matzomixture'], 'container': 'stove'}, {'label': 'matzomixture', 'states': [], 'ingredients': ['matzo', 'eggwhiteandyolk', 'salt'], 'container': 'pan'}, {'label': 'spoon', 'states': [], 'ingredients': [], 'container': None}], 'motion_node': 'spread', 'output_nodes': [{'label': 'matzobrei', 'states': ['partlycooked'], 'ingredients': [], 'container': 'pan'}]}, {'input_nodes': [{'label': 'cookingpan', 'states': [], 'ingredients': ['matzomixture'], 'container': 'stove'}, {'label': 'matzobrei', 'states': ['partlycooked'], 'ingredients': [], 'container': 'pan'}, {'label': 'turner', 'states': [], 'ingredients': [], 'container': None}], 'motion_node': 'flip', 'output_nodes': [{'label': 'matzobrei', 'states': ['flipped'], 'ingredients': [], 'container': 'pan'}]}, {'input_nodes': [{'label': 'cookingpan', 'states': [], 'ingredients': ['matzomixture'], 'container': 'stove'}, {'label': 'matzobrei', 'states': ['flipped'], 'ingredients': [], 'container': 'pan'}, {'label': 'stove', 'states': ['on'], 'ingredients': [], 'container': 'pan'}], 'motion_node': 'cook', 'output_nodes': [{'label': 'matzobrei', 'states': ['cooked'], 'ingredients': [], 'container': 'pan'}, {'label': 'cookingpan', 'states': [], 'ingredients': ['matzobrei'], 'container': 'stove'}]}, {'input_nodes': [{'label': 'matzobrei', 'states': ['cooked'], 'ingredients': [], 'container': 'pan'}, {'label': 'cookingpan', 'states': [], 'ingredients': ['matzobrei'], 'container': 'stove'}, {'label': 'turner', 'states': [], 'ingredients': [], 'container': None}, {'label': 'plate', 'states': ['empty'], 'ingredients': [], 'container': None}], 'motion_node': 'pick-and-place', 'output_nodes': [{'label': 'matzobrei', 'states': ['cooked'], 'ingredients': ['vegetableoil', 'matzo', 'water', 'matzomixture', 'eggwhiteandyolk', 'salt'], 'container': 'plate'}, {'label': 'plate', 'states': [], 'ingredients': ['matzobrei'], 'container': None}]}]"
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=1,
        # max_token = 4096
        max_tokens=12000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1  # how many response
    )
    # print(type(response["choices"][0]["message"]["content"]))
    try:
        task_tree = ast.literal_eval(
            response["choices"][0]["message"]["content"].strip('"'))
        json.dump(task_tree, open(
            "generated_task_trees/{}.json".format(id), "w"), indent=4)
    except:
        incorrect_tree = response["choices"][0]["message"]["content"].strip(
            '"')
        json.dump(incorrect_tree, open(
            "incorrect_trees/{}.json".format(id), "w"), indent=4)


if __name__ == "__main__":
    # we can do it for other categories by changing the path
    recipe_ids = os.listdir("input/drinks")
    chatgpt_responses = json.load(open("../chatgpt_responses.json"))

    cnt = 0
    for id in recipe_ids:
        if id.startswith("."):
            continue
        cnt += 1
        # if cnt <= 22:
        #     continue
        # if cnt == 50:
        #     break
        print(cnt)
        id = id.split(".")[0]
        query = chatgpt_responses[id]
        call_api(query=query, id=id)
