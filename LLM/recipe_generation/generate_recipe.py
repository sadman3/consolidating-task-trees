# The purpose of this file is to generate in natural language for each input
# we can use gpt-3, gpt-4 , chatgpt etc to do this part

import openai
import os
import json

# Set up the OpenAI API client
# openai.api_key = "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"
openai.api_key = "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"

selected_category = ["salad", "soup", "omelette", "drinks", "cake"]

# # Set up the model and prompt
# model_engine = "gpt-3.5-turbo"


# example_prompt = '''Here is a recipe of whipped cream:
# turn on the mixer.
# pour heavy cream to mixing bowl.
# pour granulated sugar to mixing bowl.
# mix everything.
# turn off the mixer.
# detach the mixing bowl from the mixer.
# scrape whipped cream from mixing bowl to bowl.
# '''

PROMPTS = json.load(open("prompts.json"))


def purify_object_state(state, object):

    if state == "juice":
        state = "liquid"

    elif state == "berries":
        state = ""

    if " fruit" in state:
        state = state.replace(" fruit", "")

    # purified_object = ""
    # object_list = object.split(" ")
    # if len(object_list) == 1:
    #     purified_object = object

    # else:
    #     if object_list[0] == "fruit":
    #         purified_object = object_list[1]

    #     return object

    if len(state) > 0:
        return " " + state + " " + object
    return " " + object


def create_prompt(input_dir="input"):

    prompts = {}
    for currentpath, folders, files in os.walk("input"):
        temp = currentpath.split('/')[-1]
        if temp not in selected_category:
            continue

        for file in files:
            input_path = os.path.join(currentpath, file)
            content = json.load(open(input_path, 'r'))

            ingredients = content["ingredients"]

            dish_type = content["type"]

            id = content["id"]

            prompt = "Write instructions only to make a {} with".format(
                dish_type)

            for ing in ingredients:
                obj = ing["object"]
                state = ing["state"]

                prompt += "{},".format(purify_object_state(state, obj))

            prompt = prompt[:-1]

            prompt += " in steps."

            prompts[id] = prompt

    json.dump(prompts, open("prompts.json", "w"), indent=4)


def call_api():
    prompts = json.load(open("prompts.json"))

    responses = json.load(open("responses.json"))
    for id, prompt in prompts.items():
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }])

        response = completion.choices[0].message["content"]
        responses[id] = response
        # print(response)

    json.dump(responses, open("responses.json", "w"), indent=4)


def parse_ingredinets_from_prompt(prompt):
    # the line starts with "Write instructions only to make a {dish_type} with"
    ingredients = prompt.split("with ")[1]
    ingredients = ingredients.split(" in steps")[0]

    ingredient_list = ingredients.split(", ")

    # print(ingredient_list)
    return ingredient_list


def check_ingredients_exist_in_recipe(result, id, response):
    print("checking recipe {}\n".format(id))
    prompt = PROMPTS[id]
    ingredients = parse_ingredinets_from_prompt(prompt)

    missing_objects = []
    for ingredient in ingredients:
        items = ingredient.split(" ")
        state = items[0]
        object = " ".join(items[1:])

        if object not in response:
            missing_objects.append(object)

        result[id] = {
            "total ingredients": len(ingredients),
            "missing": missing_objects
        }

    json.dump(result, open("response_evaluation.json", "w"), indent=4)


def evaluate_responses():
    responses = json.load(open("responses.json"))

    result = {}
    for id, response in responses.items():
        check_ingredients_exist_in_recipe(result, id, response)


if __name__ == "__main__":
    call_api()

    # evaluate_responses()
    # create_prompt()
