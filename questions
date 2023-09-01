import openai
import json
import time
import traceback
import csv
import ast
import pandas as pd
from functional import seq


class QuestionGenerator:

    def __init__(self, api_key):
        openai.api_key = api_key
        self.prompt = self.generate_prompt()

    def convert_keys_to_lowercase(self, dictionary):
        return {key.lower(): value for key, value in dictionary.items()}

    def get_completion(self, prompt, model="gpt-3.5-turbo-16k", num_iterations=1):
        messages = [
            {"role": "system", "content": " you are a curriculum creator and teacher hiring expert who wanted to hire a subject expert and intelligent teacher. Design most difficult MCQ questions"},
            {"role": "user", "content": prompt},
        ]

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message["content"]

    def generate_prompt(self):
        prompt = """
        -You are creating a test to find best teacher who can teach for "Grade VI" or class VI CBSE and IG board in India
        - You must Create very hard or difficult “Multiple choice questions” on "Science subject" with 4 options and one correct answer, where “None 
        of the above” and “all of the above” should not be an option.

        - Provide them into valid JSON array of object for Multiple choice questions in below formats :
        
        \n[{\"question\": \"question Data \", \"option A\": \"option A Data values \" ,\"option B\": \"option B data values \",
        \"option C\": \"option C data values \", \"option D\": \"option D data values \", \"answer\": \" Option A or Option B or C or D \", 
        \"hint\": \"provide hint for answers \", \"feedback\": \"Feedback on correct answer \",\"bloom level\": understand, apply,analyze, etc.. \"Feedback on correct answer \", \"complexity\": \"complexity of question \",
        \"difficulty Level\": \"difficulty Level of question \", \"learning outcomes\": using Learning Outcomes\" }]\n  

        All questions must the below guidelines:
        
            1. Must Create most difficult questions only on given learning outcomes
            2. Tag each question to its learning outcome and knowledge points
            3. Give the correct answer along with the answer explanation
            4. Create questions based on apply, analysis, and understanding level of Bloom's taxonomy and must tag each question to the same.
            5. Must integrate multiple knowledge points and learning outcomes into a single problem use outcomes from  a given list to increase the complexity of the question for at least 60% of questions out of total questions
            6. Created questions should assess the Scientific knowledge of the attempting person.
            7. Create questions in the Indian context
            8. Include multiple distractors that reflect common mistakes, or misconceptions. Make sure that each option tests a different aspect of understanding, and all of them look plausible to increase the complexity.
            9. Must is Questions should be difficult and super difficult to complex level to solve for the teacher
            10. Questions should test teacher's analytical thinking, computational thinking, and logical thinking skills along with the knowledge so add such components in each question
            11. Be smart in asking questions and try not to repeat concepts in questions
            12. Divide and create three questions of  P1, P2 and P3 each where P1 means only one learning outcome, P2 means  > 1 and <=2 learning outcomes and Knowledge points clubbed together 
            and P3 means > 2 and <=3  learning outcomes  and knowledge points clubbed together.
            13. distribute the 9 questions evenly among understand, apply and analyze blooms level in P1, P2 and P3


        The JSON object:

        """  
        return prompt
        

    def create_questions(self, repeat):
        output = []
        for i in range(repeat):
            try:
                response = self.get_completion(self.prompt)
                print('Pass ', i + 1)
                print(response)
                response_dict = json.loads(response)
                print('Type ', type(response_dict))

                if isinstance(response_dict, dict):
                    res = response_dict.values()
                    output.extend(res)
                else:
                    output.extend(response_dict)
            except Exception as e:
                print('Exception')
        return output

    def create_csv(self, output):
        updated_res = seq(output).map(lambda each : self.convert_keys_to_lowercase(each)).to_list()
        headers = list(updated_res[0].keys())
        questions_dir = set()
        filename = self.generate_filename()

        with open(filename, 'w', newline='') as f:
            try:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
            except Exception as e:
                print('Exception while writing csv')
                traceback.print_exc()

            for row in updated_res:
                question = row.get('questions') if row.get('questions') else row.get('question')
                if question:
                    question = question.lower()
                if question in questions_dir:
                    continue
                try:
                    writer.writerow(row)
                except Exception as e:
                    print('Exception while writing a row')
                    print(row)
                    traceback.print_exc()
                questions_dir.add(question)

        print(filename, ' created')
        return filename

    def generate_filename(self):
        filename = r'F:\Company_Data\Script_python\output_csv\questions.csv'
        return filename


if __name__ == '__main__':
    api_key = " "
    generator = QuestionGenerator(api_key)
    questions_data = generator.create_questions(repeat=1)
    filename = generator.create_csv(questions_data)
