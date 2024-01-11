from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "You are converting a function unit to PDDL domain and problem file. A functional has a json structure. It has input objects , motion and output objects that are similar to preconditions, action and effect respectively. The actions robot can execute are: release, grasp, pour, empty etc. Generate the pddl domain and problem. don't write robot busy. generate PDDL domain and problem\n\n"
    },
    {
      "role": "user",
      "content": "{\n        \"input_nodes\": [\n            {\n                \"label\": \"milk\",\n                \"states\": [\"liquid\"],\n                \"ingredients\": [\n                    \n                ],\n                \"container\": \"bowl\"\n            },\n            {\n                \"label\": \"glass\",\n                \"states\": [\n                    \"empty\"\n                ],\n                \"ingredients\": [],\n                \"container\": \"surface\"\n            }\n        ],\n        \"motion_node\": \"pour\",\n        \"output_nodes\": [\n            {\n                \"label\": \"milk\",\n                \"states\": [\"liquid\"],\n                \"ingredients\": [\n                   \n                ],\n                \"container\": \"glass\"\n            }\n        ]\n    }"
    },
    {
      "role": "assistant",
      "content": "DOMAIN FILE:\n\n```\n(define (domain cooking)\n  \n  (:requirements :strips :typing :negative-preconditions)\n  \n  (:types\n    object - object\n    container - object)\n  \n  (:predicates\n    (empty ?obj - object)\n    (contains ?container - container ?obj - object)\n    (liquid ?obj - object))\n  \n  (:action grasp\n    :parameters (?obj - object ?container - container)\n    :precondition (and (empty ?obj) (contains ?container ?obj))\n    :effect (not (empty ?obj)))\n  \n  (:action release\n    :parameters (?obj - object)\n    :precondition (not (empty ?obj))\n    :effect (empty ?obj))\n  \n  (:action pour\n    :parameters (?obj - object ?fromContainer - container ?toContainer - container)\n    :precondition (and (not (empty ?obj)) (contains ?fromContainer ?obj))\n    :effect (and (not (contains ?fromContainer ?obj)) \n                 (contains ?toContainer ?obj)\n                 (empty ?fromContainer))\n    )\n)\n```\nPROBLEM FILE:\n\n```\n(define (problem cooking_problem)\n  \n  (:domain cooking)\n  \n  (:objects \n    milk - object\n    glass - object\n    bowl - container\n    surface - container)\n  \n  (:init \n    (liquid milk)\n    (empty glass)\n    (contains bowl milk))\n  \n  (:goal (and (contains glass milk) \n              (empty bowl) \n              (not (contains bowl milk))\n              (not (empty glass)))\n  )\n)\n```\nThis domain and problem definition represent the process of a robot pouring milk from a bowl to a glass in a cooking scenario. The robot will grasp the milk, release it from the bowl, and pour it into the glass."
    }
  ],
  temperature=1,
  max_tokens=2176,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)